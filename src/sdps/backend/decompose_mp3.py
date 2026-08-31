from itertools import count

from mido import MidiTrack, MetaMessage
from sdps.config import MP3_FILENAME
import librosa
import mido
import numpy as np
import scipy
from sdps.backend import note_handler

class DecomposeMp3:
    def __init__(self):
        self.fn = MP3_FILENAME
        self.fmin = librosa.note_to_hz('C-2') #Note basse de la plage totale
        self.n_bins = 96 # Nombre de notes totales depuis la note basse
        self.notes = librosa.midi_to_note(librosa.hz_to_midi(librosa.cqt_frequencies(n_bins=self.n_bins, fmin=self.fmin)))
        y, sr = librosa.load("./assets/sounds/" + MP3_FILENAME)
        self.y = y
        self.sr = sr
        self.notesTiming = librosa.onset.onset_detect(y=self.y, sr=self.sr, units='time')
        self.spectral_centroids = librosa.feature.spectral_centroid(y=self.y, sr=self.sr)
        self.mfcc = librosa.feature.mfcc(y=self.y, sr=self.sr)
        self.hop_length = 512
        self.bpm = self.estimate_bmp()
        self.notes_midi = {
            "C": 60,
            "C♯": 61,
            "D": 62,
            "D♯": 63,
            "E": 64,
            "F": 65,
            "F♯": 66,
            "G": 67,
            "G♯": 68,
            "A": 69,
            "A♯": 70,
            "B": 71,
        }

        stft = librosa.stft(self.y)
        log_s = librosa.amplitude_to_db(np.abs(stft), ref=np.max)
        onset_env = librosa.onset.onset_strength(S=log_s)
        self.onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env)

    def run(self):
        # Création du fichier midi
        mid = mido.MidiFile()
        self.create_meta_track(mid)

        track = mido.MidiTrack()
        mid.tracks.append(track)
        tempo = mido.bpm2tempo(self.bpm, time_signature=(4, 4))
        last_message = 0.0

        # Calcul du CQT sur la plage définie
        C = librosa.cqt(self.y, sr=self.sr)
        cqt_energy = np.abs(C) ** 2
        note_list: list[note_handler.Note] = []

        for idx, t in enumerate(self.notesTiming):
            target_time = t + 0.12

            frame_index = librosa.time_to_frames(target_time, sr=self.sr, hop_length=self.hop_length)

            specific_cqt = C[:, frame_index]  # récup la bonne ligne du tableau librosa
            specific_db = np.abs(specific_cqt)

            # Détection des pic locaux
            peaks = scipy.signal.find_peaks(specific_db)

            db = set([])

            # Recherche de l'id de la valeur max
            max_id = specific_db.argmax()
            # print("max")
            # print(max_id)

            for p in peaks[0]:
                if specific_db[p] > (specific_db[
                                         max_id] / 5):  # On garde les valeurs plus hautes que 20% de la note jouée la plus forte
                    db.add(str(self.notes[p]).translate(str.maketrans("", "",
                                                                    "0123456789-")))  # avec maketrans on supprimes les chiffres (On a pas besoin de garder l'octave)
            # print("notes trouvées = ")
            # print(set(db))

            delta = t - last_message
            ticks = int(mido.second2tick(delta, mid.ticks_per_beat, tempo)) - (100 if len(track) > 0 else 0)

            last_message = t
            first_note = True

            if idx > self.onset_frames.shape[0] - 1:
                print("ATTENTION, OUR CODE IS ASS")

            frame_idx = min(idx, self.onset_frames.shape[0] - 1)
            instrument = self._determine_instrument(self.onset_frames[frame_idx], cqt_energy)

            for note in db:
                note_list.append(note_handler.create(note, t, t + 1, instrument))
                if first_note:
                    track.append(mido.Message('note_on', note=self.notes_midi[note], velocity=64, time=ticks))
                    first_note = False
                else:
                    track.append(mido.Message('note_on', note=self.notes_midi[note], velocity=64, time=0))

            for idx, note in enumerate(db):
                track.append(mido.Message("note_off", note=self.notes_midi[note], velocity=64, time=(100 if idx == 0 else 0)))

        midi_fn = "new_song.mid"
        mid.save(midi_fn)

        count = 0
        for note in note_list:
            if note.instrument == note_handler.InstrumentType.TRUMPET:
                count += 1
        print(count/len(note_list)*100, "%")

        return note_list

    def estimate_bmp(self):
        onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr)
        tempo = librosa.feature.tempo(onset_envelope=onset_env, sr=self.sr)
        return tempo[0]

    def create_meta_track(self, mid):
        meta_track = MidiTrack()
        mid.tracks.append(meta_track)
        meta_track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(self.bpm), time=0))
        meta_track.append(MetaMessage('time_signature', numerator=4, denominator=4, time=0))
        meta_track.append(MetaMessage('end_of_track', time=0))

    def _determine_instrument(self, frame_idx, cqt_energy) -> str:
        slope_evo = self._calculate_spectral_centroid_slope(frame_idx)
        mfcc_1_avg = self._calculate_mfcc_mean(1, frame_idx)
        mfcc_2_avg = self._calculate_mfcc_mean(2, frame_idx)
        low_ratio, high_ratio = self._calculate_low_high_ratio(frame_idx, cqt_energy)

        pts_trumpet = 0
        if mfcc_2_avg <= -60.0:
            pts_trumpet += 2
        if low_ratio <= 0.1:
            pts_trumpet += 1
        if slope_evo > -10.0:
            pts_trumpet += 1

        pts_piano = 0
        if mfcc_2_avg > -60.0:
            pts_piano += 2
        if low_ratio > 0.1:
            pts_piano += 1
        if slope_evo <= -10.0:
            pts_piano += 1

        trumpet_active = (pts_trumpet >= 3) or (mfcc_2_avg <= -50.0 and high_ratio > 0.85)
        piano_active = (pts_piano >= 3) or (low_ratio > 0.08)

        if piano_active and trumpet_active:
            if mfcc_2_avg <= -85.0 and low_ratio < 0.03:
                return "Trumpet"
            elif mfcc_2_avg >= -35.0 and low_ratio > 0.30:
                return "Piano"
            else:
                return "Both"
        elif trumpet_active:
            return "Trumpet"
        elif piano_active:
            return "Piano"
        else:
            return "Piano"

    def _calculate_spectral_centroid_slope(self, frame_idx):
        frames_offset = 4
        neighbor_frame = frame_idx + frames_offset

        start_centroid = self.spectral_centroids[0][frame_idx]
        end_centroid = self.spectral_centroids[0][neighbor_frame]

        slope = (end_centroid - start_centroid) / (neighbor_frame - frame_idx)

        return slope

    def _calculate_mfcc_mean(self, coefficient_idx, frame_idx):
        frames_offset = 4

        mfcc_start = frame_idx
        mfcc_end = frame_idx + frames_offset

        mfcc_window = self.mfcc[coefficient_idx, mfcc_start:mfcc_end]

        return np.mean(mfcc_window)

    def _calculate_low_high_ratio(self, frame_idx, cqt_energy):
        frames_offset = 4

        start_frame = frame_idx
        end_frame = frame_idx + frames_offset

        energies_matrix = cqt_energy[:, start_frame:end_frame]

        total_freq = energies_matrix.sum(axis=0).mean()
        lower_freq = energies_matrix[0:36].sum(axis=0).mean()
        higher_freq = energies_matrix[36:96].sum(axis=0).mean()

        return lower_freq / total_freq, higher_freq / total_freq
