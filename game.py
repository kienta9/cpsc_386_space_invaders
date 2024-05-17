import pygame as pg
from button import Button
from settings import Settings
import game_functions as gf
from laser import Lasers, LaserType
from alien_fleet import AlienFleet
from ship import Ship
from sound import Sound
from scoreboard import Scoreboard
from vector import Vector
from game_stats import GameStats
from barrier import Barriers
import sys, time
from pathlib import Path


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height   # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")

        self.stats = GameStats(game=self)
        self.sound = Sound("sounds/startrek.wav")
        self.scoreboard = Scoreboard(game=self)  
                                    
        self.ship_lasers = Lasers(settings=self.settings, type=LaserType.SHIP)
        self.alien_lasers = Lasers(settings=self.settings, type=LaserType.ALIEN)
        
        self.barriers = Barriers(game=self)
        self.ship = Ship(game=self)
        self.alien_fleet = AlienFleet(game=self)

        self.settings.initialize_speed_settings()

        self.game_active = False             
        self.first = True

    def handle_events(self):
        keys_dir = {pg.K_w: Vector(0, -1), pg.K_UP: Vector(0, -1), 
                    pg.K_s: Vector(0, 1), pg.K_DOWN: Vector(0, 1),
                    pg.K_a: Vector(-1, 0), pg.K_LEFT: Vector(-1, 0),
                    pg.K_d: Vector(1, 0), pg.K_RIGHT: Vector(1, 0)}
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                key = event.key
                if key in keys_dir:
                    self.ship.v += self.settings.ship_speed * keys_dir[key]
                elif key == pg.K_SPACE:
                    self.ship.open_fire()
            elif event.type == pg.KEYUP:
                key = event.key
                if key in keys_dir:
                    self.ship.v = Vector()
                elif key == pg.K_SPACE:
                    self.ship.cease_fire()

    def reset(self):
        print('Resetting game...')
        self.screen.fill(self.settings.bg_color)
        self.settings.initialize_speed_settings()
        self.barriers.reset()
        self.ship.reset()
        self.alien_fleet.reset()

    def game_over(self):
        print('All ships gone: game over!')
        pg.mouse.set_visible(True)
        self.play_button.show()
        self.first = True
        self.game_active = False
        self.stats.reset()
        self.reset()
        self.sound.gameover()
        self.show_launcher()

    def activate(self): 
        self.game_active = True
        self.first = False
        self.sound.play_bg("sounds/startrek.wav")

    def play(self):
        self.screen.fill(self.settings.bg_color)
        while True:
            self.handle_events() 
            self.screen.fill(self.settings.bg_color)
            self.ship.update()
            self.alien_fleet.update()
            self.barriers.update()
            self.scoreboard.update()
            pg.display.flip()
            time.sleep(0.02)
    
    def launcher_draw_text(self, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def show_launcher(self):
        self.alien1 = pg.image.load('images/alien__01.png')
        self.alien2 = pg.image.load('images/alien__11.png')
        self.alien3 = pg.image.load('images/alien__21.png')

        while True:
            self.screen.fill((0, 0, 0))

            self.font = pg.font.Font(None, 200)
            self.launcher_draw_text("SPACE", (255, 255, 255), self.settings.screen_width // 2, self.settings.screen_height // 2 - 250)
            self.font = pg.font.Font(None, 136)
            self.launcher_draw_text("INVADERS", (0, 255, 0), self.settings.screen_width // 2, self.settings.screen_height // 2 - 150)
            self.font = pg.font.Font(None, 36)
            self.launcher_draw_text(f'HIGH SCORE: {self.scoreboard.show_high_score()}', (255, 0, 0), self.settings.screen_width // 2, self.settings.screen_height // 2 + 100)

            image_rect1 = self.alien1.get_rect(center=(self.settings.screen_width // 2 + 300, self.settings.screen_height // 2 + 200))
            image_rect2 = self.alien2.get_rect(center=(self.settings.screen_width // 2      , self.settings.screen_height // 2 + 200))
            image_rect3 = self.alien3.get_rect(center=(self.settings.screen_width // 2 - 300, self.settings.screen_height // 2 + 200))
            
            self.screen.blit(self.alien1, image_rect1)
            self.screen.blit(self.alien2, image_rect2)
            self.screen.blit(self.alien3, image_rect3)

            self.launcher_draw_text("Point: 500", (225, 193, 110), self.settings.screen_width // 2 - 300, self.settings.screen_height // 2 + 300)
            self.launcher_draw_text("Point: 200", (250, 160, 160), self.settings.screen_width // 2      , self.settings.screen_height // 2 + 300)
            self.launcher_draw_text("Point: 100", (173, 216, 230), self.settings.screen_width // 2 + 300, self.settings.screen_height // 2 + 300)

            self.play_button = Button(game=self, text='Play')

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    b = self.play_button
                    x, y = pg.mouse.get_pos()
                    if b.rect.collidepoint(x, y):
                        b.press()
                        self.play()
                elif event.type == pg.MOUSEMOTION:
                    b = self.play_button
                    x, y = pg.mouse.get_pos()
                    b.select(b.rect.collidepoint(x, y))
            
            if self.game_active or self.first:
                self.first = False
            else:
                self.play_button.update()

            pg.display.flip()


def main():
    g = Game()
    g.show_launcher()

if __name__ == '__main__':
    main()
