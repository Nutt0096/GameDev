from src.states.BaseState import BaseState
from src.constants import *
from src.Dependencies import *
from character.Fighter import Fighter
from character.Mage import Mage
from character.Archer import Archer
import pygame, sys


class SelectCharacterState(BaseState):
    def __init__(self):
        super(SelectCharacterState, self).__init__()
        self.bg_image = pygame.image.load("./graphics/Entry.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))
        self.curr_character = 1
        self.team_character = []
        self.team_select_show = []
        self.character_select_num = []
        self.curr_num_char = 0
        self.current_stage = 1
        self.coins = 0

        self.fighter = Fighter()
        self.mage = Mage()
        self.archer = Archer()
        
        self.charter_sheet = {
            1: self.fighter,
            2: self.mage,
            3: self.archer
        }

        self.l_arrow_image = sprite_collection["l_arrow"].image
        self.r_arrow_image = sprite_collection["r_arrow"].image

    def Exit(self):
        pass

    def Enter(self, params):
        gSounds['Title_music'].stop()
        gSounds['Select_music'].play(-1)

    def update(self,  dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.curr_character == 1:
                        gSounds['no-select'].play()
                    else:
                        gSounds['select'].play()
                        self.curr_character -= 1
                elif event.key == pygame.K_RIGHT:
                    if self.curr_character == NUM_CHARACTER:
                        gSounds['no-select'].play()
                    else:
                        self.curr_character += 1
                        gSounds['select'].play()

                if event.key == pygame.K_ESCAPE:
                    gSounds['confirm'].play()
                    g_state_manager.Change('start', None)

                if event.key == pygame.K_RETURN:
                    gSounds['confirm'].play()

                    if self.curr_character not in self.character_select_num:
                        self.character_select_num.append(self.curr_character)
                        self.team_select_show.append(self.charter_sheet.get(self.curr_character).Name)
                        self.team_character.append(self.charter_sheet.get(self.curr_character))
                        self.curr_num_char += 1

                        if self.curr_num_char == NUM_CHARACTER:
                            g_state_manager.Change('stage', {
                                'level': self.current_stage,
                                'team': self.team_character,
                                'stages': [False, False, False, False, False],
                                'coins': self.coins
                            })

                    elif self.curr_character in self.character_select_num:
                        for i in range(len(self.character_select_num)):
                            if self.character_select_num[i] == self.curr_character:
                                print("print",self.character_select_num[i])
                                self.character_select_num.pop(i)
                                self.team_select_show.pop(i)
                                self.team_character.pop(i)
                                self.curr_num_char -= 1
                                break

    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))

        t_instruct = gFonts['M_medium'].render("Select your Character (left right)", False, (255, 255, 255))
        rect = t_instruct.get_rect(center=(WIDTH / 2, HEIGHT / 4))
        screen.blit(t_instruct, rect)

        t_enter = gFonts['M_small'].render("Press Enter to Select", False, (255, 255, 255))
        rect = t_enter.get_rect(center=(WIDTH / 2, HEIGHT / 3))
        screen.blit(t_enter, rect)

        t_number = gFonts['M_small'].render(f"Number of chosen: {self.curr_num_char}", False, (255, 255, 255))
        rect = t_enter.get_rect(topright=(WIDTH - 50, 20))
        screen.blit(t_number, rect)

        # Display character chosen and status
        t_team = gFonts['M_small'].render(f"Character chosen: {', '.join(map(str, self.team_select_show))}", False, (255, 255, 255))
        rect = t_team.get_rect(topright=(WIDTH - 50, 50))
        screen.blit(t_team, rect)

        current_char = self.charter_sheet[self.curr_character]
        stat_lines = [
            f"STR: {current_char.STR}  INT: {current_char.INT}  CON: {current_char.CON}",
            f"DEF: {current_char.DEF}  ACC: {current_char.ACC}  CHA: {current_char.CHA}"
        ]

        t_Name = gFonts['M_medium'].render(f"{current_char.Name}", False, (255, 255, 255))
        rect = t_Name.get_rect(center=(WIDTH / 2, HEIGHT / 3+50))
        screen.blit(t_Name, rect)

        y_position = HEIGHT / 3 + 100

        for line in stat_lines:
            t_stat = gFonts['M_small'].render(line, False, (255, 255, 255))
            rect = t_stat.get_rect(center=(WIDTH / 2, y_position))
            screen.blit(t_stat, rect)
            y_position += 30


        if self.curr_character == 1:
            self.l_arrow_image.set_alpha(128)

        screen.blit(self.l_arrow_image, (WIDTH/4-72, HEIGHT - HEIGHT/3))
        self.l_arrow_image.set_alpha(255)

        if self.curr_character == NUM_CHARACTER:
            self.r_arrow_image.set_alpha(128)
        
        screen.blit(self.r_arrow_image, (WIDTH - WIDTH/4, HEIGHT - HEIGHT/3))
        self.r_arrow_image.set_alpha(255)

        character_img = character_image_list[self.curr_character-1]
        rect = character_img.get_rect(midtop=(WIDTH/2-10, HEIGHT - HEIGHT / 3))
        screen.blit(character_img,rect)