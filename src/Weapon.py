
import pygame
from settings import *
from lib.PlayerState import PlayerState

class Weapon(pygame.sprite.Sprite):
    
    def __init__(self, player, groups):
        super().__init__(groups)
        direction = player.status.split("_")[0]
        
        # graphic
        weapon_image_path = f"{WEAPONS_FOLDER}/{player.weapon}/{direction}.png"
        
        self.image = pygame.image.load(weapon_image_path).convert_alpha()
        
        # placement relative to player
        if direction == PlayerState.UP:
            self.rect = self.image.get_rect(midbottom=player.rect.midtop+pygame.math.Vector2(-10,0))
        elif direction == PlayerState.DOWN:
            self.rect = self.image.get_rect(midtop=player.rect.midbottom+pygame.math.Vector2(-10,0))
        elif direction == PlayerState.LEFT:
            self.rect = self.image.get_rect(midright=player.rect.midleft+pygame.math.Vector2(0,16))
        elif direction == PlayerState.RIGHT:
            self.rect = self.image.get_rect(midleft=player.rect.midright+pygame.math.Vector2(0,16))
        