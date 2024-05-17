import pygame as pg
from laser import LaserType
import time


class Sound:
    def __init__(self, bg_music):
        pg.mixer.init()
        pg.mixer.music.load(bg_music)
        pg.mixer.music.set_volume(1)
        
        alienlaser_sound = pg.mixer.Sound('sounds/alienlaser.wav')
        photontorpedo_sound = pg.mixer.Sound('sounds/photon_torpedo.wav')
        self.sounds = {'alienlaser': alienlaser_sound, 'photontorpedo': photontorpedo_sound}

    def play_bg(self, bg_music):
        self.stop_bg()
        pg.mixer.music.load(bg_music)
        pg.mixer.music.play(-1, 0.0)

    # def pause_bg(self): 
    #     pg.mixer.music.pause()

    # def unpause_bg(self):
    #     pg.mixer.music.unpause()      

    def stop_bg(self):
        pg.mixer.music.stop()

    def shoot_laser(self, type):
        pg.mixer.Sound.play(self.sounds['alienlaser' if type == LaserType.ALIEN else 'photontorpedo'])

    def gameover(self): 
        self.stop_bg() 
        self.play_bg('sounds/gameover.wav')
        time.sleep(2.8)
        self.stop_bg()
