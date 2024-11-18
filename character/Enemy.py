class Enemy:
    def __init__(self, Name, HP, DEF, CHA):
        self.Name = Name
        self.HP = HP
        self.DEF = DEF
        self.CHA = CHA
        self.img = None

        # Initialize the enemy's animation
        self.animation = None  # You can use a similar animation setup as in CharacterBase

        #{'name': 'Monster1', 'hp': 25, "DEF": 12, "CHA": 7, 'img': None},

    def update(self, dt):
        # Update enemy animation (similar to how characters are animated)
        pass

    def render(self, screen):
        # Render the enemy on the screen (similar to characters)
        pass
