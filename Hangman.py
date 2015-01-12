from random import *

def load_phrases():
    phrase_cats = {}
    phrase_dict = {}
    cat_count = 0
    curr_diff = ''
    with open('hangman_phrases.txt','r') as phrases:
        for line in phrases:            
            if line[0:4] == 'CAT:':
                cat_count += 1
                phrase_cats[cat_count] = line[5:-1]
                phrase_dict[cat_count] = {'EASY':[],'MEDIUM':[],'HARD':[]}
            elif line[0:5] == 'DIFF:':
                curr_diff = line[6:-1]
            else:
                phrase_dict[cat_count][curr_diff].append(line[:-1])
    return [phrase_cats,phrase_dict]           
    
def start_guess(phrase):
    exceptions = ',:\'1234567890 &@#$!<>.()*^%'
    dashes = []
    for letter in phrase:
        if letter in exceptions:
            dashes.append(letter)
        else:
            dashes.append('_')
    return dashes

def model_guess(phrase):
    model = []
    for letter in phrase:
        model.append(letter)
    return model

def print_guess(guess):
    display = ''
    for letter in guess:
        display += letter + ' '
    print(display)

def game_end(guess,model,lives):
    if lives == 0:
        return True
    elif guess == model:
        return True
    else:
        return False

def guess_letter(letter,guess,model):
    if letter not in model:
        return (guess,False,0)
    else:
        count = 0
        for i in range(len(model)):
            if model[i] == letter:
                guess[i] = letter
                count += 1
        return (guess,True,count)

def dup_checker(letter,wrongs,corrects):
    if letter in wrongs or letter in corrects:
        print('You already guessed this...')
        return False
    else:
        return True

def get_guess(result):
    return result[0]

def get_right_wrong(result):
    return result[1]

def get_count(result):
    return result[2]

def select_cats(categories):
    if len(categories) <= 10:
        return categories
    else:
        reduced_cats = {}
        while len(reduced_cats) < 10:
            x = randint(1,len(categories))
            if x not in reduced_cats:
                reduced_cats[x] = categories[x]
            else:
                continue
        return reduced_cats

def display_cats(categories,cat_list):
    for key in categories:
        if categories[key] in cat_list:
            print(key,': ' + categories[key])
    
def new_game(categories,phrases):
    lives = 50
    rnd = 1
    cats = select_cats(categories)
    cat_list = list(cats.values())
    while cat_list:
        while True:
            print('Round ' + str(rnd) + ':')
            print('Categories to choose from...')
            display_cats(cats,cat_list)
            c = input('Choose your next category...')
            try:
                c = int(c)
            except ValueError:
                print('Invalid Category')
                continue
            
            if c not in cats:
                print('Invalid Category')
                continue
            else:
                break
            
        category = cats[c]
        cat_list.remove(category)
        del cats[c]
        
        phrase_list = phrases[c]      
        if rnd in [1,2,3]:
            x = len(phrase_list['EASY'])
            phrase = phrase_list['EASY'][randint(1,x)-1]
        elif rnd in [4,5,6,7]:
            x = len(phrase_list['MEDIUM'])
            phrase = phrase_list['MEDIUM'][randint(1,x)-1]
        else:
            x = len(phrase_list['HARD'])
            phrase = phrase_list['HARD'][randint(1,x)-1]
        guess = start_guess(phrase)
        model = model_guess(phrase)
        letters = model_guess('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        wrongs = []
        corrects = []
        while game_end(guess,model,lives) == False:
            print(category)
            print_guess(guess)
            print_guess(letters)
            print('Wrong Guesses:')
            print_guess(wrongs)
            print('Lives:' + str(lives))
            letter_g = input('Guess a letter...')
            letter_g = letter_g.upper()
            if len(letter_g) != 1:
                print('Only 1 letter at a time...')
                continue
            
            if letter_g in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if dup_checker(letter_g,wrongs,corrects):
                    result = guess_letter(letter_g,guess,model)
                    guess = get_guess(result)
                    letters.remove(letter_g)
                    if get_right_wrong(result):
                        if get_count(result) == 1:
                            print(str(get_count(result)) + ' ' + letter_g + ' found.')
                        else:
                            print(str(get_count(result)) + ' ' + letter_g + 's found.')
                        corrects.append(letter_g)
                    else:
                        print('Oops... No ' + letter_g + 's.')
                        wrongs.append(letter_g)
                        lives -= 1
                else:
                    continue
            else:
                print('Guess letters only.')
                continue
    
        if lives == 0:
            print('Game Over. Better luck next time.\nAnswer: ')
            print_guess(model)
            break
        elif rnd == len(cats):
            print_guess(guess)
            print('Round ' + str(rnd) + ' complete. Congradulations! You win!.')
        else:
            print_guess(guess)
            print('Round ' + str(rnd) + ' complete.')
            rnd += 1
    

categories = load_phrases()[0]
phrases = load_phrases()[1]
new_game(categories,phrases)
                    
