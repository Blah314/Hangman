from random import *
from tkinter import *

class Category(object):
    def __init__(self,name,p_easy,p_medium,p_hard):
        self.name = name
        self.easy = p_easy
        self.medium = p_medium
        self.hard = p_hard
        self.used = False

    def is_used(self):
        return self.used

    def get_name(self):
        return self.name

    def load_phrase(self,diff):
        self.used = True
        if diff == 'EASY':
            return Phrase(choice(self.easy))
        elif diff == 'MEDIUM':
            return Phrase(choice(self.medium))
        else:
            return Phrase(choice(self.hard))

class Phrase(object):  
    def __init__(self,phrase):
        self.correct_phrase = phrase
        self.phrase = self.process_phrase(phrase)
        self.letters_in = []
        for i in self.correct_phrase:
            if i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and i not in self.letters_in:
                self.letters_in.append(i)
        self.guesses = []
        self.wrongs = []
        self.is_solved = False

    def process_phrase(self,phrase):
        exceptions = ',:\'1234567890 &@#$!<>.()*^%-'
        dashes = []
        for letter in phrase:
            if letter in exceptions:
                dashes.append(letter)
            else:
                dashes.append('_')
        return dashes
        
    def print_guess(self,guess):
        display = ''
        for letter in guess[:-1]:
            display += letter + ' '
        return display

    def print_curr_guess(self):
        return self.print_guess(self.phrase)

    def print_model_guess(self):
        return self.print_guess(self.correct_phrase)

    def guess(self,letter):
        self.guesses.append(letter)
        if letter not in self.correct_phrase:
            self.wrongs.append(letter)
            return False
        else:
            count = 0
            for i in range(len(self.correct_phrase)):
                if self.correct_phrase[i] == letter:
                    self.phrase[i] = letter
                    count += 1

            if '_' not in self.phrase[:-1]:
                self.is_solved = True
            
            return (True,count)
    
    def reveal(self):
        not_guessed = []
        for i in self.letters_in:
            if i not in self.guesses:
                not_guessed.append(i)
        x = choice(not_guessed)
        self.guess(x)

    def elim(self):
        not_in = []
        l = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for letter in l:
            if letter not in self.letters_in and letter not in self.guesses:
                not_in.append(letter)
        for i in range(5):
            if not_in:
                x = choice(not_in)
                not_in.remove(x)
                self.guesses.append(x)

def load_help(): #Help screen
    b1.pack_forget()
    b2.pack_forget()
    b3.pack_forget()
    title.config(text='HELP')
    title2.config(text='10 Hangman Puzzles ... 10 categories.\nThe puzzles get more difficult as you advance.\n\nClick the letters to guess them...\n They will appear if they are in the phrase, if not you lose a life!\nYou have limited lives, so make every guess count!')
    title3.config(text='You have 4 power-ups at your disposal...')
    title3.pack()
    helpframe.pack()
    title4.config(text='You can\'t use any powerups in the last round.\n\nGood Luck!')
    title4.pack()
    b1.pack()
    b2.pack()

def sel_difficulty(): #Difficulty select
    lifecounter.pack_forget()
    helpframe.pack_forget()
    guess_frame.pack_forget()
    b1.pack_forget()
    b2.pack_forget()
    b3.pack_forget()
    title.config(text='Select your Difficulty...')
    title2.config(text = '')
    title2.pack_forget()
    title3.pack_forget()
    title4.pack_forget()
    b7.pack()
    b8.pack()
    b9.pack()
    title2.pack()
    b2.pack()
    
