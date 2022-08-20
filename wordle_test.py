from WordleSolver import Solver
from WordleSim import Wordle

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

main()
