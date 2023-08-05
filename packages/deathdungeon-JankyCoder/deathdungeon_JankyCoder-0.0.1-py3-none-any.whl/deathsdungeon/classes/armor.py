import random

class Armor():
    def __init__(self, name, armor):
        """Initiate the Armor"""
        self.name = name
        self.armor = armor

        # Note: Removed Magic and Fire Armor stats
        # becuase they have little bearing on
        # real armor stats. 

        self.tier = int((self.armor*6)/10)

    def stats(self):
        return f"{self.name.upper()} STRENGTH: {str(self.armor)} | TIER: {str(self.tier)}"



armor_class = ['cracked', 'thorgan', "knight's", "orc's", "goblin's", "rusty", "old", "new", "leather", "iron", "chainmail", "scale", "boiled leather", "mail", "plated mail", "plate"]


def generate_armor():
    """Generate a random set of armor"""

    armor = Armor(
        name=random.choice(armor_class) + " armor",
        armor = random.randint(1, 10),
    )

    return armor


def ghoul_armor():
    """Returns a ghouls armor. Can only be looted and not found"""

    armor = Armor(
        name="ghoul's purge",
        armor=random.randint(5, 10),
    )

    return armor


def armor_from_dict(dict):
    """Builds Armor from Dict"""
    armor = Armor(
        name = dict['name'],
        armor = dict['armor']
    )
    return armor

def armors_from_dict(list):
    """Builds Armor from List of Dict"""

    out = []

    for a in list:
        out.append(armor_from_dict(a))

    return out
