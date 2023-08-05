from people import chat
from classes import weapon
import random
from code import util, terminal

def calc_cost(w):
    """Calculates the cost of the weapon based on Tier"""

    _min = 12
    _max = 18

    if w.tier != 0:
        _min += random.randint(1, w.tier)*w.tier
        _max += random.randint(1, w.tier)*w.tier
    else:
        w = weapon.generate_weapon()
        self.calc_cost(w)


    if _min > _max:
        return random.randint(_max, _min)
    else:
        return random.randint(_min, _max)

class Maximus():
    def __init__(self):
        self.symbol = 'M'

        self.voice = chat.Chat("Maximus: ", "\033[34m")

        self.weapon1 = weapon.generate_weapon()
        self.weapon2 = weapon.generate_weapon()
        self.weapon3 = weapon.generate_weapon()

        self.weapon1_cost = calc_cost(self.weapon1)
        self.weapon2_cost = calc_cost(self.weapon2)
        self.weapon3_cost = calc_cost(self.weapon3)
        

    def speak(self, player):
        terminal.clear()
        if player.maximus_talked_to:
            self.voice.say("Eh... You again? Still haven't found your friend? Never mind... Looking for another trade?")
            i = self.choice("[1] Trade\n[2] Leave", valid=['1','2'])
            if i == '1':
                self.trade(player)
            else:
                self.voice.say("Good luck to you then!")
        else:
            player.maximus_talked_to = True
            self.voice.say("Hello there!")
            player.voice.say("Who are you?")
            self.voice.say("Me? Oh I'm Maximus Alchetren, and I was once a mighty king! Now I'm just a survivor here like the rest of us")
            player.voice.say("How long have you been here?")
            self.voice.say("Too long my friend, I cannot remember what the outside world even looks like now.")
            i = self.choice("[1] Ask him what he came here for\n[2] Ask him if he knows of a way out", valid=['1', '2'])
            if i == '1':
                player.voice.say("Why did you come here?")
                self.voice.say("Ah! A good question. I was power hungry, I wished to find the heart of magic and use it for my own")
                player.voice.say("The heart of magic?")
                self.voice.say("Isn't it what we are all here for? It is the very source of the river of magic, the ultimate power")
                i = self.choice("[1] Ask him if he has seen you before\n[2] Ask him if he knows a way out", valid=['1', '2'])
                if i == '1':
                    self.voice.say("You? I've seen you many a time, you don't remember me do you?")
                    player.voice.say('Not really')
                    self.voice.say("Hmm. Death's Dungeon has a strange way of working on the mind. Say, what happened to your friend?")
                    player.voice.say("Friend?")
                    self.voice.say("Yes, you had someone with you last time, eh... maybe he's dead")
                elif i == '2':
                    self.voice.say("A way out? I've tried so many times. This place is a maze, there is no finding your way out! I tried mining through the walls, but every time I hit rock so hard it is impossible to break, or rivers of lava")
                    player.voice.say("Has anyone made it out?")
                    self.voice.say("The only way to escape this place is by death. I have tried to stay sane and hopeful, I must admit I know I am trapped here forever, there is no way out.")
            else:
                self.voice.say("A way out? I've tried so many times. This place is a maze, there is no finding your way out! I tried mining through the walls, but every time I hit rock so hard it is impossible to break, or rivers of lava")
                player.voice.say("Has anyone made it out?")
                self.voice.say("The only way to escape this place is by death. I have tried to stay sane and hopeful, I must admit I know I am trapped here forever, there is no way out.")


    def choice(self, prompt, valid):
        """Todo: Update to Navigate Function"""
        while True:
            print(prompt)
            i = input()
    
            if i in valid:
                return i


    def trade(self, player):
        self.voice.say("What would you like to have a look at? My Weapons or my Supplies?")
        i = self.choice("[1] Weapons\n[2] Supplies", valid=['1', '2'])

        if i == '1':
            print(f"[1] {self.weapon1.name} DMG: {str(self.weapon1.damage)} | SHRP: {str(self.weapon1.sharpness)} | WGHT: {str(self.weapon1.weight)} TIER: {str(self.weapon1.tier)} --- COST: {str(self.weapon1_cost)}")
            print(f"[2] {self.weapon2.name} DMG: {str(self.weapon2.damage)} | SHRP: {str(self.weapon2.sharpness)} | WGHT: {str(self.weapon2.weight)} TIER: {str(self.weapon2.tier)} --- COST: {str(self.weapon2_cost)}")
            print(f"[3] {self.weapon3.name} DMG: {str(self.weapon3.damage)} | SHRP: {str(self.weapon3.sharpness)} | WGHT: {str(self.weapon3.weight)} TIER: {str(self.weapon3.tier)} --- COST: {str(self.weapon3_cost)}")
            print("[4] Exit")

            i = util.get_input("-> ", valid=['1', '2', '3', '4'])

            if i == '1':
                self.purchase_weapon(self.weapon1, self.weapon1_cost, player)
            elif i == '2':
                self.purchase_weapon(self.weapon2, self.weapon2_cost, player)
            elif i == '3':
                self.purchase_weapon(self.weapon3, self.weapon3_cost, player)
            elif i == '4':
                self.voice.say("Suit yourself...")
                terminal.clear()
        else:
            print("[1] Apples -- 5 silver")
            print("[2] Bread  -- 15 silver")
            print("[3] Severed Hand -- 3 Gold")
            print("[4] Exit")
            
            choice = util.get_input("-> ", valid=['1', '2', '3','4'])

            if choice == '1' and player.silver >= 5:
                player.silver -= 5
                player.inventory.append("apple")
            elif choice == '2' and player.silver >= 15:
                player.silver -= 15
                player.inventory.append("bread")
            elif choice == '3' and player.gold >= 3:
                player.gold -= 3
                player.inventory.append("severed hand")
            elif choice == '4':
                pass
            else:
                self.voice.say("Hey! Are you trying to cheat me!")
                return
            self.voice.say("Pleasure doing business with you.")






    def purchase_weapon(self, weapon, cost, player):
        if player.gold >= cost:
            print("Purchased Weapon")
            player.gold -= cost
            player.store_weapon(weapon)

        else:
            self.voice.say("Hey! Are you trying to stiff me! You don't have enough gold for that!")
        