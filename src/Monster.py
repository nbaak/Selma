
import pygame
from settings import *
from lib import load
from Entity import Entity

class Monster(Entity):
    
    def __init__(self, monster_name, pos, groups, obstacle_sprites):
        super().__init__(groups)
        
        self.sprite_type = "enemy"
        
        # graphic setup
        self.import_graphics(monster_name)
        self.status = "idle"
        self.image =  self.animations[self.status][self.frame_index]
                
        # movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites
        
        # stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']
        
        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 500
        
    def import_graphics(self, monster_name):
        self.animations = {
            "idle": [],
            "move":  [],
            "attack": [],            
        }
        #path = f"../images/monsters/{monster_name}"
        for animation in self.animations.keys():
            path = f"../images/monsters/{monster_name}/{animation}"
            self.animations[animation] = load.images_from_folder(path)
            
            
    def get_player_distance_and_direction(self, player):
        player_vector  = pygame.math.Vector2(player.rect.center)
        monster_vector = pygame.math.Vector2(self.rect.center)
        
        vector = player_vector - monster_vector
        distance = vector.magnitude()
        if distance > 0:
            direction = vector.normalize()
        else:
            direction = pygame.math.Vector2(0,0)        
            
        return (distance, direction)
            
    def get_status(self, player):
        distance, direction = self.get_player_distance_and_direction(player)
        
        if distance <= self.attack_radius and self.can_attack:
            self.status = "attack"
        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.status = "idle"
            
    def actions(self, player):
        if self.status == "attack":
            print("attack!")
            self.attack_time = pygame.time.get_ticks()
            
        elif self.status == "move":
            _, self.direction = self.get_player_distance_and_direction(player)
            
        else:
            self.direction = pygame.math.Vector2()
            
    def animate(self):
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == "attack":
                self.can_attack = False
            self.frame_index = 0
            
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
                self.attack_time = None
        
    def update(self):
        self.move()
        self.animate()
        self.cooldowns()
        
    def monster_update(self, player):
        self.get_status(player)
        self.actions(player)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        