import json

import numpy
import pandas as pd

from utils.create_model import create_model
from utils.parse_notes import load_notes, get_set_notes
from tensorflow.keras.callbacks import History
import matplotlib.pyplot as plt
from keras.utils import to_categorical

data = numpy.array(load_notes())
uniq_notes, total = get_set_notes()
uniq_notes = list(uniq_notes)

dict_note_int = {value: index for index, value in enumerate(uniq_notes)}
dict_int_note = {index: value for index, value in enumerate(uniq_notes)}

with open("dict_note_int.json", "w") as file:
    file.write(json.dumps(dict_note_int))


with open("dict_int_note.json", "w") as file:
    file.write(json.dumps(dict_int_note))


def note_to_int(note):
    return dict_note_int[note]


def int_to_note(note):
    return dict_int_note[note]


X_train = []
Y_train = []

for local_notes in data:
    X_train.append(local_notes[:9])
    Y_train.append(local_notes[9])

X_train_new = []
for x in X_train:
    local_note = []
    for note in x:
        int_note = note_to_int(note)
        local_note.append(int_note)
    X_train_new.append(local_note)

Y_train_new = []
for note in Y_train:
    Y_train_new.append(note_to_int(note))

X_train_new = numpy.array(X_train_new)
Y_train_new = numpy.array(Y_train_new)

Y_train_new = to_categorical(Y_train_new)

model = create_model()

history = History()

n_epochs = 1
model.summary()
model.fit(
    X_train_new,
    Y_train_new,
    callbacks=[history],
    epochs=n_epochs,
    batch_size=64,
    validation_split=0.2,
)
model.save("LSTMmodel.h5")

pd.DataFrame(history.history).plot()
plt.savefig("LSTM_Loss_per_Epoch.png", transparent=True)
plt.close()
