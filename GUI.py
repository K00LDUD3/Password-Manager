from tkinter import *
from tkinter import ttk
import pyperclip
from GenFunctions import GenFunc
from random import sample as r
from random import randint as ri
import mysql.connector

mydb = mysql.connector.connect(host="sql12.freesqldatabase.com", user="sql12566558", password="FqKgVkn4A7", db="sql12566558")

#Creating window
root = Tk()
root.title('Password Manager')
root.resizable(False, False)
#MISC
pass_dot = '\u2022'
current_user = None

#FRAMES
signChoose_frame = LabelFrame(root)
signIn_frame = LabelFrame(root)
signUp_frame = LabelFrame(root)
home_frame = LabelFrame(root)
addP_frame = LabelFrame(root)
changeP_frame = LabelFrame(root)
delP_frame = LabelFrame(root)
getP_frame = LabelFrame(root)


#WIDGET DICTIONARIES (GLOBAL to access anytime)
#Button features
default_button_width = 25
BUTTON_DICT = {
            'master':None,
            'act_bg':None, #Color
            'act_fg':None, #Color
            'bg':None, #Color
            'fg':None, #Color
            'border':None,
            'font':None, #Font
            'height':None, #Number
            'highl_color':None, #Color
            'image':None, #Img
            'justify':None,
            'padx':None, #Number
            'pady':None, #Number
            'relief':None,
            'underline':None,
            'w':None, #Number WIDTH
            'wraplength':None
        }
#for label features
LABEL_DICT = {
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
            'w':None,
            'wraplength':None
        }   
#Entry features
default_entry_width = 26
ENTRY_DICT = {
            'master':None,
            'bd':None,
            'height':None,
            'width':default_entry_width,
            'bg':None,
            'fg':None,
            'font':None,
            'insertofftime':None,
            'insertontime':None,
            'padx':None,
            'pady':None,
            'highthick':None,
            'charwidth':None,
            'relief':None,
            'yscrollcommand':None,
            'xscrollcommand':None,
        }
#GRID features
gd = {
            'column':0,
            'row':0,
            'cspan':1,
            'rspan':1,
            'padx':10,
            'pady':10,
            'ipadx':5,
            'ipady':5
        }

#Creating hide frame function
#Used to hide previous frame so that new frame can safely come on screen
def hideFrame(frame):
    print("Button Dict Width: ", BUTTON_DICT['w'])
    print("Label Dict Width: ", LABEL_DICT['w'])
    print("Entry Dict Width: ", ENTRY_DICT['width'])
    try:
        frame.pack_forget()
        for i in frame.winfo_children():
            i.grid_forget()
            i.destroy()
    except (TypeError, AttributeError):
        pass
    finally:
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

#Function to get username in a list (FOR DROPDOWN)
def GetAccounts():
    global current_user
    
    myc = mydb.cursor( )
    query = f"Select Username from Passwords where CurrUser='{current_user}'"
    myc.execute(query)
    l = myc.fetchall( )
    li = []
    for i in range(len(l)):
        li.append(l[i][0])
    li.sort( )
    mydb.commit( )
    return li
    
#Choose whether to sign in or sign up
def SignChoose(frame):
    '''
    Sign In/Up FRAME
    '''
    #Hiding previous frame to avoid colisions
    hideFrame(frame=frame)

    #Unbinding all hot keys to avoid errors
    root.unbind_all('<Escape>')
    root.unbind_all('<Return>')
    
    current_user = None
    s_gd = gd
    s_bd = BUTTON_DICT
    s_bd['master'] = signChoose_frame
    s_bd['w'] = default_button_width

    placements = [[0], [0], [0]]

    # 0
    s_gd['row'], s_gd['column'], placements = GetFreeCoor(placements)
    signIn_b = GenFunc('button', s_bd, 'Sign In', s_gd)
    signIn_b.widg.config(command= lambda: SignIn(frame=signChoose_frame))

    # 1
    s_gd['row'], s_gd['column'], placements = GetFreeCoor(placements)
    signUp_b = GenFunc('button', s_bd, 'Sign Up', s_gd)
    signUp_b.widg.config(command= lambda: SignUp(frame=signChoose_frame))

    # 2
    s_gd['row'], s_gd['column'], placements = GetFreeCoor(placements)
    exit_b = GenFunc('button', s_bd, 'Exit', s_gd)
    exit_b.widg.config(command= lambda: root.destroy())

    signChoose_frame.pack()
    
    current_user = None
    return

