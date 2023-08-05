from battle import buff, die
from code import terminal, util
from classes import weapon, armor
from people import chat



class Warren():
	def __init__(self):
		"""Initate Warren"""
		self.name = "Warren"
		self.life = 500 # 500
		self.max_life = 500
		self.weapon = weapon.Weapon("Kakavian Longsword", 10, 10, 10)
		self.armor = armor.Armor("Kakavian Battle Armor", 10)
		self.voice = chat.Chat("Warren: ", "\033[34m")

	def calc_hit(self, player):
		"""Calculate Damage"""
		terminal.clear()

		green = "\033[32m"
		red = "\033[31m"
		reset = "\033[0m"

		raw_dmg = (self.weapon.damage+self.weapon.sharpness)*self.weapon.weight

		terminal.slow_print(f"{green}+{str(raw_dmg)}{reset}")

		dmg = (self.weapon.damage+util.floor(self.weapon.sharpness - player.armor.armor))*self.weapon.weight

		armor_block = raw_dmg-dmg

		terminal.slow_print(f"{red}   -{str(armor_block)} -- armor{reset}")

		if dmg > 0:
			terminal.slow_print(f" {green}{str(dmg)} Damage{reset}")
		else:
			dmg = 0
			terminal.slow_print(f" {red}{str(dmg)} Damage{reset}")

		return dmg

	def get_stats(self):
		"""Return life... kinda lame"""
		return f"WARREN -- LIFE: {str(self.life)}/{str(self.max_life)}"


	def attack(self, player):
		"""Attack the Player"""

		if random.range(1, 5) == 1:
			dmg = self.calc_dmg(player)

			player.life -= dmg

		else:
			dmg = int(.9*player.life)
			terminal.slow_print(f"Super Strike: {str(dmg)} damage")

			player.life -= dmg

	def win(self, player):
		"""Warren Wins"""
		terminal.clear()

		self.voice.say("You are defeated Mikkel... Your even weaker then I remember.")
		player.voice.say("And you... are stronger then I remember...")
		self.voice.say("I warned you what would happen here Mikkel. I told you I would kill you")
		player.voice.say("You are a traitor...")
		self.voice.say("Yes... I'm a traitor, but I don't care! It's for my family Mikkel. I don't expect you to understand...")
		player.voice.say("I'm sorry about what happened to them, but you don't have to do this")
		self.voice.say("Heh... Do you know why I attacked you in the first place? Why I started fighting against you?")
		player.voice.say("No.")
		self.voice.say("You promised me you were going to take those letters to my son. You never told me he was dead!")
		player.voice.say("I'm sorry... I thought it would be better-")
		self.voice.say("If I didn't know? Ha, well how did that turn out of you")
		player.voice.say("I'm sorry Warren, I failed you")
		self.voice.say("Not just me. You failed to protect Coyote, William, Trekker, Ferric, you failed all of us. Your loved ones in the mortal realm, everyone, you failed them all")
		player.voice.say("I-")
		self.voice.say("You and your stupid gate. Guarding that gate cost more lives then would have been lost if we had just let people sort themselves out! After all, what have they done to deserve our protection? I say let them protect themselves! I have no reason to care for them")
		player.voice.say("Then you are a selfish boy, men protect the weak")
		self.voice.say("Even if you had one this battle my friend, it woudln't have mattered. Death and life are going to exist in all ages. No matter what you do to lock this place poeple will get here eventually, you can only delay the inevitable ruin. My wife and son, family, loved ones, those are things that will not always exist, they only last a short period of time, I just want to bring them back them back for just a few more days. To right my wrongs")
		player.voice.say("Even if you have to do more wrong to do it?")
		self.voice.say("You wouldn't understand Mikkel, and sadly you won't ever have the time to figure out")
		player.voice.say("Your wrong about that Warren")
		self.voice.say("Your a fool! Any last words?")
		words = input("You: ")
		self.voice.say("Goodbye Mikkel.")
		die.die("Killed by Warren Lightoot.")

	def loose(self, player):
		"""Warren Looses."""

		terminal.clear()

		player.voice.say("Give up Warren, you are defeated!")
		self.voice.say("You'll have to kill me Mikkel! I will never surrender!")
		player.voice.say("It must be done Warren, I can use that thing to destroy the gate forever, to protect our home forever, we must protect the mortal realm, it was our oath!")
		self.voice.say("Destroying the gate will trap us here forever! I have been here far too long, I cannnot live another day!")
		player.voice.say("I too fear remaining in this place, but it must be done!")
		self.voice.say("Kill me then.")
		player.voice.say("I don't want to kill you...")
		self.voice.say("DO IT! You Coward! Kill me! I will not live another day down here, do it or I'll kill myself!")
		player.voice.say("I miss my family as well Warren, you were not the only one who lost loved ones.")
		self.voice.say("Not the same way I did. If you were in my place you would use that stone to bring them back, you would do what I have done!")
		player.voice.say("I want to Warren, I want to bring them back, but I know I cannot. I must destroy the gate, it is what they would want us to do")
		self.voice.say("I just want to see them once more Mikkel! To speak to my son, hug my wife, just for one more day...")
		player.voice.say("I'm sorry Warren, it must be done. We can find another way out, together")
		self.voice.say("There is no way out except the gate, destroying it will leave us here forever!")
		player.voice.say("There is always another way out")
		self.voice.say("If there is a way out, there is a way in! Listen to me Mikkel. Destroying that gate, using a spell, those things do nothing! They only delay the inevitable. Some things were just meant to be. Death, life, this place and our home will always exist. The things that do not exist forever are our loved ones. My Wife. My Son. Ferric's family, Coyote's brother, Williams sister, Sharie. All of them are the things that pass away. Bring them back, even if just for a day. It's a better use then delaying the destruction of our mortal realm a few more short years. You can't change the future Mikkel, whatever you do death will just find another way to escape. What you can change is the past! You can bring them back, all of them!")
		player.voice.say(". . .")

		print("[1] Warren is right. Bring them all back")
		print("[2] Destroy the gate. The few must sacrifice for the good of the many")

		choice = util.get_input("-> ", valid=['1', '2'])

		print("The End...")
		print("I hope you had fun playing")

		exit()





