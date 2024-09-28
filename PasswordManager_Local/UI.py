from msilib import sequence
import os
from tkinter import *
import tkinter.font as font
from tkinter import ttk
from tkinter.ttk import *

from tkinter import filedialog

import GenFunctions as gf
import IO as io

import time
import pyperclip as p

from random import sample as r
from random import randint as ri

root = Tk()
root.title('Passwords')
#root.resizable(False, False)
root.geometry("365x150")


#Frames
encDecMenu_f = LabelFrame(root)

encrypt_f = LabelFrame(root)
decrypt_f = LabelFrame(root)
delPass_f = LabelFrame(root)
changePass_f = LabelFrame(root)
createFile_f = LabelFrame(root)

selFile_f = LabelFrame(root)
seqFrame_f = LabelFrame(root)

#Class VARs
b_dict = { #Dictionary for BUTTON
        'master':None,
        'act_bg':None,
        'act_fg':None,
        'bg':None,
        'fg':None,
        'border':None,
        'font':None,
        'height':None,
        'highl_color':None,
        'image':None,
        'justify':None,
        'padx':None,
        'pady':None,
        'relief':None,
        'underline':None,
        'w':25,
        'wraplength':None
    }
l_dict = { #Dictionary for LABEL
        'master':None,
        'anchor':None,
        'bg':None,
        'bitmap':None,
        'bd':None,
        'font':None,
        'fg':None,
        'height':None,
        'image':None,
        'justify':None,
        'padx':None,
        'pady':None,
        'relief':None,
        'text':None,
        'textvar':None,
        'underline':None,
        'w':15,
        'wraplength':None
    }
e_dict = { #Dictionary for ENTRY (Textbox)
        'master':None,
        'bd':None,
        'height':None,
        'w':26,
        'bg':None,
        'fg':None,
        'font':None,
        'insertofftime':None,
        'insertontime':None,
        'highlbg':None,
        'highlcolor':None,
        'cursor':None,
        'padx':None,
        'pady':None,
        'highthick':None,
        'charwidth':None,
        'relief':None,
        'yscrollcommand':None,
        'xscrollcommand':None,
    }
g_dict = { #Dictionary for grid packing
        'column':0,
        'row':0,
        'cspan':1,
        'rspan':1,
        'padx':10,
        'pady':10,
        'ipadx':2,
        'ipady':2
    }

#Used to hide previous frame so that new frame can safely come on screen
def hideFrame(frame):
    try:
        frame.pack_forget()
        #print(f'{frame.widgetName} Hidden')
    except (TypeError, AttributeError):
        pass
    finally:
        return

#Configuring root based on x-size, y-size and title
def configRoot(x, y, title):
    root.title(title)
    try:
        root.geometry(str(f'{x}x{y}'))
    finally:
        return
    
#Destroying window
def quit():
    root.destroy()
    return

#Getting next free coordinates starting from TOP LEFT
def GetFreeCoor(arr):
    taken = 1
    free = 0
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if arr[i][j] == free:
                arr[i][j] = taken
                return (i, j, arr)
    return (None, None, arr)

