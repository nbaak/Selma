import pygame
import random

from settings import *
from Tile import Tile
from Player import Player
from Monster import Monster
from Weapon import Weapon
from CameraGroup import YSortCameraGroup
from UI import UI

from lib import load
from lib.MapLayout import MapLayout
from lib.Monsters import Monsters

class Level:
    
    def __init__(self):
        
        self.surface = pygame.display.get_surface()
        
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        
        self.create_map()
        
        # current_attack sprites
        self.current_attack = None
        self.current_magic = None
        
        # User Interface
        self.ui = UI()
         
    def create_map(self):
        layouts = {
            "boundary": load.csv_layout("../map/map_FloorBlocks.csv"),
            "grass": load.csv_layout("../map/map_Grass.csv"),
            "object": load.csv_layout("../map/map_Objects.csv"),
            "entities": load.csv_layout("../map/map_Entities.csv")
        }
        graphics = {
            "grass": load.images_from_folder("../images/grass"),
            "object": load.images_from_folder("../images/objects")
        }
        
        for style, layout in layouts.items():
            for y, row in enumerate(layout):
                for x, col in enumerate(row):
                    if col != MapLayout.EMPTY:
                        pos = (x*TILESIZE, y*TILESIZE)                    
                        if style == "boundary":
                            Tile(pos, [self.obstacle_sprites], MapLayout.INVISIBLE)
                            
                        if style == "grass":
                            grass_image = random.choice(graphics[style])
                            Tile(pos, [self.visible_sprites, self.obstacle_sprites], MapLayout.GRASS, grass_image)
                            
                        if style == "object":
                            obj = graphics[style][int(col)]
                            Tile(pos, [self.visible_sprites, self.obstacle_sprites], MapLayout.OBJECT, obj)
                            
                        if style == "entities":
                            if col == MapLayout.PLAYER:
                                self.player = Player(
                                    pos, 
                                    [self.visible_sprites], 
                                    self.obstacle_sprites, 
                                    self.create_attack, 
                                    self.destroy_attack, 
                                    self.create_magic
                                )
                            else:
                                monster = Monsters(col).name
                                Monster(monster, pos, [self.visible_sprites], self.obstacle_sprites)
                            
                    else:
                        pass
                    
        
                
    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])
        
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
    
    def create_magic(self, style, strength, cost):
        self.current_magic = None
        print(f"style: {style}, strength: {strength}, cost: {cost}")
        
    def destroy_magic(self):
        pass
        
    def update(self):
        # update things
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.monster_update(self.player)
        
        self.ui.display(self.player)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        