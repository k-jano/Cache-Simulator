import json

class BeladyFreq():
    def __init__(self):
        self.path = "freq.json"
        self.load_order()

    def load_order(self):
        f = open(self.path)
        self.freq = json.load(f)
        f.close()

    def decrement(self, file):
        self.freq[file] -= 1

    def get(self, file):
        return self.freq[file]
