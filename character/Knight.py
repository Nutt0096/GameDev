from character.CharacterBase import Character

class Knight(Character):
    def __init__(self):
        super().__init__(Name="knight", STR=7, INT=3, CON=10, DEF=8, ACC=6, CHA=4)
        self.Weapons.append(
            {
                    "name": "Sword",
                    "ACC": 2,
                    "damage_dice": 8
            }
        )
        self.load_animations(self.Name)

        # Load knight-specific animations (idle, attack, etc.)

    
    def update(self, dt):
        # Example: Switch to attack animation when attacking
        if self.is_attacking():
            # self.current_animation = self.attack_animation
            pass
        else:
            self.current_animation = self.idle_animation
        
        # Update the current animation frame
        super().update(dt)  # Call the base class update to handle the animation

    def is_attacking(self):
        """ For demo purposes, let's say the knight is always attacking. """
        return True  # Replace with actual attack condition