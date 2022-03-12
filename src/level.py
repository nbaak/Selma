import pygame
import random

from settings import *
from Tile import Tile
from Player import Player
from Monster import Monster
from Weapon import Weapon
from CameraGroup import YSortCameraGroup
from UI import UI
from Magic import MagicPlayer

from lib import load
from lib.MapLayout import MapLayout
from lib.Monsters import Monsters
from Particles import AnimationPlayer
from Upgrade import Upgrade

class Level:
    
    def __init__(self):
        
        self.surface = pygame.display.get_surface()
        self.game_paused = False
        
        # visual sprites
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        
        # attack sprites
        self.current_attack = None
        self.current_magic = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        
        # setup sprites
        # also defines player and monsters
        self.create_map()
        
        # User Interface
        self.ui = UI()
        self.upgrade_menu = Upgrade(self.player)
        
        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)
         
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
                            
                        if style == MapLayout.GRASS:
                            grass_image = random.choice(graphics[style])
                            Tile(pos, [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], MapLayout.GRASS, grass_image)
                            
                        if style == MapLayout.OBJECT:
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
                                Monster(monster, 
                                        pos, 
                                        [self.visible_sprites, self.attackable_sprites], 
                                        self.obstacle_sprites, 
                                        self.damage_player, 
                                        self.trigger_death_particles,
                                        self.add_player_exp
                                        )
                            
                    else:
                        pass
                    
        
                
    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])
        
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
    
    def create_magic(self, style: str, strength, cost):
        print(f"style: {style}, strength: {strength}, cost: {cost}")
        
        if style =='heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites]) 
        
        elif style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])
        
        self.current_magic = None
        
    def destroy_magic(self):
        pass
    
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                
                if collision_sprites:
                    for target in collision_sprites:
                        if target.sprite_type == MapLayout.GRASS:
                            pos = target.rect.center
                            offset = pygame.math.Vector2(0,75)
                            for _ in range(random.randint(3,6)):
                                self.animation_player.create_grass_particles(pos-offset, [self.visible_sprites])
                            target.kill()
                        else:
                            # attack the enemy
                            target.get_damage(self.player, attack_sprite.sprite_type)
 
    def damage_player(self, amount: int, attack_type: str):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def add_player_exp(self, amount):
        self.player.gain_exp(amount)

    def trigger_death_particles(self, pos, animation_type):
        self.animation_player.create_particles(animation_type, pos, [self.visible_sprites])
        
    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def update(self):
        # update things
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        
        if self.game_paused:
            # show upgraade menu
            self.upgrade_menu.display()
            
        else:
            # run the game
            self.visible_sprites.update()
            self.visible_sprites.monster_update(self.player)
            self.player_attack_logic()

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        