from people import chat
from classes import weapon
import random
from code import util, terminal
from people import chat


class Laurence():
    def __init__(self):
        self.symbol = 'L'

        self.voice = chat.Chat("Laurence ", "\033[34m")

        

    def speak(self, player):
        terminal.clear()
        if player.laurence_talked_to:
            self.voice.say("'ello there! Good to see you again, what wish ye to speak about?")
            player.voice.say("Any news on that spell?")
            self.voice.say("I'm afraid not, without Ferric I have hit a block in my knowledge of the magic arts")

        else:
            self.introduce(player)


    def introduce(self, player):
        terminal.clear()
        player.laurence_talked_to = True

        self.voice.say("Hello? Is someone there?")
        player.voice.say("It's me... a fellow survivor")
        self.voice.say("You aren't one of the crazy ones are you?")
        player.voice.say("I do not think that I am")
        self.voice.say("That is good then, I am Laurence, what is your name?")
        player.voice.say("I... I can't remember")
        self.voice.say("That's a shame.")
        player.voice.say("Do you know who I am?")
        self.voice.say("No no... Not that I can remember... I forget many things though")
        player.voice.say("Do you know much about this place?")
        self.voice.say("Oh yes... I would think so")
        player.voice.say("How long have you been here?")
        self.voice.say("Three thousand nine hundred and forty one days, fifteen hours and... thirty two minutes")
        player.voice.say("How do you know?")
        self.voice.say("I calculate the time based on the geometric angle the portals form at the shifting of the dungeon")
        player.voice.say("You seem very smart")
        self.voice.say("I used to think so... Not now, I've forgotten the one thing that could of helped me escape here")
        player.voice.say("A way out?")
        self.voice.say("Not a path out, but a spell... It's a long story")
        player.voice.say("Tell me!")
        self.voice.say("Very well...")
        terminal.clear()
        self.voice.say("I have studied the dungeon and deduced that it is always shifing, any level that is not occupied by a life form has it's shape shifted.")
        self.voice.say("Each time we enter a portal the other end connects us to a random room in the portal")
        player.voice.say("Then where is the end?")
        self.voice.say("There is no end, by my calculations there are three hundred and forty million six hundred and- well you get the point. The possible configurations of the dungeon make it mathmatically impossible to find the heart of magic")
        player.voice.say("The heart of magic?")
        self.voice.say("Yes... isn't that we are all here for?")
        player.voice.say("Do you know where it is?")
        self.voice.say("No... entering each portal you have a very small chance of entering the room where the heart is stored, by my calculations it is mathmatically impossible to get there")
        player.voice.say("You spoke of an exit?")
        self.voice.say("Ah yes... the spell.")
        player.voice.say("A spell?")
        self.voice.say("Yes, nearly a thousand years ago a man by the name of Ferric came here. He was a wise scholar and powerful wizard. Together we worked to fashion a spell that would open us a portal back to the mortal realm")
        player.voice.say("Did it work?")
        self.voice.say("I'm not sure, Ferric was killed by a ghoul when the spell was nearly complete. I finished it after his death, but not being a wizard myself I could not throw it")
        player.voice.say("I'm a wizard, what is the spell?")
        self.voice.say("I'm sorry... Over the years I've forgotten the entire spell, I was such a fool and never wrote it down, thinking I could remember it")
        player.voice.say("Can't you rebuild it?")
        self.voice.say("I'm a mathmatician not a wizard. Ferric built most of the spell I added a little, mostly the calculations needed to set a correct location and such... without his knowledge I can't even come close to a working spell")
        player.voice.say("If only you could remember it, or remake it")
        self.voice.say("You are a wizard, perhaps you can, I still have Ferric's journal, it does not contain the spell but it does contain his thoughts. Most of them a spells which I do not understand but it could aide you.")
        player.inventory.append("Ferric's Journal")
        player.voice.say("Thankyou friend, I'm sure his journal will be a great help to me")
        self.voice.say("I hope it is. Sadly most of the pages have been destroyed or fallen out")
        self.voice.say("Ferric was a great man if he had survived I'm sure I would not be here")
        player.voice.say("What can you tell me about the heart of magic?")
        self.voice.say("The heart? It is the most powerful peice of magic ever, it will allow anyone who takes it a single action. According to legend they can bring back loved ones, change the travel of time, destroy or create, those are only legends however, and nobody knows it's true power")
        player.voice.say("Is everyone here seeking it?")
        self.voice.say("Nearly all of us came becuase of it. Death is no fool however, he built this dungeon beneath his castle to hide the heart as it is the only thing that can destroy him.")
        player.voice.say("Did you come here after it?")
        self.voice.say("Yes I did... although I wish I had not")
        player.voice.say("If you found it what would you use it for?")
        self.voice.say("I would hope i would leave it be. Things of such power were not meant for anyone to have. My poor choices have left me in this despicable place, I deserve this fate. Using that thing, i feel would only lead me into more horrible places, too much power will currupt anyone, no matter how strong they are")
        player.voice.say("You don't want to leave here?")
        self.voice.say("I've been here for thousands of years. I will do nearly anything to escape, but I will not let the heart be part of it. It would only bring my to ruin with it's power. I know there is an exit from this place. I have entered enough portals that mathmatically it is possible in the next few hundred years I will find that exit.")
        player.voice.say("I wish you well then Laurence")
        self.voice.say('You as well my friend')
            




    def choice(self, prompt, valid):
        """Todo: Update to Navigate Function"""
        while True:
            print(prompt)
            i = input()
    
            if i in valid:
                return i

