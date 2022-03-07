import pygame
from lib import load
from random import choice, randint

class AnimationPlayer():
    def __init__(self):
        self.frames = {
            # magic
            'flame': load.images_from_folder("../images/particles/flame/frames"),
            'aura': load.images_from_folder('../images/particles/aura'),
            'heal': load.images_from_folder('../images/particles/heal/frames'),
            
            # attacks 
            'claw': load.images_from_folder('../images/particles/claw'),
            'slash': load.images_from_folder('../images/particles/slash'),
            'sparkle': load.images_from_folder('../images/particles/sparkle'),
            'leaf_attack': load.images_from_folder('../images/particles/leaf_attack'),
            'thunder': load.images_from_folder('../images/particles/thunder'),

            # monster deaths
            'squid': load.images_from_folder('../images/particles/smoke_orange'),
            'raccoon': load.images_from_folder('../images/particles/raccoon'),
            'spirit': load.images_from_folder('../images/particles/nova'),
            'bamboo': load.images_from_folder('../images/particles/bamboo'),
            
            # leafs 
            'leaf': (
                load.images_from_folder('../images/particles/leaf1'),
                load.images_from_folder('../images/particles/leaf2'),
                load.images_from_folder('../images/particles/leaf3'),
                load.images_from_folder('../images/particles/leaf4'),
                load.images_from_folder('../images/particles/leaf5'),
                load.images_from_folder('../images/particles/leaf6'),
                self.reflect_images(load.images_from_folder('../images/particles/leaf1')),
                self.reflect_images(load.images_from_folder('../images/particles/leaf2')),
                self.reflect_images(load.images_from_folder('../images/particles/leaf3')),
                self.reflect_images(load.images_from_folder('../images/particles/leaf4')),
                self.reflect_images(load.images_from_folder('../images/particles/leaf5')),
                self.reflect_images(load.images_from_folder('../images/particles/leaf6')),
                )
            }
    
    def reflect_images(self,frames):
        new_frames = []

        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
             
        return new_frames

    def create_grass_particles(self,pos,groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self,animation_type,pos,groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos,animation_frames,groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = .15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        
    def animate(self):
        self.frame_index += self.animation_speed
        
        if self.frame_index >= len(self.frames):
            self.kill()
            
        else:
            self.image = self.frames[int(self.frame_index)]
            
    def update(self):
        self.animate()