def EncDecMenu(frame):
    hideFrame(frame=frame)
    configRoot(390,177,'Menu')

    #Three rows one column 0 -> empty, 1 -> full 
    placement_arr = [[0,0],
                     [0,0],
                     [0,0],
                     [0,0]]

    edMenu_b_dict = b_dict
    edMenu_g_dict = g_dict

    edMenu_b_dict['master'] = encDecMenu_f

    #1
    edMenu_g_dict['row'], edMenu_g_dict['column'], placement_arr = GetFreeCoor(placement_arr)
    enc_b = gf.GenFunc('button', edMenu_b_dict, 'Add Password', g_dict)
    enc_b.widg.config(command= lambda: SelectFileMenu(frame=encDecMenu_f, choice = 'e'))

    #2
    edMenu_g_dict['row'], edMenu_g_dict['column'], placement_arr = GetFreeCoor(placement_arr)
    createF_b = gf.GenFunc('button', edMenu_b_dict, 'Create Storage File', edMenu_g_dict)
    createF_b.widg.config(command= lambda: SelectFileMenu(frame=encDecMenu_f, choice='cf'))

    #3
    edMenu_g_dict['row'], edMenu_g_dict['column'], placement_arr = GetFreeCoor(placement_arr)
    dec_b = gf.GenFunc('button', edMenu_b_dict, 'Get Password', g_dict)
    dec_b.widg.config(command= lambda: SelectFileMenu(frame=encDecMenu_f, choice = 'd'))

    #4
    edMenu_g_dict['row'], edMenu_g_dict['column'], placement_arr = GetFreeCoor(placement_arr)
    delPass_b = gf.GenFunc('button', edMenu_b_dict, 'Delete Password', edMenu_g_dict)
    delPass_b.widg.config(command= lambda: SelectFileMenu(frame=encDecMenu_f, choice='del'))
    #5
    edMenu_g_dict['row'], edMenu_g_dict['column'], placement_arr = GetFreeCoor(placement_arr)
    changePass_b = gf.GenFunc('button', edMenu_b_dict, 'Change Password', edMenu_g_dict)
    changePass_b.widg.config(command= lambda: SelectFileMenu(frame=encDecMenu_f, choice='c'))

    #6
    edMenu_g_dict['row'], edMenu_g_dict['column'], placement_arr = GetFreeCoor(placement_arr)
    ex_b = gf.GenFunc('button', edMenu_b_dict, 'Exit', g_dict)
    ex_b.widg.config(command= quit)

    encDecMenu_f.pack()

    return

#Selecting file path
def SelectFile(frame, c):
    
    if c == 'cf':
        path = filedialog.askdirectory()
        if path != '':
            CreateFileMenu(frame=frame, msg=path, path=path)
            return
    else:
        file_path = filedialog.askopenfilename()
        if file_path.endswith('.txt') and not(file_path == ''):
            if c == 'd':
                Decrypt(frame=frame, file_path=file_path)
                return
            elif c == 'e':
                Encrypt(frame=frame, file_path=file_path)
                return  
            elif c == 'c':
                ChangePassMenu(frame=frame, file_path=file_path, msg='')
                return
            elif c == 'del':
                DelPasswordMenu(frame=frame, file_path=file_path)
                return
            else:
                SelectFileMenu(frame=selFile_f)
                return
    
    SelectFileMenu(frame=frame, choice=c)
    return
#Selecting file path MENU
def SelectFileMenu(frame, choice):
    hideFrame(frame=frame)
    configRoot(203,127,'Select File')

    selFile_b_dict = b_dict
    selFile_b_dict['master'] = selFile_f
    selFile_g_dict = g_dict

    place_arr = [[0],[0]]

    selFile_g_dict['row'], selFile_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    selFile_b = gf.GenFunc('Button', selFile_b_dict, 'Select (TEXT) File', selFile_g_dict)
    if choice == 'cf':
        selFile_b.widg.config(text='Select Folder')
    selFile_b.widg.config(command= lambda: SelectFile(frame= selFile_f, c=choice))

    selFile_g_dict['row'], selFile_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    cancel_b = gf.GenFunc('Button', selFile_b_dict, 'Cancel', selFile_g_dict)
    cancel_b.widg.config(command= lambda: EncDecMenu(frame=selFile_f))

    selFile_f.pack()
    return

#Generating random passwords
def GenPass(ent_obj, pass_obj, passConf_obj, cb_val=False):
    char_set = '1234567uj890qwertyuiiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM[]()#*;_-.'
    ent_list = [ent_obj, pass_obj, passConf_obj]
    for i in ent_list:
        i.widg.config(state='active')
        i.widg.delete(0, END)


    if  not cb_val:
        password = ''.join(r(char_set, ri(10,16)))
        for i in ent_list:
            i.widg.insert(END, password)
        ent_obj.widg.config(state='readonly')
        return
    
    password = ''.join(r(char_set[0:char_set.index('M')+1], ri(10,16)))
    for i in ent_list:
        i.widg.insert(END, password)
    ent_obj.widg.config(state='readonly')
    return

