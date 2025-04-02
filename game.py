import pygame
from scenes.menu import Menu
from scene_manager import SceneManager
from settings import Config

class Game:
    """Lớp quản lý game chính"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Config.SCREEN_SIZE)
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        
        # Hiển thị splash screen ngay khi khởi động game
        self.show_splash_screen(self.screen)
        
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

    def show_splash_screen(self, screen):
        """Hiển thị logo hoặc thông điệp 'Loading'"""
        screen.fill((158, 198, 243))  # Màu đen
        logo = pygame.image.load("assets/images/logo-pacman.png")
        
        # Điều chỉnh kích thước logo về một tỉ lệ nhỏ hơn (ví dụ: 500x266)
        logo = pygame.transform.scale(logo, (500, 266))  # Điều chỉnh kích thước logo
        
        # Lấy kích thước màn hình từ Config
        screen_width, screen_height = Config.SCREEN_SIZE
        # Hiển thị logo ở giữa màn hình
        screen.blit(logo, (screen_width // 2 - logo.get_width() // 2, screen_height // 2 - logo.get_height() // 2))
        pygame.display.update()  # Cập nhật màn hình


# Khởi chạy game
if __name__ == "__main__":
    game = Game()  # Khởi tạo và chạy game
    game.run()  # Chạy vòng lặp game chính
