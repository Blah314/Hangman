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

class Game(object):
    def __init__(self,diff,cats):
        if diff == 'EASY':
            lives = 50
        elif diff == 'MEDIUM':
            lives = 40
        else:
            lives = 30   
        rnd = 1
        cats = cats
        ls_on = False
        fg_on = False
        ls_used = False
        lr_used = False
        le_used = False
        fg_used = False

    def cat_select(self):
        root.unbind_all('<Key>')               
        if self.rnd == 1:
            for i in range(10):
                cat_buttons[i].config(text = self.cats[i].get_name(),command = lambda i=i: self.start_puzzle(self.cats[i]))
        else:
            for i in range(10):
                if self.cats[i].is_used():
                    cat_buttons[i].config(bg = 'red',command = None)
        c1.config(text = 'Round: ' + str(self.rnd) + '\n')
        catsel.pack()

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
    
def start_game(diff,cats): #main game function
    nonlocal curr_game
    diffmenu.pack_forget()
    curr_game = Game(diff,cats)
    
    def start_puzzle(cat): #main puzzle function
        catsel.pack_forget()
        guessframe.pack()
        nonlocal rnd
        if rnd in [1,2,3]:
            sel_phrase = cat.load_phrase('EASY')
        elif rnd in [4,5,6]:
            sel_phrase = cat.load_phrase('MEDIUM')
        else:
            sel_phrase = cat.load_phrase('HARD')

        g1.config(text = 'Round: ' + str(rnd))
        g2.config(text = cat.get_name())
        lsb.config(command = lambda: guess_letter('save'))
        lrb.config(command = lambda: guess_letter('reveal'))
        leb.config(command = lambda: guess_letter('elim'))
        fgb.config(command = lambda: guess_letter('free'))

        if lives == 0: #Game Over screen
            guessframe.pack_forget()
            go3.config(text = sel_phrase.print_curr_guess())
            gameoverframe.pack()
                
        elif not sel_phrase.is_solved: #window refresh code
            g3.config(text = sel_phrase.print_curr_guess())
            if fg_on and ls_on:
                g4.config(text = 'Life Saver and Free Guess active...')
            elif fg_on:
                g4.config(text = 'Free Guess active...')
            elif ls_on:
                g4.config(text = 'Life Saver active...')
            else:
                g4.config(text = 'Guess a letter...')
            root.bind_all('<Key>',key_guess)
            if rnd == 10:
                powerups.pack_forget()
            g5.config(text = 'Lives: ' + str(lives))
            
        else: #Round completed screen
            g3.config(text = sel_phrase.print_curr_guess())
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
            
    def reload(): #refreshes the screen after each guess
        nonlocal rnd
        if ls_used == True:
            lsb.config(command = lambda: g4.config(text = 'You already used this...'),bg = 'red')
        if lr_used == True:
            lrb.config(command = lambda: g4.config(text = 'You already used this...'),bg = 'red')
        if le_used == True:
            leb.config(command = lambda: g4.config(text = 'You already used this...'),bg = 'red')
        if fg_used == True:
            fgb.config(command = lambda: g4.config(text = 'You already used this...'),bg = 'red')

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
        reload()

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
    cat_select()

#master category list

CATS = load_phrases()

def diff_select():
    mainmenu.pack_forget()
    diffmenu.pack()

def diff_back():
    diffmenu.pack_forget()
    mainmenu.pack()

def load_help():
    mainmenu.pack_forget()
    helpframe.pack()

def help_back():
    helpframe.pack_forget()
    mainmenu.pack()

def try_again():
    gameoverframe.pack_forget()
    mainmenu.pack()

#UI Stuff   
root = Tk()
root.title('HANGMAN')
frame = Frame(root)
frame.pack()

mainmenu = Frame(frame)

main1 = Label(mainmenu, font = ("Trebuchet MS",9),text = 'Welcome to HANGMAN')
main1.pack()

main2 = Label(mainmenu,font = ("Trebuchet MS",9), text = 'Select an Option...')
main2.pack()
#startbutton
mainb1 = Button(mainmenu,width = 48, text= 'Start Game', font = ("Trebuchet MS",9), bg= 'green',command = diff_select)
mainb1.pack()
#helpbutton
mainb2 = Button(mainmenu, width = 48, text= 'Help', font = ("Trebuchet MS",9),bg = 'blue',command = load_help)
mainb2.pack()
#quitbutton
mainb3 = Button(mainmenu, width = 48, text= 'QUIT', font = ("Trebuchet MS",9),bg = 'red',command = frame.quit)
mainb3.pack()

