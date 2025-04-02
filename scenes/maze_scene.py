import sys
import pygame

from board_info import BoardInfo
from entities.ghost import Ghost
from entities.pacman import Pacman
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
        self.board = BoardInfo()        
        self.maze = MazeDrawing(screen)  # Khởi tạo mê cung từ lớp Maze

        # Khởi tạo Pacman
        self.pacman = Pacman(1, 1, self.board.game_map)  # (1, 1) là vị trí khởi tạo Pacman
        
        # Khởi tạo Ghosts
        self.ghosts = [
            Ghost(5, 5, self.board.game_map, "blue", "blue"),
            Ghost(5, 10, self.board.game_map, "pink", "pink"),
            Ghost(5, 15, self.board.game_map, "red", "red"),
            Ghost(5, 20, self.board.game_map, "orange", "orange")
        ]
        
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
        # Cập nhật vị trí Pacman (ví dụ: di chuyển theo hướng người chơi)
        self.pacman.move(0, 0)  # Giả sử dx, dy là sự thay đổi theo hướng (có thể nhận từ các phím bấm)

        # Cập nhật di chuyển của các Ghost
        pacman_x, pacman_y = self.pacman.x, self.pacman.y
        for ghost in self.ghosts:
            ghost.move(pacman_x, pacman_y)  # Các Ghost di chuyển đến vị trí Pacman
            ghost.follow_path()  # Di chuyển Ghost theo đường tìm được

    def render(self, screen):
        """Vẽ mê cung"""
        self.screen.fill((0, 0, 0))  
        self.maze.draw()  # Vẽ mê cung lên màn hình

        # Vẽ Pacman
        self.pacman.draw(self.screen, Config.TILE_HEIGHT)

        # Vẽ các Ghost
        for ghost in self.ghosts:
            # print(f"Vẽ ghost {ghost.color} tại ({ghost.x}, {ghost.y})")  # Debug
            ghost.draw(self.screen, Config.TILE_HEIGHT)

        # Vẽ các nút bấm
        for button in self.buttons:
            button.draw(self.screen)

        # Vẽ nút thoát
        self.quit_button.draw(self.screen)

        pygame.display.flip()


    def handle_quit_event(self, event):
        """Xử lý sự kiện thoát game"""
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def on_enter(self):
        """Được gọi khi vào scene maze"""
        # Phát nhạc nền
        Sounds().play_music("menu")

        # Khởi tạo Pacman và Ghosts khi vào scene
        self.pacman = Pacman(2, 2, self.board.game_map)  # Pacman ở vị trí (1, 1)
        self.ghosts = [
            Ghost(27, 29, self.board.game_map, "BFS", "blue"),
            # Ghost(27, 29, self.board.game_map, "DFS", "pink"),
            # Ghost(17, 15, self.board.game_map, "A*", "red"),
            # Ghost(17, 16, self.board.game_map, "UCS", "orange")
        ]
        print("Đã vào Maze Scene")

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
