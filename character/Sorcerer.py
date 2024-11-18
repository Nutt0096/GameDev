from character.CharacterBase import Character

class Sorcerer(Character):
    def __init__(self):
        super().__init__(Name="sorcerer", STR=3, INT=9, CON=4, DEF=4, ACC=6, CHA=8)
        self.Weapons.append(
            {
                "name": "Dagger",
                "ACC": 4,
                "damage_dice": 4
            }
        )

        self.Spells = [
            {
                "name": "Magic Missile",
                "ACC": 4,
                "damage_dice": 6,
                "mana_cost": 5,
                "effect": "force_damage"
            },
            {
                "name": "Charm",
                "ACC": 3,
                "damage_dice": 0,
                "mana_cost": 6,
                "effect": "charm"
            },
            {
                "name": "Shield",
                "ACC": 0,
                "damage_dice": 0,
                "mana_cost": 7,
                "effect": "defense_boost"
            }
        ]

        self.load_animations(self.Name)

    def update(self, dt):
        # Example: Switch to casting spell animation when the mage is casting a spell
        if self.is_casting_spell():
            # self.current_animation = self.attack_animation
            pass
        else:
            self.current_animation = self.idle_animation
        
        super().update(dt)

    def is_casting_spell(self):
        """ For demo purposes, let's say the mage is always casting a spell. """
        return True  # Replace with actual spell-casting condition