def SignUp(frame):
    '''
    Sign Up FRAME
    '''
    #Hiding previous frame to avoid colisions
    hideFrame(frame=frame)

    #Unbinding all hot keys to avoid errors
    root.unbind_all('<Escape>')
    root.unbind_all('<Return>')

    s_gd = gd
    s_bd = BUTTON_DICT
    s_ld = LABEL_DICT
    s_ed = ENTRY_DICT
    s_bd['master'] = signUp_frame
    s_ld['master'] = signUp_frame
    s_ed['master'] = signUp_frame
    # s_bd['w'] = 20

    placements = [[0,0],[0,0],[0,0],[0,0],[0,0]]

    # 0,0
    s_gd['row'], s_gd['column'], placements = GetFreeCoor(placements)
    userPrompt_l = GenFunc('label', s_ld, 'Username: ', s_gd)

    # 0,1
    s_gd['row'], s_gd['column'], placements = GetFreeCoor(placements)
    user_e =  GenFunc('entry', s_ed, StringVar(), s_gd)

    # 1,0
    s_gd['row'], s_gd['column'], placements = GetFreeCoor(placements)
    passPrompt_l =  GenFunc('label', s_ld, 'Password: ', s_gd)
    
    # 1,1
    s_gd['row'], s_gd['column'], placements = GetFreeCoor(placements)
    pass_e =  GenFunc('entry', s_ed, StringVar(), s_gd)
    pass_e.widg.config(show=pass_dot)

    # 2,0
    s_gd['row'], s_gd['column'], placements = GetFreeCoor(placements)
    confpassprompt_l =  GenFunc('label', s_ld, 'Confirm Password: ', s_gd)
    
    # 2,1
    s_gd['row'], s_gd['column'], placements = GetFreeCoor(placements)
    confpass_e =  GenFunc('entry', s_ed, StringVar(), s_gd)
    confpass_e.widg.config(show=pass_dot)

    # 3,0
    s_gd['row'], s_gd['column'], placements = GetFreeCoor(placements)
    s_gd['cspan'] = 2
    msg_l =  GenFunc('label', s_ld, 'Enter Credentials', s_gd)
    s_gd['cspan'] = 1
    s_gd['row'], s_gd['column'], placements = GetFreeCoor(placements)

    # 4,0
    s_gd['row'], s_gd['column'], placements = GetFreeCoor(placements)
    back_b =  GenFunc('button', s_bd, 'Back', s_gd)
    back_b.widg.config(command= lambda: SignChoose(frame=signUp_frame))
    
    # 4,1
    s_gd['row'], s_gd['column'], placements = GetFreeCoor(placements)
    go_b =  GenFunc('button', s_bd, 'Sign In', s_gd)
    go_b.widg.config(command=lambda: SignUpConf(user_e.widg.get(), pass_e.widg.get(), confpass_e.widg.get(), msg_l))
    
    signUp_frame.pack()
    return

