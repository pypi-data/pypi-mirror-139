from classes import weapon, armor
import random
from code import util, terminal
from battle import buff


class Enemy():
    def __init__(self, name, life, magic, weapon, armor, can_magic=False, can_heal=False, silver=0, gold=0, diamonds=0, buff=False):
        """Initate the Enemy Class"""
        self.name = name
        self.life = life
        self.max_life = life
        self.magic = magic
        self.max_magic = magic
        self.weapon = weapon
        self.armor = armor
        self.can_magic = can_magic
        self.buff = buff
        self.silver = silver
        self.gold = gold
        self.diamonds = diamonds

        self.can_heal = can_heal


        self.dead = False


    def get_battle_stats(self):
        """Get the Stats important to battle"""

        stats = f"LIFE: {str(self.life)}/{str(self.max_life)}"

        if self.can_magic:
            stats += f" | MAGIC: {str(self.magic)}/{str(self.max_magic)}"

        return stats


    def desperate_attack(self, player):
        """Attack the Player in a last ditch effort -- No Buffs"""

        green = "\033[32m"
        red = "\033[31m"
        reset = "\033[0m"

        terminal.slow_print(f"The {self.name.capitalize()} Charges!")

        dmg = (self.weapon.damage+self.weapon.sharpness)*self.weapon.weight

        terminal.slow_print(f"{red}+{str(dmg)}{reset}")

        true_dmg = (self.weapon.damage+util.floor(self.weapon.sharpness-player.armor.armor))*self.weapon.weight

        armor_block = dmg-true_dmg

        terminal.slow_print(f"{green}   -{str(armor_block)} -- armor{reset}")

        if dmg > 0:
            terminal.slow_print(f"{red}{true_dmg} Damage{reset}")
            player.life -= true_dmg
        else:
            terminal.slow_print(f"{green}0{reset}")


    def heal(self, player, player_turn, buffs, enemies):
        """Attempt to heal self using spell `sana ego` or `sana vulnera`"""
        if self.magic >= 5:
            terminal.slow_print(f"{self.name} heals")
            self.magic -= 5
            self.life += 15
            terminal.slow_print("+15")
        elif self.magic == 4:
            terminal.slow_print(f"{self.name} heals")
            self.magic -= 4
            self.life += 10
            terminal.slow_print("+10")
        else:
            self.choose_attack(player, player_turn, buffs, enemies)


    def choose_attack(self, player, player_turn, buffs, enemies):
        """Pick an attack based on the player and battle position/fellow enemies"""

        green = "\033[32m"
        red = "\033[31m"
        reset = "\033[0m"

        # Defualt to attack the player
        # check if buddies
        # ENEMIES CAN NO LONGER SUMMON

        # if len(enemies) == 1:
        #     # if no buddies and can sommon, summon buddies
        #     if self.can_summon and not summoned:
        #         self.summon(enemies)
        #         summoned = True
        #         return
        #     # else return to process

        # calc damage

        raw_dmg = (self.weapon.damage+self.weapon.sharpness)*self.weapon.weight
        true_dmg = (self.weapon.damage+util.floor(self.weapon.sharpness-player.armor.armor))*self.weapon.weight

        # if player is one hit away from dead. Finish them
        # NOTE: This is sort of OP

        if player.life <= true_dmg:
            terminal.slow_print(f"{self.name} attacks")
            terminal.slow_print(f"+{str(raw_dmg)}")
            terminal.slow_print(f"   -{str(raw_dmg-true_dmg)} -- armor")

            for buff in buffs:
                true_dmg += buff.enemy_dmg
                if buff.enemy_dmg > 0:
                    terminal.slow_print(f"{red}   +{str(buff.enemy_dmg)} --{buff.reason}{reset}")
                else:
                    terminal.slow_print(f"{green}   -{str(buff.enemy_dmg)} --{buff.reason}{reset}")

            if true_dmg < 0:
                true_dmg = 0

            terminal.slow_print(f" {red}{str(true_dmg)} Damage{reset}")

            player.life -= true_dmg

            return

        # TODO: if magic and magic attack and magic attack is enough to finish them damage than use magic
            
        # if more then two buddies and buff available, use buff

        if len(enemies) >= 3 and self.buff:
            terminal.slow_print(f"{self.name} used {self.buff.reason}")
            terminal.slow_print(self.buff.des)
            buffs.append(self.buff)
            self.buff = False
            return

        # TODO: if magic more damage then weapon and enough magic to throw, throw spell

        # TODO: if inventory item more damage then weapon use inventory item

        # TODO: if stamina use weapon

        terminal.slow_print(f"{self.name} attacks")
        terminal.slow_print(f"+{str(raw_dmg)}")
        green = "\033[32m"
        terminal.slow_print(f"{green}   -{str(raw_dmg-true_dmg)} -- armor{reset}")

        for buff in buffs:
            true_dmg += buff.enemy_dmg
            if buff.enemy_dmg > 0:
                terminal.slow_print(f"{red}   +{str(buff.enemy_dmg)} --{buff.reason}{reset}")
            else:
                terminal.slow_print(f"{green}   -{str(buff.enemy_dmg)} --{buff.reason}{reset}")

        if true_dmg < 0:
            true_dmg = 0

        terminal.slow_print(f" {red}{str(true_dmg)} Damage{reset}")

        player.life -= true_dmg

        return

        # TODO: if no stamina look for inventory item

            # TODO: if potion of energy found use over weapon

        # TODO: if no inventory item rest

        

        
        
        
    