warren = Warren()


def fight(player):
	"""Fight between Player and Warren"""

	player_turn = True # player always start, might switch to player_turn = random.randint(0, 1)

	valid_nums = [str(i) for i in range(0, 9)]

	buffs = []

	last_hit = None

	green = "\033[32m"
	red = "\033[31m"
	reset = "\033[0m"


	while player.life > 0 and warren.life > 0:
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
			print("\n\n---------- WARREN -----------\n")
			print(warren.get_stats())
			print("\n-----------------------------")

			commands = ['?', 'attack', 'loadout', 'drink', 'magicae', 'run']
			
			full = input("-> ")

			c = full.split()

			command = c[0]

			if command in commands:
				# use try to invalid commands
				if command == '?':
					print("Figure it out loser!")
				
				elif command == 'attack':
					player.attack(warren, buffs, [warren], noloot=True)
					player_turn = False
				
				elif command == 'loadout':
					player.shuffle_loadout()
				
				elif command == 'run':
					warren.voice.say("You fool. You can't run away from this!")
				
				elif command == 'drink':
					potion = " ".join(c[1:]).lower()

					if potion in player.inventory and potion in randomness.valid_potions:
						player.inventory.remove(potion)
						
						if potion == 'potion of energy':
							b = buff.Buff(50, 0, 1, "Potentia Navitas", "+50 on next attack")
							print("Buff Activated: +50 on next attack")
							buffs.append(b)
							player_turn = False
						elif potion == 'healing potion':
							print("You drank the healing potion...")
							player.life = player.max_life
							player_turn = True
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
								player_turn = False
							else:
								print("You do not have enough power to throw that spell")
					else:
						print("Your strange magic words are confusing...")
						print(spell + " is not a spell")
			util.cont()

		if warren.life <= 0:
			warren.loose(player)
		

		while not player_turn:
			player_turn = True
			warren.attack(player, buffs)

		for b in buffs:
			b.lasts -= 1
			if b.lasts <= 0:
				buffs.remove(b)

		if player.life <= 0:
			warren.win(player)
		

	print("Game Over")