'''Assign commands for below func'''
#Adding password
def AddPassVer(status_lab_obj, password, pass_conf, username, target_file):
    username = username.lower().strip()
    msg = ''
    
    '''
    Priority of credential checking
        1. check if pass/pass_conf/username is null
        2. check if website duplicate is there
        3. NEW check if website has a ':' (colon) in it
        4. check if pass and pass_conf match
        5. check if pass/pass_conf is atleast 4 characters
        6. check if pass/pass_conf is atmost 16 characters
    '''
    text = io.FileInp(read_from=target_file)
    text, titles = TextCleaner(text=text)

    for i in [password, pass_conf, username]:
        i = i.strip()
        if i == '' or i == ' ' or i == None:
            msg = 'Cannot Have Void Entries!'
            status_lab_obj.widg.config(text=msg)
            return
    for i in range(len(titles)):
        if titles[i] == username:
            msg = 'Password already exists'
            status_lab_obj.widg.config(text=msg)
            return
    if ':' in pass_conf or ':' in password or ':' in username:
        msg = 'please remove the ":"'
        status_lab_obj.widg.config(text=msg)
        return
    if not(pass_conf == password):
        msg = 'Passwords Dont Match!'
        status_lab_obj.widg.config(text=msg)
        return
    elif len(password) < 4:
        msg = 'Password Minimum Length: 4'
        status_lab_obj.widg.config(text=msg)
        return
    elif len(password) > 16:
        msg = 'Password Maximum Length: 16'
        status_lab_obj.widg.config(text=msg)
        return
    else:
        msg = 'Updating...'
        status_lab_obj.widg.config(text=msg)
    
    io.FileAppend([f'{username.lower()}: {password}'], target_file=target_file)
    msg = f'Password for {username} added'
    status_lab_obj.widg.config(text=msg)

    return