def SignIn(frame):
    '''
    Sign In FRAME
    '''
    #Hiding previous frame to avoid colisions
    hideFrame(frame=frame)

    #Unbinding all hot keys to avoid errors
    root.unbind_all('<Escape>')
    root.unbind_all('<Return>')

    s_gd = gd
    s_bd = BUTTON_DICT
    s_bd['w'] = default_button_width
    s_ld = LABEL_DICT
    s_ed = ENTRY_DICT
    s_bd['master'] = signIn_frame
    s_ld['master'] = signIn_frame
    s_ed['master'] = signIn_frame
    s_ed['width'] = default_entry_width + 7

    placements = [[0,0],[0,0],[0,0],[0,0]]

    # 0,0
    s_gd['row'], s_gd['column'], placements = GetFreeCoor(placements)
    userPrompt_l =   GenFunc('label', s_ld, 'Username: ', s_gd)

    # 0,1
    s_gd['row'], s_gd['column'], placements = GetFreeCoor(placements)
    user_e =   GenFunc('entry', s_ed, StringVar(), s_gd)

    # 1,0
    s_gd['row'], s_gd['column'], placements = GetFreeCoor(placements)
    passPrompt_l =   GenFunc('label', s_ld, 'Password: ', s_gd)
    
    # 1,1
    s_gd['row'], s_gd['column'], placements = GetFreeCoor(placements)
    pass_e =   GenFunc('entry', s_ed, StringVar(), s_gd)
    pass_e.widg.config(show=pass_dot)
    
    # 2,0
    s_gd['row'], s_gd['column'], placements = GetFreeCoor(placements)
    s_gd['cspan'] = 2
    msg_l =   GenFunc('label', s_ld, 'Enter Credentials', s_gd)
    s_gd['cspan'] = 1
    s_gd['row'], s_gd['column'], placements = GetFreeCoor(placements)

    # 3,0
    s_gd['row'], s_gd['column'], placements = GetFreeCoor(placements)
    back_b =   GenFunc('button', s_bd, 'back', s_gd)
    back_b.widg.config(command= lambda: SignChoose(frame=signIn_frame))

    # 3,1
    s_gd['row'], s_gd['column'], placements = GetFreeCoor(placements)
    go_b =   GenFunc('button', s_bd, 'Sign In', s_gd)
    go_b.widg.config(command=lambda: CredVerSignIn(user_e.widg.get(), pass_e.widg.get(), msg_l))

    signIn_frame.pack()
    s_ed['width'] = default_entry_width
    root.bind_all('<Return>', lambda e: CredVerSignIn(user_e.widg.get(), pass_e.widg.get(), msg_l))
    return

def Home(frame):
    '''
    Homescreen to display available options(sign out, start pricing)
    '''
    #Hiding previous frame to avoid colisions
    hideFrame(frame=frame)

    #Unbinding all hot keys to avoid errors
    root.unbind_all('<Escape>')
    root.unbind_all('<Return>')

    h_gd = gd
    h_bd = BUTTON_DICT
    h_bd['w'] = default_button_width
    h_bd['master'] = home_frame

    placements = [[0,0],[0,0],[0,0]]

    accounts = GetAccounts()
    
    #0,0
    h_gd['row'], h_gd['column'], placements = GetFreeCoor(placements)
    add_b = GenFunc('button', h_bd, 'Add Password', h_gd)
    add_b.widg.config(command= lambda: AddPassMenu(frame=home_frame))

    #0,1
    h_gd['row'], h_gd['column'], placements = GetFreeCoor(placements)
    change_b = GenFunc('button', h_bd, 'Change Acct Password', h_gd)
    change_b.widg.config(command=lambda: ChangePassMenu(frame=home_frame))

    #1,1
    h_gd['row'], h_gd['column'], placements = GetFreeCoor(placements)
    del_b = GenFunc('button', h_bd, 'Delete An Account', h_gd)
    del_b.widg.config(command=lambda: DeletePassMenu(frame=home_frame))

    #2,1
    h_gd['row'], h_gd['column'], placements = GetFreeCoor(placements)
    get_b = GenFunc('button', h_bd, 'Get Account Password', h_gd)
    get_b.widg.config(command=lambda: GetPass(frame=home_frame))

    #2,0
    h_gd['row'], h_gd['column'], placements = GetFreeCoor(placements)
    h_bd['w'] = int(h_bd['w']*2.2)
    h_gd['cspan'] = 2
    back_b = GenFunc('button', h_bd, 'Sign Out', h_gd)
    h_gd['cspan'] = 1
    h_bd['w'] = default_button_width
    back_b.widg.config(command=lambda: SignChoose(frame=home_frame))

    if accounts == []:
        #Disable chnage, delete, and get funcs since no accounts exist
        get_b.widg.config(state='disabled')
        change_b.widg.config(state='disabled')
        del_b.widg.config(state='disabled')

    home_frame.pack()
    root.bind_all('<Escape>', lambda e: SignChoose(frame=home_frame))
    return

