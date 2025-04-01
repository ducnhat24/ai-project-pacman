import pygame
import sys
from scenes.base_scene import BaseScene
from settings import *
from utils.image_button import ImageButton
from utils.sounds import Sounds
class Menu(BaseScene):
    """Scene menu chính"""
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.buttonConfig = LevelButtonImageConfig
        self.level_buttons = []
        self.create_level_buttons()
        self.quit_button = self.create_quit_button()




    def create_level_buttons(self):
        """Tạo các nút level"""
        # Vị trí bắt đầu cho các nút
        start_x = self.screen_width // 2 + 60  # Adjusted for centering with 2 buttons per row
        start_y = self.screen_height // 2 - 110  # Adjusted to fit 3 rows
        normal_width = 220
        normal_height = 86
        hover_width = 220
        hover_height = 106
        button_margin_x = 30  # Horizontal spacing between buttons
        button_margin_y = 40  # Vertical spacing between rows
        
        # Tạo 6 nút level (3 dòng, mỗi dòng 2 nút)
        for level in range(1, 7):  # Tạo 6 nút level
            # Tính toán hàng và cột
            row = (level - 1) // 2  # 0 cho hàng đầu tiên, 1 cho hàng hai, 2 cho hàng ba
            col = (level - 1) % 2   # 0 cho cột đầu tiên, 1 cho cột hai
            
            # Đường dẫn ảnh cho từng level
            image_path = f"assets/images/buttons/btn-level{level}-normal.png"
            hover_image_path = f"assets/images/buttons/btn-level{level}-hover.png"
            
            # Tính toán vị trí của nút
            x = start_x + (normal_width + button_margin_x) * col
            y = start_y + (normal_height + button_margin_y) * row
            
            # Tạo nút với callback là hàm start_level
            button = ImageButton(
                x, y, 
                normal_width, normal_height, image_path, 
                hover_width, hover_height, hover_image_path,
                callback=self.start_level,
                data=level
            )

            self.level_buttons.append(button)
       
    def create_quit_button(self):
        """Tạo nút thoát"""
        x = self.screen_width // 2 + 180
        y = self.screen_height // 2 + 260
        normal_width = 220
        normal_height = 54
        image_path = "assets/images/quit-button.png"
        return ImageButton(
            x, y, 
            normal_width, normal_height, image_path,
            callback=self.quit_game
        )

    def quit_game(self, _=None):
        """Thoát game"""
        pygame.quit()
        sys.exit()

    def on_enter(self):
        """Được gọi khi vào scene menu"""
        # Phát nhạc nền
        Sounds().play_music("menu")

        print("Đã vào Main Menu")

    def on_exit(self):
        """Được gọi khi rời scene menu"""
        # Dừng nhạc nền
        Sounds().stop_music("menu")
        print("Đã rời Main Menu")

    def handle_events(self, events):
        """Xử lý sự kiện"""
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Xử lý sự kiện cho từng nút
            for button in self.level_buttons:
                button.handle_event(event)

            # Xử lý sự kiện cho nút thoát
            self.quit_button.handle_event(event)

    def start_level(self, level):
        """Bắt đầu level được chọn"""
        print(f"Chuyển sang Level {level}")
        # Chuyển sang scene level tương ứng
        self.scene_manager.switch_to(f"Level{level}")

    def update(self, dt):
        """Cập nhật logic menu"""
        for button in self.level_buttons:
            button.update()

        self.quit_button.update()
        pass

    def render(self, screen):
        """Vẽ menu"""
        
        # Vẽ background
        background  = pygame.image.load("assets/images/menu-background.jpg")
        background = pygame.transform.smoothscale(background, Config.SCREEN_SIZE) 
        screen.blit(background, (0, 0))

        # Vẽ logo
        logo = pygame.image.load("assets/images/logo-pacman.png")
        logo = pygame.transform.smoothscale(logo, (540, 288))
        logo_rect = logo.get_rect(center=(self.screen_width // 2 + 300, self.screen_height // 2 - 200))
        screen.blit(logo, logo_rect)
      
        # Vẽ nút level
        for btn in self.level_buttons:
            btn.draw(screen)

        # Vẽ nút thoát
        self.quit_button.draw(screen)