#Adding password MENU
def Encrypt(frame, file_path):
    hideFrame(frame=frame)
    configRoot(400,435,'Add Password')

    place_arr = [[0,0],
                 [0,0],
                 [0,0],
                 [0,0],
                 [0,0],
                 [0,0],
                 [0,0],
                 [0,0],
                 [0,0]]

    enc_b_dict = b_dict
    enc_b_dict['master'] = encrypt_f
    enc_l_dict = l_dict
    enc_l_dict['master'] = encrypt_f
    enc_l_dict['w'] = 20
    enc_e_dict = e_dict
    enc_e_dict['master'] = encrypt_f
    enc_g_dic = g_dict

    #1
    enc_g_dic['row'], enc_g_dic['column'], place_arr = GetFreeCoor(place_arr)
    websiteInp_l = gf.GenFunc('label', enc_l_dict, 'Name of Website:', enc_g_dic)

    #2
    enc_g_dic['row'], enc_g_dic['column'], place_arr = GetFreeCoor(place_arr)
    websiteInp_e = gf.GenFunc('entry', enc_e_dict, '', enc_g_dic)

    #3
    enc_g_dic['row'], enc_g_dic['column'], place_arr = GetFreeCoor(place_arr)
    passInp_l = gf.GenFunc('label', enc_l_dict, 'Password:', enc_g_dic)

    #4
    enc_g_dic['row'], enc_g_dic['column'], place_arr = GetFreeCoor(place_arr)
    passInp_e = gf.GenFunc('entry', enc_e_dict, '', enc_g_dic)
    passInp_e.widg.config(show='\u2022')

    #5
    enc_g_dic['row'], enc_g_dic['column'], place_arr = GetFreeCoor(place_arr)
    passConfInp_l = gf.GenFunc('label', enc_l_dict, 'Confirm Password:', enc_g_dic)

    #6
    enc_g_dic['row'], enc_g_dic['column'], place_arr = GetFreeCoor(place_arr)
    passConfInp_e = gf.GenFunc('entry', enc_e_dict, '', enc_g_dic)
    passConfInp_e.widg.config(show='\u2022')

    #7
    enc_g_dic['row'], enc_g_dic['column'], place_arr = GetFreeCoor(place_arr)
    targetF_l = gf.GenFunc('label', enc_l_dict, 'Target File:', enc_g_dic)

    #8
    enc_g_dic['row'], enc_g_dic['column'], place_arr = GetFreeCoor(place_arr)
    currF_l = gf.GenFunc('label', enc_l_dict, file_path[len(file_path)-file_path[::-1].index('/'):], enc_g_dic)

    #9 & 10
    enc_g_dic['row'], enc_g_dic['column'], place_arr = GetFreeCoor(place_arr)
    enc_g_dic['cspan'] = 2
    enc_b_dict['w'] = 57
    changeF_b = gf.GenFunc('Button', enc_b_dict, 'Change Target File', enc_g_dic)
    changeF_b.widg.config(command= lambda: SelectFileMenu(frame=encrypt_f, choice='e'))
    enc_g_dic['row'], enc_g_dic['column'], place_arr = GetFreeCoor(place_arr)
    enc_g_dic['cspan'] = 1
    enc_b_dict['w'] = 25

    #11
    enc_g_dic['row'], enc_g_dic['column'], place_arr = GetFreeCoor(place_arr)
    genPass_b = gf.GenFunc('button', enc_b_dict, 'Generate Password', enc_g_dic)
    genPass_b.widg.config(command= lambda: GenPass(pass_obj=passInp_e, passConf_obj=passConfInp_e, ent_obj=genPass_e, cb_val=agreement.get()))

    #12
    enc_g_dic['row'], enc_g_dic['column'], place_arr = GetFreeCoor(place_arr)
    genPass_e = gf.GenFunc('entry', enc_e_dict, '', enc_g_dic)
    genPass_e.widg.config(state='readonly')

    #13 & 13
    agreement = BooleanVar()
    enc_g_dic['row'], enc_g_dic['column'], place_arr = GetFreeCoor(place_arr)
    alphanum_cb = Checkbutton(master=encrypt_f,
                text='Letters & Numbers Only',
                variable=agreement,
                onvalue=True,
                offvalue=False).grid(row=enc_g_dic['row'], column=enc_g_dic['column'], columnspan=2)
    enc_g_dic['row'], enc_g_dic['column'], place_arr = GetFreeCoor(place_arr)

    #15 & 16
    enc_g_dic['row'], enc_g_dic['column'], place_arr = GetFreeCoor(place_arr)
    enc_g_dic['cspan'] = 2
    enc_b_dict['w'] = 57
    add_b = gf.GenFunc('button', enc_b_dict, 'Add Pass', enc_g_dic)
    add_b.widg.config(command= lambda: AddPassVer(status_l, passInp_e.widg.get(), passConfInp_e.widg.get(), websiteInp_e.widg.get(), file_path))
    enc_b_dict['w'] = 25
    enc_g_dic['cspan'] = 1
    enc_g_dic['row'], enc_g_dic['column'], place_arr = GetFreeCoor(place_arr)

    #17
    enc_g_dic['row'], enc_g_dic['column'], place_arr = GetFreeCoor(place_arr)
    back_b = gf.GenFunc('button', enc_b_dict, 'Back', enc_g_dic)
    back_b.widg.config(command= lambda: EncDecMenu(frame=encrypt_f))

    #18
    enc_g_dic['row'], enc_g_dic['column'], place_arr = GetFreeCoor(place_arr)
    l_dict['wraplength'] = 100
    status_l = gf.GenFunc('label', enc_l_dict, '', enc_g_dic)

    encrypt_f.pack()

    return

#Fetching password
def FetchPass(titles, text, index, l_obj):

    index_val = titles.index(index)
    focus_text = text[index_val]
    
    password = focus_text[focus_text.index(':')+1:].strip()
    
    l_obj.widg.config(text=password)
    
    return

#Removing redundancies
def TextCleaner(text):
    new_text = []
    try:
        text.remove('\n')
    except:
        None

    for i in range(len(text)):
        if not(text[i] == ""):
            new_text.append(text[i])
    
    text = new_text
    new_text = []


    for i in range(len(text)):
        if ':' in text[i]:
            new_text.append(text[i])

    text = new_text
    new_text = []
    
    titles = [(text[i][0: text[i].index(':')]) for i in range(len(text))]
    return text, titles

#Copy to clipboard
def Copy(op_obj, text):
    p.copy(text=text)
    op_obj.widg.config(text='Copied Password')
    #print(f'Copied {text}')
    return

