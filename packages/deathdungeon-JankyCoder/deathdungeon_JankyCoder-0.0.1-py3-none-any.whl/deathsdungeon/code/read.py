from code import terminal, util





def pick_book(player):
	terminal.clear()

	print("Choose Something to Read: ")

	v = ['1', 'exit']

	print("[1] Pack of Letters")

	if "Ferric's Journal" in player.inventory:
		print("[2] Ferric's Journal")
		v.append('2')

	i = util.get_input("-> ", valid=v)

	if i == 'exit':
		return

	if i == '1':
		print("The letters are not marked and old... ")
		print("\n[1] Letter 1")
		print("[2] Letter 2")
		print("[3] Letter 3")
		print("[4] Letter 4")
		print('[5] Back')

		i = util.get_input("-> ", valid=['1', '2', '3', '4', '5'])

		if i == '5':
			pick_book(player)

		else:
			read('story/letters/warren'+i+'.txt')

	elif i == '2':
		read('story/books/ferrics_journal.txt', parts=True)


def read(item, parts=False):
	with open(item, 'r') as file:
		data = file.read()

	if parts:
		content = data.split("PART")
	else:
		content = data.split("\n")


	for i in content:
		terminal.slow_print(i, .001)
		input()

	util.cont()

	terminal.clear()



