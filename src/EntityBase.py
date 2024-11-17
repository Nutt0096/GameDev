import pygame


class EntityBase():
    def __init__(self, conf):
        self.direction = 'down'
        self.animation_list = conf.animation

        # dims
        self.x = conf.x
        self.y = conf.y
        self.width = conf.width
        self.height = conf.height

        # sprite offset          check
        self.offset_x = conf.offset_x or 0
        self.offset_y = conf.offset_y or 0

        self.walk_speed = conf.walk_speed

        self.health = conf.health

        #invincible
        self.invulnerable = False
        self.invulnerable_duration = 0
        self.invulnerable_timer = 0

        #timer for turning transparency (flash)
        self.flash_timer = 0

        self.is_dead = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.state_machine = None
        self.curr_animation = None


    def CreateAnimations(self):
        pass

    def Damage(self, dmg):
        self.health -= dmg
    
    def ChangeState(self, name):
        self.state_machine.Change(name)

    def ChangeAnimation(self, name):
        self.curr_animation = self.animation_list[name]

    def update(self, dt, events):
        pass

    def ProcessAI(self, params, dt):
        self.state_machine.ProcessAI(params, dt)

    def render(self):
        pass
