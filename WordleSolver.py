from string import ascii_lowercase as alpha

class Solver:
    def __init__(self):
        self.vocab = open('wordle-possible-answers.txt', 'r').read().split('\n')
        self.guesses = []

    # just pulls everything together to return the best guess based on previous guesses' feedback
    def guess(self, view, keys):
        self.narrow_vocab(view, keys)
        if not self.vocab:
            raise ValueError('No possible answers found')
        return self.best_word()

    # removes disqualified words from global vocab list
    def narrow_vocab(self, view, keys):
        pass # rewrite

    # find the best qualifying word as ranked by frequency of letters in other possible words
    def best_word(self):
        scores = {}
        letterCounts = {letter: [0, 0, 0, 0, 0] for letter in alpha}
        for word in self.vocab:
            for i in range(5):
                letter = word[i]
                letterCounts[letter][i] +=1
        for word in self.vocab:
            thisScore = 0
            for i in range(5):
                letter = word[i]
                thisScore += letterCounts[letter][i]
            scores[word] = thisScore
        return max(scores, key=scores.get)
