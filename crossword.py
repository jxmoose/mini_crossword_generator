from pathlib import Path
import json

class crossword():
    word_lists = [[] for i in range(130)]
    scores = {}
    word_tries = 10

    def parse_data(self, file):
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

        with open("lists.txt", "w") as txt_file:
            for line in self.word_lists:
                txt_file.write(" ".join(line) + "\n") # works with any number of elements in a line

    def __init__(self, word):
        self.across = []
        self.down = []
        if len(word) != 5:
            return
        for c in word:
            if not c.isalpha():
                return
        self.across.append(word.upper())

        filepath = Path(__file__).parent / "wordlist.txt"

        with open(filepath) as f:
            lines = f.readlines()
            for line in lines:
                word, score = line.strip().split(';')
                if len(word) != 5:
                    continue
                self.scores[word] = int(score)
                for i in range(5):
                    self.get_list(word[i], i).append(word)
        self.add_down([])

    def add_across(self, banned):
        print("START ADD ACROSS")
        pos = len(self.across)
        inter = []
        for i, word in enumerate(self.down):
            inter.append(self.get_list(word[pos], i))
        fit_words = list(self.intersection(inter))
        if not fit_words:
            print("no fit words across")
            self.backtrack_across(banned)
        else:
            scores = []
            words = []
            for i in range(min(len(fit_words), self.word_tries)):
                score = 1
                word = fit_words[i]
                if word in banned:
                    print("across ban")
                    continue
                self.across.append(word)
                for j in range(len(self.down), 4):
                    inter = []
                    for k in range(len(self.across)):
                        inter.append(self.get_list(self.across[k][j], k))
                        score *= len(self.intersection(inter))
                scores.append(score)
                words.append(word)
                self.across.remove(word)
            print("SCORES:")
            print(scores)
            print(words)
            top_word = words[scores.index(max(scores))]
            if not any(scores):
                self.backtrack_across(banned)
            else:
                self.across.append(top_word)
            #    if (len(self.across) != 5):
            #        self.add_down([])

    def backtrack_across(self, banned):
        print("backtrack_across")
        del self.down[-1]
        ban_word = self.across.pop()
        self.add_across(banned + [ban_word])
        print("DONE BACKTRACKING")
        self.add_down([])
        self.add_across([])

    def backtrack_down(self, banned):
        print("backtrack_down")
        del self.across[-1]
        ban_word = self.down.pop()
        self.add_down(banned + [ban_word])
        print("DONE BACKTRACKING")

    def add_down(self, banned):
        print("START ADD DOWN")
        pos = len(self.down)
        inter = []
        for i, word in enumerate(self.across):
            inter.append(self.get_list(word[pos], i))
        fit_words = list(self.intersection(inter))
        if not fit_words:
            print("no fit words down")
            self.backtrack_down()
        else:
            scores = []
            words = []
            for i in range(min(self.word_tries, len(fit_words))):
                score = 1
                word = fit_words[i]
                if word in banned:
                    continue
                self.down.append(word)
                for j in range(len(self.across), 4):
                    inter = []
                    for k in range(len(self.down)):
                        inter.append(self.get_list(self.down[k][j], k))
                        score *= len(self.intersection(inter))
                scores.append(score)
                words.append(word)
                self.down.remove(word)
            top_word = words[scores.index(max(scores))]
            if not any(scores):
                self.backtrack_down(banned)
            else: 
                self.down.append(top_word)
            #    if (len(self.down) != 5):
            #        self.add_across([])

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

c = crossword('hello')
c.add_across([])
c.add_down([])
c.add_across([])
c.add_down([])
c.add_across([])
c.add_down([])
c.add_across(["ALKFJDLSKJFLSDKFJLSDKFJLSDKFJSDLFKJSDLFKSDJFLKSDJFLKDSJFKLSDFJ"])
print("DONE")
print("ACROSS", c.across)
print("DOWN", c.down)