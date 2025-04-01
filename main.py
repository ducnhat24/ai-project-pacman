import pygame
from scenes.menu import Menu
from scene_manager import SceneManager
from settings import *
class Game:
    """Lớp quản lý game chính"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Config.SCREEN_SIZE)
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        
        # Tạo Scene Manager
        self.scene_manager = SceneManager()
        
        # Tạo scene main menu
        main_menu = Menu(self.scene_manager)
        self.scene_manager.add_scene("MainMenu", main_menu)

        self.scene_manager.switch_to("MainMenu")

    def run(self):
        """Vòng lặp game chính"""
        while True:
            # Xử lý events
            events = pygame.event.get()
            self.scene_manager.handle_events(events)
            
            # Cập nhật
            dt = self.clock.tick(60) / 1000.0 
            self.scene_manager.update(dt)
            
            # Vẽ
            self.scene_manager.render(self.screen)
            
            # Cập nhật màn hình
            pygame.display.flip()

# Khởi chạy game
if __name__ == "__main__":
    game = Game()
    game.run()