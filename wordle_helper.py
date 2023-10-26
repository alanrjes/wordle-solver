VOCAB = open('wordle-possible-answers.txt', 'r').read().split('\n')

def answer_search(letter, position):
    i = 0
    while i < len(VOCAB):
        if VOCAB[i][position] != letter:
            del VOCAB[i]
        else:
            i += 1

k = input("Enter known letters, in order of position, with other spaced indicated by underspaces: ")
x = input("Enter excluded letters, not separated: ")

i = 0
while i < len(VOCAB):
    for j in range(len(x)):
        c = x[j]
        if c in VOCAB[i]:
            del VOCAB[i]
            break
        else:
            if j == len(x)-1:
                i += 1

for i in range(5):
    c = k[i]
    if (c != "_"):
        answer_search(c, i)

print("Possible answers:", VOCAB)
