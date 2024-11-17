import pygame
from src.Util import SpriteManager
from src.StateMachine import StateMachine

g_state_manager = StateMachine()

sprite_collection = SpriteManager().spriteCollection

character_image_list = [sprite_collection["knight_idle"].image,
                        sprite_collection["wizard_idle"].image,
                        sprite_collection["archer_idle"].image
                        ]

gFonts = {
    'M_small': pygame.font.Font('./fonts/MedievalSharp-Regular.ttf', 24),
    'M_medium': pygame.font.Font('./fonts/MedievalSharp-Regular.ttf', 48),
    'M_large': pygame.font.Font('./fonts/MedievalSharp-Regular.ttf', 96)
}

gSounds = {
    'Title_music': pygame.mixer.Sound('sounds/xDeviruchi - Title Theme .wav'),
    'Select_music': pygame.mixer.Sound('sounds/xDeviruchi - And The Journey Begins .wav'),
    'Shop_music': pygame.mixer.Sound('sounds/xDeviruchi - Take some rest and eat some food!.wav'),
    'Stage5_music': pygame.mixer.Sound('sounds/xDeviruchi - Prepare for Battle! .wav'),
    'Stage3_music': pygame.mixer.Sound('sounds/xDeviruchi - Exploring the Unknown.wav'),
    'Stage1_music': pygame.mixer.Sound('sounds/xDeviruchi - Mysterious Dungeon.wav'),
    'select': pygame.mixer.Sound('sounds/select.wav'),
    'no-select': pygame.mixer.Sound('sounds/no-select.wav'),
    'confirm': pygame.mixer.Sound('sounds/confirm.wav'),
    
}