def start_game(diff): #main game function
    guess_frame.pack_forget()
    powerups.pack_forget()
    b2.pack_forget()
    b7.pack_forget()
    b8.pack_forget()
    b9.pack_forget()
    title2.pack_forget()
    def load_phrases(): #loads categories and phrases from the file provided
        cat_count = 0
        cats = []
        with open('hangman_phrases.txt','r') as phrases:
            curr_cat_name = ''
            curr_cat_phrases = {'EASY':[],'MEDIUM':[],'HARD':[]}
            curr_diff = ''
            for line in phrases:
                if line[0:4] == 'CAT:':
                    if cat_count != 0:
                        cats.append(Category(curr_cat_name,curr_cat_phrases['EASY'],curr_cat_phrases['MEDIUM'],curr_cat_phrases['HARD']))
                        curr_cat_name = ''
                        curr_cat_phrases = {'EASY':[],'MEDIUM':[],'HARD':[]}
                    cat_count += 1
                    curr_cat_name = line[5:-1]
                elif line[0:5] == 'DIFF:':
                    curr_diff = line[6:-1]
                else:
                    curr_cat_phrases[curr_diff].append(line)
            phrases.close()
        
        cats.append(Category(curr_cat_name,curr_cat_phrases['EASY'],curr_cat_phrases['MEDIUM'],curr_cat_phrases['HARD']))
        return cats

    def filter_cats(cats): #randomly chooses 10 categories from those provided
        new_cats = []
        while len(new_cats) < 10:
            x = randint(0,len(cats)-1)
            new_cats.append(cats[x])
            cats.pop(x)
        return new_cats

    def cat_select(): #creates the category selection menu
        root.unbind_all('<Key>')
        b1.pack_forget()
        b2.pack_forget()      
        title3.pack_forget()
        title4.pack_forget()
        guess_frame.pack_forget()
        powerups.pack_forget()
        lifecounter.pack_forget()
        def start_puzzle(cat): #main puzzle function  
            sel_frame.pack_forget()
            nonlocal rnd
            if rnd in [1,2,3]:
                sel_phrase = cat.load_phrase('EASY')
            elif rnd in [4,5,6]:
                sel_phrase = cat.load_phrase('MEDIUM')
            else:
                sel_phrase = cat.load_phrase('HARD')
            b1.pack_forget()
            b2.pack_forget()
                
            def reload_phrase_options(): #refreshes the screen after each guess
                nonlocal rnd
                b4.config(command = lambda: guess_letter('save'))
                b5.config(command = lambda: guess_letter('reveal'))
                b6.config(command = lambda: guess_letter('elim'))
                b10.config(command = lambda: guess_letter('free'))
                
                if ls_used == True:
                    b4.config(command = lambda: title4.config(text = 'You already used this...'),bg = 'red')
                if lr_used == True:
                    b5.config(command = lambda: title4.config(text = 'You already used this...'),bg = 'red')
                if le_used == True:
                    b6.config(command = lambda: title4.config(text = 'You already used this...'),bg = 'red')
                if fg_used == True:
                    b10.config(command = lambda: title4.config(text = 'You already used this...'),bg = 'red')

                def guess_letter(letter):
                    nonlocal lives
                    nonlocal fg_on
                    nonlocal ls_on
                    nonlocal ls_used
                    nonlocal lr_used
                    nonlocal le_used
                    nonlocal fg_used
                    if letter == 'save':
                        ls_used = True
                        ls_on = True
                    elif letter == 'reveal':
                        lr_used = True
                        sel_phrase.reveal()
                    elif letter == 'elim':
                        le_used = True
                        sel_phrase.elim()
                    elif letter == 'free':
                        fg_used = True
                        fg_on = True
                    else:
                        x = sel_phrase.guess(letter)
                        if not x:
                            if not fg_on:
                                lives -= 1
                        elif ls_on:
                            lives += x[1]

                        if fg_on:
                            fg_on = False
                        if ls_on:
                            ls_on = False
                    
                    b2.pack_forget()
                    reload_phrase_options()

                def key_guess(event):
                    nonlocal sel_phrase
                    k = event.char
                    if k not in sel_phrase.guesses and k.upper() not in sel_phrase.guesses:
                        if k in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                            guess_letter(k)
                        elif k in 'abcdefghijklmnopqrstuvwxyz':
                            guess_letter(k.upper())
                
                for l,b in letter_buttons.items():
                    if l in sel_phrase.guesses:
                        b.config(bg = 'red', command = lambda: title4.config(text = 'You\'ve already guessed this...'))
                    else:
                        b.config(bg = 'yellow', command = lambda l=l: guess_letter(l))
                
                if lives == 0: #Game Over screen
                    guess_frame.pack_forget()
                    powerups.pack_forget()
                    title.config(text = 'Game Over. Better luck next time')
                    title2.config(text = cat.get_name())
                    title3.config(text = sel_phrase.print_model_guess())
                    title3.pack()
                    title4.config(text = 'was the correct answer.')
                    title4.pack()
                    root.unbind_all('<Key>')
                    lifecounter.config(text = 'Lives left: ' + str(lives))
                    lifecounter.pack()   
                    #b1.config(text = 'Try again?',command = sel_difficulty)
                    #b1.pack()
                    b2.pack()
                        
                elif not sel_phrase.is_solved: #window refresh code
                    title.config(text = 'Round: ' + str(rnd))
                    title2.config(text = cat.get_name())
                    title3.config(text = sel_phrase.print_curr_guess())
                    title3.pack()
                    if fg_on and ls_on:
                        title4.config(text = 'Life Saver and Free Guess active...')
                    elif fg_on:
                        title4.config(text = 'Free Guess active...')
                    elif ls_on:
                        title4.config(text = 'Life Saver active...')
                    else:
                        title4.config(text = 'Guess a letter...')
                    title4.pack()
                    guess_frame.pack()
                    root.bind_all('<Key>',key_guess)
                    if rnd != 10:
                        powerups.pack()
                    lifecounter.config(text = 'Lives left: ' + str(lives))
                    lifecounter.pack()
                    b2.pack()
                    
                else: #Round completed screen
                    powerups.pack_forget()
                    guess_frame.pack_forget()
                    title4.pack_forget()
                    title.config(text = 'Round ' + str(rnd) + ' complete!')
                    title2.config(text = cat.get_name())
                    title3.config(text = sel_phrase.print_curr_guess())
                    title3.pack()
                    root.unbind_all('<Key>')
                    if rnd == 10:
                        title4.config(text = "Congratulations! You win!")
                        title4.pack()
                        #b1.config(text = 'Play Again?',command = sel_difficulty)
                        #b1.pack(fill = X)
                        b2.pack()
                    else:    
                        rnd += 1
                        b1.config(text = 'Continue',command = cat_select)
                        b1.pack(fill = X)
                        b2.pack()
                    lifecounter.config(text = 'Lives left: ' + str(lives))
                    lifecounter.pack()
                    
            reload_phrase_options() # inital creation of puzzle window

        #Category selection                
        nonlocal rnd
        nonlocal cats
        title.config(text = 'Round: ' + str(rnd))
        title2.config(text = 'Choose a Category...')
        title2.pack()
        if rnd == 1:
            for c in cats:
                cat_buttons[c] = Button(sel_frame, text = c.get_name(), font = ("Trebuchet MS",9), width = 48, bg = 'yellow', command = lambda c=c: start_puzzle(c))
                cat_buttons[c].pack()
        else:
            for c,b in cat_buttons.items():
                if c.is_used():
                    b.pack_forget()
        sel_frame.pack()
        b2.pack()

    #initailisations
    if diff == 'EASY':
        lives = 50
    elif diff == 'MEDIUM':
        lives = 40
    else:
        lives = 30
    
    rnd = 1
    cats_main = load_phrases()
    cats = filter_cats(cats_main)
    ls_on = False
    fg_on = False
    ls_used = False
    lr_used = False
    le_used = False
    fg_used = False
    cat_select()


