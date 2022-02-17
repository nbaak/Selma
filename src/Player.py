import pygame
from settings import *
from lib import load
from lib.PlayerState import PlayerState
from Entity import Entity

class Player(Entity):
    
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('../images/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,-25)
        
        # import player assets
        self.import_player_assets()
        self.sprite_type = "player"
        
        # player status
        self.status = PlayerState.DOWN
        
        # movement
        self.attacking = False
        self.attacking_cooldown = 400
        self.attacking_time = None
        
        # weapons and attacks
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack 
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.weapon_switchable = True
        self.weapon_switch_time = None
        self.weapon_switch_cooldown = 200
        
        # magic 
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.magic_switchable = True
        self.magic_switch_time = None
        self.magic_switch_cooldown = 200
        
        # stats
        self.stats = {
            "health": 100,
            "energy": 100,
            "attack": 10,
            "magic": 4,
            "speed": 5,
        }
        self.health = self.stats["health"]
        self.energy = self.stats["energy"]
        self.exp = 0
        self.exp_percent = 0
        self.speed = self.stats["speed"]
        
        # obstacles
        self.obstacle_sprites = obstacle_sprites
        
        # vulnerability
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500
        
        
    def import_player_assets(self):
        character_path = "../images/player"
        
        self.animations = {
            "up": [], 
            "down": [],
            "left": [],
            "right": [],
            "up_idle": [],
            "down_idle": [],
            "left_idle": [],
            "right_idle": [],
            "up_attack": [],
            "down_attack": [],
            "left_attack": [],
            "right_attack": [],            
        }
        
        for animation in self.animations.keys():
            self.animations[animation] = load.images_from_folder(f"{character_path}/{animation}")
            
        print(self.animations)
               
    def read_keyboard_input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()
            
            # Movement
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = PlayerState.UP
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = PlayerState.DOWN
            else:
                self.direction.y = 0
    
            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = PlayerState.RIGHT
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = PlayerState.LEFT
            else:
                self.direction.x = 0
                
            # Attack
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attacking_time = pygame.time.get_ticks()
                self.create_attack()
            
            # Magic
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attacking_time = pygame.time.get_ticks()
                
                style = self.magic
                strength = magic_data[style]["strength"] + self.stats["magic"]
                cost = magic_data[style]["cost"]
                
                self.create_magic(style, strength, cost)
                
                
            # Weapon switch
            if keys[pygame.K_q] and self.weapon_switchable:
                self.weapon_switch_time = pygame.time.get_ticks()
                
                if self.weapon_index < len(list(weapon_data.keys()))-1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                    
                self.weapon = list(weapon_data.keys())[self.weapon_index]
                self.weapon_switchable = False
                
            # Magic switch
            if keys[pygame.K_e] and self.magic_switchable:
                self.magic_switch_time = pygame.time.get_ticks()
                
                if self.magic_index < len(list(magic_data.keys()))-1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                    
                self.magic = list(magic_data.keys())[self.magic_index]
                self.magic_switchable = False
    
    def get_state(self):
        # idle
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.status and "attack" not in self.status:
                self.status  += "_idle"
                
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status = self.status + "_attack"
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')

    def get_full_weapon_damage(self):
        print(self.stats["attack"] + weapon_data[self.weapon]["damage"])
        return self.stats["attack"] + weapon_data[self.weapon]["damage"]

    def gain_exp(self, amount = 0):
        self.exp += amount
        self.exp_percent = self.exp
        
        if self.exp > 100:
            self.exp = 0

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attacking_time >= self.attacking_cooldown + weapon_data[self.weapon]["cooldown"]:
                self.attacking = False
                self.destroy_attack()
                
        if not self.weapon_switchable:
            if current_time - self.weapon_switch_time >= self.weapon_switch_cooldown:
                self.weapon_switchable = True
                
        if not self.magic_switchable:
            if current_time - self.magic_switch_time >= self.magic_switch_cooldown:
                self.magic_switchable = True
                
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        
        # flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def update(self):
        self.read_keyboard_input()
        self.cooldowns()
        self.get_state()
        self.animate()
        self.move()
        #self.gain_exp(1)
        
        #print(f"status: {self.status}")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        