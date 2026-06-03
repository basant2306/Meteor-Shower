import pygame.font
from pygame.sprite import Group
from ship import Ship
import os

class Scoreboard:

     def __init__(self,ms_game):

         self.ms_game = ms_game
         self.screen = ms_game.screen
         self.screen_rect =self.screen.get_rect()
         self.settings = ms_game.settings
         self.stats = ms_game.stats
         self.text_color = (30,30,30)
         self.font = pygame.font.SysFont(None,48)
         self.game_over_font = pygame.font.SysFont(None, 72)
         self.load_high_score()
         self.prep_score()
         self.prep_high_score()
         self.prep_level()
         self.prep_ships()
         self.prep_game_over()


     def prep_game_over(self):
          
         game_over_str = "GAME OVER"
         self.game_over_image = self.game_over_font.render(game_over_str, True, (255, 0, 0), (0, 0, 0))
         self.game_over_rect = self.game_over_image.get_rect()
         self.game_over_rect.centerx = self.screen_rect.centerx
         self.game_over_rect.centery = self.screen_rect.centery - 50
         final_score_str = f"Final Score: {self.stats.score}"
         self.final_score_image = self.font.render(final_score_str, True, self.text_color, self.settings.bg_color)
         self.final_score_rect = self.final_score_image.get_rect()
         self.final_score_rect.centerx = self.screen_rect.centerx
         self.final_score_rect.top = self.game_over_rect.bottom + 20

     def show_game_over(self):
          
         self.screen.blit(self.game_over_image, self.game_over_rect)
         self.screen.blit(self.final_score_image, self.final_score_rect)
         play_again_str = "Click anywhere to play again"
         play_again_image = self.font.render(play_again_str, True, self.text_color, self.settings.bg_color)
         play_again_rect = play_again_image.get_rect()
         play_again_rect.centerx = self.screen_rect.centerx
         play_again_rect.top = self.final_score_rect.bottom + 30
         self.screen.blit(play_again_image, play_again_rect)

     def prep_score(self):
         
         rounded_score = round(self.stats.score, -1)
         score_str = f"{rounded_score:,}"
         self.score_image = self.font.render(score_str,True,self.text_color,self.settings.bg_color)
         self.score_rect = self.score_image.get_rect()
         self.score_rect.right = self.screen_rect.right - 20
         self.score_rect.top = 20
         

     def show_score(self):

         self.screen.blit(self.score_image,self.score_rect)
         self.screen.blit(self.high_score_image,self.high_score_rect)
         self.screen.blit(self.level_image,self.level_rect)
         self.ships.draw(self.screen)

     def prep_high_score(self):

         high_score = round(self.stats.high_score, -1)
         high_score_str = f"{high_score:,}"
         self.high_score_image = self.font.render(high_score_str,True,self.text_color,self.settings.bg_color)
         self.high_score_rect = self.high_score_image.get_rect()
         self.high_score_rect.centerx = self.screen_rect.centerx
         self.high_score_rect.top = self.score_rect.top

     def check_high_score(self):

         if self.stats.score > self.stats.high_score:
             self.stats.high_score = self.stats.score
             self.prep_high_score()
             self.save_high_score()

     def save_high_score(self):
          
          f = open('high_score.txt', 'w')
          f.write(str(self.stats.high_score))
          f.close()

     def load_high_score(self):
         if os.path.exists('high_score.txt'):
             f = open('high_score.txt', 'r')
             content = f.read()
             f.close()
             if content.isdigit():
                 self.stats.high_score = int(content)
             else:
                 self.stats.high_score = 0
         else:
             self.stats.high_score = 0

     def prep_level(self):

         level_str = str(self.stats.level)
         self.level_image = self.font.render(level_str,True,self.text_color,self.settings.bg_color)
         self.level_rect = self.level_image.get_rect()
         self.level_rect.right = self.score_rect.right
         self.level_rect.top = self.score_rect.bottom + 10

     def prep_ships(self):

         self.ships = Group()
         for ship_number in range(self.stats.ships_left):
             ship = Ship(self.ms_game)
             ship.rect.x = 10 + ship_number * (ship.rect.width + 5)
             ship.rect.y = 10
             self.ships.add(ship)
