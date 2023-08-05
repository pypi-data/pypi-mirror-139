import random

from people import maximus


screen_size = 10


def build_display_map(dungeon, x, y):
    """Cuts the full map into a size based on the users location"""
    # TODO: Fix this crap
    display_map = []
    for i in range(-screen_size, screen_size):
        try:
            display_map.append(dungeon[y+i])
        except:
            display_map.append(["."]*screen_size)
    final = []
    for row in display_map:
        new_row = []
        for i in range(-screen_size+x, screen_size+1+x):
            try:
                new_row.append(row[i])
            except:
                new_row.append(".")
                
        final.append(new_row)
    return final
    
    

def display(dungeon, x, y, stats=[]):
    print("\033[H",end="")
    dungeon[y][x] = 'p'
    _map = build_display_map(dungeon, x, y)
    print("---"*21+"--")
    for stat in stats:
        count = int((60-len(stat))/2)
        _str = "|  " + (" "*count) + stat + (" "*count)
        if len(_str) == 62:
            _str += "  |"
        else:
            _str += " |"

        print(_str)

        
    print("---"*21+"--")
    for row in _map:
        r = "|"
        for cell in row:
            if cell == 't':
                r += " []"
            elif cell == '*':
                r += "\033[34m * \033[0m"
            else:
                r += " "+cell+" "
        print(r+"|")
    print("---"*21+"--")


class action():
    def __init__(self, dungeon, x, y):
        self.dungeon = dungeon
        self.x = x
        self.y = y
        self.valid = False
        self.treasure = False
        self.portal = False
        self.character = False
        self.enemy = False
        self.shard = False


        self.check_position()

    def check_position(self):
        """Check the position of the character"""
        item = self.dungeon[self.y][self.x]

        if item in ['#', '@']:
            self.valid = False
        else:
            self.valid = True

        if item == 't':
            self.treasure = True

        if item == '@':
            self.portal = True

        if item in ['M', 'G', 'L', 'R', 'T', 'W']:
            self.valid = False
            self.character = item

        if item == 'e':
            self.enemy = True
            self.valid = False
        
        if item == '*':
            self.shard = True
        

def getSpawn(dungeon):
    valid = False
    count = 0
    spawny, spawnx = 0,0
    while not valid:
        try:
            if ' ' in dungeon[count]:
                spawny = count
                spawnx = random.randint(0, len(dungeon))
                if dungeon[spawny][spawnx] == ' ':
                    valid = True
            else:
                count += 1
        except:
            pass
    return spawny, spawnx


def check_pos(y, x, dungeon):
    """Checks if the position is valid for Character Placement"""

    # Checks if the character is in a legal spot
    # to keep them from blocking the way for the player
    # checks if the spot above, below, to the right and left
    # of the spawn being tested are clear. 
    # While this will not completely keep the character
    # from blocking the players movement. it should
    # make it a lot less likely to accur. Hopefull...

    pos = dungeon[y][x]
    if pos != ' ':
        return False
    else:
        spots = []

        #check position above
        spots.append(dungeon[y+1][x])

        # check position below
        spots.append(dungeon[y-1][x])

        # check position right
        spots.append(dungeon[y][x+1])

        # check position left
        spots.append(dungeon[y][x-1])

        for position in spots:
            if position != ' ':
                return False
    return True

def add_character(dungeon, character):
    """Add a character in random location"""
    # Note. Check Character to surroundings to make sure
    # they are not blocking the path of the character
    attempts = 0
    while 1:
        y = random.randint(0, 98)
        if ' ' in dungeon[y]:
            while 2: # never seen this before have you?
                attempts += 1
                x = random.randint(0, 98)
                if check_pos(y, x, dungeon):
                    dungeon[y][x] = character.symbol
                    return
                if attempts == 1000:
                    # Find First Open (And Valid) Spot
                    while True:
                        print("Switching to Linear Placement")
                        y = 0
                        if ' ' in dungeon[y]:
                            while True:
                                x = 0
                                if check_pos(y, x, dungeon):
                                    dungeon[y][x] = character.symbol
                                    return
                                else:
                                    x += 1
                        else:
                            y += 1

                        if y <= 98:
                            util.log("Placing Character " + str(character.symbol) + " failed.")

def add_enemy(dungeon):
    """Add an enemy in a random location"""
    valid = False
    while True:
        y = random.randint(0, 98)
        if ' ' in dungeon[y]:
            while True:
                if ' ' in dungeon[y]:
                    x = random.randint(0, 98)
                    if dungeon[y][x] == ' ':
                        dungeon[y][x] = 'e'
                        return


def add_shard(dungeon):
    """Adds a shard of the heart of Magic"""
    while True:
        y = random.randint(0, 98)
        if ' ' in dungeon[y]:
            while True:
                x = random.randint(0, 98)
                if dungeon[y][x] == ' ':
                    dungeon[y][x] = '*'
                    return


def add_loot(dungeon, min_loot, max_loot):
    loot_count = random.randint(min_loot, max_loot)

    for i in range(loot_count):
        while True:
            y = random.randint(0, 98)
            if ' ' in dungeon[y]:
                while True:
                    x = random.randint(0, 98)
                    if dungeon[y][x] == ' ':
                        dungeon[y][x] = 't'
                        break
                break


def add_exit(dungeon):
    valid = False
    while True:
        y = random.randint(0, 99)
        if ' ' in dungeon[y]:
            while True:
                x = random.randint(0, 99)
                if dungeon[y][x] == ' ':
                    dungeon[y][x] = '@'
                    return
            
        