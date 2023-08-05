

class Buff():
    def __init__(self, dmg, enemy_dmg,lasts, reason, des, enemy=False):
        """Initiate a Buff"""
        self.dmg = dmg
        self.enemy_dmg = enemy_dmg
        self.lasts = lasts+1 # to account for buff being removed after calling
        self.reason = reason
        self.des = des
        self.enemy = enemy