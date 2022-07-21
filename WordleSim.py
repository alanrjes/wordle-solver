import random
from string import ascii_lowercase as alpha
from WordleSolver import Solver

ANSWERS = open('wordle-possible-answers.txt', 'r').read().split('\n')
LOG = open('log.txt', 'w')

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
                    places = [j for j in range(5) if guess[i] == self.answer[j]]  # all indices j of given letter guess[i] found in answer
                    for j in places:
                        if 2 not in [line[j] for line in self.view]:  # check for non-green occurance of this letter at answer[j]
                            self.view[l][i] = 1
                            break
                    else:  # didn't break so all occurances are already green, no more unguessed duplicates
                        self.view[l][i] = -1

                else:  # standard yellow case
                    self.view[l][i] = 1
                    self.keys[guess[i]] = 1

        if all(n==2 for n in self.view[l]):  # win condition (all green)
            return l+1  # number of guesses to win, just returns None if looses

def main():
    loops = int(input('Number of rounds? -> '))
    total = 0
    fails = 0
    for i in range(loops):
        game = Wordle()
        LOG.write('Answer -> ' + game.answer + '\n\n')
        player = Solver()
        for i in range(6):  # 6 tries
            playerGuess = player.guess(game.view)
            LOG.write(playerGuess)
            result = game.turn(playerGuess, i)
            LOG.write(' ->\n' + '\n'.join(', '.join([str(i) for i in l]) for l in game.view) + '\n\n')
            if result:
                total += result
                break
        else:
            fails += 1
    avg = round(total/loops, 4)
    print('In', loops, 'rounds, averaged', avg, 'guesses with', fails, 'failures.')
