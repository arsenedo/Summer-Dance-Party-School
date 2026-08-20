
from sdps.config import MP3_FILENAME
import librosa
import mido
import numpy as np
import scipy

class DecomposeMp3:
    def __init__(self):
        self.fn = MP3_FILENAME
        self.fmin = librosa.note_to_hz('C-2') #Note basse de la plage totale
        self.n_bins = 96 # Nombre de notes totales depuis la note basse
        self.notes = librosa.midi_to_note(librosa.hz_to_midi(librosa.cqt_frequencies(n_bins=self.n_bins, fmin=self.fmin)))
        y, sr = librosa.load("./assets/sounds/" + MP3_FILENAME, sr=None)
        self.y = y
        self.sr = sr
        self.notesTiming = librosa.onset.onset_detect(y=self.y, sr=self.sr, units='time')
        self.hop_length = 512
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



    def run(self):
        # Création du fichier midi
        mid = mido.MidiFile()
        track = mido.MidiTrack()
        mid.tracks.append(track)
        tempo = 500000
        last_message = 0.0

        # Calcul du CQT sur la plage définie
        C = librosa.cqt(self.y, sr=self.sr, hop_length=self.hop_length, fmin=self.fmin, n_bins=self.n_bins)

        for t in self.notesTiming:
            print(t)

            target_time = t
            center_sample = int(target_time * self.sr)
            target_time = t + 0.12

            # Permets de convertir le temps en seconde en saut de temps (hop)
            frame_index = librosa.time_to_frames(target_time, sr=self.sr, hop_length=self.hop_length)
            specific_cqt = C[:, frame_index]  # récup la bonne ligne du tableau librosa
            specific_db = np.abs(specific_cqt)

            # Détection des pic locaux
            peaks = scipy.signal.find_peaks(specific_db)

            db = []

            # Recherche de l'id de la valeur max
            max_id = specific_db.argmax()
            # print("max")
            # print(max_id)

            for p in peaks[0]:
                if specific_db[p] > (specific_db[
                                         max_id] / 5):  # On garde les valeurs plus hautes que 20% de la note jouée la plus forte
                    db.append(str(self.notes[p]).translate(str.maketrans("", "",
                                                                    "0123456789-")))  # avec maketrans on supprimes les chiffres (On a pas besoin de garder l'octave)
            # print("notes trouvées = ")
            # print(set(db))

            delta = t - last_message
            ticks = int(mido.second2tick(delta, mid.ticks_per_beat, tempo))

            last_message = t
            first_note = True

            for note in db:

                if first_note:
                    track.append(mido.Message('note_on', note=self.notes_midi[note], velocity=64, time=ticks))
                    first_note = False
                else:
                    track.append(mido.Message('note_on', note=self.notes_midi[note], velocity=64, time=0))

        midi_fn = "new_song.mid"
        mid.save(midi_fn)
        print("Fichier midi créé et sauvegardé sous " + midi_fn)
