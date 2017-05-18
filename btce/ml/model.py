#!/usr/bin/env python

import csv
from random import shuffle
import sys

from keras import regularizers
from keras.callbacks import ReduceLROnPlateau
from keras.layers import BatchNormalization, LeakyReLU, Dense, Activation, Dropout
from keras.models import Sequential
from keras.optimizers import Nadam
import numpy as np


def create_Xt_Yt(x, y, percentage=0.9):
    p = int(len(x) * percentage)
    X_train = x[0:p]
    Y_train = y[0:p]
    X_test = x[p:]
    Y_test = y[p:]
    return X_train, X_test, Y_train, Y_test


reader = csv.reader(open(sys.argv[1]))
rows = list(reader)[1:]
shuffle(rows)
X = [row[:-1] for row in rows]
Y = [([0, 1] if row[-1] == '0' else [1, 0]) for row in rows]

X, Y = np.array(X), np.array(Y)
X_train, X_test, Y_train, Y_test = create_Xt_Yt(X, Y)

model = Sequential()
model.add(Dense(64, input_dim=6, activity_regularizer=regularizers.l2(0.01)))
# model.add(BatchNormalization())
model.add(LeakyReLU())
model.add(Dropout(0.5))
model.add(Dense(16, activity_regularizer=regularizers.l2(0.01)))
model.add(BatchNormalization())
model.add(LeakyReLU())
model.add(Dense(2))
model.add(Activation('softmax'))

model.compile(optimizer=Nadam(lr=0.001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(X_train, Y_train,
                    epochs=50,
                    batch_size=128,
                    verbose=1,
                    validation_data=(X_test, Y_test),
                    shuffle=True,
                    callbacks=[ReduceLROnPlateau(monitor='val_loss', factor=0.9, patience=5, min_lr=0.000001, verbose=1)])

model.save(sys.argv[2])

if len(sys.argv) > 3:
    import matplotlib.pylab as plt
    plt.figure()
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('acc')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='best')
    plt.show()
