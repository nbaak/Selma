from math import sin
import pygame

class Entity(pygame.sprite.Sprite):
    
    def __init__(self, groups):
        super().__init__(groups)
        
        self.speed = .1
        
        self.frame_index = 0
        self.animation_speed = .15
        
        self.direction = pygame.math.Vector2()
        
    
    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right
        
        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y < 0: # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0: # moving down
                        self.hitbox.bottom = sprite.hitbox.top
            
    def move(self, speed=.1):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            
        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        
        self.rect.center = self.hitbox.center

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value > 0:
            return 255
        else:
            return 0