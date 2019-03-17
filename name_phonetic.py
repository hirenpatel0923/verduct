name = 'ghanshyam'


def phonetic_generator(name):
    vovels = ['a','e','i','o','u','aa','ai','ee','oo']

    phonetic = []
    sub_str = ''
    double_vovels = False

    for i in range(len(name)-1):
        if double_vovels != True:
            if name[i] not in vovels:
                sub_str += name[i]
            else:
                if name[i+1] in vovels:
                    sub_str += name[i]
                    sub_str += name[i+1]
                    double_vovels = True
                else:
                    sub_str += name[i]
                phonetic.append(sub_str)
                sub_str = ''

            if i == len(name) - 2:
                    sub_str += name[-1]
                    phonetic.append(sub_str)
        else:
            double_vovels = False

    return phonetic
