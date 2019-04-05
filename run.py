import numpy as np
import pandas as pd
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM, RNN, TimeDistributed
from keras.optimizers import RMSprop
from sklearn.model_selection import train_test_split
import functions
import random
import sys

df = pd.read_csv('data/Indian-Male-Names - Copy.csv')
df['names'] = df['names'].str.lower()

phonetic = df['names'].apply(functions.remove_after_space)
phonetic = df['names'].apply(functions.encode_names)
phonetic = df['names'].apply(functions.phonetic_generator)
functions.add_to_dictionary(phonetic)
phones_lst = functions.get_phones_from_dictionary()


#indices to phones and vice a versa
phones_indices, indices_phones = functions.encode_phones()

#generate raw data
x = functions.generate_raw_data(phonetic)

#make the sequence
max_length = 1
step = 1

names = []
next_char = []

for i in range(0, len(x)-max_length, step):
    names.append(x[i: i+max_length])
    next_char.append(x[i+max_length])

# print('len of names : ', len(names))
# print('10 names series : ')
# for i in range(10):
#     print('[{}] : [{}]'.format(names[i], next_char[i]))

X = np.zeros((len(names), max_length, len(phones_lst)), dtype=np.bool)
y = np.zeros((len(names), len(phones_lst)), dtype=np.bool)

for i, name in enumerate(names):
    for j, phone in enumerate(name):
        X[i, j, phones_indices[phone]] = 1
    y[i, phones_indices[next_char[i]]] = 1

# print('Size of X: {:.2f} MB'.format(X.nbytes/1024/1024))
# print('Size of y: {:.2f} MB'.format(y.nbytes/1024/1024))
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

#keras model
model = Sequential()
model.add(LSTM(256, input_shape=(max_length, len(phones_lst)), return_sequences=True))
model.add(LSTM(128, activation='tanh', return_sequences=True))
model.add(LSTM(64, activation='tanh'))
model.add(Dense(len(phones_lst), activation='softmax'))

optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy',
              optimizer=optimizer)

#print(model.summary())

print('Training started...')
model.fit(X_train, y_train, 
                    validation_data=(X_test, y_test),
                    epochs=15, 
                    batch_size=128,
                    verbose=2)

model.save_weights('model/model1.h5')

start_index = random.randint(0, len(x) - max_length - 1)

gen_names = x[start_index: start_index+max_length]


while True:
    x = np.zeros((1, max_length, len(phones_lst)))
    for j, phone in enumerate(gen_names):
        x[0, j, phones_indices[phone]] = 1
    
    preds = model.predict(x, verbose=0)[0]
    next_char = indices_phones[functions.sample(preds)]

    gen_names.append(next_char)

    print('\n')
    name = ''
    for i in gen_names:
        name += i
    print(name)
    #print('like name: y/n')
    response = input()
    if response == 'y':
        functions.write_to_names(name)   
    if response == 'q':
        sys.exit()

    gen_names = gen_names[1:]