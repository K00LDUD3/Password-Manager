from IO import FileInp as inp

print('File Before Cleansing:   ',inp('PassEnc.txt'))

def removeBlank(text):
    new_text = []
    for i in range(len(text)):
        print(i)
        if not(text[i] == ""):
            new_text.append(text[i])
    return new_text

print(removeBlank(text=inp('PassEnc.txt')))
