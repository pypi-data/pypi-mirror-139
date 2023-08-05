import random

class Weapon():
    def __init__(self, name, damage, sharpness, weight):
        """Initiate the Weapon"""
        self.name = name
        self.damage = damage
        self.sharpness = sharpness
        self.weight = weight

        self.tier = int(((self.damage+self.sharpness+self.weight)*2)/10)


    def stats(self):
        return f"{self.name.upper()} DMG: {str(self.damage)} | SHRP: {str(self.sharpness)} | WGHT: {str(self.weight)} | TIER: {str(self.tier)}"



weapon_class = ['cracked', 'thorgan', "knight's", "orc's", "goblin's", "rusty", "old", "new"]

weapon_type = ["sword", "spear", "club", "mace", "morning star", "broad sword", "longsword", "dagger", "dirk", "shortsword", "sabre", "katana", "battle axe", "flail", "quarter staff", "war hammer", "pike", "poleaxe"]

def generate_weapon():
    """Generate a random weapon"""

    weapon = Weapon(
        name=random.choice(weapon_class) + " " + random.choice(weapon_type),
        damage = random.randint(1, 10),
        sharpness = random.randint(1, 10),
        weight = random.randint(1, 10)
    )

    return weapon


def ghoul_weapon():
    """Returns a Ghoul's Voulge. This weapon can only be looted from a ghoul and not found"""
    weapon = Weapon(
        name="ghoul's voulge",
        damage = random.randint(8,10),
        sharpness = random.randint(8,10),
        weight = random.randint(8,10),
    )
    
    return weapon


def weapon_from_dict(dict):
    """Builds a weapon from Dict"""
    weapon = Weapon(
        name = dict['name'],
        damage = dict['damage'],
        sharpness = dict['sharpness'],
        weight = dict['weight'],
    )

    return weapon


def weapons_from_dict(_list):
    """Builds a list of weapons from list of Dicts"""

    out = []


    for w in _list:
        out.append(weapon_from_dict(w))

    return out