#Fetching password MENU
def Decrypt(frame, file_path):
    hideFrame(frame=frame)
    configRoot(390,260,'Get Password')

    place_arr = [[0,0],
                 [0,0],
                 [0,0],
                 [0,0],
                 [0,0]]

    dec_b_dict = b_dict
    dec_b_dict['master'] = decrypt_f
    dec_g_dict = g_dict
    dec_l_dict = l_dict
    dec_l_dict['w'] = 20
    dec_l_dict['master'] = decrypt_f
    text = io.FileInp(file_path)

    if text == False:
        EncDecMenu(frame=frame)
        return
    
    text, titles = TextCleaner(text)
    if text == []:
        SequenceFrame('Menu', seqFrame_f, msg = 'Empty File')
        return
    #1
    dec_g_dict['row'], dec_g_dict['column'], place_arr = GetFreeCoor(arr=place_arr)
    prompt_l = gf.GenFunc('label', dec_l_dict, 'Select Site:', dec_g_dict)

    #2
    combo = ttk.Combobox(master=decrypt_f, values= titles, state= 'readonly', width=15)
    combo.current(0)
    x, y, place_arr = GetFreeCoor(place_arr)
    combo.grid(row=x, column=y)
    combo.bind('<<ComboboxSelected>>', lambda event: status_l.widg.config(text=''))

    #3
    dec_g_dict['row'], dec_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    pass_l = gf.GenFunc('label', dec_l_dict, 'Password:', dec_g_dict)

    #4
    dec_g_dict['row'], dec_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    op_l = gf.GenFunc('label', dec_l_dict, '', dec_g_dict)
    op_l.widg.bind("<Button-1>", lambda e: Copy(op_l, op_l.widg.cget('text')))
    
    #5
    dec_g_dict['row'], dec_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    copy_b = gf.GenFunc('button', dec_b_dict, 'Copy Password', dec_g_dict)
    
    #6
    dec_g_dict['row'], dec_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    status_l = gf.GenFunc('label', dec_l_dict, '', dec_g_dict)
    copy_b.widg.config(command= lambda: Copy(status_l, op_l.widg.cget('text')))

    #7
    dec_g_dict['row'], dec_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    changeF_b = gf.GenFunc('button', dec_b_dict, 'Change File', dec_g_dict)
    changeF_b.widg.config(command= lambda: SelectFileMenu(frame= decrypt_f, choice='d'))

    #8
    dec_g_dict['row'], dec_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    file_name = file_path[len(file_path)-file_path[::-1].index('/'):]
    path_l = gf.GenFunc('label', dec_l_dict, file_name, dec_g_dict)

    #9
    dec_g_dict['row'], dec_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    back_b = gf.GenFunc('button', dec_b_dict, 'Back', dec_g_dict)
    back_b.widg.config(command= lambda: EncDecMenu(frame=decrypt_f))

    #10
    dec_g_dict['row'], dec_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    go_b = gf.GenFunc('button', dec_b_dict, 'Get', dec_g_dict)
    go_b.widg.config(command= lambda: FetchPass(titles=titles, text= text, index= combo.get(), l_obj=op_l))
    
    decrypt_f.pack()

    return
#Change Password verification and excecution
def ChangePassVer(l_status_obj, oldPass, newPass, confPass, choice, text, file_path, frame):
    msg = ''
    '''
    Priority of credential checking
        1. check if pass/pass_conf/pass_new is null
        2. check if oldPass matches with pass in txt file
        2. check if pass and pass_conf match
        3. check if pass/pass_conf is atleast 4 characters
        4. check if pass/pass_conf is atmost 16 characters
    '''
    text, titles = TextCleaner(text)
    ind = titles.index(choice)
    focus_text = text[ind]
    password = focus_text[focus_text.index(':')+1:].strip()
    if oldPass == '' or newPass == '' or confPass == '':
        msg = 'Void Entries Detected!'
        l_status_obj.widg.config(text=msg)
        return
    elif password != oldPass:
        msg = 'Old Pass Doesn\'t match'
        l_status_obj.widg.config(text=msg)
        return
    elif newPass != confPass:
        msg = 'Passwords Don\'t match'
        l_status_obj.widg.config(text=msg)
        return
    elif len(newPass) < 4:
        msg = 'New Pass Too Short!'
        l_status_obj.widg.config(text=msg)
        return
    elif len(newPass) > 16:
        msg = 'New Pass Too Long!'
        l_status_obj.widg.config(text=msg)
        return
    msg = 'updating...'
    l_status_obj.widg.config(text=msg)

    x = io.FileRewrite(choice, newPass, titles, text, file_path)
    if not x:
        msg = 'ERROR'
        l_status_obj.widg.config(text=msg)
        return
    else:
        msg = 'Password Changed'
        
        ChangePassMenu(frame, file_path, msg)
        return
