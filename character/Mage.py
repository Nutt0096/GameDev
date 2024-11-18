from character.CharacterBase import Character

class Mage(Character):
    def __init__(self):
        super().__init__(Name="mage", STR=3, INT=8, CON=5, DEF=4, ACC=6, CHA=7)
        self.Weapons.append(
            {
                "name": "Dagger",
                "ACC": 4,
                "damage_dice": 4
            }
        )
        self.Spells = [
            {
                "name": "Fireball",
                "ACC": 2,
                "damage_dice": 10,
                "mana_cost": 10,
                "effect": None
            },
            {
                "name": "Lightning Bolt",
                "ACC": 5,
                "damage_dice": 6,
                "mana_cost": 8,
                "effect": None
            },
            {
                "name": "Healing",
                "ACC": 0,
                "damage_dice": 10,
                "mana_cost": 15,
                "effect": "heal"
            }
        ]

        self.load_animations(self.Name)

    def update(self, dt):
        self.current_animation = self.idle_animation
        super().update(dt)