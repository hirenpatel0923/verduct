import numpy as np
import pandas as pd
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM, RNN, TimeDistributed
from keras.optimizers import RMSprop
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
raw_data = functions.generate_raw_data(phonetic)

#make the sequence
max_length = 1
step = 1

names = []
next_char = []

#keras model
model = Sequential()
model.add(LSTM(256, input_shape=(max_length, len(phones_lst)), return_sequences=True))
model.add(LSTM(128, activation='tanh', return_sequences=True))
model.add(LSTM(64, activation='tanh'))
model.add(Dense(len(phones_lst), activation='softmax'))

optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy',
              optimizer=optimizer)



model.load_weights('model/model1.h5')




for intensity in [0.2,0.5,1.0,1.2,1.5,2.0]:
    print('Temperature Intensity : ', intensity)
    for name_legth in [2,3,4,5]:
        print('Name Length: ', name_legth)

        count = 1
        #initial letter
        start_index = random.randint(0, len(raw_data) - max_length)
        gen_names = raw_data[start_index: start_index+max_length]

        name = ''
        name += gen_names[-1]

        while count < name_legth:
            x = np.zeros((1, max_length, len(phones_lst)))
            for j, phone in enumerate(gen_names):
                x[0, j, phones_indices[phone]] = 1
            
            preds = model.predict(x, verbose=0)[0]
            next_char = indices_phones[functions.sample(preds, intensity)]

            name += next_char
            gen_names.append(next_char)
            gen_names = gen_names[1:]
            count += 1
        
        print(name)


        