#Exit sequence
def returnEncDecMenu(status_obj, widgObj_list, frame):
    for i in range(len(widgObj_list)):
        widgObj_list[i].widg.config(state='disabled')
    for i in range(3,0,-1):
        status_obj.widg.config(text=f'exiting in {i}s')
        time.sleep(1)
    #print(frame.__dict__)
    hideFrame(frame=frame)
#Return Sequence FRAME
def SequenceFrame(choice='Menu', frame=None, msg='Error Occurred'):
    place_arr = [[0],
                 [0],
                 [0]]

    sf_b_dict = b_dict
    sf_b_dict['master'] = seqFrame_f
    sf_l_dict = l_dict
    sf_l_dict['master'] = seqFrame_f
    sf_g_dict = g_dict

    #1
    sf_g_dict['row'], sf_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    msg_l = gf.GenFunc('label', sf_l_dict, msg, sf_g_dict)
    
    #2
    sf_g_dict['row'], sf_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    return_l = gf.GenFunc('label', sf_l_dict, f'Return to {choice}', sf_g_dict)
        
    #3
    sf_g_dict['row'], sf_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    return_b = gf.GenFunc('button', sf_b_dict, 'OK', sf_g_dict)
    if choice.lower() == 'menu':
        return_b.widg.config(command= lambda: EncDecMenu(frame=seqFrame_f))
            
    seqFrame_f.pack()

    return

#Change Password MENU
def ChangePassMenu(frame, file_path, msg):
    hideFrame(frame=frame)
    configRoot(396,427,'Get Password')
    
    place_arr = [[0,0],
                 [0,0],
                 [0,0],
                 [0,0],
                 [0,0],
                 [0,0],
                 [0,0],
                 [0,0],
                 [0,0],
                 [0,0],]

    cp_b_dict = b_dict
    cp_b_dict['master'] = changePass_f
    cp_l_dict = l_dict
    cp_l_dict['master'] = changePass_f
    cp_e_dict = e_dict
    cp_e_dict['master'] = changePass_f
    cp_g_dict = g_dict
    text=''
    text = io.FileInp(file_path)
    if text == False:
        EncDecMenu(frame=changePass_f)
        return
    

    #print(f'{text=}\tUncleansed')
    text, titles = TextCleaner(text)
    if text == []:
        SequenceFrame(choice='Menu', frame=changePass_f, msg='Empty File')
        return
    
    #1
    cp_g_dict['row'], cp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    site_l = gf.GenFunc('label', cp_l_dict, 'Select Site:', cp_g_dict)

    #2
    combo = ttk.Combobox(master=changePass_f, values= titles, state= 'readonly', width=15)
    x, y, place_arr = GetFreeCoor(place_arr)
    combo.current(0)
    combo.grid(row=x, column=y)

    #3
    cp_g_dict['row'], cp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    pass_l = gf.GenFunc('label', cp_l_dict, 'Old Password:', cp_g_dict)

    #4
    cp_g_dict['row'], cp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    pass_e = gf.GenFunc('entry', cp_e_dict, '', cp_g_dict)
    pass_e.widg.config(show='\u2022')

    #5 
    cp_g_dict['row'], cp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    passNew_l = gf.GenFunc('label', cp_l_dict, 'New Password:', cp_g_dict)

    #6
    cp_g_dict['row'], cp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    passNew_e = gf.GenFunc('entry', cp_e_dict, '', cp_g_dict)
    passNew_e.widg.config(show='\u2022')

    #7
    cp_g_dict['row'], cp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    passConf_l = gf.GenFunc('label', cp_l_dict, 'Confirm Password:', cp_g_dict)

    #8
    cp_g_dict['row'], cp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    passConf_e = gf.GenFunc('entry', cp_e_dict, '', cp_g_dict)
    passConf_e.widg.config(show='\u2022')

    
    #9
    cp_g_dict['row'], cp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    genPass_b = gf.GenFunc('button', cp_b_dict, 'Generate Password', cp_g_dict)
    genPass_b.widg.config(command= lambda: GenPass(pass_obj=passNew_e, passConf_obj=passConf_e, ent_obj=genPass_e, cb_val=agreement.get()))

    #10
    cp_g_dict['row'], cp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    genPass_e = gf.GenFunc('entry', cp_e_dict, '', cp_g_dict)
    genPass_e.widg.config(state='readonly')

    #11 & 12
    agreement = BooleanVar()
    agreement.set(False)
    cp_g_dict['row'], cp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    alphanum_cb = Checkbutton(master=changePass_f,
                text='Letters & Numbers Only',
                variable=agreement).grid(row=cp_g_dict['row'], column=cp_g_dict['column'], columnspan=2)
    cp_g_dict['row'], cp_g_dict['column'], place_arr = GetFreeCoor(place_arr)

    #13
    cp_g_dict['row'], cp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    changeFile_b = gf.GenFunc('button', cp_b_dict, 'Change Target File', cp_g_dict)
    changeFile_b.widg.config(command= lambda: SelectFileMenu(frame=changePass_f, choice='c'))
    
    #14
    cp_g_dict['row'], cp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    currFile_l = gf.GenFunc('label', cp_l_dict, file_path[len(file_path)-file_path[::-1].index('/'):], cp_g_dict)


    #15 & 16
    cp_g_dict['row'], cp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    cp_g_dict['cspan'] = 2
    cp_b_dict['w'] = 57
    changePass_b = gf.GenFunc('button', cp_b_dict, 'Change Password', cp_g_dict)
    changePass_b.widg.config(command= lambda: ChangePassVer(status_l, pass_e.widg.get(), passNew_e.widg.get(), passConf_e.widg.get(), combo.get(), text, file_path, changePass_f))
    cp_b_dict['w'] = 25
    cp_g_dict['cspan'] = 1
    cp_g_dict['row'], cp_g_dict['column'], place_arr = GetFreeCoor(place_arr)

    #17
    cp_g_dict['row'], cp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    back_b = gf.GenFunc('button', cp_b_dict, 'Back', cp_g_dict)
    back_b.widg.config(command= lambda: EncDecMenu(frame=changePass_f))

    #18
    cp_g_dict['row'], cp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    status_l = gf.GenFunc('label', cp_l_dict, msg, cp_g_dict)
    
    changePass_f.pack()
    
    return

