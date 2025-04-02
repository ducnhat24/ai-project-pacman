import pygame
from game import Game
from scenes.menu import Menu
from scene_manager import SceneManager
from settings import *


# Khởi chạy game
if __name__ == "__main__":
    game = Game()
    game.show_splash_screen(game.screen)  # Gọi phương thức show_splash_screen từ đối tượng game
    game.run()