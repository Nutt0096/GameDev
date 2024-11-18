from character.CharacterBase import Character

class Knight(Character):
    def __init__(self):
        super().__init__(Name="Knight", STR=7, INT=3, CON=10, DEF=8, ACC=6, CHA=4)