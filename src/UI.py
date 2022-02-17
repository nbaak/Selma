
import pygame

from settings import *

class UI():
    
    def __init__(self):
        # general
        self.surface = pygame.display.get_surface()
        self.font = pygame.font.FontType(UI_FONT, UI_FONT_SIZE)
        
        # bars
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 25, ENERGY_BAR_WIDTH, BAR_HEIGHT)
        self.exp_bar_rect = pygame.Rect(10, 45, EXP_BAR_WIDTH, EXP_BAR_HEIGHT)
        
        # weapons
        self.weapon_graphics = []
        self.import_graphics(weapon_data, self.weapon_graphics)
            
        # magic
        self.magic_graphics = []
        self.import_graphics(magic_data, self.magic_graphics)
            
    def import_graphics(self, data: dict, target_list: list):
        for item in data.values():
            target_list.append(pygame.image.load(item['graphic']).convert_alpha())
            
    def show_bar(self, current_amount, max_amount, bg_rect, color):
        # Backgroundfirst
        pygame.draw.rect(self.surface, UI_BG_COLOR, bg_rect)
        
        # normalize bars 
        ratio = current_amount / max_amount
        new_width = bg_rect.width * ratio
        new_rect = bg_rect.copy()
        new_rect.width = new_width
        
        pygame.draw.rect(self.surface, color, new_rect)
    
    def show_exp(self, exp):
        text = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = pygame.display.get_window_size()[0] -10  
        y = pygame.display.get_window_size()[1] -10
        text_rect = text.get_rect(bottomright=(x,y))        
        
        # self.show_bar(exp, 1000, text_rect, "gold")
        self.surface.blit(text, text_rect)
        
    def selection_box(self, left, top, switched=False):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.surface, UI_BG_COLOR, bg_rect)
        if switched:
            pygame.draw.rect(self.surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.surface, UI_BORDER_COLOR, bg_rect, 3)
             
        return bg_rect
    
    def item_overlay(self, switchable: bool, item_list: list, item_index: int, order=0):
        y = pygame.display.get_window_size()[1] -10 - ITEM_BOX_SIZE
        rect = self.selection_box(10 + ITEM_BOX_SIZE*order, y, not switchable)
        
        surface = item_list[item_index]
        rect = surface.get_rect(center=rect.center)
        
        self.surface.blit(surface, rect)
     
    def display(self, player):
        self.show_bar(player.health, player.stats["health"], self.health_bar_rect, HEALTH_BAR_COLOR)
        self.show_bar(player.energy, player.stats["energy"], self.energy_bar_rect, ENERGY_BAR_COLOR)
        self.show_bar(player.exp_percent, 100, self.exp_bar_rect, EXP_BAR_COLOR)
        
        self.item_overlay(player.weapon_switchable, self.weapon_graphics, player.weapon_index, 0)
        self.item_overlay(player.magic_switchable, self.magic_graphics, player.magic_index, 1)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        