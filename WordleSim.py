import random
from string import ascii_lowercase as alpha
from WordleSolver import Solver

ANSWERS = open('wordle-possible-answers.txt', 'r').read().split('\n')

class Wordle:
    # green (known) is 2, yellow (included) is 1, grey (not guessed) is 0, and black (excluded) is -1
    def __init__(self):
        self.answer = random.choice(ANSWERS)
        self.view = [[0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0]]
        self.keys = {letter: 0 for letter in alpha}

    def play(self):
        wordlePlayer = Solver()
        for i in range(6):  # 6 tries
            myGuess = wordlePlayer.guess(self.view, self.keys)
            self.turn(myGuess, i)
            if all(n==2 for n in self.view[i]):  # win condition (all green)
                return i

    def turn(self, guess, l):
        for i in range(5):
            if guess[i] == self.answer[i]:  # green
                self.view[l][i] = 2
                self.keys[guess[i]] = 2
            elif guess[i] not in self.answer:  # black
                self.view[l][i] = -1
                self.keys[guess[i]] = -1
            else:  # yellow (conditionally)

                if self.keys[guess[i]] == 2:  # already green in different pos
                    places = [j for j in range(5) if guess[i] == answer[j]]  # all indices j of given letter guess[i] found in answer
                    for j in places:
                        if 2 not in [line[j] for line in self.view]:  # check for non-green occurance of this letter at answer[j]
                            self.view[l][j] = 1
                            break
                    else:  # didn't break so all occurances are already green, no more unguessed duplicates
                        self.view[l][j] = -1

                elif 0:
                    pass  # more cases?

def main():
    loops = int(input('Number of rounds? -> '))
    total = 0
    fails = 0
    for i in range(loops):
        game = Wordle()
        result = game.play()
        if result:
            total += result
        else:
            fails += 1
    avg = round(total/loops, 4)
    print('In', loops, 'rounds, averaged', avg, 'guesses with', fails, 'failures.')

main()
