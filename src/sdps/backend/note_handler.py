from enum import Enum

class NoteType(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6

class InstrumentType(Enum):
    PIANO = 0
    TRUMPET = 1

class Note:
    def __init__(self, note: NoteType, start: int, end: int, instrument: InstrumentType, is_half_note: bool = False):
        self.note = note
        self.start = start
        self.end = end
        self.instrument = instrument
        self.is_half_note = is_half_note


def create(note: str, start: int, end: int, instrument: str):
    return Note(NoteType[note[0]], start, end, InstrumentType[instrument.upper()], len(note) > 1)