#Checking if file has \ / : * ? < > | .
def CheckFileName(name, path, label_obj):
    msg = ''
    char_string = '''/\<>.?*|:'''
    name = name.strip()
    print(f'{name=}')
    if name == '':
        msg = 'Enter File Name'
        label_obj.widg.config(text=msg)
        return
    else:
        for i in name:
            if i in char_string:
                msg = '''/\<>.?*|: Not Allowed'''
                label_obj.widg.config(text=msg)
                return
    msg = io.NewFile(name=name, path=path)
    label_obj.widg.config(text=msg)
    return

#Create Filel MENU
def CreateFileMenu(frame, msg='', path=f'C:/Users/{os.getlogin()}/Desktop'):
    hideFrame(frame=frame)
    #configRoot()
    
    place_arr = [[0,0],
                 [0,0],
                 [0,0],
                 [0,0],
                 [0,0]]
    
    cf_b_dict = b_dict
    cf_b_dict['master'] = createFile_f
    cf_b_dict['w'] = 25
    cf_l_dict = l_dict
    cf_l_dict['master'] = createFile_f
    cf_e_dict = e_dict
    cf_e_dict['master'] = createFile_f
    cf_e_dict['w'] = 20
    cf_g_dict = g_dict
    
    #1
    cf_g_dict['row'], cf_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    prompt_l = gf.GenFunc('label', cf_l_dict, 'Enter File Name:', cf_g_dict)

    #2
    cf_g_dict['row'], cf_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    name_e = gf.GenFunc('entry', cf_e_dict, '', cf_g_dict)

    #3
    cf_g_dict['row'], cf_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    pathPrompt_l = gf.GenFunc('label', cf_l_dict, 'Current Directory:', cf_g_dict)

    #4
    cf_g_dict['row'], cf_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    path_l = gf.GenFunc('label', cf_l_dict, path, cf_g_dict)

    #5 & 6
    cf_g_dict['row'], cf_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    cf_g_dict['cspan'] = 2
    cf_b_dict['w'] = 54
    selFolder_b = gf.GenFunc('button', cf_b_dict, 'Change Directory', cf_g_dict)
    selFolder_b.widg.config(command= lambda: SelectFileMenu(frame=createFile_f, choice='cf'))
    cf_b_dict['w'] = 25
    cf_g_dict['cspan'] = 1
    cf_g_dict['row'], cf_g_dict['column'], place_arr = GetFreeCoor(place_arr)

    #7 & 8
    cf_g_dict['row'], cf_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    cf_g_dict['cspan'] = 2
    cf_l_dict['w'] = 50
    status_l = gf.GenFunc('labeL', cf_l_dict, '', cf_g_dict)
    cf_g_dict['cspan'] = 1
    cf_g_dict['row'], cf_g_dict['column'], place_arr = GetFreeCoor(place_arr)

    #9
    cf_g_dict['row'], cf_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    back_b = gf.GenFunc('button', cf_b_dict, 'Back', cf_g_dict)
    back_b.widg.config(command= lambda: EncDecMenu(createFile_f))
    
    #10
    cf_g_dict['row'], cf_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    go_b = gf.GenFunc('button', cf_b_dict, 'Create File', cf_g_dict)
    go_b.widg.config(command= lambda: CheckFileName(name_e.widg.get(), path, status_l))
    createFile_f.pack()
    
    return

