class Character:
    def __init__(self, Name, STR , INT , CON , DEF , ACC , CHA ):
        self.Name = Name
        self.STR = STR  # Physical damage
        self.INT = INT  # Magical damage
        self.CON = CON  # Health pool
        self.DEF = DEF  # Dodge chance
        self.ACC = ACC  # Hit chance and critical chance
        self.CHA = CHA  # Resistance to debuffs, chance to inflict buffs

    def show_stats(self):
        print(f"{self.name}'s Stats:")
        print(f"STR: {self.STR}, INT: {self.INT}, CON: {self.CON}")
        print(f"DEF: {self.DEF}, ACC: {self.ACC}, CHA: {self.CHA}")