def AddPassMenu(frame):
    '''Adding a password to DB,  MENU'''

    #Hiding previous frame to avoid colisions
    hideFrame(frame=frame)

    #Unbinding all hot keys to avoid errors
    root.unbind_all('<Escape>')
    root.unbind_all('<Return>')

    a_bd = BUTTON_DICT
    a_bd['w'] = 1
    a_bd['master'] = addP_frame
    a_ld = LABEL_DICT
    a_ld['master'] = addP_frame
    a_ld['w'] = 14
    a_ed = ENTRY_DICT
    a_ed['master'] = addP_frame
    a_ed['width'] = 30
    a_gd = gd

    placements = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
    
    #Row 1
    a_gd['row'], a_gd['column'], placements = GetFreeCoor(placements)
    userPrompt_l = GenFunc('label', a_ld, 'Account Name:', a_gd)

    a_gd['row'], a_gd['column'], placements = GetFreeCoor(placements)
    user_e = GenFunc('entry', a_ed, StringVar(), a_gd)

    #Row 2
    a_gd['row'], a_gd['column'], placements = GetFreeCoor(placements)
    passPrompt_l = GenFunc('label', a_ld, 'Password:', a_gd)

    a_gd['row'], a_gd['column'], placements = GetFreeCoor(placements)
    pass_e = GenFunc('entry', a_ed, StringVar(), a_gd)
    pass_e.widg.config(show=pass_dot)

    #Row 3
    a_gd['row'], a_gd['column'], placements = GetFreeCoor(placements)
    confPassPrompt_l = GenFunc('label', a_ld, 'Confirm Password:', a_gd)

    a_gd['row'], a_gd['column'], placements = GetFreeCoor(placements)
    confPass_e = GenFunc('entry', a_ed, StringVar(), a_gd)
    confPass_e.widg.config(show=pass_dot)

    #Row 4
    a_gd['cspan'] = 2
    a_gd['row'], a_gd['column'], placements = GetFreeCoor(placements)
    a_bd['w'] = default_button_width * 2
    generate_b = GenFunc('button', a_bd, 'Generate Password', a_gd)
    generate_b.widg.config(command= lambda: GenPass(generatedPass_e, pass_e, confPass_e))
    a_gd['row'], a_gd['column'], placements = GetFreeCoor(placements)
    a_gd['cspan'] = 1
    a_bd['w'] = default_button_width

    #Row 5
    a_gd['cspan'] = 2
    a_gd['row'], a_gd['column'], placements = GetFreeCoor(placements)
    a_ed['width'] = int(default_entry_width*2.5)
    generatedPass_e = GenFunc('entry', a_ed, '', a_gd)
    generatedPass_e.widg.config(state='readonly', justify=CENTER)
    a_ed['width'] = default_entry_width
    a_gd['row'], a_gd['column'], placements = GetFreeCoor(placements)
    a_gd['cspan'] = 1

    #Row 6
    a_gd['cspan'] = 2
    a_ld['w'] = 28
    a_gd['row'], a_gd['column'], placements = GetFreeCoor(placements)
    msg_l = GenFunc('label', a_ld, 'Enter Credentials', a_gd)
    a_gd['row'], a_gd['column'], placements = GetFreeCoor(placements)
    a_gd['cspan'] = 1
    a_ld['w'] = 14

    #Row 7
    a_bd['w'] = default_button_width
    a_gd['row'], a_gd['column'], placements = GetFreeCoor(placements)
    back_b = GenFunc('button', a_bd, 'Back', a_gd)
    back_b.widg.config(command= lambda: Home(frame=addP_frame))

    a_gd['row'], a_gd['column'], placements = GetFreeCoor(placements)
    go_b = GenFunc('button', a_bd, 'Add Password', a_gd)
    go_b.widg.config(command= lambda: AddPassConfirm(user_e.widg.get(), pass_e.widg.get(), confPass_e.widg.get(), msg_l))

    addP_frame.pack()
    root.bind_all('<Return>', lambda e: AddPassConfirm(user_e.widg.get(), pass_e.widg.get(), confPass_e.widg.get(), msg_l))
    root.bind_all('<Escape>', lambda e: Home(frame=addP_frame))
    return

