from classes import weapon, armor
import random
from code import util, terminal
from battle import buff, enemy

#############
#  GOBLINS  #
#############

def generate_goblin():
    name = "goblin"
    life = random.randint(10, 20)
    magic = 0
    can_magic = False
    w = weapon.generate_weapon()
    a = armor.generate_armor()

    silver = random.randint(1, 5)
    gold = 0
    diamonds = 0


    can_heal = False

    b = buff.Buff(0, 10, 1, "Cobalorum Unify", "Goblins Do +10 Damage")

    goblin = enemy.Enemy(name, life, magic, w, a, can_magic, can_heal, silver, gold, diamonds, b)

    return goblin

##########
#  ORCS  #
##########

def generate_orc():
    name = "orc"
    life = random.randint(50, 100)
    magic = 0
    can_magic = False
    w = weapon.generate_weapon()
    a = armor.generate_armor()

    silver = random.randint(10, 20)
    gold = random.randint(5, 8)
    diamonds = 0

    can_heal = False

    b = buff.Buff(-10, 0, 3, "debilitatem fluxus", "-10 Damage on Your Attacks")

    orc = enemy.Enemy(name, life, magic, w, a, can_magic, can_heal, silver, gold, diamonds, b)

    return orc

##############
#  THORGANS  #
##############

def generate_thorgan():
    name = "thorgan"
    life = random.randint(150, 500)
    magic = 0
    can_magic = False
    w = weapon.generate_weapon()
    a = armor.generate_armor()

    silver = random.randint(50, 90)
    gold = random.randint(10, 30)
    diamonds = random.randint(1, 6)

    can_heal = False

    b = None

    thorgan = enemy.Enemy(name, life, magic, w, a, can_magic, can_heal, silver, gold, diamonds, b)

    return thorgan

############
#  VITTRA  #
############

# note: only invisible enemy

def generate_vittra():
    name = "vittra"
    life = random.randint(5, 10)
    magic = 30
    can_magic = True
    w = weapon.generate_weapon()
    a = armor.generate_armor()

    silver = random.randint(10, 20)
    gold = random.randint(5, 10)
    diamonds = random.randint(0, 1)

    can_heal = True

    b = None

    vittra = enemy.Enemy(name, life, magic, w, a, can_magic, can_heal, silver, gold, diamonds, b)

    return vittra


#############
#  WYBBERS  #
#############

def generate_wybber():
    name = "wybber"
    life = random.randint(35, 60)
    magic = 15
    can_magic = True
    w = weapon.generate_weapon()
    a = armor.generate_armor()

    silver = 0
    gold = 0
    diamonds = random.randint(3, 5)

    can_heal = True

    b = buff.Buff(0, 100, 1, "Exponentia Instantis Mortis", "+100 Damage")

    wybber = enemy.Enemy(name, life, magic, w, a, can_magic, can_heal, silver, gold, diamonds, b)

    return wybber


############
#  GHOULS  #
############

def generate_ghoul():
    name = "ghoul"
    life = 100
    magic = 0
    can_magic = False
    w = weapon.ghoul_weapon()
    a = armor.ghoul_armor()

    silver = 0
    gold = 0
    diamonds = 0

    can_heal = False

    b = buff.Buff(-30, 0, 1, "Gelida Cogitationes", "-30 Damage on Your Attacks")

    ghoul = enemy.Enemy(name, life, magic, w, a, can_magic, can_heal, silver, gold, diamonds, b)

    return ghoul



def generate_monsters():
    i = random.randint(1, 20)
    count = random.randint(1, 3)

    monsters = []

    if i in range(1, 5):
        for i in range(count):
            monsters.append(generate_goblin())
    elif i in range(6, 10):
        for i in range(count):
            monsters.append(generate_orc())
    elif i in range(11, 13):
        for i in range(count):
            monsters.append(generate_vittra())
    elif i == 14:
        monsters.append(generate_thorgan())
    elif i in range(15, 18):
        monsters.append(generate_wybber())
    elif i == 19:
        monsters.append(generate_ghoul())
    else:
        for i in range(count):
            monsters.append(generate_ghoul())
    
    return monsters
        
        
