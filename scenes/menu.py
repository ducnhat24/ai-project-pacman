from copy import deepcopy
import pygame
import sys
from maze_drawing import MazeDrawing
from scenes.base_scene import BaseScene
from scenes.maze_scene import MazeScene
from settings import *
from utils.image_button import ImageButton 
from utils.sounds import Sounds
from board_info import BoardInfo

class Menu(BaseScene):
    """Scene menu chính"""
    def __init__(self, scene_manager, screen):
        super().__init__(scene_manager, screen)
        self.buttonConfig = LevelButtonImageConfig
        self.level_buttons = []
        self.create_level_buttons()
        self.quit_button = self.create_quit_button()

        # Vẽ và lưu trữ background và logo chỉ một lần
        self.background = pygame.image.load("assets/images/menu-background.jpg")
        self.background = pygame.transform.smoothscale(self.background, Config.SCREEN_SIZE)
        
        self.logo = pygame.image.load("assets/images/logo-pacman.png")
        self.logo = pygame.transform.smoothscale(self.logo, (540, 288))
        self.logo_rect = self.logo.get_rect(center=(self.screen_width // 2 + 300, self.screen_height // 2 - 200))

    def create_level_buttons(self):
        """Tạo các nút level"""
        start_x = self.screen_width // 2 + 60
        start_y = self.screen_height // 2 - 110
        normal_width = 220
        normal_height = 86
        hover_width = 220
        hover_height = 106
        button_margin_x = 30
        button_margin_y = 40
        
        # Tạo 6 nút level
        for level in range(1, 7):
            row = (level - 1) // 2
            col = (level - 1) % 2
            image_path = f"assets/images/buttons/btn-level{level}-normal.png"
            hover_image_path = f"assets/images/buttons/btn-level{level}-hover.png"
            
            x = start_x + (normal_width + button_margin_x) * col
            y = start_y + (normal_height + button_margin_y) * row
            
            button = ImageButton(
                x, y, normal_width, normal_height, image_path, 
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
            x, y, normal_width, normal_height, image_path,
            callback=self.quit_game
        )

    def quit_game(self, _=None):
        """Thoát game"""
        pygame.quit()
        sys.exit()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.handle_quit_event(event)  # Xử lý sự kiện thoát game
            self.handle_button_events(event)  # Xử lý sự kiện cho các nút

    def handle_quit_event(self, event):
        """Xử lý sự kiện thoát game"""
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def handle_button_events(self, event):
        """Xử lý sự kiện cho các nút"""
        for button in self.level_buttons:
            button.handle_event(event)  # Gọi method handle_event của mỗi button
        self.quit_button.handle_event(event)  # Xử lý nút thoát game

    def update(self, dt):
        """Cập nhật logic menu"""
        for button in self.level_buttons:
            button.update(dt)  # Chỉ gọi update cho từng button mà không cần event

        self.quit_button.update(dt)  # Cập nhật nút thoát game


    def start_level(self, level):
        """Bắt đầu level được chọn, chuyển sang MazeScene"""
        print(f"Chuyển sang Level {level}")
        maze_scene = MazeScene(self.scene_manager, self.screen, level)
        self.scene_manager.add_scene(f"Level{level}", maze_scene)
        self.scene_manager.switch_to(f"Level{level}")


    def render(self, screen):
        """Vẽ menu"""
        screen.blit(self.background, (0, 0))
        screen.blit(self.logo, self.logo_rect)
        for button in self.level_buttons:
            button.draw(screen)
        self.quit_button.draw(screen)
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