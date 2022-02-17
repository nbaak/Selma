
import pygame
from pygame import sprite

class YSortCameraGroup(pygame.sprite.Group):
    
    def __init__(self):
        super().__init__()
        self.surface = pygame.display.get_surface()
        self.half_width = self.surface.get_size()[0]//2
        self.half_height = self.surface.get_size()[1]//2
        self.offset = pygame.math.Vector2()
        
        # floor
        self.floor_surface = pygame.image.load("../images/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0,0))
        
    def custom_draw(self, player):
        # offset from Player
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        
        # draw with offset
        # floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.surface.blit(self.floor_surface, floor_offset_pos)
        
        # tiles
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.surface.blit(sprite.image, offset_position)
            
    def monster_update(self, player):
        monster_sprites = [sprite for sprite in self.sprites() if  hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"]
        for monster in monster_sprites:
            monster.monster_update(player)