diffmenu = Frame(frame)
#difficulty buttons
d1 = Label(diffmenu,font = ("Trebuchet MS",9), text = 'Select your Difficulty...')
easyb = Button(diffmenu,width = 48, text= 'EASY: 50 lives', font = ("Trebuchet MS",9),bg= 'green',command = lambda: start_game('EASY',filter_cats(CATS)))
mediumb = Button(diffmenu,width = 48, text= 'MEDIUM: 40 lives', font = ("Trebuchet MS",9),bg= 'yellow',command = lambda: start_game('MEDIUM',filter_cats(CATS)))
hardb = Button(diffmenu,width = 48, text= 'HARD: 30 lives', font = ("Trebuchet MS",9),bg= 'red',command = lambda: start_game('HARD',filter_cats(CATS)))
d2 = Label(diffmenu,text = '')
dbackb = Button(diffmenu,width = 48, text= 'BACK', font = ("Trebuchet MS",9),bg= 'blue',command = diff_back)
dquitb = Button(diffmenu,width = 48, text= 'QUIT', font = ("Trebuchet MS",9),bg= 'red',command = frame.quit)

d1.pack()
easyb.pack()
mediumb.pack()
hardb.pack()
d2.pack()
dbackb.pack()
dquitb.pack()

#powerup images
ls = PhotoImage(file = 'life_saver.gif')
le = PhotoImage(file = 'letter_elim.gif')
lr = PhotoImage(file = 'letter_reveal.gif')
fg = PhotoImage(file = 'free_guess.gif')
helpframe = Frame(frame)
helpinner = Frame(helpframe)

#help content
h1 = Label(helpframe,font = ("Trebuchet MS",9),text = 'HELP')
h2 = Label(helpframe,font = ("Trebuchet MS",9),text = '10 Hangman Puzzles ... 10 categories.\nThe puzzles get more difficult as you advance.\n\nClick the letters to guess them...\n They will appear if they are in the phrase, if not you lose a life!\nYou have limited lives, so make every guess count!')
h3 = Label(helpframe,font = ("Trebuchet MS",9),text = 'You have 4 power-ups at your disposal...')
h4 = Label(helpinner,image = ls)
h5 = Label(helpinner,image = lr)
h6 = Label(helpinner,image = le)
h7 = Label(helpinner,image = fg)
h8 = Label(helpinner,font = ("Trebuchet MS",9),text = 'The Life Saver: Your next guess will give you lives depending\n on how many of the letter you guessed are in the phrase!')
h9 = Label(helpinner,font = ("Trebuchet MS",9),text = 'The Letter Reveal: Reveals a random letter in the current phrase.')
h10 = Label(helpinner,font = ("Trebuchet MS",9),text = 'The Letter Eliminator: Eliminates up to 5 random letters that are not in the phrase.')
h11 = Label(helpinner,font = ("Trebuchet MS",9),text = 'The Free Guess: Your next guess won\'t cost you a life if it\'s wrong!')
h12 = Label(helpframe,font = ("Trebuchet MS",9),text='You can\'t use any powerups in the last round.\n\nGood Luck!')
hbackb = Button(helpframe,width = 48, text= 'BACK', font = ("Trebuchet MS",9),bg= 'blue',command = help_back)
hquitb = Button(helpframe,width = 48, text= 'QUIT', font = ("Trebuchet MS",9),bg= 'red',command = frame.quit)

h4.grid(row = 0,column = 0)
h8.grid(row = 0,column = 1)
h5.grid(row = 1,column = 0)
h9.grid(row = 1,column = 1)
h6.grid(row = 2,column = 0)
h10.grid(row = 2,column = 1)
h7.grid(row = 3,column = 0)
h11.grid(row = 3,column = 1)

h1.pack()
h2.pack()
h3.pack()
helpinner.pack()
h12.pack()
hbackb.pack()
hquitb.pack()

