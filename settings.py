import pygame

class Config: 
    SCREEN_WIDTH = 1300
    SCREEN_HEIGHT = 760
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
    BOARD_WIDTH = 630 #1020
    BOARD_HEIGHT = 672
    TITLE_WIDTH = BOARD_WIDTH/30
    TITLE_HEIGHT = BOARD_HEIGHT/32

class LevelButtonImageConfig:
    NORMAL_WIDTH = 220
    NORMAL_HEIGHT = 86
    HOVER_WIDTH = 220
    HOVER_HEIGHT = 106
    MARGIN_X = 30
    MARGIN_Y = 40
    
    IMAGE_PATH = "assets/images/buttons/"

class Sounds:
    def __init__(self):
        pygame.mixer.init()  # Khởi tạo mixer của pygame
        self.sounds = {
            "chomp": pygame.mixer.Sound("assets/sounds/chomp.wav"),
            "death": pygame.mixer.Sound("assets/sounds/death.wav"),
            "eat_ghost": pygame.mixer.Sound("assets/sounds/eat_ghost.wav"),
            "powerup": pygame.mixer.Sound("assets/sounds/powerup.wav"),
            "start": pygame.mixer.Sound("assets/sounds/start.wav"),
        }

        # Đặt âm lượng mặc định (0.0 - 1.0)
        for sound in self.sounds.values():
            sound.set_volume(0.5)

    def play(self, sound_name):
        """Phát âm thanh theo tên"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def stop(self, sound_name):
        """Dừng âm thanh theo tên"""
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()

    def set_volume(self, sound_name, volume):
        """Chỉnh âm lượng (0.0 - 1.0)"""
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(volume)

    def stop_all(self):
        """Dừng tất cả âm thanh"""
        pygame.mixer.stop()

class Color:
  color_wall = (0, 255, 255)
  color_power_food = (255, 0, 255)
  color_food = (250, 218, 94)
  color_bg = (20, 20, 40)
  color_fence = (255, 0, 255)
  color_text = 'white'