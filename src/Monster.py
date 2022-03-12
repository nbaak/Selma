
import pygame
from settings import *
from lib import load
from Entity import Entity
from Player import Player

class Monster(Entity):
    
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_player_exp):
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
        self.damage_player = damage_player
        self.add_player_exp = add_player_exp
        self.trigger_death_particles = trigger_death_particles
        
        # vulnerability timer
        self.vulnerable = True
        self.hit_time = None
        self.invincible_duration = 300
        
        # sound
        self.sound_death = pygame.mixer.Sound("../audio/death.wav")
        self.sound_death.set_volume(.2)
        
        self.attack_sound = pygame.mixer.Sound(monster_info["attack_sound"])
        self.attack_sound.set_volume(.3)
        
        self.sound_hit = pygame.mixer.Sound("../audio/hit.wav")
        self.sound_hit.set_volume(.2)
        
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
            if self.status != "attack":
                    self.frame_index = 0
            self.status = "attack"
        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.status = "idle"
            
    def get_damage(self, player: Player, attack_type: str):
        if self.vulnerable:
            self.sound_hit.play()
            self.direction = self.get_player_distance_and_direction(player)[1]
            if attack_type == "weapon":
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False
            
    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance
        
    def check_death(self):
        if self.health <= 0:
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.add_player_exp(self.exp)
            self.kill()
            self.sound_death.play()
                        
    def actions(self, player: Player):
        if self.status == "attack":
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
            self.attack_sound.play()
            
        elif self.status == "move":
            _, self.direction = self.get_player_distance_and_direction(player)
            
        else:
            # stop moving if player is to far away
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
        
        # flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
        
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
                
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincible_duration:
                self.vulnerable = True
        
    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()
        
    def monster_update(self, player):
        self.get_status(player)
        self.actions(player)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        