import random
from code import terminal
from people import chat


class Trekker():
    def __init__(self):
        self.symbol = 'T'
        
        self.voice = chat.Chat("Trekker: ", "\033[34m")

    def speak(self, player):
        terminal.clear()
        if player.trekker_alive:   
            player.trekker_alive = False # RIP

            self.voice.say("M-Mikkel... It's you...")
            player.voice.say("Mikkel? Wh-what happened to you? Your bleeding all over!")
            self.voice.say("Those... those darn ghouls... we- we thought you left us Mikkel")
            player.voice.say("Your dying, I can heal you-")
            self.voice.say("It's too late Mikkel, besides i- i'm tired")
            player.voice.say("I can heal you...")
            self.voice.say("You left us Mikkel! ... you- we were... it's been so many years")
            player.voice.say("I'm sorry-")
            self.voice.say("They died Mikkel! C-coyote, william... ferr-ferric")
            self.voice.say("It's your fault... you could have saved us... we- we should have never... came... here...")

        else:
            print("Trekker is Dead.")
            input()
        

            