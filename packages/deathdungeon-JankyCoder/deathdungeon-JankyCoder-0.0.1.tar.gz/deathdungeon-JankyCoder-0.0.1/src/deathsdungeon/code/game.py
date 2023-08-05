from code import terminal, map, randomness, util, read
from battle import enemy, battle
from getkey import getkey, keys
import random, time
from classes import weapon, armor
from generators import monsters
from save_game import save

class Game():
    def __init__(self, dungeon, player, characters, posx=False, posy=False):
        """Initiate the Game"""
        self.dungeon = dungeon

        self.player = player

        self.characters = characters

        if not posx and not posy:
            self.y, self.x = map.getSpawn(dungeon)
        else:
            self.y = posy
            self.x = posx


    def next_dungeon(self):
        """Generate a new dungeon and move the player into it"""
        print("The portal swirls before you!")

        print("[1] Enter")
        print("[2] Leave")

        choice = util.get_input("-> ", valid=["1", "2"])

        if choice == '1':
            print("You enter the swirling portal...")
            return True

        else:
            return False

    def play(self):
        """The main Game Loop"""
        count = 0
        
        while True:
            # disabled count clear for now. Manual clear is 9
            count += 1
            if count == 10:
                #terminal.clear() # just to keep things from being messy
                count = 0
                save.save_player_data(self.player, self.dungeon, self.x, self.y)

            stats = [self.player.get_stats()]
            
            map.display(self.dungeon, self.x, self.y, stats)

            self.dungeon[self.y][self.x] = ' '

            key = getkey()

            x = 0
            y = 0
            
            if key == 'w' or key == keys.UP:
                y = -1

            elif key == 's' or key == keys.DOWN:
                y = 1

            elif key == 'd' or key == keys.RIGHT:
                x = +1

            elif key == 'a' or key == keys.LEFT:
                x = -1

            elif key == '1':
                self.player_stats()
            elif key == '2':
                self.player.shuffle_loadout()
            elif key == '3':
                self.player.eat()
            elif key == '4':
                read.pick_book(self.player)
            elif key == '8':
                save.save_player_data(self.player, self.dungeon, self.x, self.y)
            elif key == '9':
                terminal.clear()
            elif key == '0':
                print("Are you Sure you want to exit?")
                print("y/n")
                choice = util.get_input("-> ", valid=['y', 'n'])
                if choice == 'y':
                    print("Saving...")
                    save.save_player_data(self.player, self.dungeon, self.x, self.y)
                    exit()
                elif choice == 'n':
                    terminal.clear()

            action = map.action(self.dungeon, self.x+x, self.y+y)

            if action.valid:
                self.y += y
                self.x += x

            if action.treasure:
                self.open_treasure()
            
            if action.shard:
                self.collect_shard()

            if action.enemy:
                m = monsters.generate_monsters()
                if self.choose_fight(m):
                    self.y += y
                    self.x += x

            if action.portal:
                if self.next_dungeon():
                    return True


            if action.character:
                for character in self.characters:
                    if character.symbol == action.character:
                        character.speak(self.player)

    def player_stats(self):
        """Show the user inventory, armor, etc"""

        terminal.clear()

        width = 70

        util.center(self.player.get_stats(), width)

        print("\n")
        util.center(f"SILVER: {str(self.player.silver)} | GOLD: {str(self.player.gold)} | DIAMONDS: {str(self.player.diamonds)}", width)

        print("\n")
        util.center(f"SHARDS: {str(self.player.shards)}", width)

        print("\n\n")

        util.center("---------- WEAPONS -----------", width)
        print("\n")

        print(self.player.weapon.stats())
        print(self.player.armor.stats())

        print("\n")
        util.center("------------------------------", width)

        print("\n\n")

        util.center("|~ INVENTORY ~|", width)

        print("\n")

        items = []

        for item in sorted(self.player.inventory):
            exist = False
            for i in items:
                if item == i[0]:
                    i[1] += 1
                    exist = True
            if not exist:
                items.append([item, 1])

        for item in items:
            util.indent(f"{item[0]} x{str(item[1])}", 26)
            


        util.cont()



    def open_treasure(self):
        """Gens Random Box and opens it"""

        terminal.clear()

        loot = random.choice(randomness.loot)

        if loot['type'] == 'weapon':
            w = weapon.generate_weapon()
            print('You found a tier ' + str(w.tier) + " " + str(w.name))
            print("[1] Equip")
            print("[2] Keep")
            print("[3] Throw away")
            choice = util.get_input("-> ", valid=["1", "2", "3"])

            if choice == '1':
                self.player.equip_weapon(w)
                self.player.store_weapon(w)

            elif choice == '2':
                self.player.store_weapon(w)

            else:
                print("You threw away the " + w.name)

        elif loot['type'] == 'armor':
            a = armor.generate_armor()
            print('You found tier ' + str(a.tier) + " " + str(a.name))
            print("[1] Equip")
            print("[2] Keep")
            print("[3] Throw away")
            choice = util.get_input("-> ", valid=["1", "2", "3"])

            if choice == '1':
                self.player.equip_armor(a)
                self.player.store_armor(a)

            elif choice == '2':
                self.player.store_armor(a)

            else:
                print("You threw away the " + a.name)

        elif loot['type'] == 'money':
            val = random.randint(1, loot['max'])

            print('You found ' + str(val) + ' ' + loot['name'])

            if loot['name'] == 'gold':
                self.player.gold += val
            elif loot['name'] == 'silver':
                self.player.silver += val
            elif loot['name'] == 'diamond':
                self.player.diamonds += val

        elif loot['type'] == 'inventory':
            print("You found a " + loot['name'])
            self.player.inventory.append(loot['name'])

        util.cont()
            

    def choose_fight(self, enemies):
        if len(enemies) > 1:
            print("A group of " + enemies[0].name + "'s approach!")
        else:
            print("A loan " + enemies[0].name + " approaches")

        print("[1] Battle")
        print("[2] Run")

        choice = util.get_input("-> ", valid=['1', '2'])

        if choice == '1':
            battle.fight(self.player, enemies)
            return True
        else:
            print("You chose to run!")
            
        util.cont()
        
        return False
    
    def collect_shard(self):
        if self.player.shards == 0:
            terminal.slow_print("The small blue crystal glows in your hand")
            terminal.slow_print("It eminates a strange aurora...")
            terminal.slow_print("Something... something familar...")
            self.player.remember_convo1()
        elif self.player.shards == 5:
            terminal.slow_print("Hmm... More of these little things... It's almost as if someone is leaving there here on purpose")
            terminal.slow_print("The more you pick up, the more your start to remember...")
            terminal.slow_print("....................")
            self.player.remember_convo2()
        else:
            print("You found a shard!")
            print("Your magic Powers and Health have grown!")
        
        self.player.shards += 1
        self.player.max_life += 10
        self.player.life += 10
        self.player.max_magic += 5
        self.player.magic += 5
        
        util.cont()

        

        

                
            