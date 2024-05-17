
from random import randint
import pygame as pg
from pygame.sprite import Sprite, Group
from laser import Lasers
from timer import Timer


class Alien(Sprite):
    points = [100, 200, 500]
    alien_images0 = [pg.transform.rotozoom(pg.image.load(f'images/alien__0{n}.png'), 0, 0.7) for n in range(2)]
    alien_images1 = [pg.transform.rotozoom(pg.image.load(f'images/alien__1{n}.png'), 0, 0.7) for n in range(2)]
    alien_images2 = [pg.transform.rotozoom(pg.image.load(f'images/alien__2{n}.png'), 0, 0.7) for n in range(2)]

    alien_timers = {0 : Timer(image_list=alien_images0), 
                    1 : Timer(image_list=alien_images1), 
                    2 : Timer(image_list=alien_images2)} 

    explosion_100 = [pg.transform.scale(pg.image.load(f'images/explode_100_0{n}.png'), (80,80)) for n in range(5)]
    explosion_200 = [pg.transform.scale(pg.image.load(f'images/explode_200_0{n}.png'), (80,80)) for n in range(5)]
    explosion_500 = [pg.transform.scale(pg.image.load(f'images/explode_500_0{n}.png'), (80,80)) for n in range(5)]
    alien_explosion_images = [explosion_100, explosion_200, explosion_500]

    def __init__(self, game, type):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pg.image.load('images/alien0.bmp')
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.type = type
        self.point = Alien.points[type]
        self.sb = game.scoreboard
        self.stats = game.stats
        
        self.dying = self.dead = False
                      
        self.timer_normal = Alien.alien_timers[type]              
        self.timer_explosion = Timer(image_list=Alien.alien_explosion_images[type], is_loop=False)  
        self.timer = self.timer_normal                                    

    def check_edges(self): 
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
    
    def check_bottom_or_ship(self, ship):
        screen_rect = self.screen.get_rect()
        return self.rect.bottom >= screen_rect.bottom or self.rect.colliderect(ship.rect)
    
    def hit(self):
        if not self.dying:
            self.dying = True 
            self.timer = self.timer_explosion
            self.sb.increment_score(self.point)

    def update(self): 
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.kill()
        settings = self.settings
        self.x += (settings.alien_speed * settings.fleet_direction)
        self.rect.x = self.x
        self.draw()

    def draw(self): 
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)



