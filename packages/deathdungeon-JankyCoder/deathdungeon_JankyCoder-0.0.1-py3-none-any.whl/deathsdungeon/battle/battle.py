from code import terminal, util, randomness
from battle import die, buff
import random


def living_enemies(enemies):
    """Check if any enemies are still alive"""
    val = False
    for enemy in enemies:
        print(enemy)
        if enemy.life > 0:
            val = True

    return val


def fight(player, enemies):
    """Fight between Player and Enemy"""

    player_turn = True # player always start, might switch to player_turn = random.randint(0, 1)

    valid_nums = [str(i) for i in range(0, 9)]

    buffs = []

    last_hit = None

    green = "\033[32m"
    red = "\033[31m"
    reset = "\033[0m"

    ########################
    # DON'T FORGET TO USE  #
    # MINIMAL BATTLE STYLE #
    ########################

    while player.life > 0 and living_enemies(enemies) > 0:
        while player_turn:
            terminal.clear()
            print(player.get_stats())
            print("\n\n---------- BUFFS -----------\n")
            for b in buffs:
                if not b.enemy:
                    print(f"{red}{b.reason} -> {b.des}{reset}")
                else:
                    print(f"{green}{b.reason} -> {b.des}{reset}")
            if not buffs:
                print("None")
            print("\n------------------------------")
            print("\n\n---------- ENEMIES -----------\n")
            for enemy in enemies:
                print(f"[{str(enemies.index(enemy))}] {enemy.name}-> {enemy.get_battle_stats()}")
            print("\n------------------------------")

            commands = ['?', 'attack', 'loadout', 'drink', 'magicae', 'run']
            
            full = input("-> ")

            c = full.split()

            command = c[0]

            if command in commands:
                # use try to invalid commands
                if command == '?':
                    print("Figure it out loser!")
                
                elif command == 'attack':
                    target = c[1]

                    if target in valid_nums:
                        enemy = enemies[int(target)]
                        player.attack(enemy, buffs, enemies)
                        last_hit = enemy
                        player_turn = False
                    else:
                        print("No enemy found!")
                
                elif command == 'loadout':
                    player.shuffle_loadout()
                
                elif command == 'run':
                    if random.randint(1, 4) == 1:
                        die.die("Struck in the back while running like a coward.")
                    else:
                        print("You flee the battle")
                        return
                
                elif command == 'drink':
                    potion = " ".join(c[1:]).lower()

                    if potion in player.inventory and potion in randomness.valid_potions:
                        player.inventory.remove(potion)
                        
                        if potion == 'potion of energy':
                            b = buff.Buff(50, 0, 1, "Potentia Navitas", "+50 on next attack")
                            print("Buff Activated: +50 on next attack")
                            buffs.append(b)
                        elif potion == 'healing potion':
                            print("You drank the healing potion...")
                            player.life = player.max_life
                        player_turn = False
                    else:
                        print("You don't have that potion!")
                
                elif command == 'magicae':
                    spell = " ".join(c[1:])
                    if spell in randomness.valid_spells:
                        if spell == 'sana ego':
                            if player.magic >= 4:
                                player.magic -= 4
                                player.life += 10
                                if player.life > player.max_life:
                                    player.life = player.max_life
                            else:
                                print("You do not have enough power to throw that spell")

                        elif spell == 'sana vulnera':
                            if player.magic >= 5:
                                player.magic -= 5
                                player.life += 15
                                if player.life > player.max_life:
                                    player.life = player.max_life
                            else:
                                print("You do not have enough power to throw that spell")
                        
                        elif spell == 'sana omnis vulnera':
                            if player.magic >= 10:
                                player.magic -= 10
                                player.life += 40
                                if player.life > player.max_life:
                                    player.life = player.max_life
                            else:
                                print("You do not have enough power to throw that spell")
                        
                        elif spell == 'confirma impetum':
                            if player.magic >= 10:
                                player.magic -= 10
                                b = buff.Buff(40, 0, 1, "Confirma Impetum", "+40 Damage on Next Attack")
                                buffs.append(b)
                                print("Buff Activated: +40 Damage on Next Attack")
                            else:
                                print("You do not have enough power to throw that spell")
                        
                        elif spell == 'confirma defensio':
                            if player.magic >= 10:
                                player.magic -= 10
                                b = buff.Buff(0, -40, 1, "Confirma Defensio", "-40 Damage On Next Enemy Attack")
                                buffs.append(b)
                                print("Buff Activated: -40 Damage on Next Enemy Attack")
                            else:
                                print("You do not have enough power to throw that spell")
                        
                        elif spell == 'noxa hostilis':
                            if player.magic >= 25:
                                player.magic -= 25
                                print("All Enemies Recieve 50 Damage")
                                for enemy in enemies:
                                    enemy.life -= 50
                                    if enemy.life <= 0:
                                        enemies.remove(enemy)
                                        player.loot(enemy)
                            else:
                                print("You do not have enough power to throw that spell")
                    else:
                        print("Your strange magic words are confusing...")
                        print(spell + " is not a spell")
            util.cont()

        

        while not player_turn:
            player_turn = True
            for enemy in enemies:
                while True:
                    if enemy.life <= (player.weapon.damage+util.floor(player.weapon.sharpness-enemy.armor.armor))*player.weapon.weight:
                        if enemy.can_heal:
                            # try to save them selves
                            enemy.heal(player, player_turn, buffs, enemies)
                        else:
                            # else try to kill the player as they cannot heal
                            if last_hit == enemy:
                                enemy.desperate_attack(player)
                            else:
                                enemy.choose_attack(player, player_turn, buffs, enemies)
                        break
                    else:
                        # pick the attack based on on player, buffs for fellow enemies, current buffs against them, player life and possible damage they might deal to the player
                        t = enemy.choose_attack(player, player_turn, buffs, enemies)
                        if t == 1:
                            # Enemy Plays turn again
                            pass
                        elif t == 2:
                            # all enemies play again
                            player_turn = False
                        else:
                            break

        for b in buffs:
            b.lasts -= 1
            if b.lasts <= 0:
                buffs.remove(b)

    if player.life <= 0:
        die.die("slaughtered in battle")
                            