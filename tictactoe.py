#! python3

### This utility will copy a folder and its contents into a different folder
###
import tkinter
from tkinter import *

from tkinter.ttk import *
from tkinter import messagebox

from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename

import os
import shutil
import random
import datetime

import time
import subprocess as sp

import itertools

from tagent import LearningAgent

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
        Style().configure("M.TLabel", font="Courier 24 bold", height="20", foreground="blue", anchor="center")
        Style().configure("B.TLabel", font="Verdana 8", background="white", width="38")
        Style().configure("MS.TLabel", font="Verdana 10" )
        Style().configure("S.TLabel", font="Verdana 8" )
        Style().configure("G.TLabel", font="Verdana 8")

        # Set button styles
        Style().configure("B.TButton", font="Verdana 8", width=18, highlightthickness=4, relief="ridge")
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
        self.resetGame = Button(self.main_container, text="RESET", style="B.TButton", command=self.resetGame)
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

        self.trainMachine.grid(row=11, column=0, padx=5, pady=5, sticky='W')
        self.resetGame.grid(row=11, column=0, padx=(150,5), pady=5, sticky='W')
        self.exitGame.grid(row=12, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.sep_eh.grid(row=13, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.progress_bar.grid(row=14, column=0, columnspan=3, padx=10, pady=5, sticky='NSEW')

        self.machineTrained.set(0)
        self.winner.set(0)

        ## create agent here
        self.agent = LearningAgent()

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

                if self.checkWinner('X', True):

                    messagebox.showinfo('You Win!', 'Congratulations, you win!')

                else:

                    self.machineSelection()


    def machineSelection(self):

        # Get all available selections

        state = tuple([x['text'] if x['text'] != ' ' else None for x in self.buttonArray])

        idx_options = []
        for i in range(9):
            if self.buttonVar[i].get() == 'S':
                pass
            else:
                idx_options.append(i)

        # Randomly select from available selections if there are more options

        if state.count('X') + state.count('O') < 9:

            idx_selection = self.agent.choose_action(state)

            # Set the choice of the computer
            self.buttonArray[idx_selection]['text'] = 'O'
            self.buttonVar[idx_selection].set("S")

            if self.checkWinner('O', True):

                messagebox.showinfo('Computer Wins!', 'Computer wins!')

        else:
            response = messagebox.askquestion('Tied Game!', 'It"s a tie! Do you want to play again?')

            if response == 'yes':
                for i in range(9):
                    self.buttonArray[i]['state'] = NORMAL
                    self.buttonArray[i]['text'] = ' '
                    self.buttonVar[i].set("")

    def updateAgent(self):

        state = [x['text'] if x['text'] != ' ' else None for x in self.buttonArray]

        return self.agent.update(state, self.winner.get())


    def checkWinner(self, mark, disabl):

        if (self.buttonArray[0]['text'] == self.buttonArray[1]['text'] == self.buttonArray[2]['text'] == mark ) or \
           (self.buttonArray[3]['text'] == self.buttonArray[4]['text'] == self.buttonArray[5]['text'] == mark ) or \
           (self.buttonArray[6]['text'] == self.buttonArray[7]['text'] == self.buttonArray[8]['text'] == mark ) or \
           (self.buttonArray[0]['text'] == self.buttonArray[3]['text'] == self.buttonArray[6]['text'] == mark ) or \
           (self.buttonArray[1]['text'] == self.buttonArray[4]['text'] == self.buttonArray[7]['text'] == mark ) or \
           (self.buttonArray[2]['text'] == self.buttonArray[5]['text'] == self.buttonArray[8]['text'] == mark ) or \
           (self.buttonArray[0]['text'] == self.buttonArray[4]['text'] == self.buttonArray[8]['text'] == mark ) or \
           (self.buttonArray[2]['text'] == self.buttonArray[4]['text'] == self.buttonArray[6]['text'] == mark ):
           if mark == 'X':
               self.winner.set(1)
           else:
               self.winner.set(2)

           if disabl:
               for i in range(9):
                   self.buttonArray[i]['state'] = DISABLED
           return True

        return False


    def resetGame(self):

        ''' This function will select reset the buttons
        '''
        if self.winner.get() == 0:

            response = messagebox.askquestion('Game Reset', 'Are you sure you want to reset the game?')

            if response == 'no':
                return

        self.resetButtons()

    def resetButtons(self):

        for i in range(9):
            self.buttonArray[i]['state'] = NORMAL
            self.buttonArray[i]['text'] = ' '
            self.buttonVar[i].set("")

        self.winner.set(0)

    def checkTraining(self):

        response = messagebox.askquestion('Train Machine', 'Are you sure you want to train the machine?')

        if response == 'yes':

            #messagebox.showwarning('Training', 'Training is currently unavailable.')

            self.startTraining()
            #self.machineTrained.set(1)

    def startTraining(self):

        import threading

        t = threading.Thread(None, self.trainComputer, ())
        t.start()


    def trainComputer(self):

        ''' This code will check which of the combinations have winning patterns
        '''

        winning_idx = [(0,1,2), (0,3,6), (0,4,8), (1,4,7), (2,4,6), (2,5,8), (3,4,5), (6,7,8)]

        self.progress_bar.start()

        self.agent = LearningAgent(True, 1.0, 0.5)

        while winning_idx:

            sub_idx = list(winning_idx.pop(0))
            # sub_idx.append(random.choice([i for i in range(9) if i not in sub_idx]))

            iterator = itertools.permutations(sub_idx)
            # add two more numbers
            # sub_indices.append(random.choice([i for i in range(9) if i not in sub_indices]))

            # use the same pattern 10 times to generate more data
            while True:

                try:
                    indices = next(iterator)
                except:
                    break

                self.agent.reset()

                for i in range(10):

                    # shuffle
                    # random.shuffle(sub_indices)
                    # iterator = iter(sub_indices)
                    iter_idx = iter(indices)

                    continue_game = True
                    getX = True

                    while continue_game:

                        options, selected = self.getSelection()

                        if len(options) > 0:

                            if getX:

                                idx = next(iter_idx)

                                self.buttonArray[idx]['text'] = 'X'
                                self.buttonVar[idx].set("S")

                                time.sleep(0.05)

                                if self.checkWinner('X', False):

                                    # update the state and action last done to show it was a bad choice
                                    self.agent.update(None, None, self.winner.get())

                                    continue_game = False

                                getX = False

                            else:

                                # get the state and the suggested action
                                state = tuple([x['text'] if x['text'] != ' ' else None for x in self.buttonArray])

                                idx_selection = self.agent.choose_action(state)

                                while idx_selection in indices:
                                    idx_selection = self.agent.choose_action(state)

                                self.buttonArray[idx_selection]['text'] = 'O'
                                self.buttonVar[idx_selection].set("S")

                                time.sleep(0.05)

                                if self.checkWinner('O', False):
                                    continue_game = False

                                # update the Q whether the computer wins or not
                                self.agent.update(state, idx_selection, self.winner.get())

                                getX= True

                        else:
                            continue_game = False

                    self.resetButtons()

        self.progress_bar.stop()

        print(len(self.agent.get_queues()))
        messagebox.showinfo('Training', 'Training Complete.')

    def trainComputerv2(self):

        self.progress_bar.start()

        # get all possible combination of indices taken five at a time
        idx_sets = itertools.combinations([i for i in range(9)], 5)

        self.agent = LearningAgent(True, 1.0, 0.5)

        while True:

            try:
                idx_set = next(idx_sets)
            except:
                break

            random.shuffle(list(idx_set))

            iterator = iter(idx_set)

            self.agent.reset()

            continue_game = True
            getX = True

            while continue_game:

                options, selected = self.getSelection()

                if len(options) > 0:

                    if getX:

                        idx = next(iterator)

                        self.buttonArray[idx]['text'] = 'X'
                        self.buttonVar[idx].set("S")

                        time.sleep(0.2)

                        if self.checkWinner('X', False):

                            # update the state and action last done to show it was a bad choice
                            self.agent.update(None, None, self.winner.get())

                            continue_game = False

                        getX = False

                    else:

                        # get the state and the suggested action
                        state = tuple([x['text'] if x['text'] != ' ' else None for x in self.buttonArray])

                        idx_selection = self.agent.choose_action(state)

                        while idx_selection in idx_set:
                            idx_selection = self.agent.choose_action(state)

                        self.buttonArray[idx_selection]['text'] = 'O'
                        self.buttonVar[idx_selection].set("S")

                        time.sleep(0.2)

                        if self.checkWinner('O', False):
                            continue_game = False

                        # update the Q whether the computer wins or not
                        self.agent.update(state, idx_selection, self.winner.get())

                        getX= True

                else:
                    continue_game = False

            self.resetButtons()

        self.progress_bar.stop()

        print(len(self.agent.get_queues()))
        messagebox.showinfo('Training', 'Training Complete.')

    def trainComputerv1(self):

        self.progress_bar.start()

        # get all possible combination of indices taken five at a time
        idx_sets = itertools.combinations([i for i in range(9)], 5)

        self.agent = LearningAgent(True, 1.0, 0.5)

        while True:

            try:
                idx_set = next(idx_sets)
            except:
                break

            iterator = iter(idx_set)

            self.agent.reset()

            continue_game = True
            getX = True

            while continue_game:

                options, selected = self.getSelection()

                if len(options) > 0:

                    if getX:

                        try:
                            idx = next(iterator)
                        except:
                            break

                        while True:

                            if idx in selected:
                                idx += 1

                                if idx > 8:
                                    # get the first index that is not selected
                                    idx = min([i for i in range(9) if i not in selected])

                            else:
                                self.buttonArray[idx]['text'] = 'X'
                                self.buttonVar[idx].set("S")

                                time.sleep(0.5)

                                if self.checkWinner('X', False):

                                    # update the state and action last done to show it was a bad choice
                                    self.agent.update(None, None, self.winner.get())

                                    continue_game = False

                                break


                        getX = False

                    else:

                        # get the state and the suggested action
                        state = tuple([x['text'] if x['text'] != ' ' else None for x in self.buttonArray])
                        idx_selection = self.agent.choose_action(state)

                        self.buttonArray[idx_selection]['text'] = 'O'
                        self.buttonVar[idx_selection].set("S")

                        time.sleep(0.5)

                        if self.checkWinner('O', False):
                            continue_game = False

                        # update the Q
                        self.agent.update(state, idx_selection, self.winner.get())

                        getX= True

                else:
                    continue_game = False

            self.resetButtons()

        print(len(self.agent.get_queues()))
        self.progress_bar.stop()

        messagebox.showinfo('Training', 'Training Complete.')

    def trainComputerv0(self):

        self.progress_bar.start()

        self.agent = LearningAgent(True, 0.3, 0.5)

        for i in range(100):

            self.agent.reset()

            continue_game = True
            getX = True

            while continue_game:

                # get the available selections
                idx_options = self.getSelection()

                # if there are more selections, get. else exit loop
                if len(idx_options) > 0:

                    if getX:

                        self.randomX(idx_options)

                        if self.checkWinner('X', False):

                            # update the state and action last done to show it was a bad choice
                            self.agent.update(None, None, self.winner.get())

                            continue_game = False

                        getX = False
                    else:

                        # get the state and the suggested action
                        state = tuple([x['text'] if x['text'] != ' ' else None for x in self.buttonArray])
                        idx_selection = self.agent.choose_action(state)

                        self.buttonArray[idx_selection]['text'] = 'O'
                        self.buttonVar[idx_selection].set("S")

                        time.sleep(0.1)

                        if self.checkWinner('O', False):
                            continue_game = False

                        # update the Q
                        self.agent.update(state, idx_selection, self.winner.get())

                        getX = True
                else:
                    continue_game = False


            self.resetButtons()

        self.progress_bar.stop()

        messagebox.showinfo('Training', 'Training Complete.')

    def getSelection(self):

        idx_options = []
        selected = []

        for i in range(9):
            if self.buttonVar[i].get() == 'S':
                selected.append(i)
            else:
                idx_options.append(i)

        return idx_options, selected

    def randomX(self, idx_options):

        idx_selection = random.choice(idx_options)

        self.buttonArray[idx_selection]['text'] = 'X'
        self.buttonVar[idx_selection].set("S")

        time.sleep(0.1)

        return idx_selection

    def randomO(self, idx_options):

        idx_selection = random.choice(idx_options)

        self.buttonArray[idx_selection]['text'] = 'O'
        self.buttonVar[idx_selection].set("S")

        time.sleep(0.05)

        return idx_selection

root = Tk()
root.title("TIC - TAC - TOE")

# Set size

wh = 510
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
