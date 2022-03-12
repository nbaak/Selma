
import pygame


from settings import *
import Player

class Upgrade:
    
    def __init__(self, player: Player):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        
        self.attribute_count = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        
        # bar items
        self.height = self.display_surface.get_size()[1] * .8
        self.width = self.display_surface.get_size()[0] // (self.attribute_count+1)
        self.create_items()
        
        # selection system
        self.selection_index = 0
        self.selection_time = None
        self.selection_can_move = True
        
    def input(self):
        keys = pygame.key.get_pressed()
        
        # set focus
        if self.selection_can_move:
            if keys[pygame.K_RIGHT]:
                self.selection_index += 1 
                if self.selection_index >= self.attribute_count:
                    self.selection_index = 0
                
            elif keys[pygame.K_LEFT]:
                self.selection_index -= 1
                if self.selection_index < 0:
                    self.selection_index = self.attribute_count-1

            # select
            if keys[pygame.K_SPACE]:
                self.item_list[self.selection_index].trigger(self.player)
            
            #print(self.selection_index)
            self.selection_can_move = False
            self.selection_time = pygame.time.get_ticks()
            
    def selection_cooldown(self):
        if not self.selection_can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 100:
                self.selection_can_move = True
    
    def create_items(self):
        self.item_list = []

        for item_index in range(self.attribute_count):
            # horizontal post
            width = self.display_surface.get_size()[0]
            increment = width // self.attribute_count
            left = (item_index*increment) + (increment - self.width) // 2
            
            # vertical pos
            top = self.display_surface.get_size()[1] * .1
            # create object
            item = Item(left, top, self.width, self.height, item_index, self.font)
            self.item_list.append(item)
           
    def display(self):
        self.input()
        self.selection_cooldown()
        
        for index, item in enumerate(self.item_list):
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            item.draw(self.display_surface, self.selection_index, name, value, max_value, cost)
        
class Item:
    
    def __init__(self, left, top, width, height, index, font):
        self.rect = pygame.rect.Rect(left, top, width, height)

        self.index = index
        self.font = font
     
    def trigger(self, player:Player):
        selected_attribute = player.get_stats_label_by_index(self.index)
        
        if player.exp >= player.upgrade_cost[selected_attribute] and player.stats[selected_attribute] < player.max_stats[selected_attribute]:
            player.exp -= player.upgrade_cost[selected_attribute]
            player.stats[selected_attribute] *= 1.2
            player.upgrade_cost[selected_attribute] *= 1.4
            
        if player.stats[selected_attribute] > player.max_stats[selected_attribute]:
            player.stats[selected_attribute] = player.max_stats[selected_attribute]
        
    def draw_names(self, surface:pygame.surface, name:str, cost, selected:bool):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        
        # titles
        title_surface = self.font.render(name, False, color)
        title_rect = title_surface.get_rect(midtop=self.rect.midtop+pygame.math.Vector2(0,20))
        
        cost_surface = self.font.render(str(int(cost)), False, color)
        cost_rect = cost_surface.get_rect(midbottom=self.rect.midbottom+pygame.math.Vector2(0,-20))
        
        surface.blit(title_surface, title_rect)
        surface.blit(cost_surface, cost_rect)
        
    def draw_bar(self, surface:pygame.surface, value, max_value, selected:bool):
        # setup
        
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0,60) 
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR
        
        full_height = bottom[1] - top[1]
        relative_value = (value / max_value) * full_height
        value_rect = pygame.Rect(top[0]-15, bottom[1]-relative_value, 30, 10)
        
        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)
        
    def draw(self, surface:pygame.surface, selection_index:int, name:str, value, max_value, cost):
        selected = self.index == selection_index
        if selected:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect,4)
        
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect,4)
        
        
        self.draw_names(surface, name, cost, selected)
        self.draw_bar(surface, value, max_value, selected)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        