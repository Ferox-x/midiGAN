from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    LSTM,
    Dense,
    Bidirectional,
)

from utils.parse_notes import get_set_notes


def create_model():
    _, total = get_set_notes()

    model = Sequential()
    model.add(LSTM(128, input_shape=(9, 1), return_sequences=True))
    model.add(Dense(total // 2, activation="relu"))
    model.add(Bidirectional(LSTM(128)))
    model.add(Dense(total // 2, activation="relu"))
    model.add(Dense(total, activation="softmax"))
    model.compile(loss="categorical_crossentropy", optimizer="adam")

    return model
