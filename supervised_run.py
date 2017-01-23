import numpy as np
from collections import deque
from keras.models import load_model
from util import *
from midi_util import *
from music import NUM_CLASSES, NOTES_PER_BAR

time_steps = 8
BARS = 8

model = load_model('out/model.h5')

# Generate
prev_notes = deque(maxlen=time_steps)
prev_beats = deque(maxlen=time_steps)

i = NOTES_PER_BAR - 1
for _ in range(time_steps):
    prev_notes.append(np.zeros((NUM_CLASSES,)))
    prev_beats.appendleft(one_hot(i, NOTES_PER_BAR))

    i -= 1
    if i < 0:
        i = NOTES_PER_BAR

composition = []

for i in range(NOTES_PER_BAR * BARS):
    results = model.predict([np.array([prev_notes]), np.array([prev_beats])])
    prob_dist = results[0]
    note = np.random.choice(len(prob_dist), p=prob_dist)

    result = one_hot(note, NUM_CLASSES)
    prev_notes.append(result)
    prev_beats.append(one_hot(i % NOTES_PER_BAR, NOTES_PER_BAR))
    composition.append(note)

mf = midi_encode_melody(composition)
midi.write_midifile('out/output.mid', mf)
