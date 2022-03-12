
import pygame
import random
from settings import *
from Player import Player
from Particles import AnimationPlayer


class MagicPlayer():
    
    def __init__(self, animation_player:AnimationPlayer):
        self.animation_player = animation_player
        self.sounds = {
            "heal":pygame.mixer.Sound("../audio/heal.wav"),
            "flame":pygame.mixer.Sound("../audio/Fire.wav"),}
        
    def heal(self, player: Player, strength, cost, groups):
        if player.energy >= cost:
            self.sounds["heal"].play()
            player.health += strength
            player.energy -= cost
            
            if player.health > player.stats["health"]:
                player.health = player.stats["health"]
                
            self.animation_player.create_particles('aura', player.rect.center, groups)
            self.animation_player.create_particles('heal', player.rect.center, groups)
    
    def flame(self, player: Player, cost, groups):
        if player.energy >= cost:
            self.sounds["flame"].play()
            player.energy -= cost
            
            direction = player.get_direction_vector()
            
            for i in range(1,6):
                if direction.x: # horizontal
                    offset_x = direction.x * i * TILESIZE
                    x = player.rect.centerx + offset_x + random.randint(-TILESIZE//3 , TILESIZE//3)
                    y = player.rect.centery + random.randint(-TILESIZE//3 , TILESIZE//3)
                else:   # vertical
                    offset_y = direction.y * i * TILESIZE
                    x = player.rect.centerx + random.randint(-TILESIZE//3 , TILESIZE//3)
                    y = player.rect.centery + offset_y + random.randint(-TILESIZE//3 , TILESIZE//3)

                self.animation_player.create_particles("flame", (x,y), groups)