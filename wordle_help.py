from WordleSolver import Solver

def translate_view(vStr):
    vStrs = vStr.split()
    vInts = [0, 0, 0, 0, 0]
    for i in range(5):
        if vStrs[i] == 'G':
            vInts[i] = 2
        elif vStrs[i] == 'Y':
            vInts[i] = 1
        elif vStrs[i] == 'X':
            vInts[i] = -1
        else:
            raise ValueError('Invalid character in results.')
    return vInts

def main():
    view = [[0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]]
    print('Instructions: enter results as _ _ _ _ _, with G for green, Y for yellow, or X for black squares.')
    player = Solver()
    for i in range(6):
        helperGuess = player.guess(view)
        print('Guess', helperGuess+'.')
        view[i] = translate_view(input('Results? -> '))
        if all(n==2 for n in view[i]):
            print('Congrats, we won!')
            break

main()
