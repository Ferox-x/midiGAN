import glob
import json
from multiprocessing.pool import Pool

import music21
import numpy


def target(file) -> list[list[str]]:
    notes = []
    midi = music21.converter.parse(file)
    print("Parsing %s" % file)
    try:
        s2 = music21.instrument.partitionByInstrument(midi)
        notes_to_parse = s2.parts[0].recurse()
    except Exception:
        notes_to_parse = midi.flat.notes
    local_notes = []
    for element in notes_to_parse:
        if isinstance(element, music21.note.Note):
            local_notes.append(str(element.pitch))
        elif isinstance(element, music21.chord.Chord):
            local_notes.append(
                ".".join(str(n) for n in element.normalOrder),
            )

        if len(local_notes) == 10:
            notes.append(local_notes.copy())
            local_notes.pop(0)
    return notes


def get_notes() -> list[list[str]]:
    files = glob.glob("../midi/*.mid")

    global_notes = []
    with Pool(processes=16) as pool:
        results = pool.map(target, files)
        for local_notes in results:
            global_notes.extend(local_notes)

    with open("notes.json", "w") as file:
        content = json.dumps(global_notes)
        file.write(content)
    return global_notes


def get_set_notes() -> tuple[set[str], int]:
    notes = load_notes()
    all_notes = []
    for local_notes in notes:
        for local_note in local_notes:
            all_notes.append(local_note)

    set_notes = set(all_notes)
    return set_notes, len(set_notes)


def load_notes() -> list[list[str]]:
    with open("/home/gerox/PyCharmProjects/testjulia/utils/notes.json", "r") as file:
        notes = json.loads(file.read())

    return notes


notes = load_notes()
notes = numpy.array(notes)