#Main Menu Creation
    
root = Tk()
root.title('HANGMAN')
frame = Frame(root)
frame.pack()

title = Label(frame, font = ("Trebuchet MS",9),text = 'Welcome to HANGMAN')
title.pack()

title2 = Label(frame,font = ("Trebuchet MS",9), text = 'Select an Option...')
title2.pack()

title3 = Label(frame,font = ("Trebuchet MS",9),text = '')
title4 = Label(frame,font = ("Trebuchet MS",9),text = '')
lifecounter = Label(frame,font = ("Trebuchet MS",9), text = '')

guess_frame = Frame(frame)

msg = Label(frame,font = ("Trebuchet MS",9),text='')
msg.pack()
    
b1 = Button(frame,width = 48, text= 'Start Game', font = ("Trebuchet MS",9), bg= 'green', command = sel_difficulty)
b1.pack()

b3 = Button(frame,width = 48, text = 'Help', font = ("Trebuchet MS",9),bg = 'blue', command = load_help)
b3.pack()

b2 = Button(frame, width = 48, text= 'QUIT', font = ("Trebuchet MS",9),bg = 'red', command = frame.quit)
b2.pack()

b7 = Button(frame,width = 48, text= 'EASY: 50 lives', font = ("Trebuchet MS",9),bg= 'green', command = lambda: start_game('EASY'))
b8 = Button(frame,width = 48, text= 'MEDIUM: 40 lives', font = ("Trebuchet MS",9),bg= 'yellow', command = lambda: start_game('MEDIUM'))
b9 = Button(frame,width = 48, text= 'HARD: 30 lives', font = ("Trebuchet MS",9),bg= 'red', command = lambda: start_game('HARD'))

