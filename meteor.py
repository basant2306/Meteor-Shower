import pygame
import random
from pygame.sprite import Sprite

class Meteor(Sprite):

    def __init__(self,ms_game):

        super().__init__()
        self.screen = ms_game.screen
        self.settings = ms_game.settings
        self.image = pygame.image.load('images/meteor.bmp')
        self.rect = self.image.get_rect()
        self.reset_positions()
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):

        screen_rect = self.screen.get_rect()
        return(self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):

        self.y += self.settings.meteor_speed
        self.rect.y = self.y
        if self.rect.top > self.screen.get_height():
            self.kill()  

    def reset_positions(self):

        self.rect.x = random.randint(0,self.screen.get_width() - self.rect.width)
        self.rect.y = random.randint(-150,-40)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
            
             


        
