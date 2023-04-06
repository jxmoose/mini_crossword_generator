from pathlib import Path
import json
import sys
import os
import openai
openai.api_key = "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"

class recursionlimit:
    def __init__(self, limit):
        self.limit = limit

    def __enter__(self):
        self.old_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(self.limit)

    def __exit__(self, type, value, tb):
        sys.setrecursionlimit(self.old_limit)

class crossword_gen():
    word_lists = [[] for i in range(130)]
    scores = {}
    word_tries = 10

    #just reads data and puts it in .txt file
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

    #haven't changed to read data from lists.txt yet because I accidentally just added all the lines as one line and I need to parse the string instead.
    def __init__(self, word):
        self.banned_down = set()
        self.banned_across = set()
        self.across = []
        self.down = []
        self.down_clues = []
        self.across_clues = []
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
        self.add_down()

    #deletes down and across and then adds a new across, down, across
    #i added a instance variable "banned" rather than putting it as inputs into add_across/down and it seems to work better. haven't edited out parameter banned yet but nothing should be using it
    def backtrack_across(self):
        print("backtrack_across")
        ban_word = self.down.pop()
        self.banned_down.add(ban_word)
        print("ACROSS", self.across)
        print("DOWN", self.down)
        print("ban length: ", len(self.banned_down))
        self.add_down()
        self.add_across()
        print("DONE BACKTRACKING")

    def backtrack_down(self):
        print("backtrack_down")
        ban_word = self.across.pop()
        self.banned_across.add(ban_word)
        print("ACROSS", self.across)
        print("DOWN", self.down)
        print("ban length: ", len(self.banned_across))
        self.add_across()
        self.add_down()
        print("DONE BACKTRACKING")

    #add_across and add_down are basically the same code but switching across and down in variables
    def add_across(self):
        print("START ADD ACROSS")
        pos = len(self.across)
        inter = []
        #basically check what word can fit into next across
        for i, word in enumerate(self.down):
            inter.append(self.get_list(word[pos], i))
        fit_words = list(self.intersection(inter))
        print("length", len(fit_words))
        #if no words fit then you want to backtrack
        if not fit_words:
            print("no fit words across")
            self.backtrack_across()
        else:
            scores = []
            words = []
            #basically want 10 words if possible unless theres less in fit_words
            while i < len(fit_words) and i < self.word_tries:
                score = 1
                word = fit_words.pop(0)
                if word in self.banned_across:
                    continue
                self.across.append(word)
                #basically checking for all the intersections and multiplying a score
                for j in range(len(self.down), 5):
                    inter = []
                    for k in range(len(self.across)):
                        inter.append(self.get_list(self.across[k][j], k))
                        score *= len(self.intersection(inter))
                if score == 0:
                    self.across.remove(word)
                    continue
                scores.append(score)
                words.append(word)
                self.across.remove(word)
                i += 1
            print("SCORES:")
            print(scores)
            print(words)
            #all scores = 0 means no words fit
            if not any(scores):
                self.backtrack_across()
            #if there's at least one word that fits just add word and continue
            else:
                top_word = words[scores.index(max(scores))]
                self.across.append(top_word)

    def add_down(self):
        print("START ADD DOWN")
        pos = len(self.down)
        inter = []
        for i, word in enumerate(self.across):
            inter.append(self.get_list(word[pos], i))
        fit_words = list(self.intersection(inter))
        print("length", len(fit_words))
        if not fit_words:
            print("no fit words down")
            self.backtrack_down()
        else:
            scores = []
            words = []
            while i < len(fit_words) and i < self.word_tries:
                score = 1
                word = fit_words.pop(0)
                if word in self.banned_down:
                    continue
                self.down.append(word)
                for j in range(len(self.across), 5):
                    inter = []
                    for k in range(len(self.down)):
                        inter.append(self.get_list(self.down[k][j], k))
                        score *= len(self.intersection(inter))
                if score == 0:
                    self.down.remove(word)
                    continue
                scores.append(score)
                words.append(word)
                self.down.remove(word)
                i += 1
            print("SCORES:", scores, words)
            if not any(scores):
                self.backtrack_down()
            else:
                top_word = words[scores.index(max(scores))]
                self.down.append(top_word)
            #    if (len(self.down) != 5):
            #        self.add_across([])

    #simple function that takes in letter and position to return the associated word list
    def get_list(self, letter, position):
        letter = letter.upper()
        return self.word_lists[ord(letter) - 65 + 26 * position]
    
    #haven't used yet bc not done with crossword
    def score(self):
        total = 0
        for word in self.down:
            total += self.scores[word]
        for word in self.across:
            total += self.scores[word]
        return total

    def intersection(self, inputs):
        if not inputs: 
            sys.exit()
        return set.intersection(*map(set, inputs))
    
    def generate_clues(self):
        for word in self.across:
            input = "Generate a crossword clue for " + word
            response = openai.Completion.create(
                model = "text-davinci-003",
                prompt = input,
                max_tokens = 100,
                temperature = 0
            )
            self.across_clues.append(response.choices[0].text)
        for i, word in enumerate(self.down):
            input = "Generate a crossword clue for " + word
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt= input,
                max_tokens=100,
                temperature=0
            )
            self.down_clues.append(response.choices[0].text)

#right now just hard testing. once the generator works ill make it so it generates automatically in constructor
# with recursionlimit(3000):
#     c = crossword_gen('tasty')
#     c.add_across()
#     c.add_down()
#     c.add_across()
#     c.add_down()
#     c.add_across()
#     c.add_down()
#     c.add_across()
#     print("ACROSS", c.across)
#     print("DOWN", c.down)

#tasty
#blane
#am
#se
#sn