powerups = Frame(frame)

ls = PhotoImage(file = 'life_saver.gif')
le = PhotoImage(file = 'letter_elim.gif')
lr = PhotoImage(file = 'letter_reveal.gif')
fg = PhotoImage(file = 'free_guess.gif')

b4 = Button(powerups, height = 40, width = 40, image = ls, bg = 'green')
b4.grid(row = 0,column = 0)

b5 = Button(powerups, height = 40, width = 40, image = lr, bg = 'green')
b5.grid(row = 0,column = 1)

b6 = Button(powerups, height = 40, width = 40, image = le, bg = 'green')
b6.grid(row = 0,column = 2)

b10 = Button(powerups, height = 40, width = 40, image = fg, bg = 'green')
b10.grid(row = 0,column = 3)

helpframe = Frame(frame)

h1 = Label(helpframe,image = ls)
h2 = Label(helpframe,image = lr)
h3 = Label(helpframe,image = le)
h7 = Label(helpframe,image = fg)
h4 = Label(helpframe,font = ("Trebuchet MS",9),text = 'The Life Saver: Your next guess will give you lives depending\n on how many of the letter you guessed are in the phrase!')
h5 = Label(helpframe,font = ("Trebuchet MS",9),text = 'The Letter Reveal: Reveals a random letter in the current phrase.')
h6 = Label(helpframe,font = ("Trebuchet MS",9),text = 'The Letter Eliminator: Eliminates up to 5 random letters that are not in the phrase.')
h8 = Label(helpframe,font = ("Trebuchet MS",9),text = 'The Free Guess: Your next guess won\'t cost you a life if it\'s wrong!')

h1.grid(row = 0,column = 0)
h4.grid(row = 0,column = 1)
h2.grid(row = 1,column = 0)
h5.grid(row = 1,column = 1)
h3.grid(row = 2,column = 0)
h6.grid(row = 2,column = 1)
h7.grid(row = 3,column = 0)
h8.grid(row = 3,column = 1)

sel_frame = Frame(frame)
cat_buttons = {}

guess_frame = Frame(frame)
letter_buttons = {}
count = 0
for l in 'ABCDEFGHIJKLM':
    letter_buttons[l] = Button(guess_frame,text = l,font = ("Trebuchet MS",9), bg = 'yellow', width = 3)
    letter_buttons[l].grid(row = 0, column = count)
    count += 1
count = 0
for l in 'NOPQRSTUVWXYZ':
    letter_buttons[l] = Button(guess_frame,text = l,font = ("Trebuchet MS",9), bg = 'yellow', width = 3)
    letter_buttons[l].grid(row = 1, column = count)
    count += 1

root.mainloop()
root.destroy()
