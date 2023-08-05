import random
from code import terminal
from people import chat


class Warren():
    def __init__(self):
        self.symbol = 'W'
        
        self.voice = chat.Chat("Warren: ", "\033[34m")

    def speak(self, player):
        terminal.clear()
        if not player.warren_talked_to:   
            player.warren_talked_to = True

            self.voice.say("Well well well, if it isn't good old Mikkel")
            player.voice.say("Warren? Is that... You?")
            self.voice.say("What's the matter Mikkel? Forgot about me already?")
            player.voice.say("I can't seem to remember a lot of things")
            self.voice.say("I'm not surprised. I hit you hard enough with that mace I thought your brains were going to be splattered on the wall")
            player.voice.say("I don't remember fighting you... I thought we were freinds")
            self.voice.say("Yeah, we were friends, we aren't any more, so turn around before I kill you for real this time")
            player.voice.say("I don't want to fight you Warren. I just want to find the heart of magic and get out of here!")
            self.voice.say("LIAR! You just want the power for yourself!")
            player.voice.say("We can find it together")
            self.voice.say("I don't think you realize exactly what is going on here. The heart of magic can only be used for a single wish. And I'm planning on using it")
            player.voice.say("Don't we want the same thing? To destroy Death and escape this place?")
            self.voice.say("Destroy Death? Your more insane then I am. Death and Life are two things that must always exist in the universe. You can't make death die, he is the very definition of dying and thus cannot be killed by it. Even if you could make him vanish, he is a universial being and will only be reincarnated the second someone anywhere in the universe dies")
            player.voice.say("Then I can destroy the gate, that way he will never be able to enter the mortal realm")
            self.voice.say("And we would be trapped here forever! Are you forgetting about that")
            player.voice.say("A sacrifice must be made somewhere")
            self.voice.say("... Right. A sacrifice. I suppose Ferric was just a sacrifice, Terkker was just a sacrifice... coyote william all of them... just a sacrifice weren't they?")
            player.voice.say("I don't know. I can't remember...")
            
            terminal.clear()

            self.voice.say("How about I remind you then? Yeah, I'll tell you what happened to them. They all came here, here to find that blasted thing and stop death. Then they all died.")
            player.voice.say("Trekker was alive... I spoke with him")
            self.voice.say("Was? I'm assuming he's dead now. Did you kill him like you did William?")
            player.voice.say("William? I didn't kill him!")
            self.voice.say("Yes you did Mikkel. You attacked us, you were raving mad, screaming garbage. William tried to help you, he was trying to heal you. And what did you do?")
            player.voice.say("I... I don't remember")
            self.voice.say("You killed him. Stabbed him through the heart.")
            player.voice.say("And Coyoote? Did I kill him?")
            self.voice.say("No no, I did that. That scrappy little scout got in my way. I told him to step aside, being the idiot he was he wouldn't, so I killed him.")
            player.voice.say("Coyote was our brother")
            self.voice.say("So was William, and Ferric, who died trying to escape")
            player.voice.say("No! I didn't kill William, I can't have")
            self.voice.say("Heh. Your right. I killed him")
            player.voice.say("You what?")
            self.voice.say("You and William teamed up against me. Becuase I didn't want to use that stupid stone to destroy death, I want to use it to bring my family back, and that's what I'm going to do.")
            player.voice.say("So you killed him?")
            self.voice.say("Yeah... You guys thought you were such powerful warriors... such amazing soldiers. Util I ran William through to the hilt and bashed your head in with a mace.")
            player.voice.say("Your a traitor then?")
            self.voice.say("You could call me that. And I accept that title with honor. All my life I've served the king, served you, faught to protect everybody else. This time I want to fight for myself. I want to fight for the things I want. Call me selfish if you like, but I spent a thousand years guarding that gate to protect the mortal realm, now I want to do one thing for myself and you try and kill me. I don't want to fight you Mikkel, I don't want to kill you. But I will")
            player.voice.say("Our oath as a silent warrior was to protect the mortal realm from the dangers of this place. I must complete that mission")
            self.voice.say("Too bad... The heart of magic can only be used for a single wish.")
            player.voice.say("I don't want to fight you Warren. I will part ways with you here.")
            self.voice.say("Be warned Mikkel, I am going to find that heart of magic. Even if I have to kill you to get it.")
        else:
            self.voice.say("Stay away from me Mikkel, or I'll kill you.")
        

            