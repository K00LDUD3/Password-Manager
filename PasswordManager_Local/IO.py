import math
import os
import tkinter as tk
from tkinter import filedialog

def FileInp(read_from):
    x = ''
    try:
        with open(read_from, "r") as txt_file:
            x = txt_file.readlines()
    except FileNotFoundError:
        return False
    for i in range(len(x)):
        if x[i].endswith('\n'):
            x[i] = str(x[i])[0:len(x[i])-1]

    return x
'''
    REPLACE TXT WITH FILE UN-OPENABLE FILE
'''
def FileAppend(text=[], target_file='passEnc.txt'):
    for i in range(len(text)):
        print('for loop reached')
        print(not text[i].startswith('\n'))
        if not text[i].startswith('\n'):
            text[i] = '\n'+text[i] 
    try:
        with open(target_file, 'a') as f:
            f.writelines(text[0])
    except FileNotFoundError:
        return False
    finally:
        return

def FileRewrite(choice, newPass, titles=[], text=[], target_file='passEnc.txt'):
    ind = titles.index(choice)
    text[ind] = f'{choice}: {newPass}'

    for i in range(len(text)):
        print('for loop reached')
        print(not text[i].startswith('\n'))
        if not text[i].startswith('\n'):
            text[i] = '\n'+text[i] 
    try:
        with open(target_file, 'x') as f:
            f.writelines(text)
    except FileNotFoundError:
        return False
    finally:
        return True

def NewFile(name='passwordEnc', path=f'C:/Users/{os.getlogin()}/Desktop'):
    #Checking if file exists
    final_path = f'{path}/{name}.txt'
    try:
        with open(final_path, 'r') as f:
            f.readlines()
            #print('File Exists')
            return 'File Already Exists'
    except FileNotFoundError:
        #print('File doesnt exist')
        with open(final_path, 'w'):
            return 'File Created'