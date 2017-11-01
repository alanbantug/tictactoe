#! python3

### This utility will copy a folder and its contents into a different folder
###
import Tkinter
from Tkinter import *

import ttk
from ttk import *

from tkFileDialog import askdirectory
from tkFileDialog import askopenfilename

import os
import shutil
import datetime 
import tkMessageBox

from time import time
import subprocess as sp

class Application(Frame):

    def __init__(self, master):
        
        self.master = master
        self.main_container = Frame(self.master)

        # Define the source and target folder variables
        
        self.origin = os.getcwd()
        self.copied = IntVar()
        self.copying = 0
        self.source = ""
        self.target = ""
        self.script = ""
        self.allSet = True
        self.getMatch3 = IntVar()
        self.getMatch4 = IntVar()
        self.getMatch5 = IntVar()
        self.numberA = StringVar()
        self.numberB = StringVar()
        self.numberC = StringVar()
        self.numberD = StringVar()
        self.numberE = StringVar()

        self.buttonVar = []

        for i in range(9):
            self.buttonVar.append(StringVar())
        
        # Create main frame
        self.main_container.grid(column=0, row=0, sticky=(N,S,E,W))

        # Set Label styles
        Style().configure("M.TLabel", font="Courier 20 bold", height="20", foreground="blue", background="white", anchor="center")
        Style().configure("B.TLabel", font="Verdana 8", background="white", width="38")
        Style().configure("MS.TLabel", font="Verdana 10" )
        Style().configure("S.TLabel", font="Verdana 8" )
        Style().configure("G.TLabel", font="Verdana 8")

        # Set button styles
        Style().configure("B.TButton", font="Verdana 8", width=10, highlightthickness=4, relief="ridge")
        Style().configure("BL.TButton", font="Courier 40", width=2, relief="raised")

        # Set check button styles
        Style().configure("B.TCheckbutton", font="Verdana 8")

        Style().configure("L.TListbox", font="Verdana 8", width="40")
        Style().configure("E.TEntrybox", width="10")

        
        Style().configure("O.TLabelframe.Label", font="Verdana 8", foreground="black")
        
        # Create widgets
        self.sep_ah = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_bh = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_ch = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_dh = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_eh = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_fh = Separator(self.main_container, orient=HORIZONTAL)
        
        self.sep_av = Separator(self.main_container, orient=VERTICAL)
        self.sep_bv = Separator(self.main_container, orient=VERTICAL)
        self.sep_cv = Separator(self.main_container, orient=VERTICAL)
        self.sep_dv = Separator(self.main_container, orient=VERTICAL)
        self.sep_ev = Separator(self.main_container, orient=VERTICAL)
        self.sep_fv = Separator(self.main_container, orient=VERTICAL)

        self.mainLabel = Label(self.main_container, text="TIC-TAC-TOE", style="M.TLabel" )
        self.subLabelA = Label(self.main_container, text="Play Tic-Tac-Toe against the machine. ", style="S.TLabel" )
        self.subLabelB = Label(self.main_container, text="Train the machine to make the game more challenging. ", style="S.TLabel" )

        # Create the button selection widgets
        
        self.buttonArray = []

        for i in range(9):
            #self.buttonArray.append(Button(self.main_container, text='*', style="BL.TButton", command=self.selectResponse))
            self.buttonArray.append(Button(self.main_container, text='*', style="BL.TButton"))

        for i in range(9):
            self.buttonArray[i].bind(['<Enter>', i], self.enterEvent)
            #self.buttonArray[i].bind('<FocusOut>', self.outFocus)

        '''   
        self.button_1 = Button(self.main_container, text="1", style="BL.TButton", command=self.selectResponse)
        self.button_2 = Button(self.main_container, text="*", style="BL.TButton", command=self.selectResponse)
        self.button_3 = Button(self.main_container, text="*", style="BL.TButton", command=self.selectResponse)
        self.button_4 = Button(self.main_container, text="*", style="BL.TButton", command=self.selectResponse)
        self.button_5 = Button(self.main_container, text="*", style="BL.TButton", command=self.selectResponse)
        self.button_6 = Button(self.main_container, text="*", style="BL.TButton", command=self.selectResponse)
        self.button_7 = Button(self.main_container, text="*", style="BL.TButton", command=self.selectResponse)
        self.button_8 = Button(self.main_container, text="*", style="BL.TButton", command=self.selectResponse)
        self.button_9 = Button(self.main_container, text="*", style="BL.TButton", command=self.selectResponse)
        '''

        self.trainMachine = Button(self.main_container, text="TRAIN", style="B.TButton", command=self.checkTraining)
        self.resetGame = Button(self.main_container, text="RESET", style="B.TButton", command=self.resetButtons)
        self.exitGame = Button(self.main_container, text="EXIT", style="B.TButton", command=root.destroy)

        self.progress_bar = Progressbar(self.main_container, orient="horizontal", mode="indeterminate", maximum=50)
        
        # Position widgets        
        self.mainLabel.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.subLabelA.grid(row=1, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')
        self.subLabelB.grid(row=2, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')
        #self.subLabelC.grid(row=3, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')

        self.sep_ah.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        # Position the first 3 button selection widgets

        for i in range(3):
            idx = i
            self.buttonArray[i].grid(row=4, column=i, padx=10, pady=(5, 10), sticky='NSEW')    

        '''
        self.button_1.grid(row=4, column=0, padx=10, pady=(5, 10), sticky='NSEW')
        self.button_2.grid(row=4, column=1, padx=10, pady=(5, 10), sticky='NSEW')
        self.button_3.grid(row=4, column=2, padx=10, pady=(5, 10), sticky='NSEW')
        '''

        self.sep_bh.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        for i in range(3):
            idx = i + 3
            self.buttonArray[idx].grid(row=6, column=i, padx=10, pady=(5, 10), sticky='NSEW')    
        
        '''
        self.button_4.grid(row=6, column=0, padx=10, pady=(5, 10), sticky='NSEW')
        self.button_5.grid(row=6, column=1, padx=10, pady=(5, 10), sticky='NSEW')
        self.button_6.grid(row=6, column=2, padx=10, pady=(5, 10), sticky='NSEW')
        '''

        self.sep_ch.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        for i in range(3):
            idx = i + 6
            self.buttonArray[idx].grid(row=8, column=i, padx=10, pady=(5, 10), sticky='NSEW')    

        '''
        self.button_7.grid(row=8, column=0, padx=10, pady=(5, 10), sticky='NSEW')
        self.button_8.grid(row=8, column=1, padx=10, pady=(5, 10), sticky='NSEW')
        self.button_9.grid(row=8, column=2, padx=10, pady=(5, 10), sticky='NSEW')
        '''

        self.sep_dh.grid(row=9, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.trainMachine.grid(row=10, column=0, padx=10, pady=5, sticky='NSEW')
        self.resetGame.grid(row=10, column=1, padx=10, pady=5, sticky='NSEW')
        self.exitGame.grid(row=10, column=2, padx=10, pady=5, sticky='NSEW')

        self.sep_eh.grid(row=11, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.progress_bar.grid(row=12, column=0, columnspan=3, padx=10, pady=5, sticky='NSEW')

    def enterEvent(self, event, i):

        self.buttonArray[i]['text'] = 'X'

    def leaveEvent(self, event):

        for i in range(9):
            if self.buttonArray[i]['state'] == ACTIVE:
                self.buttonArray[i]['text'] = ''

    def selectResponse(self):

        # tkMessageBox.showinfo('Responding')

        for i in range(9):
            self.buttonArray[i]['state'] = ACTIVE
            #if self.buttonArray[i]["state"] == ACTIVE:
            #    print 'active'
            #    self.buttonArray[i]['state'] = DISABLED

        
    def resetButtons(self):

        ''' This function will select reset the buttons
        '''

        for i in range(9):
            self.buttonArray[i]['state'] = NORMAL
            self.buttonArray[i]['text'] = '*'


    def checkTraining(self):

        response = tkMessageBox.askquestion('Train Machine', 'Are you sure you want to train the machine?')            

        if response == 'yes':
            self.startTraining()

    def startTraining(self):

        import threading

        t = threading.Thread(None, self.trainMachine, ())
        t.start()


    def trainMachine(self):

        self.progress_bar.start()

        tkMessageBox.showinfo('Training', 'Training Complete. Reset game if needed')

        self.progress_bar.stop()            
        

root = Tk()
root.title("TIC - TAC - TOE")
#root.minsize(480, 380)
#root.maxsize(480, 380)

# Set size

wh = 460
ww = 340

#root.resizable(height=False, width=False)

root.minsize(ww, wh)
root.maxsize(ww, wh)

# Position in center screen

ws = root.winfo_screenwidth() 
hs = root.winfo_screenheight() 

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (ww/2)
y = (hs/2) - (wh/2)

root.geometry('%dx%d+%d+%d' % (ww, wh, x, y))

app = Application(root)

root.mainloop()
