from string import ascii_lowercase as alpha
from WordleSolver import Solver
from WordleSim import Wordle

class WordleQuizzer(Wordle):
    def __init__(self, answer):
        self.answer = answer
        self.view = [[0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0]]
        self.keys = {letter: 0 for letter in alpha}

def main():
    answer = input('Answer to play for? -> ')
    game = WordleQuizzer(answer)
    player = Solver()
    for i in range(6):
        playerGuess = player.guess(game.view)
        result = game.turn(playerGuess, i)
        if result:
            print('Guessed', answer, 'in', result, 'rounds.')
            break
    else:
        print('Failed to guess', answer, '!')

main()