#generating a password for the user
def GenPass(op_e, opPass_e, opConfPass_e):
    char_set = '1234567uj890qwertyuiiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    password = ''.join(r(char_set[0:char_set.index('M')+1], ri(10,16)))
    
    op_e.widg.config(state='active')
    ent_list = [op_e, opPass_e, opConfPass_e]
    for i in ent_list:
        i.widg.delete(0, END)
        i.widg.insert(END, password)
    
    ent_list[0].widg.config(state='readonly')
    return

#Deleting a password from one of the users accounts
def DeletePassMenu(frame):
    hideFrame(frame=frame)

    #Unbinding all hot keys to avoid errors
    root.unbind_all('<Escape>')
    root.unbind_all('<Return>')

    d_bd = BUTTON_DICT
    #d_bd['w'] = 20
    d_bd['master'] = delP_frame
    d_ld = LABEL_DICT
    d_ld['master'] = delP_frame
    d_ld['w'] = 25
    d_ed = ENTRY_DICT
    d_ed['master'] = delP_frame
    d_ed['width'] = default_entry_width
    d_gd = gd

    #MISC
    accounts = GetAccounts()#['hello', 'hellasdfasfas'] #Add below line here
    '''GetAccounts()''' #func definition at :128:


    placements = [[0,0],[0,0],[0,0],[0,0],[0,0]]

    #Row 1
    d_gd['row'], d_gd['column'], placements = GetFreeCoor(placements)
    acctPrompt_l = GenFunc('label', d_ld, 'Choose Account', d_gd)

    d_gd['row'], d_gd['column'], placements = GetFreeCoor(placements)
    combo = ttk.Combobox(master=delP_frame, values= accounts, state= 'readonly', width=23, justify=CENTER)

    combo.grid(row=d_gd['row'], column=d_gd['column'])
    combo.bind('<<ComboboxSelected>>', lambda event: msg_l.widg.config(text=''))

    #Row 2
    d_gd['row'], d_gd['column'], placements = GetFreeCoor(placements)
    passPrompt_l = GenFunc('label', d_ld, 'Account Password:', d_gd)

    d_gd['row'], d_gd['column'], placements = GetFreeCoor(placements)
    acctPass_e = GenFunc('entry', d_ed, '', d_gd)
    acctPass_e.widg.config(show=pass_dot)

    #Row 3
    d_gd['row'], d_gd['column'], placements = GetFreeCoor(placements)
    userPassPrompt_l = GenFunc('label', d_ld, 'Your Password', d_gd)

    d_gd['row'], d_gd['column'], placements = GetFreeCoor(placements)
    userPass_e = GenFunc('entry', d_ed, '', d_gd)
    userPass_e.widg.config(show=pass_dot)

    #Row 4
    d_gd['row'], d_gd['column'], placements = GetFreeCoor(placements)
    d_gd['cspan'] = 2
    d_ld['width'] = 25
    msg_l = GenFunc('label', d_ld, 'Fill Out Fields', d_gd)
    d_ld['width'] = None
    d_gd['cspan'] = 1
    d_gd['row'], d_gd['column'], placements = GetFreeCoor(placements)

    #Row 5
    d_gd['row'], d_gd['column'], placements = GetFreeCoor(placements)
    back_b = GenFunc('button', d_bd, 'Back', d_gd)
    back_b.widg.config(command=lambda: Home(frame=delP_frame))

    d_gd['row'], d_gd['column'], placements = GetFreeCoor(placements)
    go_b = GenFunc('button', d_bd, 'Delete Account', d_gd)
    go_b.widg.config(command=lambda: DelPassConfirm(account_name=combo.get(), accountPass=acctPass_e.widg.get(), userPass=userPass_e.widg.get(), label_obj=msg_l))
    
    if accounts != []:
        combo.current(0)
        root.bind_all('<Escape>', lambda e: Home(frame=delP_frame))
    else:
        combo.config(state='disabled')
        msg_l.widg.config(text='No acct, back to home in 5s')
        root.after(5000, lambda: Home(frame=delP_frame))

    delP_frame.pack()
    
    return

