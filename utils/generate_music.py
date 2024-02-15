import json
import random
import uuid

import numpy as np
from tensorflow.keras.models import load_model
import music21
from utils.parse_notes import load_notes


def create_midi(prediction_output, filename):
    offset = 0
    output_notes = []

    for pattern in prediction_output:
        pattern = str(pattern)
        if ("." in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split(".")
            notes = []
            for current_note in notes_in_chord:
                new_note = music21.note.Note(int(current_note))
                new_note.storedInstrument = music21.instrument.Piano()
                notes.append(new_note)
            new_chord = music21.chord.Chord(notes)
            new_chord.offset = offset
            output_notes.append(new_chord)
        else:
            new_note = music21.note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = music21.instrument.Piano()
            output_notes.append(new_note)
        offset += 0.5

    midi_stream = music21.stream.Stream(output_notes)
    midi_stream.write("midi", fp="{}.mid".format(filename))


with open("../dict_note_int.json", "r") as file:
    dict_note_int = json.loads(file.read())


with open("../dict_int_note.json", "r") as file:
    dict_int_note = json.loads(file.read())


def note_to_int(key):
    return dict_note_int[key]


def int_to_note(key):
    return dict_int_note[key]


dataset = load_notes()
model = load_model("../LSTMmodel.h5")

for _ in range(10):
    total_notes = 100
    result = random.choice(dataset)[:9]
    result_new = []
    for note in result:
        result_new.append(note_to_int(note))
    result = result_new
    for number in range(total_notes):
        input_array = result[number : 9 + number]
        prediction = model.predict(np.array([input_array]))
        indices = np.argsort(prediction)[0][-3:]
        index = random.choice(indices)
        result.append(index)
    create_midi(result, f"./generated/{uuid.uuid4()}")
    break
