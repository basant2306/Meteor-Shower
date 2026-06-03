import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):

    def __init__(self,ms_game):

        super().__init__()
        self.screen=ms_game.screen
        self.settings=ms_game.settings
        self.image = pygame.image.load('images/bullet.bmp')
        self.rect = self.image.get_rect()
        self.rect.midtop=ms_game.ship.rect.midtop
        self.y=float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):

       self.screen.blit(self.image, self.rect)