#Delete Password Menu
'''Assign Commands for below Function'''
def DelPasswordMenu(frame, file_path):
    hideFrame(frame=frame)
    #configRoot()
    
    place_arr = [[0,0],
                 [0,0],
                 [0,0],
                 [0,0],
                 [0,0],
                 [0,0]]

    dp_b_dict = b_dict
    dp_b_dict['master'] = delPass_f
    dp_l_dict = l_dict
    dp_l_dict['master'] = delPass_f
    dp_e_dict = e_dict
    dp_e_dict['master'] = delPass_f
    dp_g_dict = g_dict
    
    text = io.FileInp(file_path)

    if text == False:
        EncDecMenu(frame=frame)
        return
    
    text, titles = TextCleaner(text)
    if text == []:
        SequenceFrame('Menu', delPass_f, msg = 'Empty File')
        return
    
    #1
    dp_g_dict['row'], dp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    selSite_l = gf.GenFunc('label', dp_l_dict, 'Select Site:', dp_g_dict)

    #2
    combo = ttk.Combobox(master=delPass_f, values= titles, state= 'readonly', width=15)
    x, y, place_arr = GetFreeCoor(place_arr)
    combo.current(0)
    combo.grid(row=x, column=y)

    #3
    dp_g_dict['row'], dp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    pass_l = gf.GenFunc('label', dp_l_dict, 'Enter Password:', dp_g_dict)

    #4
    dp_g_dict['row'], dp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    pass_e = gf.GenFunc('entry', dp_e_dict,'', dp_g_dict)

    #5
    dp_g_dict['row'], dp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    filePrompt_l = gf.GenFunc('label', dp_l_dict, 'Target File:', dp_g_dict)

    #6
    dp_g_dict['row'], dp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    file_l = gf.GenFunc('label', dp_l_dict, file_path, dp_g_dict)

    #7
    dp_g_dict['cspan'] = 2
    dp_g_dict['row'], dp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    change_b = gf.GenFunc('button', dp_b_dict, 'Change Target File', dp_g_dict)
    dp_g_dict['cspan'] = 1
    _,_, place_arr = GetFreeCoor(place_arr)

    #8
    dp_g_dict['cspan'] = 2
    dp_g_dict['row'], dp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    status_l = gf.GenFunc('label', dp_l_dict, '<STATUS>', dp_g_dict)
    dp_g_dict['cspan'] = 1
    _,_, place_arr = GetFreeCoor(place_arr)

    #9
    dp_g_dict['row'], dp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    back_b = gf.GenFunc('button', dp_b_dict, 'Delete Password', dp_g_dict)

    #10
    dp_g_dict['row'], dp_g_dict['column'], place_arr = GetFreeCoor(place_arr)
    go_b = gf.GenFunc('button', dp_b_dict, 'Delete Password', dp_g_dict)

    delPass_f.pack()
    return

EncDecMenu(None)
root.mainloop()


