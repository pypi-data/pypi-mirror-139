from generators import dungeon
from code import game, map, terminal, util
from classes import player
from save_game import menu, save
import time, random, cursor

from battle import bossfight

cursor.hide()

util.clear_log()


##################
#  BUILD PEOPLE  #
##################

from people import maximus, grarlan, rohan, laurence, trekker, warren

maximus = maximus.Maximus()
grarlan = grarlan.Grarlan()
rohan = rohan.Rohan()
laurence = laurence.Laurence()
trekker = trekker.Trekker()
warren = warren.Warren()


characters = [maximus, grarlan, rohan, laurence, trekker, warren]






def build_dungeon(p):
    """Generates a Random Dungeon"""
    print("Loading Dungeon....")


    util.log("Initating Dungeon")

    gen = dungeon.Generator(
        width=100,
        height=100,
        max_rooms=15,
        min_room_xy=5,
        max_room_xy=15,
        rooms_overlap=False,
        random_connections=1,
        random_spurs=1
    )

    util.log("Generating Level")
    gen.gen_level()

    util.log("Generating Tiles")
    d = gen.gen_tiles_level()

    util.log("Adding Loot")
    map.add_loot(
        d,
        min_loot = 4,
        max_loot = 15,
    )

    util.log("Adding Exit Portal")
    map.add_exit(
        d
    )


    util.log("Adding Characters")
    
    if random.randint(1, 10) == 1:
        util.log("Placing M")
        map.add_character(d, maximus)

    if random.randint(1, 10) == 1:
        util.log("Placing G")
        map.add_character(d, grarlan)

    if random.randint(1, 10) == 1:
        util.log('Placing R')
        map.add_character(d, rohan)

    if random.randint(1, 10) == 1:
        util.log("Placing L")
        map.add_character(d, laurence)

    if random.randint(1, 10) == 1 and not p.trekker_alive:
        map.add_character(d, warren)

    if random.randint(1, 3) == 1 and p.trekker_alive:
        util.log("Placing T")
        map.add_character(d, trekker)

    util.log("Adding Enemies")

    for i in range(random.randint(3, 8)):
        map.add_enemy(d)
    
    util.log("Adding Shards")

    if random.randint(1, 4) == 1:
        map.add_shard(d)


    util.log("Dungeon Created")

    terminal.clear()
    
    return d




###############
#  INIT GAME  #
###############

save.initiate()

game_data = menu.menu()


if not game_data:
    player = player.Player()
    d = build_dungeon(player)

    g = game.Game(
        dungeon = d,
        player = player,
        characters = characters,
    )

elif game_data:
    g = game.Game(
        dungeon = game_data[1],
        player = game_data[0],
        characters = characters,
        posx = game_data[2],
        posy = game_data[3]
    )

else:
    print("Error! Game Both Does not exist and Exists")
    exit()




####################
#  MAIN GAME LOOP  #
####################


while True:
    go_next = g.play()
    if not go_next:
        print("Hope you had a fun time playing!")
        exit()
    else:
        g.player.rooms_played += 1
        if g.player.warren_talked_to:
            if g.player.rooms_played >= 20:
                # start checking for win room
                if random.randint(1, 10) == 1:
                    print("You won!") # TODO: Replace with Win Room/Boss Fight
                    exit()
        print("...")
        time.sleep(1) # just for effect
        terminal.clear()
        d = build_dungeon(g.player)
        g = game.Game(
            dungeon=d,
            player=g.player,
            characters=characters,
        )
        