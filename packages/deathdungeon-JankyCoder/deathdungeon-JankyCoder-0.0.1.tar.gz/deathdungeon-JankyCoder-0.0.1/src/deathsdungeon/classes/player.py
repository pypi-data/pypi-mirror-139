from classes import armor, weapon
from code import util, terminal, randomness
from people import chat
import random

class Player():
    def __init__(self):
        """Initiate the Player"""

        # Life/Magic
        # EDIT: Stamina has been Removed
        self.life = 100
        self.max_life = 100
        self.magic = 10
        self.max_magic = 10

        # Weapons/Armor
        self.weapon = weapon.generate_weapon()
        self.armor = armor.generate_armor()

        # Inventory/Money
        self.inventory = ["Pack of Letters"]
        self.weapons = [self.weapon]
        self.armors = [self.armor]
        self.max_weapons = 3
        self.max_armors = 3
        self.gold = 10
        self.silver = 50
        self.diamonds = 2
        self.shards = 0

        # voice
        self.voice = chat.Chat("You: ", "\033[37m")

        #Keep track of rooms played
        self.rooms_played = 0

        #Keep Track of who you talked with/who is still alive

        self.trekker_alive = False
        self.maximus_talked_to = False
        self.laurence_talked_to = False
        self.warren_talked_to = False

    def attack(self, enemy, buffs, enemies, noloot=False):
        """Attack the Enemy and add Effects for Buffs"""

        terminal.clear()

        green = "\033[32m"
        red = "\033[31m"
        reset = "\033[0m"

        raw_dmg = (self.weapon.damage+self.weapon.sharpness)*self.weapon.weight

        terminal.slow_print(f"{green}+{str(raw_dmg)}{reset}")


        dmg = (self.weapon.damage+util.floor(self.weapon.sharpness - enemy.armor.armor))*self.weapon.weight

        armor_block = raw_dmg-dmg

        terminal.slow_print(f"{red}   -{str(armor_block)} -- armor{reset}")

        for buff in buffs:
            if buff.dmg:
                dmg += buff.dmg
                if buff.dmg > 0:
                    terminal.slow_print(f"{green}   +{buff.dmg} --{buff.reason}{reset}")
                else:
                    terminal.slow_print(f"{red}   -{buff.dmg} --{buff.reason}{reset}")

        if dmg > 0:
            terminal.slow_print(f" {green}{str(dmg)} Damage{reset}")
        else:
            dmg = 0
            terminal.slow_print(f" {red}{str(dmg)} Damage{reset}")

        enemy.life -= dmg

        if enemy.life <= 0:
            print("You defeated the " + enemy.name)
            enemies.remove(enemy)
            if noloot:
                return
            else:
                self.loot(enemy)

            

    def loot(self, enemy):
        """Loot the Enemy"""
        if enemy.silver:
            print(f"You looted {str(enemy.silver)} silver")
            
        if enemy.gold:
            print(f"You looted {str(enemy.gold)} gold")
            
        if enemy.diamonds:
            print(f"You looted {str(enemy.diamonds)} diamonds")

        self.silver += enemy.silver
        self.gold += enemy.gold
        self.diamonds += enemy.diamonds

        magic = random.randint(1, 3)

        print(f"You gained {str(magic)} magic")

        self.magic += magic
        if self.magic > self.max_magic:
            self.magic = self.max_magic

        print(enemy.weapon.stats())

        print("[1] Keep")
        print("[2] Throw Away")
        
        choice = util.get_input("-> ", valid=['1','2'])

        if choice == '1':
            self.store_weapon(enemy.weapon)
        else:
            print('You threw it away')

        print(enemy.armor.stats())

        print("[1] Keep")
        print("[2] Throw Aaway")

        choice = util.get_input("-> ", valid=['1', '2'])

        if choice == '1':
            self.store_armor(enemy.armor)
        else:
            print("You threw it away")
        
                
            

        

    
    def get_stats(self):
        """Return Basic Player Stats"""
        return f"LIFE: {str(self.life)}/{str(self.max_life)} | MAGIC: {str(self.magic)}/{str(self.max_magic)}"


    def eat(self):
        """Eat Food to Heal"""
        while True:
            terminal.clear()
            print(self.get_stats())

            print("\n\n")
    
            items = []
    
            for item in sorted(self.inventory):
                exist = False
                for i in items:
                    if item == i[0]:
                        i[1] += 1
                        exist = True
                if not exist:
                    items.append([item, 1])
    
            for item in items:
                print(f"{item[0]} x{str(item[1])}")
    
            print("\nChoose an item to eat")
    
            choice = input("-> ").lower()

            if choice == 'exit':
                return
    
            if choice in self.inventory:
                found = False
                for food in randomness.foods:
                    if food['name'].lower() == choice:
                        print("You ate a " + choice)
                        print("+"+str(food['health']) + " health")
                        self.life += food['health']
                        if self.life > self.max_life:
                            self.life = self.max_life
                        found = True
                        self.inventory.remove(choice)
                if not found:
                    print(choice+" is not a food!")
    
            input("\n\nPress Enter to Continue")

    def shuffle_loadout(self):
        """Shuffle Weapon and Armor Loadout"""
        while True:
            terminal.clear()
    
            print("#### CURRENT LOADOUT ####\n")
            print(f"\nWEAPON: {self.weapon.name.capitalize()} DMG: {str(self.weapon.damage)} | SHRP: {str(self.weapon.sharpness)} | WGHT: {str(self.weapon.weight)} | TIER: {str(self.weapon.tier)}")
            print(f"\nARMOR: {self.armor.name.capitalize()} ARMOR: {str(self.armor.armor)} | TIER: {str(self.armor.tier)}")
    
            print("\n\n")
    
            print("[1] Equip Weapon")
            print("[2] Equip Armor")
            print("[3] Exit")
    
            choice = util.get_input('-> ', valid=['1', '2', '3'])
    
            if choice == '1':
                valids = []
                for w in self.weapons:
                    index = str(self.weapons.index(w))
                    valids.append(index)
                    print(f"[{index}] {w.name} DMG: {str(w.damage)} | SHRP: {str(w.sharpness)} | WGHT: {str(w.weight)} | TIER: {str(w.tier)}")
    
                index = int(util.get_input("-> ", valid=valids))
    
                self.equip_weapon(self.weapons[index])
    
            elif choice == '2':
                valids = []
                for a in self.armors:
                    index = str(self.armors.index(a))
                    valids.append(index)
                    print(f"[{index}] {a.name} ARMOR: {str(a.armor)} | TIER: {str(a.tier)}")
    
                index = int(util.get_input("-> ", valid=valids))
    
                self.equip_armor(self.armors[index])
    
            else:
                break

            input("Press Enter to Continue")

            
        

    def equip_weapon(self, weapon):
        """Equip A Weapon"""
        self.weapon = weapon
        print(f"{self.weapon.name} equiped")

    def store_weapon(self, weapon):
        """Store A Weapon"""
        if len(self.weapons) >= 3:
            print("Not enough space to store weapon!")
            print("[1] Throw away")
            print("[2] Replace a different weapon")

            choice = util.get_input("-> ", valid=['1', '2'])

            if choice == '1':
                print("You threw the " + weapon.name + " away")

            else:
                print("Choose a weapon to be replaced: \n")
                
                valids = []
                for w in self.weapons:
                    index = str(self.weapons.index(w))
                    valids.append(index)
                    print(f"[{index}] {w.name} DMG: {str(w.damage)} | SHRP: {str(w.sharpness)} | WGHT: {str(w.weight)} | TIER: {str(w.tier)}")

                choice = util.get_input("-> ", valid=valids)

                self.weapons[int(choice)] = weapon

                print("Weapon stored.")
        else:
            self.weapons.append(weapon)
            print("Weapon stored.")


    def equip_armor(self, armor):
        """Equip Armor"""
        self.armor = armor
        print(f"{self.armor.name} equiped")

    def store_armor(self, armor):
        """Store Armor"""
        if len(self.armors) >= 3:
            print("Not enough space to store armor!")
            print("[1] Throw away")
            print("[2] Replace a different armor")

            choice = util.get_input("-> ", valid=['1', '2'])

            if choice == '1':
                print("You threw the " + armor.name + " away")

            else:
                print("Choose armor to be replaced: \n")
                
                valids = []
                for a in self.armors:
                    index = str(self.armors.index(a))
                    valids.append(index)
                    print(f"[{index}] {a.name} ARMOR: {str(a.armor)} | TIER: {str(a.tier)}")

                choice = util.get_input("-> ", valid=valids)

                self.armors[int(choice)] = armor
                print("Armor stored.")
        else:
            self.armors.append(armor)
            print("Armor stored.")
    
    def remember_convo1(self):
        """Remember the Conversation you had with Trekker"""

        trekker = chat.Chat("Trekker: ", "\033[34m")

        terminal.slow_print("The shard pulsates in light and a vision flashes infront of your eyes")

        input()

        terminal.clear()

        self.voice.say("How will you find it Trekker? Even with your abilities it will be nearly impossible!")
        trekker.say("Calm down Mikkel, remember the shards")
        self.voice.say("Shards? I though Ferric was just joking around")
        trekker.say("He wasn't, I found one today. I can follow the trail, I'm sure of it")
        self.voice.say("It is too dangerous, we must stay and gaurd the gate")
        trekker.say("We are all grown men here, when we swore our oath to protect this place we knew how dangerous it would be. We cannot just sit and guard the gate, we have to go on the offensive")
        self.voice.say("It's too dangerous... I can't as the leader let you do it")
        trekker.say("Mikkel! Listen to yourself! Do you seriously think we can stay here and guard it forever? Even if our bodies do not grow older our minds will. Ferric himself has admitted the spell will not last forever, it is already decaying! Something has to be done!")
        self.voice.say("And you think traveling into Death's very own dungeon is what we have to do")
        trekker.say("It's our only option.")
        self.voice.say("We don't know that, there is always another way, we can recruit successors for the guard")
        trekker.say("That isn't going to work, death grows more powerful each day, we cannot let it continue. We must do something!")
        self.voice.say("I cannot argue with you Trekker, I know you are correct. ")
        trekker.say("Me, Warren and William will go. That will leave you Ferric and Coyote to guard the portal. If we do not return, don't come after us")
        self.voice.say("Good luck Trekker.")

        terminal.clear()

        terminal.slow_print("The stone's light fades and the voices grow quieter and quieter")

        util.cont()

        terminal.clear()

        terminal.slow_print("For some reason you feel stronger and more powerful now, as if the shard has made your strength grow!")

    def remember_convo2(self):
        """Remember your Second Conversation with Trekker"""

        util.cont()

        terminal.clear()

        trekker = chat.Chat("Trekker: ", "\033[34m")

        trekker.say("Mikkel!")
        self.voice.say("What is it Trekker? Is something wrong?")
        trekker.say("Yes... horribly the wrong")
        self.voice.say("What has happened?")
        trekker.say("The king attacked our supporters in the mortal realm, all of them are dead")
        self.voice.say("Warrens-")
        trekker.say("Yes, his son. Ferric's brother, all of them. What are we going to do?")
        self.voice.say("Guard the gate. I will return")

        util.cont()

        terminal.clear()
                    

    def remember_convo3(self):
        """Warren Gives you the Letters for his son"""

        util.cont()

        terminal.clear()


        warren = chat.Chat("Warren: ", "\033[34m")


        warren.say("Take these, I cannot leave the gate, if I do I will not have the willpower to return to my post")
        self.voice.say("What is it-")
        warren.say("My letters for my son. I wanted to send them a long time ago... but I... I was a little afraid he wouldn't even want to read them")
        self.voice.say("Warren i-")
        warren.say("Just take them to him, please. Swear to me you will take them to him")
        self.voice.say("I never told you about... ")
        warren.say('About what?')
        self.voice.say("Never mind. I give you my word I will take these two your son")
        warren.say('Thankyou Mikkel, I trust you will')

        util.cont()

        terminal.clear()
    

    def remember_convo4(self):
        """Coyote and Ferric go into Deaths Dungeon"""

        util.cont()

        terminal.clear()

        coyote = chat.Chat("Coyote: ", "\033[34m")
        ferric = chat.Chat("Ferric: ", "\033[42m")


        coyote.say("We have to go after them. We cannot just let them perish")

        self.voice.say("We cannot abandon our post")

        coyote.say("I'm not saying that we should. I can stay here and guard the gate. You and Ferric go save them")

        ferric.say("You are a mighty warrior Coyote, but also the smallest and weakest among us, you would be overwhelmed and defeated if the Ghouls attacked")

        coyote.say("I'm faster then both of you, that makes up for my lack of size and strength")

        self.voice.say("I will stay. Coyote you know Trekker best, if anyone can find him it will be you. And Ferric, I barely count as a wizard, if they are wounded or hurt, they will need your healing magic")

        coyote.say("Are you sure Mikkel?")

        self.voice.say("My size and weight would only make fighting more difficult in that dungeon maze. Both of you should go. I will protect the gate till you return")

        ferric.say("And if we don't?")

        self.voice.say("If you do not return, then all hope is lost. We can only protect the mortal realm for so long, we must find the heart of magic")

        util.cont()

        terminal.clear()

    
