import pygame, sys

from settings import *
from level import Level

class Game():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Selma")
        self.clock = pygame.time.Clock()
        self.running = True
        self.level = Level()
        
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()
                    
            self.screen.fill("black")
            self.level.update()
            
            pygame.display.update()
            self.clock.tick(FPS)
            

if __name__ == '__main__':
    game = Game()
    game.run()