# strategy:
# start with a word containing as many of the most common letters as possible (using a library indexing letters by a value of common-ness)
# pick each next word based on option with highest common-ness sum of letters, which also fulfills existing restraints

from english_words import english_words_lower_alpha_set as allWords
from string import ascii_lowercase as alpha
import ast
from copy import deepcopy

# set up alphabet character dictionary for later general use
ALPHAD = {letter: [] for letter in alpha}

# get only 5-letter words
vocab = []
for word in allWords:
    if '.' in word:  # because for some reason this library includes 'U.S.A'
        pass
    elif len(word) == 5:
        vocab.append(word)

# set up letter frequency dict & fill dictionary with data
alphaFreqs = {letter: [0, 0, 0, 0, 0] for letter in alpha}
for word in vocab:
    for i in range(5):
        letter = word[i]
        alphaFreqs[letter][i] +=1

# rank words by common-ness of letters
scores = {}
for word in vocab:
    thisScore = 0
    for i in range(5):
        letter = word[i]
        thisScore += alphaFreqs[letter][i]
    scores[word] = thisScore

# core function to pick optimal word
def guess(green, yellow, excludes):
    # green are dictionaries of {letter: [position, ...]}. Excluded is list of just [letter, ...]
    disqualifiedWords = []  # to avoid modifying loop while for-looping over it
    for word in vocab:
        for letter in green:
            for pos in green[letter]:
                if word[pos] != letter:
                    disqualifiedWords.append(word)
        for letter in yellow:
            if letter not in word and yellow[letter]:  # checks key (letter) in word, but also checks value of letter in dict to ignore initialized values (empty lists)
                disqualifiedWords.append(word)
            else:
                for pos in yellow[letter]:
                    if word[pos] == letter:
                        disqualifiedWords.append(word)
        for letter in excludes:
            if letter in word:
                disqualifiedWords.append(word)
    # reconfigure list
    disqualifiedWords = list(set(disqualifiedWords))  # removes duplicates
    for word in disqualifiedWords:
        vocab.remove(word)
        del scores[word]
    # return both the best guess (highest scoring qualifying word), and the number of possible guesses
    return max(scores, key=scores.get), len(vocab)

def parseResults(results, prevGuess):
    green, yellow = deepcopy(ALPHAD), deepcopy(ALPHAD)
    excludes = []
    resList = results.split(' ')
    for pos in range(5):
        res = resList[pos]
        char = prevGuess[pos]
        if res == 'G':
            green[char].append(pos)
        elif res == 'Y':
            yellow[char].append(pos)
        else:
            excludes.append(char)
    return green, yellow, excludes

# program body
print('Instructions: Enter the results from each guess in the format of _ _ _ _ _, with Y (yellow) or G (green).')
prevGuess = guess([], [], [])[0]
print('Starting word:', prevGuess)  # first guess should be "SAUTE"

for i in range(1, 5):  # start loop at second try (1)
    guessResults = input('Results? -> ')
    green, yellow, excludes = parseResults(guessResults, prevGuess)
    currentGuess, optionCount = guess(green, yellow, excludes)
    print(optionCount, 'matching word' + 's'*(optionCount!=1), 'found.', end=' ')
    if optionCount==1:
        print('Only guess:', currentGuess)
        break
    elif optionCount==0:
        print('Sorry, no guesses. :(')
        break
    elif i==4:
        print('Final try:', currentGuess)
        # loop naturally concludes
    else:
        print('Best guess:', currentGuess)
    prevGuess = currentGuess
