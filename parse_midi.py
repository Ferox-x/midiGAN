import os
from music21 import converter


folder_path = "midi"
notes_and_instruments = []
instrument_names = []


for file in os.listdir(folder_path):
    if file.endswith(".mid"):
        file_path = os.path.join(folder_path, file)
        midi = converter.parse(file_path)
        full_matrix = []
        parts = midi.parts.parts
        print(file)
        print(f"Количество дорожек {len(parts)}")
        for part in parts:
            part = part.recurse()
            part.stream()
            print(part.getInstrument(), end=" ")
            matrix = [
                part.getInstrument(),
            ]
            notes = []
        print()
        # for note_or_chord in part.notes:
        #     if isinstance(note_or_chord, note.Note):
        #         _note: note.Note = note_or_chord
        #         data_note = [_note.name, _note.octave, _note.duration.quarterLength, 1,]
        #         notes.append(data_note)
        #     if isinstance(note_or_chord, chord.Chord):
        #         _chord: chord.Chord = note_or_chord
        #         chord_notes = []
        #         for __note in _chord.notes:
        #             if isinstance(__note, note.Note):
        #                 __note: note.Note
        #                 data_note = [
        #                     __note.name, __note.octave, __note.duration.quarterLength, 1,
        #                 ]
        #                 chord_notes.append(data_note)
        #         notes.append(chord_notes)
        #     matrix.append(notes)
        # full_matrix.append(matrix)
        # print(full_matrix)
