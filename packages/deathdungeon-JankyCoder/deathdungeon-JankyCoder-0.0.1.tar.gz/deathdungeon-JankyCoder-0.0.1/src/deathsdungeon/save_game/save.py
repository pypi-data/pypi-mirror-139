import json
from classes import weapon, armor, player, player_from_dict
import os


def initiate():
	if not os.path.isfile('save.txt'):
		with open('save.txt', 'x') as file:
			pass
	if not os.path.isfile('save_map.txt'):
		with open('save_map.txt', 'x') as file:
			pass



def class_to_json(object):
	"""Converts a 'nested' class to 'nested' JSON"""

	result = json.loads(json.dumps(object, default=lambda o: o.__dict__))

	return result



def get_game_data():
	"""Converts 'nested' JSON to 'nested' Game Data and Player Object"""

	with open('save.txt', 'r') as file:
		JSON = json.loads(file.read())

	player = player_from_dict.PlayerFromDict(JSON['player'])
	game_map = map_from_file(JSON['game_map'])
	posx = JSON['posx']
	posy = JSON['posy']

	return [player, game_map, posx, posy]




def save_player_data(player, _map, posx, posy):
	"""Writes Player Data to File"""

	JSON = {
		'player' : class_to_json(player),
		'game_map' : 'save_map.txt',
		'posx' : posx,
		'posy' : posy,
	}

	with open('save_map.txt', 'w') as file:
		file.write(map_to_string(_map))

	with open('save.txt', 'w') as file:
		file.write(json.dumps(JSON))




def map_to_string(_map):
	"""Converts a Nested List map to String"""
	string = ""

	for i in _map:
		row = ""
		for j in i:
			row += j
		row += '\n'
		string += row

	return string


def map_from_file(file):
	"""Converts a string to a nested list"""
	with open(file, 'r') as file:
		data = file.read()

	_map = []

	rows = data.split("\n")

	for row in rows:
		r = [char for char in row]
		_map.append(r)

	return _map

