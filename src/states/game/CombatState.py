from src.states.BaseState import BaseState
from src.combat_utils import *
from character import *
from monster.Monster import MONSTER_POOLS
import pygame, sys, random

from src.constants import *
from src.resources import *

# CombatState Class
class CombatState(BaseState):
    def __init__(self):
        super().__init__()
        self.bg_image = pygame.image.load("./graphics/Dungeon.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))

        # Colors
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.PANEL_COLOR = (64, 32, 64)

        # <--- DUMMY DATA

        # Character and monster setup
        self.team_characters = []
        self.selected_weapon = None 
        self.selected_spell = None
        self.spell_positions = []
        self.selected_character = 0
        self.selected_monster = 0
        self.characters = [
        {
            "name": "Hero1",
            "hp": 100,
            "mp": 50,
            "ACC": 5,
            "STR": 8,
            "INT": 6,
            "DEF": 10,
            "CHA": 9,
            'img': None,
            "weapons": [
                {
                    "name": "Sword",
                    "ACC": 2,
                    "damage_dice": 8
                }
            ],
            "spells": []
        },
        {
            "name": "Hero2",
            "hp": 90,
            "mp": 60,
            "ACC": 6,
            "STR": 6,
            "INT": 4,
            "DEF": 12,
            "CHA": 8,
            'img': None,
            "weapons": [
                {
                    "name": "Axe",
                    "ACC": 1,
                    "damage_dice": 10
                }
            ],
            "spells": []
        },
        {
            "name": "Hero3",
            "hp": 60,
            "mp": 80,
            "ACC": 8,
            "STR": 4,
            "INT": 10,
            "DEF": 9,
            "CHA": 14,
            'img': None,
            "weapons": [
                {
                    "name": "Dagger",
                    "ACC": 4,
                    "damage_dice": 4
                }
            ],
            "spells": [
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
        }
    ]

        self.monsters = []   
        # self.item_inventory = [{'name': 'Item1', 'img': None}]
        # self.weapon_inventory = [{'name': 'Weapon1', 'img': None}]
        # self.spell_inventory = [{'name': 'Spell1', 'img': None}]
        # self.attack_style = [{'name': 'Attack1', 'img': None}]
        self.bought_items = []
        self.bought_weapons = []
        self.bought_spells = []
        self.bought_armors = []

        # <--- DUMMY DATA

        self.right_panel_show = 0 # initial as show item (0=item, 1=item_selected, 2=weapon_selected, 3=spell_selected, 4=attack_selected, 5=escape_selected)

        # Positioning
        self.character_positions = [(WIDTH/4, 150), (WIDTH/4, 250), (WIDTH/4, 350)]
        self.monster_positions = [(3*WIDTH/4, 150), (3*WIDTH/4, 250), (3*WIDTH/4, 350)]

        # Turns
        self.player_turn = True
        self.turn_order = self.characters + self.monsters
        self.current_turn_index = 0
        self.waiting_for_player_action = True

    def handle_turn(self):
        """Handle the current entity's turn."""
        if self.waiting_for_player_action and self.player_turn:
            return  # Only wait for player input during the player's turn

        current_entity = self.turn_order[self.current_turn_index]
        print(f"Turn Index: {self.current_turn_index}, Entity: {current_entity['name']}")

        if not self.monsters:
            print("No monsters left!")
            return

        if self.player_turn:
            # Handle player's turn
            if current_entity in self.characters:
                self.selected_character = self.characters.index(current_entity)
                target = self.monsters[self.selected_monster]

                print(f"{current_entity['name']}'s turn!")
                if self.right_panel_show == 1:  # Weapon panel selected
                    if self.selected_weapon is None:
                        print(f"{current_entity['name']} has no weapon selected!")
                        self.waiting_for_player_action = True
                        return

                    weapon = current_entity["weapons"][self.selected_weapon]
                    if self.monsters:  # Check if there are still monsters to target
                        target = self.monsters[self.selected_monster]
                        result = resolve_attack(current_entity, target, weapon)
                        print(result)

                        if target["hp"] <= 0:
                            print(f"{target['name']} is defeated!")
                            self.monsters.remove(target)
                            if not self.monsters:
                                self.selected_monster = 0  # Reset if no monsters remain
                            else:
                                self.selected_monster = min(self.selected_monster, len(self.monsters) - 1)

                elif self.right_panel_show == 2:  # Spell selected
                    if self.selected_spell is None:
                        print(f"No spell selected!")
                        self.waiting_for_player_action = True
                        return

                    spell = current_entity["spells"][self.selected_spell]
                    if self.monsters:  # Check if there are still monsters to target
                        target = self.monsters[self.selected_monster]
                        result = resolve_spell(current_entity, target, spell, self.monsters, self.selected_monster)
                        print(result)

                        if target["hp"] <= 0:  # Adjust selection after a monster is defeated
                            print(f"{target['name']} is defeated!")
                            self.monsters.remove(target)
                            if not self.monsters:
                                self.selected_monster = 0  # Reset if no monsters remain
                            else:
                                self.selected_monster = min(self.selected_monster, len(self.monsters) - 1)

            if self.current_turn_index < len(self.characters):  # Ensure it's a character's turn
                self.selected_character = self.current_turn_index
                print(f"Pointer moved to character: {self.characters[self.selected_character]['name']}")

        else:
            # Handle enemy's turn automatically
            if current_entity in self.monsters:
                target = random.choice(self.characters)
                result = resolve_attack_monster(current_entity, target)
                print(result)

                # Remove defeated character if necessary
                if target["hp"] <= 0:
                    self.characters.remove(target)

        self.end_turn()

    def end_turn(self):
        """Advance to the next entity's turn."""
        # Rebuild the turn order dynamically
        self.turn_order = [entity for entity in self.characters if entity["hp"] > 0] + \
                      [entity for entity in self.monsters if entity["hp"] > 0]

        # Skip defeated entities
        while self.turn_order and (
            (self.current_turn_index < len(self.characters) and self.characters[self.current_turn_index]["hp"] <= 0) or
            (self.current_turn_index >= len(self.characters) and 
            self.monsters and 
            self.current_turn_index - len(self.characters) < len(self.monsters) and
            self.monsters[self.current_turn_index - len(self.characters)]["hp"] <= 0)
        ):
            self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)

        # Increment turn index safely
        if self.turn_order:
            self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)

            # Update selected_character for player's turn
            if self.current_turn_index < len(self.characters):  # If it's a player's turn
                self.selected_character = self.current_turn_index
                print(f"Pointer updated to character: {self.characters[self.selected_character]['name']}")
            else:
                self.selected_character = None  # No character selected during monsters' turn
        else:
            self.current_turn_index = 0

        # Check if all enemies have acted
        if not self.player_turn and (not self.monsters or self.current_turn_index < len(self.characters)):
            self.player_turn = True  # Switch back to player's turn
            self.current_turn_index = 0  # Restart player turns

        # If all players have acted, switch to enemies' turn
        if self.player_turn and self.current_turn_index >= len(self.characters):
            self.player_turn = False
            self.current_turn_index = len(self.characters)  # Start enemy turns

        self.waiting_for_player_action = self.player_turn  # Only wait for action during player's turn

        # Check game over conditions
        if not self.monsters:  # If no monsters remain, transition to victory
            print("All monsters defeated! You win!")
            self.stages[self.current_stage - 1] = True
            self.current_stage += 1
            self.coins += 50

            if self.current_stage >= 6:  # set to 6, may change for debugging purpose
                g_state_manager.Change('victory', None)
            else:
                g_state_manager.Change('shop', {
                    'level': self.current_stage,
                    'team': self.characters,
                    'stages': self.stages,
                    'coins': self.coins,
                    'item-list': self.bought_items,
                    'weapon-list': self.bought_weapons,
                    'spell-list': self.bought_spells,
                    'armor-list': self.bought_armors
                })
        elif not self.characters:  # If no characters remain, transition to game over
            print("All characters defeated! Game over.")

    def process_player_action(self, action):
        """Process player inputs."""
        if action == "up":
            self.selected_monster = (self.selected_monster - 1) % len(self.monsters)
        elif action == "down":
            self.selected_monster = (self.selected_monster + 1) % len(self.monsters)
        elif action == "attack":
            self.waiting_for_player_action = False  # Execute the attack on the selected monster

    def load_monsters_for_stage(self, stage):
        """Load monsters for the given stage."""
        if stage in MONSTER_POOLS:
            pool = MONSTER_POOLS[stage]
            num_monsters = min(3, len(pool))
            self.monsters = random.sample(pool, num_monsters)
        else:
            self.monsters = []

    def draw_health_bar(self, screen, x, y, health):
        pygame.draw.rect(screen, self.RED, (x, y, health, 10))

    def draw_mana_bar(self, screen, x, y, mana):
        pygame.draw.rect(screen, self.BLUE, (x, y, mana, 10))

    def display_characters_and_monsters(self, screen, selected_character, selected_monster):
        # Display characters
        for i, character in enumerate(self.characters):
            pos = self.character_positions[i]
            if character['img']:
                screen.blit(character['img'], pos)
            else:
                pygame.draw.circle(screen, self.BLACK, pos, 30)  # Placeholder for character image
            self.draw_health_bar(screen, pos[0] - 40, pos[1] - 50, character['hp'])
            self.draw_mana_bar(screen, pos[0] - 40, pos[1] - 35, character['mp'])
            if i == selected_character:
                pygame.draw.polygon(screen, self.GREEN, [(pos[0], pos[1] - 50), (pos[0] - 10, pos[1] - 60), (pos[0] + 10, pos[1] - 60)])

        # Display monsters
        for i, monster in enumerate(self.monsters):
            pos = self.monster_positions[i]
            if monster['img']:
                screen.blit(monster['img'], pos)
            else:
                pygame.draw.circle(screen, self.BLACK, pos, 30)  # Placeholder for monster image
            self.draw_health_bar(screen, pos[0] - 40, pos[1] - 50, monster['hp'])
            if i == selected_monster:
                pygame.draw.polygon(screen, self.GREEN, [(pos[0], pos[1] - 50), (pos[0] - 10, pos[1] - 60), (pos[0] + 10, pos[1] - 60)])

    def display_action_panel(self, screen, selected_character):
        if selected_character is None:
            return
    
        pygame.draw.rect(screen, self.PANEL_COLOR, (35, HEIGHT/2 + 50, 600, 300)) 
        current_character = self.characters[selected_character]
        char_text = gFonts['M_small'].render(f"{current_character['name']} HP: {current_character['hp']} MP: {current_character['mp']}", True, self.WHITE)
        screen.blit(char_text, (90, 430))

        # Action buttons
        weapon_button = pygame.draw.rect(screen, self.BLACK, (125, 520, 150, 50))
        spell_button = pygame.draw.rect(screen, self.BLACK, (375, 520, 150, 50))
        item_button = pygame.draw.rect(screen, self.BLACK, (125, 600, 150, 50))
        escape_button = pygame.draw.rect(screen, self.BLACK, (375, 600, 150, 50))
        
        screen.blit(gFonts['M_small'].render("WEAPON", True, self.WHITE), (135, 530))
        screen.blit(gFonts['M_small'].render("SPELL", True, self.WHITE), (385, 530))
        screen.blit(gFonts['M_small'].render("ITEM", True, self.WHITE), (135, 610))
        screen.blit(gFonts['M_small'].render("ESCAPE", True, self.WHITE), (385, 610))
        
        return weapon_button, spell_button, item_button, escape_button

    def display_right_panel(self, screen, bought_items):
        if self.right_panel_show == 1:  # Weapon panel
            if 0 <= self.current_turn_index < len(self.characters):  # Validate index
                pygame.draw.rect(screen, self.PANEL_COLOR, (645, HEIGHT / 2 + 50, 600, 300))
                char_text = gFonts['M_small'].render("WEAPONS", True, self.WHITE)
                screen.blit(char_text, (700, 430))

                # Show weapons for the current character
                current_character = self.characters[self.current_turn_index]
                for i, weapon in enumerate(current_character.get("weapons", [])):
                    color = self.GREEN if i == self.selected_weapon else self.WHITE
                    weapon_text = gFonts['M_small'].render(f"{weapon['name']} ACC: {weapon['ACC']} D: d{weapon['damage_dice']}", True, color)
                    screen.blit(weapon_text, (700, 470 + (i * 40)))

        elif self.right_panel_show == 2:  # Spell panel
            if self.player_turn and 0 <= self.current_turn_index < len(self.characters):
                pygame.draw.rect(screen, self.PANEL_COLOR, (645, HEIGHT / 2 + 50, 600, 300))
                char_text = gFonts['M_small'].render("SPELLS", True, self.WHITE)
                screen.blit(char_text, (700, 430))

                current_character = self.characters[self.current_turn_index]
                for i, spell in enumerate(current_character.get("spells", [])):
                    # Highlight selected spell
                    color = self.GREEN if i == self.selected_spell else self.WHITE
                    spell_text = gFonts['M_small'].render(f"{spell['name']} ACC: {spell['ACC']} D: d{spell['damage_dice']} MP: {spell['mana_cost']}", True, color)
                    screen.blit(spell_text, (700, 470 + (i * 40)))

                    if not hasattr(self, "spell_positions"):
                        self.spell_positions = []
                    if i >= len(self.spell_positions):
                        self.spell_positions.append(spell_text)

        elif self.right_panel_show == 3:  # Default to showing items
            pygame.draw.rect(screen, self.PANEL_COLOR, (645, HEIGHT / 2 + 50, 600, 300))
            char_text = gFonts['M_small'].render("ITEMS", True, self.WHITE)
            screen.blit(char_text, (700, 430))

            for i, item in enumerate(bought_items):
                item_text = gFonts['M_small'].render(item['name'], True, self.WHITE)
                screen.blit(item_text, (700, 470 + (i * 40)))

        elif self.right_panel_show == 4:  # Escape selected
            pygame.draw.rect(screen, self.PANEL_COLOR, (645, HEIGHT / 2 + 50, 600, 300))
            char_text = gFonts['M_small'].render("Are you sure?", True, self.WHITE)
            screen.blit(char_text, (700, 430))

            # Draw "I will come back" and "Just kidding" buttons
            comeback_button = pygame.draw.rect(screen, self.BLACK, (700, 520, 250, 50))
            just_kidding_button = pygame.draw.rect(screen, self.BLACK, (700, 600, 250, 50))

            screen.blit(gFonts['M_small'].render("I will come back! >:(", True, self.RED), (710, 530))
            screen.blit(gFonts['M_small'].render("Just kidding! >:P", True, self.GREEN), (710, 610))

            return comeback_button, just_kidding_button
        return None, None
    
    def Enter(self, params):
        self.selected_weapon = None 
        self.selected_spell = None
        self.spell_positions = []
        self.selected_character = 0
        self.selected_monster = 0

        self.player_turn = True
        self.turn_order = self.characters + self.monsters
        self.current_turn_index = 0
        self.waiting_for_player_action = True

        for i in params:
            if i == "level":
                self.current_stage = params[i]
                self.load_monsters_for_stage(self.current_stage)
            elif i == "team":
                self.team_characters = params[i]
            elif i == "stages":
                self.stages = params[i]
            elif i == "coins":
                self.coins = params[i]
            elif i == "item-list":
                self.bought_items = params[i]
            elif i == "weapon-list":
                self.bought_weapons = params[i]
            elif i == "spell-list":
                self.bought_spells = params[i]
            elif i == "armor-list":
                self.bought_armors = params[i]
   
    def update(self, dt, events):

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    g_state_manager.Change('stage', None)  # Exit to stage
                elif event.key == pygame.K_RETURN:
                    self.process_player_action("attack")

                # Navigate monsters
                if event.key == pygame.K_UP:
                    self.process_player_action("up")
                elif event.key == pygame.K_DOWN:
                    self.process_player_action("down")
                
                # Reset right panel display when arrow keys are pressed
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    self.right_panel_show = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                weapon_button, spell_button, attack_button, escape_button = self.display_action_panel(
                    g_state_manager.screen, self.selected_character
                )
                if weapon_button.collidepoint(event.pos):
                    print("Weapon selected")
                    self.right_panel_show = 1
                    self.selected_weapon = None
                elif spell_button.collidepoint(event.pos):
                    print("Spell selected")
                    self.right_panel_show = 2
                    self.selected_spell = None
                elif attack_button.collidepoint(event.pos):
                    print("Attack selected")
                    self.right_panel_show = 3
                elif escape_button.collidepoint(event.pos):
                    print("Escape selected")
                    self.right_panel_show = 4

                if self.right_panel_show == 1:
                    current_character = self.characters[self.selected_character]
                    for i, weapon in enumerate(current_character.get("weapons", [])):
                        # Check if the click is within this weapon's row
                        weapon_rect = pygame.Rect(700, 470 + (i * 40), 400, 30)  # Adjust as needed
                        if weapon_rect.collidepoint(event.pos):
                            self.selected_weapon = i
                            print(f"Selected weapon: {current_character['weapons'][i]['name']}")

                if self.right_panel_show == 2:  # Spell panel is open
                    current_character = self.characters[self.current_turn_index]
                    for i, spell in enumerate(self.spell_positions):
                        spell_rect = pygame.Rect(700, 470 + (i * 40), 400, 30)
                        if spell_rect.collidepoint(event.pos):
                            self.selected_spell = i
                            print(f"Selected spell: {current_character['spells'][i]['name']}")

                 # Handle the "I will come back" and "Just kidding" buttons
                comeback_button, just_kidding_button = self.display_right_panel(
                    g_state_manager.screen, self.bought_items
                )
                if comeback_button and comeback_button.collidepoint(event.pos):
                    print("Returning to stage state")
                    g_state_manager.Change('start', None)  # Go back to stage state
                elif just_kidding_button and just_kidding_button.collidepoint(event.pos):
                    print("Returning to item selection")
                    self.right_panel_show = 0  # Go back to item display
        
        self.handle_turn()

    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))  # Draw background image
        self.display_characters_and_monsters(screen, self.selected_character, self.selected_monster)
        self.display_action_panel(screen, self.selected_character)  # Update action panel
        self.display_right_panel(screen, self.bought_items)  # Update right panel

    def Exit(self):
        # Clean up when leaving the combat state
        pass
