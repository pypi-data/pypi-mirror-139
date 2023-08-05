import random
from code import terminal
from people import chat


words = ['the...', 'the', 'peice', 'heart', 'magic', 'flow', 'river', 'stone', 'walls', 'ghouls', 'they', 'them', 'i...', 'i', 'who...']

class Grarlan():
    def __init__(self):
        self.symbol = 'G'

        self.voice = chat.Chat("Grarlan: ", "\033[34m")

    def speak(self, player):
        terminal.clear()
        t = []
        for i in range(random.randint(1, 8)):
            t.append(random.choice(words))

        self.voice.say(" ".join(t))

