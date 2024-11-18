from character.CharacterBase import Character

class Mage(Character):
    def __init__(self):
        super().__init__(Name="Mage", STR=3, INT=8, CON=5, DEF=4, ACC=6, CHA=7)