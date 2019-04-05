import numpy as np

def phonetic_generator(name):
    vovels = ['a','e','i','o','u','aa','ai','ee','oo']

    phonetic = []
    sub_str = ''
    jump_char = False

    for i in range(len(name)-1):
        if jump_char != True:
            if name[i] not in vovels:
                sub_str += name[i]
            else:
                if name[i+1] in vovels:  #consicutive vovels
                    sub_str += name[i]
                    sub_str += name[i+1]
                    jump_char = True
                else:
                    sub_str += name[i]
                phonetic.append(sub_str)
                sub_str = ''
            
            if name[i+1] == ' ':   #jump spaces
                phonetic.append(sub_str)
                sub_str = ''
                jump_char = True

            if name[i] == 'n':  #for n(gh/kj/sh....)
                if name[i+1] not in vovels:
                    phonetic.append(sub_str)
                    sub_str = ''

            if i == len(name) - 2:
                    sub_str += name[-1]
                    phonetic.append(sub_str)
        else:
            jump_char = False

    return phonetic

def add_to_dictionary(pandas_series):
    #read phones from dictionary 
    dictionary_lst = []
    with open('dictionary.csv','r') as f:
        dictionary_lst = f.readlines()
        dictionary_lst = [phone.replace('\n','') for phone in dictionary_lst]

    with open('dictionary.csv','w') as f:
        temp_lst = []
        for i in range(pandas_series.count()):
            for p in pandas_series[i]: 
                if p not in temp_lst: #check for copy is not exists in dictionary
                    temp_lst.append(p)
        for p in temp_lst:
            #print(p)
            f.write(p)
            f.write('\n')
    print('All phonetics are added to dicitonary')

def get_phones_from_dictionary():
    #read phones from dictionary 
    dictionary_lst = []
    with open('dictionary.csv','r') as f:
        dictionary_lst = f.readlines()
        dictionary_lst = [phone.replace('\n','') for phone in dictionary_lst]
    return dictionary_lst

def encode_phones():
    phones_indices = {}
    indices_phones = {}
    with open('dictionary.csv', 'r') as f:
        phones_lst = f.readlines()
        for i in range(len(phones_lst)):
            indices_phones[i] = phones_lst[i].replace('\n','')
            phones_indices[phones_lst[i].replace('\n','')] = i
    return phones_indices, indices_phones

def generate_raw_data(pandas_series):
    text = []
    for i in range(pandas_series.count()):
        lst = pandas_series[i]
        for phone in lst:
            text.append(phone)

    return text

def write_to_names(name):
    with open('data/new_names.csv','w') as f:
        f.write(name)
        f.write('\n')

def remove_after_space(name):
    return name.partition(' ')[0]

def encode_names(name):
    return name.encode("ascii", "ignore")

def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


