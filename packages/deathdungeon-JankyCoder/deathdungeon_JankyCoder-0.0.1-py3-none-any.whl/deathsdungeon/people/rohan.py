import random
from code import terminal
from people import chat


class Rohan():
    def __init__(self):
        self.symbol = 'R'

        self.voice = chat.Chat("Rohan: ", "\033[34m")

    def speak(self, player):
        terminal.clear()

        self.voice.say("I thought I'd never see you again!")
        player.voice.say("Me?")
        self.voice.say("Yes yes... I... ah never mind then")
        player.voice.say("What is it?")
        self.voice.say("*cackles*")
        player.voice.say("What's so funny?")
        self.voice.say("Nothing... nothing at all.")

        i = self.choice("[1] Ask him how he got here\n[2] Leave him alone", valid=['1', '2'])

        if i == '1':
            terminal.clear()
            self.voice.say("Crazy one ain't you. Dem were the breaks where I where been")
            player.voice.say("I don't understand...")
            self.voice.say("I saw it... It was there, just through the portal infront of me")
            player.voice.say("What was it?")
            self.voice.say("I was too weak. I fell to my knees, so close. Then it was gone")
            player.voice.say("What was gone?")
            self.voice.say('Gone gone gone... I saw and it now it is gone')
        else:
            terminal.clear()
            self.voice.say("The ghouls are close by... beware")
        
    def choice(self, prompt, valid):
        """Todo: Update to Navigate Function"""
        while True:
            print(prompt)
            i = input()
    
            if i in valid:
                return i