#MENU for getting a certain account's password
def GetPass(frame):
    '''
    MENU for getting an account password of a certain user
    '''
    hideFrame(frame=frame)

    #Unbinding all hot keys to avoid errors
    root.unbind_all('<Escape>')
    root.unbind_all('<Return>')

    g_bd = BUTTON_DICT
    g_bd['master'] = getP_frame
    #g_bd['w'] = 20
    g_ld = LABEL_DICT
    g_ld['master'] = getP_frame
    g_ld['w'] = 14
    g_gd = gd
    placements = [[0,0],[0,0],[0,0]]

    #Row 1
    g_gd['row'], g_gd['column'], placements = GetFreeCoor(placements)
    acctPrompt_l = GenFunc('label', g_ld, 'Account:', g_gd)
    
    g_gd['row'], g_gd['column'], placements = GetFreeCoor(placements)
    accounts = GetAccounts()
    combo = ttk.Combobox(master=getP_frame, values= accounts, state= 'readonly', width=23, justify=CENTER)
    combo.current(0)
    combo.grid(row=g_gd['row'], column=g_gd['column'])
    #combo.bind('<<ComboboxSelected>>', lambda event: msg_l.widg.config(text=''))

    #Row 2
    g_gd['row'], g_gd['column'], placements = GetFreeCoor(placements)
    g_gd['cspan'] = 2
    g_ld['w'] = 30
    msg_l = GenFunc('label', g_ld, 'Choose Account', g_gd)
    g_gd['cspan'] = 1
    g_gd['row'], g_gd['column'], placements = GetFreeCoor(placements)

    #Row 3
    g_gd['row'], g_gd['column'], placements = GetFreeCoor(placements)
    back_b = GenFunc('button', g_bd, 'Back', g_gd)
    back_b.widg.config(command=lambda: Home(frame=getP_frame))

    g_gd['row'], g_gd['column'], placements = GetFreeCoor(placements)
    go_b = GenFunc('button', g_bd, 'Get Password', g_gd)
    go_b.widg.config(command=lambda: GetPassword(combo.get(), msg_l))

    getP_frame.pack()

    root.bind_all("<Return>", lambda e: GetPassword(combo.get(), msg_l))
    root.bind_all('<Escape>', lambda e:Home(frame=getP_frame))
    return

