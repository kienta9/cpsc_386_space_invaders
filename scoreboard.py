import pygame as pg 
from pygame.sprite import Group
import pygame.font
from ship import Ship

class Scoreboard:
    def __init__(self, game): 
        
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = game.stats

        self.stats.high_score = self.load_high_score()

        self.text_color = (30, 30, 30)
        self.font = pg.font.SysFont(None, 48)

        self.score_image = None 
        self.score_rect = None
        self.prep_score()
        self.prep_high_score()

    def prep(self):
        self.prep_score()

    def increment_score(self, point): 
        self.stats.score += point
        self.prep_score()

    def prep_score(self): 
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"High: {high_score:,}"

        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
            self.save_high_score(self.stats.high_score)

    def load_high_score(self):
        try:
            with open('highscore.txt', 'r') as file:
                return int(file.read())
        except FileNotFoundError:
            # Return a default value if the file doesn't exist yet
            return 0

    def save_high_score(self, score):
        with open('highscore.txt', 'w') as file:
            file.write(str(score))
    
    def show_high_score(self):
        return str(self.stats.high_score)

    def update(self): 
        self.draw()

    def draw(self): 
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)