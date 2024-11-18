from character.CharacterBase import Character

class Archer(Character):
    def __init__(self):
        super().__init__(Name="Archer", STR=6, INT=4, CON=6, DEF=6, ACC=8, CHA=5)