def ChangePassMenu(frame):
    '''
    MENU for changing an account password of a certain user
    '''
    hideFrame(frame=frame)

    #Unbinding all hot keys to avoid errors
    root.unbind_all('<Escape>')
    root.unbind_all('<Return>')

    c_bd = BUTTON_DICT
    #c_bd['w'] = 20
    c_bd['master'] = changeP_frame
    c_ld = LABEL_DICT
    c_ld['master'] = changeP_frame
    c_ld['w'] = 14
    c_ed = ENTRY_DICT
    c_ed['master'] = changeP_frame
    c_ed['width'] = default_entry_width
    c_gd = gd

    placements = [[0,0],[0,0],[0,0],[0,0],[0,0]]

    #Row 1
    c_gd['row'], c_gd['column'], placements = GetFreeCoor(placements)
    acctPrompt_l = GenFunc('label', c_ld, 'Account:', c_gd)

    c_gd['row'], c_gd['column'], placements = GetFreeCoor(placements)
    accounts = GetAccounts()
    combo = ttk.Combobox(master=changeP_frame, values= accounts, state= 'readonly', width=23, justify=CENTER)
    combo.current(0)
    combo.grid(row=c_gd['row'], column=c_gd['column'])

    #Row 2
    c_gd['row'], c_gd['column'], placements = GetFreeCoor(placements)
    acctPassPrompt_l = GenFunc('label', c_ld, 'New Password:', c_gd)

    c_gd['row'], c_gd['column'], placements = GetFreeCoor(placements)
    newPass_e = GenFunc('entry', c_ed, '', c_gd)
    newPass_e.widg.config(show=pass_dot)

    #Row 3
    c_gd['row'], c_gd['column'], placements = GetFreeCoor(placements)
    userPassPrompt_l = GenFunc('label', c_ld, 'Your Password:', c_gd)

    c_gd['row'], c_gd['column'], placements = GetFreeCoor(placements)
    userPass_e = GenFunc('entry', c_ed, '', c_gd)
    userPass_e.widg.config(show=pass_dot)

    #Row 4
    c_gd['row'], c_gd['column'], placements = GetFreeCoor(placements)
    c_ld['w'] = 30
    c_gd['cspan'] = 2
    msg_l = GenFunc('label', c_ld, 'Fill Out Fields', c_gd)
    c_gd['row'], c_gd['column'], placements = GetFreeCoor(placements)
    c_ld['w'] = None
    c_gd['cspan'] = 1

    c_gd['row'], c_gd['column'], placements = GetFreeCoor(placements)
    back_b = GenFunc('button', c_bd, 'Back', c_gd)
    back_b.widg.config(command=lambda: Home(frame=changeP_frame))

    c_gd['row'], c_gd['column'], placements = GetFreeCoor(placements)
    go_b = GenFunc('button', c_bd, 'Change Password', c_gd)
    go_b.widg.config(command=lambda: ChangePassword(combo.get(), userPass_e.widg.get(), newPass_e.widg.get(), msg_l))

    changeP_frame.pack()
    c_ed['width'] = default_entry_width
    root.bind_all('<Return>', lambda e: ChangePassword(combo.get(), userPass_e.widg.get(), newPass_e.widg.get(), msg_l))
    root.bind_all('<Escape>', lambda e: Home(frame=changeP_frame))
    return

#WHILE signing IN
def CredVerSignIn(user, password, lab_obj):

    mycursorU = mydb.cursor( )
    mycursorP = mydb.cursor( )
    mycursorU.execute(f"select User from Users where User='{user}'")
    log = False
    users = mycursorU.fetchall( ) #list 
    if(users==[]):
        log = False
    else:
        mycursorP.execute(f"select Passcode from Users where User='{user}'")
        passwor = (mycursorP.fetchall( ))[0][0]
        if(passwor==password):
            log = True
    
    if(log==True):
        users = users[0][0]
        #successful
        global current_user
        current_user = user.lower( )
        Home(signIn_frame)
        return
    # acc doesnt exist 
    lab_obj.widg.config(text='Invalid Credentials!')

    mydb.commit( )
    return

#User Verify for Signing UP
def SignUpConf(user, password, conf_password, lab_obj):
    
    query = "INSERT INTO Users values(%s,%s)"
    myc = mydb.cursor( )
    if(len(user)<4):
        lab_obj.widg.config(text='Username length cannot be less than 4')
    else:
        if(password == conf_password):
            try:
                acc = [(user,password)]
                myc.executemany(query,acc)
                mydb.commit( )
                lab_obj.widg.config(text='Account Created')
                return
            except:
                lab_obj.widg.config(text="Account alredy exists!")
                return
        lab_obj.widg.config(text='Passwords dont match')
    return  

