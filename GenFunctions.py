from tkinter import *
import tkinter.font as font
from tkinter import ttk
from tkinter.ttk import *
import tkinter as tk

theme = 'xpnative'
class GenFunc:
    FONT = None
    widg = None
    text = ''
    wd = {} #Widget Dictionary
    gd = {}
    #frame = None
    def __init__(self, type, widg_dict, text, grid_dict) -> None:
        #Assigning param variables to class variables
        self.FONT = 11
        self.text = text
        self.wd = widg_dict
        self.gd = grid_dict

        #checking type of widg (button, label, textbox), then call a function to create that specific widg
        if type.upper() == 'BUTTON':
            self.createB()
        elif type.upper() == 'LABEL':
            self.createL()
        elif type.upper() == 'ENTRY':
            self.createE()
        else:
            print('err: widget unidentified')
        return

    #Generating a BUTTON using parameters stored in a dictionary
    def createB(self):
        s=ttk.Style(master=None)
        s.theme_use(theme)
        s.configure(style=theme, font="Helvetica 10 bold")
        self.widg = Button(
            master= self.wd['master'],
            text=self.text,
            width=self.wd['w'],
            height=self.wd['height'],
            justify=self.wd['justify'],
            padx=self.wd['padx'],
            pady=self.wd['pady'],
            style='small.TButton'
        )

        s.configure('small.TButton', font=(None, self.FONT))
        self.widg.grid(
            column= self.gd['column'],
            row= self.gd['row'],
            columnspan= self.gd['cspan'],
            rowspan= self.gd['rspan'],
            padx= self.gd['padx'],
            pady= self.gd['pady'],
            ipadx= self.gd['ipadx'],
            ipady= self.gd['ipady']
        )
        return

    #Generating a LABEL using parameters stored in a dictionary
    def createL(self):
        s=ttk.Style(master=None)
        s.theme_use(theme)
        self.widg = tk.Label(
            master= self.wd['master'],
            text=  self.text,
            padx=  self.wd['padx'],
            pady=  self.wd['pady'],
            width=  self.wd['w'],
            wraplength=  self.wd['wraplength'],
            #style='small.TButton'
            font=(None, 11)
        )
        s.configure('xpnative', font=(None, self.FONT))
        self.widg.grid(
            column= self.gd['column'],
            row= self.gd['row'],
            columnspan= self.gd['cspan'],
            rowspan= self.gd['rspan'],
            padx= self.gd['padx'],
            pady= self.gd['pady'],
            ipadx= self.gd['ipadx'],
            ipady= self.gd['ipady']
        )
        return

    #Generating a ENTRY (aka textbox) using parameters stored in a dictionary
    def createE(self):
        s=ttk.Style(master=None)
        s.theme_use(theme)
        self.widg = Entry(
            master= self.wd['master'],
            textvariable= self.text,
            width= self.wd['width'],
        )
        self.widg.grid(
            column= self.gd['column'],
            row= self.gd['row'],
            columnspan= self.gd['cspan'],
            rowspan= self.gd['rspan'],
            padx= self.gd['padx'],
            pady= self.gd['pady'],
            ipadx= self.gd['ipadx'],
            ipady= self.gd['ipady']
        )
        return
