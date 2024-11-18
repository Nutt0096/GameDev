from character.CharacterBase import Character

class Fighter(Character):
    def __init__(self):
        super().__init__(Name="Fighter", STR=9, INT=3, CON=7, DEF=5, ACC=6, CHA=4)