#Adding new acccount under a certain username
def AddPassConfirm(user, password, confPass, label_obj):
    print("REACHED CONFIRM FUNC")

    global current_user
    print(f"{current_user=}")
    account = user.capitalize( )
    print(f"{account=}")

    query1 = "Insert into Passwords values('" + str(current_user) + "',%s,%s)"
    query2 = f"select CurrUser from Passwords where Username='{user}'"
    myc = mydb.cursor( )
    myc1 = mydb.cursor( )
    c = 0

    print(f"{password=}")
    print(f"{confPass=}")
    if(password == confPass):

        myc1.execute(query2)
        l = myc1.fetchall( )
        li = []
        if(l==[]):
            c = 1
        else:
            for i in range(len(l)):
                li.append(l[i][0])
        print(f"{li=}")
        if(c==0):
            if(current_user in li):
                label_obj.widg.config(text=f'You have already added a password for this account\nMaybe you want to "CHANGE"')
            else:
                c = 1
        if(c==1):
            acc = [(account,password)]
            myc.executemany(query1,acc)
            label_obj.widg.config(text=f'Account Added to {current_user}')  
            mydb.commit( )      
            return
    else:
        label_obj.widg.config(text='Passwords do not match')
    return  

#Crosschecking credentials to verify a deletion of an account
def DelPassConfirm(account_name, accountPass, userPass, label_obj):

    try:
        if account_name == '':
            label_obj.widg.config(text='Account doesnt exist')
            root.after(5000, lambda: Home(frame=delP_frame))
            return
        print("REACHED CONFIRM FUNC")
        global current_user

        count1 = 0
        count2 = 0

        myc1 = mydb.cursor( )
        query1 = f"Select Password from Passwords where Username='{account_name}'"
        myc1.execute(query1)
        p1 = myc1.fetchall( )

        myc2 = mydb.cursor( )
        query2 = f"Select Passcode from Users where User='{current_user}'"
        myc2.execute(query2)
        p2 = myc2.fetchall( )

        if(accountPass==p1[0][0]):
            count1+=1
        if(userPass==p2[0][0]):
            count2+=1

        if(count1==1) and (count2==1):
            query = f"delete from Passwords where Username='{account_name}' and CurrUser='{current_user}'"
            myc = mydb.cursor( )
            myc.execute(query)
            label_obj.widg.config(text="Successfully deleted password")
            mydb.commit( )
        else:
            if(count1==0):
                label_obj.widg.config(text="Account password is wrong")
            else:
                label_obj.widg.config(text="Your password is wrong")
    except:
        label_obj.widg.config(text="Account doesnt exist")
    return

#Getting a certain user's password for a certain account
def GetPassword(account, label_obj):
    try:
        global current_user
        print("REACHED CONFIRM FUNC")

        query = f"select Password from Passwords where Username='{account}' and CurrUser='{current_user}'"
        myc = mydb.cursor( )
        myc.execute(query)
        li = myc.fetchall( )
        print(li)
        password = li[0][0]
        label_obj.widg.config(text=f'\"{password}\" copied to clipboard')
        pyperclip.copy(password)
        mydb.commit( )
    except:
        label_obj.widg.config(text="[ERROR]")
    return

#Changing a certain user's password for a certain account
def ChangePassword(account, user_password, new_account_pass, label_obj):
    print('REACHED VER FUNC')
    global current_user
    
    query = f"Select Passcode from Users where User='{current_user}'"
    myc = mydb.cursor( )
    myc.execute(query)
    li = myc.fetchall()
    p = li[0][0]
    
    if(user_password==p):
        query_update = f"Update Passwords set Password='{new_account_pass}' where Username='{account}' and CurrUser='{current_user}'"
        myc1 = mydb.cursor( )
        myc1.execute(query_update)
        label_obj.widg.config(text="Successfully updated password")
        mydb.commit( )
    else:
        label_obj.widg.config(text="Your password does not match current password")
    return

SignChoose(None)
root.mainloop()
