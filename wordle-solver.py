# strategy:
# start with a word containing as many of the most common letters as possible (using a library indexing letters by a value of common-ness)
# pick each next word based on option with highest common-ness sum of letters, which also fulfills existing restraints

from english_words import english_words_lower_alpha_set as allWords
from string import ascii_lowercase as alpha
import ast

# get only 5-letter words
vocab = []
for word in allWords:
    if '.' in word:  # because for some reason this library includes 'U.S.A'
        pass
    elif len(word) == 5:
        vocab.append(word)
# set up letter frequency dict
alphaData = {}
for letter in alpha:
    alphaData[letter] = [0, 0, 0, 0, 0]  # one value for each position in a word
# fill dictionary with data
for word in vocab:
    i=0
    for letter in word:
        alphaData[letter][i] +=1
        i+=1

def guess(green, yellow, excludes):  # known are lists of (letter, position)
    # narrow down options
    disqualifiedWords = []  # to avoid modifying loop while for-looping over it
    for word in vocab:
        for letterList in green:
            if letterList[0]:  # in case no data is entered (first guess)
                print(green, yellow, excludes)
                letter = letterList[0]
                pos = letterList[1]
                if word[pos] != letter:
                    disqualifiedWords.append(word)
        for letterList in yellow:
            if letterList[0]:
                letter = letterList[0]
                posList = letterList[1:]
                if letter not in word:
                    disqualifiedWords.append(word)
                else:
                    for pos in posList:
                        if word[pos] == letter:
                            disqualifiedWords.append(word)
        for letter in excludes[0]:  # get rid of layered list ("if letter and...") gets rid of no-data case
            if letter and letter in word:
                disqualifiedWords.append(word)
    disqualifiedWords = list(set(disqualifiedWords))  # removes duplicates
    for word in disqualifiedWords:
        vocab.remove(word)
    # rank words by common-ness of letters
    scores = {}
    for word in vocab:
        thisScore = 0
        i=0
        for letter in word:
            thisScore += alphaData[letter][i]
            i+=1
        scores[word] = thisScore
    return max(scores, key=scores.get), len(vocab)

# just a helper function for formatting inputs
def ask(prompt):
    text = input(prompt)
    firstSplit = text.split('. ')
    outList = []
    for piece in firstSplit:
        nextSplit = piece.split(', ')
        normalList = []
        for char in nextSplit:
            try:
                normalList.append(int(char))
            except ValueError:
                normalList.append(char)
        outList.append(normalList)
    return outList

# program body
print('Instructions: Enter letters and cooresponding positions separated by ",", and further letters separated by ".". Do not end lines with ".".\n')

while True:
    green = ask('Green letters -> ')
    yellow = ask('Yellow letters, attempted positions -> ')
    excludes = ask('Excluded letters -> ')
    guesses, optionCount = guess(green, yellow, excludes)
    print(optionCount, 'matching words found.', end=' ')

    if optionCount:
        print('Suggested words:', guesses)
    else:
        print('Sorry, no guesses. :(')
        break
