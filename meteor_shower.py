import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from meteor import Meteor
import random

class MeteorShower:
    
    def __init__(self):

        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.bg_image = pygame.image.load('images/background.bmp').convert_alpha()
        self.bg_image = pygame.transform.scale(self.bg_image,(self.settings.screen_width,self.settings.screen_height)) 
        pygame.display.set_caption("Meteor Shower")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.meteors = pygame.sprite.Group()
        self.last_meteor_time = 0
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.game_active = False
        self.play_button = Button(self,"play")
        pygame.mixer.music.load('images/background_music.mp3')
        pygame.mixer.music.set_volume(0.5)  
        pygame.mixer.music.play(-1)
        self.bullet_sound = pygame.mixer.Sound('images/laser_sound.mp3')
        self.bullet_sound.set_volume(0.3)
        self.explosion_sound = pygame.mixer.Sound('images/explosion.mp3')
        self.explosion_sound.set_volume(0.3)
        
    def run_game(self):
        
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_meteors()
                self._spawn_meteors()
            else:
                self._show_game_over()
            self._update_screen()
            self.clock.tick(60)

    def _show_game_over(self):
        
        if self.stats.ships_left == 0:
            self.sb.show_game_over()
            
    def _spawn_meteors(self):

        current_time = pygame.time.get_ticks()
        if (current_time - self.last_meteor_time > self.settings.meteor_spawn_delay and len(self.meteors) < self.settings.max_meteors):
            new_meteor = Meteor(self)
            self.meteors.add(new_meteor)
            self.last_meteor_time = current_time
            self.settings.meteor_spawn_delay = random.randint(self.settings.min_spawn_delay, self.settings.max_spawn_delay)

    def _toggle_fullscreen(self):
        
        if self.settings.fullscreen:
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
            self.settings.fullscreen = False
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.fullscreen = True
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.bg_image = pygame.transform.scale(pygame.image.load('images/background.bmp').convert_alpha(),(self.settings.screen_width, self.settings.screen_height))
        self.ship.centre_ship()
        self.play_button = Button(self, "play") 
        self.sb.prep_score() 
    
    def _check_events(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if not self.game_active and self.stats.ships_left == 0:
                    self._check_play_button(mouse_pos)
                elif not self.game_active:
                    self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

    def _check_keydown_events(self,event):
        
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right=True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left=True
        if event.key == pygame.K_DOWN:
            self.ship.moving_down=True
        elif event.key == pygame.K_UP:
            self.ship.moving_up=True
        elif event.key == pygame.K_q:
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_ESCAPE:
            self._toggle_fullscreen()
        elif event.key == pygame.K_f:
            self._toggle_fullscreen()

    def _check_keyup_events(self,event):
        
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right=False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left=False
        if event.key == pygame.K_DOWN:
            self.ship.moving_down=False
        elif event.key == pygame.K_UP:
            self.ship.moving_up=False

    def _fire_bullet(self):

        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)
            if self.bullet_sound:
                self.bullet_sound.play()
        
    def _update_screen(self):

        self.screen.blit(self.bg_image,(0,0))
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.meteors.draw(self.screen)
        self.sb.show_score()
        if not self.game_active:
            if self.stats.ships_left == 0:
                self.sb.show_game_over()
            else:
                self.play_button.draw_button()     
        pygame.display.flip()

        
    def _update_bullets(self):

        self.bullets.update()
        for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)

        self._check_bullet_meteor_collision()

    def _check_bullet_meteor_collision(self):
        collisions = pygame.sprite.groupcollide(self.bullets,self.meteors,True,True)
        if collisions:
            for meteors in collisions.values(): 
                self.stats.score +=self.settings.meteor_points * len(meteors)
            if self.explosion_sound:
                 self.explosion_sound.play()    
            self.sb.prep_score()
            self.sb.check_high_score()
            if len(self.meteors) == 0:
                self._level_up()

    def _level_up(self):
        
        self.stats.level += 1
        self.sb.prep_level()
        self.settings.increase_speed()


    def _update_meteors(self):

        self.meteors.update()
        if pygame.sprite.spritecollideany(self.ship,self.meteors):
            self._ship_hit()
            
    def _ship_hit(self):

        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.bullets.empty()
            self.meteors.empty()
            self.ship.centre_ship()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
            self.sb.prep_game_over()

    def _check_play_button(self, mouse_pos):
        
        if self.stats.ships_left > 0:
            button_clicked = self.play_button.rect.collidepoint(mouse_pos)
            if button_clicked:
                self._start_game()
        else:
            self._start_game()

    def _start_game(self):
        
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.game_active = True
        self.bullets.empty()
        self.meteors.empty()
        self.last_meteor_time = pygame.time.get_ticks() 
        self.ship.centre_ship()
        pygame.mouse.set_visible(False)

    

if __name__  ==  '__main__':
    ms = MeteorShower()
    ms.run_game()
