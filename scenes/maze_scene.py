import sys
import pygame

from board_info import Board
from maze_drawing import MazeDrawing
from scenes.base_scene import BaseScene
from utils.button import Button
from utils.sounds import Sounds
from utils.text_button import TextButton
from settings import Config


class MazeScene(BaseScene):
    """Scene hiển thị mê cung"""
    def __init__(self, scene_manager, screen):
        super().__init__(scene_manager, screen)  # Truyền screen vào constructor của BaseScene
        self.board = Board()
        self.maze = MazeDrawing(screen)  # Khởi tạo mê cung từ lớp Maze
        
        # Kích thước nút bấm (dùng để vẽ các nút)
        self.button_width = 100
        self.button_height = 50
        # Tạo danh sách các nút bấm sử dụng TextButton
        button_font = pygame.font.Font(None, 28) # Tạo một đối tượng font

        self.screen_height = Config.SCREEN_HEIGHT
        self.screen_width = Config.SCREEN_WIDTH

        spacing = 15

        self.buttons = [
            TextButton(spacing, self.screen_height - self.button_height - 10, self.button_width, self.button_height,
                    text="Test 1", font=button_font, callback=None, data="test1"), # Truyền font và text

            TextButton(spacing * 2 + self.button_width, self.screen_height - self.button_height - 10, self.button_width, self.button_height,
                    text="Test 2", font=button_font, callback=None, data="test2"), # Ví dụ: dùng callback khác và truyền data

            TextButton(spacing * 3 + self.button_width * 2, self.screen_height - self.button_height - 10, self.button_width, self.button_height,
                    text="Test 3", font=button_font, callback=None, data="test3"),

            TextButton(spacing * 4 + self.button_width * 3, self.screen_height - self.button_height - 10, self.button_width, self.button_height,
                    text="Test 4", font=button_font, callback=None, data="test4"),

            TextButton(spacing * 5 + self.button_width * 4, self.screen_height - self.button_height - 10, self.button_width, self.button_height,
                    text="Test 5", font=button_font, callback=None, data="test5"),
        ]

        # Nút thoát ở góc dưới bên phải
        # self.quit_button = Button(1150, 650, self.button_width, self.button_height, self.quit_game)
        self.quit_button = TextButton(self.screen_width - self.button_width - 10, self.screen_height - self.button_height - 10, self.button_width, self.button_height, 
                                      text="Quit", font=button_font, callback=self.quit_game, data=None)

    def handle_events(self, events):
        """Xử lý sự kiện trong mê cung"""
        for event in events:
            if event.type == pygame.QUIT:
                self.handle_quit_event(event)
            # Xử lý các nút bấm
            for button in self.buttons:
                button.update(event)
            self.quit_button.update(event)

    def update(self, dt):
        """Cập nhật trạng thái trong mê cung"""
        pass  # Bạn có thể thêm logic cập nhật nếu cần (ví dụ: di chuyển Pac-Man)

    def render(self, screen):
        """Vẽ mê cung"""
        self.screen.fill((0, 0, 0))  
        self.maze.draw()  

        # Vẽ các nút bấm ở phía dưới
        for button in self.buttons:
            button.draw(self.screen)

        # Vẽ nút thoát ở góc dưới bên phải
        self.quit_button.draw(self.screen)

        pygame.display.flip()

    def handle_quit_event(self, event):
        """Xử lý sự kiện thoát game"""
        if event.type == pygame.QUIT:
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

    # Các hàm callback cho các nút
    def start_game(self, data):
        print("Game bắt đầu")

    def pause_game(self, data):
        print("Game tạm dừng")

    def resume_game(self, data):
        print("Game tiếp tục")

    def restart_game(self, data):
        print("Game khởi động lại")

    def settings_game(self, data):
        print("Cài đặt game")

    def quit_game(self, data):
        print("Thoát game")
        pygame.quit()
        sys.exit()
