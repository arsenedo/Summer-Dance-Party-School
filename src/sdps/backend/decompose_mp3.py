from mido import MidiTrack, MetaMessage
from numba.cpython.numbers import literal_int_to_boolean

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
        print(len(self.notesTiming), len(self.onset_frames))



    def run(self):
        # Création du fichier midi
        mid = mido.MidiFile()
        self.create_meta_track(mid)

        track = mido.MidiTrack()
        mid.tracks.append(track)
        tempo = mido.bpm2tempo(self.bpm, time_signature=(4, 4))
        last_message = 0.0

        # Calcul du CQT sur la plage définie
        C = librosa.cqt(self.y, sr=self.sr, hop_length=self.hop_length, fmin=self.fmin, n_bins=self.n_bins)

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

            if idx > len(self.onset_frames - 1):
                print("ATTENTION, OUR CODE IS ASS")
            instrument = self._determine_instrument(self.onset_frames[min(idx, len(self.onset_frames - 1))])

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

        counter = 0

        for note in note_list:
            if note.instrument == note_handler.InstrumentType.PIANO:
                counter += 1

        print("SUCCess rate is ", counter / len(note_list) * 100, "%", len(note_list))

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

    def _determine_instrument(self, frame_idx) -> str:
        first_option = self._calculate_spectral_centroid_slope(frame_idx)

        return first_option

    def _calculate_spectral_centroid_slope(self, frame_idx):
        frames_offset = 2  # 93ms per frame, 186ms neighbor frames, in total 279ms to avoid falling into trumpet's fall off on note end
        neighbor_frame = frame_idx + frames_offset
        slope_evo_threshold = -20

        start_centroid = self.spectral_centroids[0][frame_idx]
        end_centroid = self.spectral_centroids[0][neighbor_frame]

        slope = (end_centroid - start_centroid) / (neighbor_frame - frame_idx)

        if slope < slope_evo_threshold:
            return "Piano"
        else:
            return "Trumpet"