catsel = Frame(frame)
#category selection menu
c1 = Label(catsel,font = ("Trebuchet MS",9),text = 'Round: ')
c2 = Label(catsel,font = ("Trebuchet MS",9),text = 'Choose a category...\n')
c1.pack()
c2.pack()
cat_buttons = []
for i in range(10):
    cat_buttons.append(Button(catsel,width = 48, text= '', font = ("Trebuchet MS",9),bg= 'yellow'))
    cat_buttons[i].pack()
cquitb = Button(catsel,width = 48, text= 'QUIT', font = ("Trebuchet MS",9),bg= 'red',command = frame.quit)
cquitb.pack()

guessframe = Frame(frame)
#main game interface
g1 = Label(guessframe,font = ("Trebuchet MS",9),text = 'Round: ')
g2 = Label(guessframe,font = ("Trebuchet MS",9),text = 'Category')
g3 = Label(guessframe,font = ("Trebuchet MS",9),text = 'Phrase')
g4 = Label(guessframe,font = ("Trebuchet MS",9),text = 'Status')

letterframe = Frame(guessframe)
letter_buttons = {}
count = 0
for l in 'ABCDEFGHIJKLM':
    letter_buttons[l] = Button(letterframe,text = l,font = ("Trebuchet MS",9), bg = 'yellow', width = 3)
    letter_buttons[l].grid(row = 0, column = count)
    count += 1
count = 0
for l in 'NOPQRSTUVWXYZ':
    letter_buttons[l] = Button(letterframe,text = l,font = ("Trebuchet MS",9), bg = 'yellow', width = 3)
    letter_buttons[l].grid(row = 1, column = count)
    count += 1

powerups = Frame(guessframe)
#powerup buttons
lsb = Button(powerups, height = 40, width = 40, image = ls, bg = 'green')
lsb.grid(row = 0,column = 0)

lrb = Button(powerups, height = 40, width = 40, image = lr, bg = 'green')
lrb.grid(row = 0,column = 1)

leb = Button(powerups, height = 40, width = 40, image = le, bg = 'green')
leb.grid(row = 0,column = 2)

fgb = Button(powerups, height = 40, width = 40, image = fg, bg = 'green')
fgb.grid(row = 0,column = 3)

g5 = Label(guessframe,font = ("Trebuchet MS",9),text = 'Lifecounter')
gquitb = Button(guessframe,width = 48, text= 'QUIT', font = ("Trebuchet MS",9),bg= 'red',command = frame.quit)

g1.pack()
g2.pack()
g3.pack()
g4.pack()
letterframe.pack()
powerups.pack()
g5.pack()
gquitb.pack()

#game over screen
gameoverframe = Frame(frame)
go1 = Label(gameoverframe,font = ("Trebuchet MS",9),text = 'GAME OVER')
go2 = Label(gameoverframe,font = ("Trebuchet MS",9),text = 'Category')
go3 = Label(gameoverframe,font = ("Trebuchet MS",9),text = 'Phrase')
go4 = Label(gameoverframe,font = ("Trebuchet MS",9),text = 'was the right answer')
go5 = Label(gameoverframe,font = ("Trebuchet MS",9),text = 'Lives: x.x')
gobackb = Button(gameoverframe,width = 48, font = ("Trebuchet MS",9),text = 'Try Again?',bg = 'blue',command = try_again)
goquitb = Button(gameoverframe,width = 48, text= 'QUIT', font = ("Trebuchet MS",9),bg= 'red',command = frame.quit)
go1.pack()
go2.pack()
go3.pack()
go4.pack()
go5.pack()
gobackb.pack()
goquitb.pack()

#round passed screen
roundframe = Frame(frame)
r1 = Label(roundframe,font = ("Trebuchet MS",9),text = 'Round complete')
r2 = Label(roundframe,font = ("Trebuchet MS",9),text = 'Category')
r3 = Label(roundframe,font = ("Trebuchet MS",9),text = 'Correct Phrase')
r4 = Label(roundframe,font = ("Trebuchet MS",9),text = 'Win?')
r5 = Label(roundframe,font = ("Trebuchet MS",9),text = 'Lives left')
rbackb = Button(gameoverframe,width = 48, font = ("Trebuchet MS",9),text = 'Continue',bg = 'green',command = 
rquitb = Button(gameoverframe,width = 48, text= 'QUIT', font = ("Trebuchet MS",9),bg= 'red',command = frame.quit)

#initiation
mainmenu.pack()
curr_game = None

root.mainloop()
root.destroy()