from string import ascii_lowercase as alpha

class Solver:
    def __init__(self):
        self.vocab = open('wordle-possible-answers.txt', 'r').read().split('\n')
        self.guesses = []

    # just pulls everything together to return the best guess based on previous guesses' feedback
    def guess(self, view):
        self.narrow_vocab(view)
        if not self.vocab:
            return None
        bestGuess = self.best_word()
        self.guesses.append(bestGuess)
        return bestGuess

    # removes disqualified words from global vocab list
    def narrow_vocab(self, view):
        green = {letter: [] for letter in alpha}
        yellow = {letter: [] for letter in alpha}
        black = []
        for v, w in zip(view[:len(self.guesses)], self.guesses):  # note that view is trimmed to only what's been filled
            for i in range(5):  # iterating over each char in each guess
                if v[i] == -1 and w[i] not in black:  # black
                    black.append(w[i])
                elif v[i] == 1 and i not in yellow[w[i]]:  # yellow
                    yellow[w[i]].append(i)
                elif v[i] == 2 and i not in green[w[i]]:  # green
                    green[w[i]].append(i)

        # helper function to check if a word should be disqualified--returns True if it *shouldn't* be disqualified
        def word_qualifies(word):
            trimmedGreen = [k for k in green if green[k]]  # remove empty letters
            trimmedYellow = [k for k in yellow if yellow[k]]
            for letter in trimmedGreen:  # green
                for pos in green[letter]:
                    if letter != word[pos]:
                        return False
            for letter in trimmedYellow:  # yellow
                for pos in yellow[letter]:
                    if letter == word[pos] or letter not in word:
                        return False
            for letter in black:  # black
                if letter in word and letter not in trimmedGreen:
                    return False
                elif letter in trimmedGreen:
                    for pos in green[letter]:
                        if letter in [word[i] for i in range(5) if i != pos]:
                            # provides list of letters that aren't that specific green letter
                            return False
            return True

        # rewrite vocab list nice & tidy
        self.vocab = [word for word in self.vocab if word_qualifies(word)]

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
