from pathlib import Path

class crossword():
    word_lists = [[] for i in range(130)]
    scores = {}
    word_tries = 10

    def __init__(self, file, word):
        self.across = []
        self.down = []
        if len(word) != 5:
            return
        for c in word:
            if not c.isalpha():
                return
        self.across.append(word.upper())

        filepath = Path(__file__).parent / file

        with open(filepath) as f:
            lines = f.readlines()
            for line in lines:
                word, score = line.strip().split(';')
                if len(word) != 5:
                    continue
                self.scores[word] = int(score)
                for i in range(5):
                    self.get_list(word[i], i).append(word)
            
        #while len(self.across) and len(self.down) != 5:
        #    self.add_next()

    def add_down(self):
        self.down.append("HALAH")
        self.down.append("EMILY")
        self.down.append("LENIS")
        self.down.append("LEUTE")
        pos = len(self.down)
        inter = []
        for i, word in enumerate(self.across):
            inter.append(self.get_list(word[pos], i))
        fit_words = list(self.intersection(inter))
        scores = []
        for i in range(self.word_tries):
            score = 1
            word = fit_words[i]
            self.down.append(word)
            for j in range(len(self.across), 4):
                inter = []
                for k in range(len(self.down)):
                    inter.append(self.get_list(self.down[k][j], k))
                    score *= len(self.intersection(inter))
            scores.append(score)
            self.down.remove(word)
        self.down.append(fit_words[scores.index(max(scores))])
        print(self.down)
        print(scores)

    def get_list(self, letter, position):
        letter = letter.upper()
        return self.word_lists[ord(letter) - 65 + 26 * position]
    
    def score(self):
        total = 0
        for word in self.down:
            total += self.scores[word]
        for word in self.across:
            total += self.scores[word]
        return total

    def intersection(self, inputs):
        return set.intersection(*map(set, inputs))
        
c = crossword("wordlist.txt", 'hello')
c.add_down()