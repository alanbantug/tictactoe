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
import random
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
        self.machineTrained = IntVar()
        self.winner = IntVar()

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
        Style().configure("BL.TButton", font="Courier 40 bold", width=2, borderwidth="0", relief="flat")

        # Set check button styles
        Style().configure("B.TCheckbutton", font="Verdana 8")

        Style().configure("L.TListbox", font="Verdana 8", width="40")
        Style().configure("E.TEntrybox", width="10")

        Style().configure("S.TSeparator", borderwidth=8, background="black", relief="flat")
        
        Style().configure("O.TLabelframe.Label", font="Verdana 8", foreground="black")
        
        # Create widgets
        self.sep_ah = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_bh = Separator(self.main_container, style="S.TSeparator", orient=HORIZONTAL)
        self.sep_ch = Separator(self.main_container, style="S.TSeparator", orient=HORIZONTAL)
        self.sep_dh = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_eh = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_fh = Separator(self.main_container, orient=HORIZONTAL)
        
        self.sep_av = Separator(self.main_container, style="S.TSeparator", orient=VERTICAL)
        self.sep_bv = Separator(self.main_container, style="S.TSeparator", orient=VERTICAL)
        self.sep_cv = Separator(self.main_container, style="S.TSeparator", orient=VERTICAL)
        self.sep_dv = Separator(self.main_container, style="S.TSeparator", orient=VERTICAL)
        self.sep_ev = Separator(self.main_container, style="S.TSeparator", orient=VERTICAL)
        self.sep_fv = Separator(self.main_container, style="S.TSeparator", orient=VERTICAL)

        self.mainLabel = Label(self.main_container, text="TIC-TAC-TOE", style="M.TLabel" )
        self.subLabelA = Label(self.main_container, text="Let's play Tic-Tac-Toe!", style="S.TLabel" )
        self.subLabelB = Label(self.main_container, text="Play against the machine, or train the machine", style="S.TLabel")
        self.subLabelC = Label(self.main_container, text="to make the game more challenging.", style="S.TLabel")

        # Create the button selection widgets
        
        self.buttonArray = []

        for i in range(9):
            self.buttonArray.append(Button(self.main_container, text=' ', style="BL.TButton", command=self.markSelection))

        for i in range(9):
            self.buttonArray[i].bind('<Enter>', lambda event, idx=i: self.enterEvent(idx))
            self.buttonArray[i].bind('<Leave>', lambda event, idx=i: self.leaveEvent(idx))

        self.trainMachine = Button(self.main_container, text="TRAIN", style="B.TButton", command=self.checkTraining)
        self.resetGame = Button(self.main_container, text="RESET", style="B.TButton", command=self.resetButtons)
        self.exitGame = Button(self.main_container, text="EXIT", style="B.TButton", command=root.destroy)

        self.progress_bar = Progressbar(self.main_container, orient="horizontal", mode="indeterminate", maximum=50)
        
        # Position widgets        
        self.mainLabel.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.subLabelA.grid(row=1, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')
        self.subLabelB.grid(row=2, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')
        self.subLabelC.grid(row=3, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')

        self.sep_ah.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        # Position the first 3 button selection widgets

        px = 10
        for i in range(3):
            idx = i 
            self.buttonArray[idx].grid(row=5, column=0, padx=(px, 10), pady=10, sticky='W')   
            px += 100 

        self.sep_av.grid(row=5, column=0, rowspan=1, padx=(96,5), pady=(5,0), sticky='NSW')
        self.sep_bv.grid(row=5, column=0, rowspan=1, padx=(196,5), pady=(5,0), sticky='NSW')

        self.sep_bh.grid(row=6, column=0, padx=5, pady=0, sticky='NSEW')

        px = 10
        for i in range(3):
            idx = i + 3
            self.buttonArray[idx].grid(row=7, column=0, padx=(px, 10), pady=10, sticky='W')   
            px += 100 
        
        self.sep_cv.grid(row=7, column=0, rowspan=1, padx=(96,5), pady=0, sticky='NSW')
        self.sep_dv.grid(row=7, column=0, rowspan=1, padx=(196,5), pady=0, sticky='NSW')

        self.sep_ch.grid(row=8, column=0, padx=5, pady=0, sticky='NSEW')

        px = 10
        for i in range(3):
            idx = i + 6
            self.buttonArray[idx].grid(row=9, column=0, padx=(px, 10), pady=10, sticky='W')   
            px += 100 

        self.sep_ev.grid(row=9, column=0, rowspan=1, padx=(96,5), pady=(0, 5), sticky='NSW')
        self.sep_fv.grid(row=9, column=0, rowspan=1, padx=(196,5), pady=(0, 5), sticky='NSW')

        self.sep_dh.grid(row=10, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.trainMachine.grid(row=11, column=0, padx=10, pady=5, sticky='W')
        self.resetGame.grid(row=11, column=0, padx=(110,10), pady=5, sticky='W')
        self.exitGame.grid(row=11, column=0, padx=(210,10), pady=5, sticky='W')

        self.sep_eh.grid(row=12, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.progress_bar.grid(row=13, column=0, columnspan=3, padx=10, pady=5, sticky='NSEW')

        self.machineTrained.set(0)
        self.winner.set(0)


    def enterEvent(self, i):

        if self.buttonVar[i].get() == 'S':
            pass
        else:
            self.buttonArray[i]['text'] = 'X'
            self.buttonVar[i].set("A")

        self.buttonVar[i].get()

    def leaveEvent(self, i):

        if self.buttonVar[i].get() == 'S':
            pass
        else:
            self.buttonArray[i]['text'] = ' '
            self.buttonVar[i].set("")

    def markSelection(self):

        for i in range(9):
            if self.buttonVar[i].get() == 'A':
                self.buttonArray[i]['text'] = 'X'
                self.buttonVar[i].set("S")

                if self.checkWinner('X'):

                    tkMessageBox.showinfo('You Win!', 'Congratulations, you win!')

                else:

                    self.machineSelection()


    def machineSelection(self):

        # Get all available selections  

        idx_options = []

        for i in range(9):
            if self.buttonVar[i].get() == 'S':
                pass
            else:
                idx_options.append(i)

        # Randomly select from available selections if there are more options

        if len(idx_options) > 0:
            idx_selection = random.choice(idx_options)

            # Set the choice of the computer
            self.buttonArray[idx_selection]['text'] = 'O'
            self.buttonVar[idx_selection].set("S")

            if self.checkWinner('O'):

                tkMessageBox.showinfo('Computer Wins!', 'Computer wins!')


        else:
            response = tkMessageBox.askquestion('Tied Game!', 'It"s a tie! Do you want to play again?')

            if response == 'yes':
                for i in range(9):
                    self.buttonArray[i]['state'] = NORMAL
                    self.buttonArray[i]['text'] = ' '
                    self.buttonVar[i].set("")

    def checkWinner(self, mark):

        if (self.buttonArray[0]['text'] == self.buttonArray[1]['text'] == self.buttonArray[2]['text'] == mark ) or \
           (self.buttonArray[3]['text'] == self.buttonArray[4]['text'] == self.buttonArray[5]['text'] == mark ) or \
           (self.buttonArray[6]['text'] == self.buttonArray[7]['text'] == self.buttonArray[8]['text'] == mark ) or \
           (self.buttonArray[0]['text'] == self.buttonArray[3]['text'] == self.buttonArray[6]['text'] == mark ) or \
           (self.buttonArray[1]['text'] == self.buttonArray[4]['text'] == self.buttonArray[7]['text'] == mark ) or \
           (self.buttonArray[2]['text'] == self.buttonArray[5]['text'] == self.buttonArray[8]['text'] == mark ) or \
           (self.buttonArray[0]['text'] == self.buttonArray[4]['text'] == self.buttonArray[8]['text'] == mark ) or \
           (self.buttonArray[2]['text'] == self.buttonArray[4]['text'] == self.buttonArray[6]['text'] == mark ):
            self.winner.set(1)

            # if a winner is found, disable all the buttons

            for i in range(9):
                self.buttonArray[i]['state'] = DISABLED

            return True

        else:
            return False


    def resetButtons(self):

        ''' This function will select reset the buttons
        '''
        if self.winner.get() == 0:

            response = tkMessageBox.askquestion('Game Reset', 'Are you sure you want to reset the game?')

            if response == 'no':
                return

        for i in range(9):
            self.buttonArray[i]['state'] = NORMAL
            self.buttonArray[i]['text'] = ' '
            self.buttonVar[i].set("")

        self.winner.set(0)



    def checkTraining(self):

        response = tkMessageBox.askquestion('Train Machine', 'Are you sure you want to train the machine?')            

        if response == 'yes':

            tkMessageBox.showwarning('Training', 'Training is currently unavailable.')
            
            #self.startTraining()
            #self.machineTrained.set(1)


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

# Set size

wh = 450
ww = 300

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
