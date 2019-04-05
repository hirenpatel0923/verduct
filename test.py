name = 'ghantbhai'

def phonetic_generator(name):
    vovels = ['a','e','i','o','u','aa','ai','ee','oo']

    phonetic = []
    sub_str = ''
    jump_char = False
    i=0
    while i < len(name)-1:
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

                if name[i+1] == 'n':
                    if name[i+2] not in vovels:
                        sub_str += name[i+1]
                        i += 1
                phonetic.append(sub_str)
                sub_str = ''
            
            if name[i+1] == ' ':   #jump spaces
                phonetic.append(sub_str)
                sub_str = ''
                jump_char = True

            # if name[i] == 'n':  #for n(gh/kj/sh....)
            #     if name[i+1] not in vovels:
            #         sub_str += name[i+1]
            #         i += 1
            #         phonetic.append(sub_str)
            #         sub_str = ''

            if i == len(name) - 2:
                    sub_str += name[-1]
                    phonetic.append(sub_str)
        else:
            jump_char = False

        i += 1
    return phonetic

print(phonetic_generator(name))