import sys
import pygame
import time

from board_info import BoardInfo
from entities.ghost import Ghost
from entities.pacman import Pacman
from maze_drawing import MazeDrawing
from scenes.base_scene import BaseScene
from utils.button import Button
from utils.sounds import Sounds
from utils.text_button import TextButton
from utils.performance_monitor import PerformanceMonitor
from settings import Config
from level_config import TEST_CASES, LEVELS

class MazeScene(BaseScene):
    """Scene hiển thị mê cung"""
    def __init__(self, scene_manager, screen, level_id=1):
        super().__init__(scene_manager, screen)
        self.board = BoardInfo()        
        self.maze = MazeDrawing(screen)
        
        # Lưu level hiện tại
        self.level_id = level_id
        self.level_config = LEVELS[level_id]
        
        # Test case hiện tại
        self.current_test_case = "test1"

        # Khởi tạo Pacman
        self.pacman = Pacman(2, 2, self.board.game_map) 
        
        # Khởi tạo PerformanceMonitor
        self.performance_monitor = PerformanceMonitor()
        
        # Khởi tạo Ghosts theo cấu hình level
        self.ghosts = []
        for ghost_config in self.level_config["ghosts"]:
            ghost_type = ghost_config["type"]
            ghost_color = ghost_config["color"]
            ghost_pos = ghost_config["pos"]
            ghost = Ghost(ghost_pos[0], ghost_pos[1], self.board.game_map, ghost_type, ghost_color)
            self.ghosts.append(ghost)
        
        # Kích thước nút bấm
        self.button_width = 100
        self.button_height = 50
        button_font = pygame.font.Font(None, 28)

        self.screen_height = Config.SCREEN_HEIGHT
        self.screen_width = Config.SCREEN_WIDTH

        spacing = 15

        # Tạo danh sách các nút test nếu level cho phép
        self.buttons = []
        if self.level_config["show_test_buttons"]:
            self.buttons = [
                TextButton(spacing, self.screen_height - self.button_height - 10, self.button_width, self.button_height,
                        text="Test 1", font=button_font, callback=self.set_test_case, data="test1"),

                TextButton(spacing * 2 + self.button_width, self.screen_height - self.button_height - 10, self.button_width, self.button_height,
                        text="Test 2", font=button_font, callback=self.set_test_case, data="test2"),

                TextButton(spacing * 3 + self.button_width * 2, self.screen_height - self.button_height - 10, self.button_width, self.button_height,
                        text="Test 3", font=button_font, callback=self.set_test_case, data="test3"),

                TextButton(spacing * 4 + self.button_width * 3, self.screen_height - self.button_height - 10, self.button_width, self.button_height,
                        text="Test 4", font=button_font, callback=self.set_test_case, data="test4"),

                TextButton(spacing * 5 + self.button_width * 4, self.screen_height - self.button_height - 10, self.button_width, self.button_height,
                        text="Test 5", font=button_font, callback=self.set_test_case, data="test5"),
            ]

        # Nút thoát
        self.quit_button = TextButton(
            self.screen_width - self.button_width - 10, 
            self.screen_height - self.button_height - 10, 
            self.button_width, 
            self.button_height, 
            text="Quit", 
            font=button_font, 
            callback=self.quit_to_main_menu
        )

        # Thêm biến để kiểm soát trạng thái bắt đầu
        self.game_started = False
        self.start_message_font = pygame.font.Font(None, 48)
        self.blink_timer = 0
        self.show_text = True
        self.last_blink_time = time.time()

        # Tạo surface cho hiệu ứng mờ
        self.blur_surface = pygame.Surface((self.screen_width, self.screen_height - self.button_height - 10), pygame.SRCALPHA)
        self.blur_surface.fill((0, 0, 0, 128))

    def set_test_case(self, test_case_name):
        """Cấu hình vị trí Ghost theo test case"""
        # Đóng popup hiệu suất nếu đang mở
        self.performance_monitor.close_popup()
        
        if test_case_name in TEST_CASES:
            self.current_test_case = test_case_name
            test_case = TEST_CASES[test_case_name]
            x, y = test_case["ghost_pos"]
            
            # Reset trạng thái game
            self.game_started = False
            self.show_text = True
            self.last_blink_time = time.time()

            # Reset vị trí Pacman về vị trí ban đầu
            self.pacman = Pacman(2, 2, self.board.game_map)
            
            # Tạo lại danh sách Ghosts với vị trí mới
            self.ghosts = []
            for ghost_config in self.level_config["ghosts"]:
                ghost_type = ghost_config["type"]
                ghost_color = ghost_config["color"]
                ghost = Ghost(x, y, self.board.game_map, ghost_type, ghost_color)
                self.ghosts.append(ghost)
            
            # Phát âm thanh khi thay đổi test case
            #Sounds().play_sound("test_case_change")
            
            print(f"Đã đặt Ghost vào vị trí ({x}, {y}) - {test_case}")
            
            # Vẽ lại màn hình
            self.render(self.screen)

    def handle_events(self, events):
        """Xử lý sự kiện trong mê cung"""
        for event in events:
            # Xử lý sự kiện cho PerformanceMonitor trước
            if self.performance_monitor.handle_events(event):
                # Nếu popup được đóng, reset test case
                print("current_test_case", self.current_test_case)
                self.reset_test_case()
                continue

            if event.type == pygame.QUIT:
                self.handle_quit_event(event)
            # Bắt những sự kiện nhấn phím
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_started:
                    self.game_started = True
                    memory = 0
                    # Cho ghost tính toán đường đi
                    for ghost in self.ghosts:
                        memory = ghost.move(self.pacman.x, self.pacman.y)
                        self.performance_monitor.set_memory(memory)
                    # Bắt đầu đo thông số
                    self.performance_monitor.start_monitoring()

                # Xử lý di chuyển Pacman trong level 6
                elif self.game_started and self.level_id == 6:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.pacman.move(0, -1)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.pacman.move(0, 1)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.pacman.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.pacman.move(1, 0)
            # Xử lý các nút bấm
            for button in self.buttons:
                button.update(event)
            self.quit_button.update(event)

    def update(self, dt):
        """Cập nhật trạng thái trong mê cung"""

        if not self.game_started:
            # Cập nhật hiệu ứng nhấp nháy
            current_time = time.time()
            if current_time - self.last_blink_time > 0.2:
                self.show_text = not self.show_text
                self.last_blink_time = current_time

        if self.game_started:
            # Nếu là level 6 thì cho ghost tính toán đường đi liên tục
            if self.level_id == 6:
                pacman_x, pacman_y = self.pacman.x, self.pacman.y
                for ghost in self.ghosts:
                    ghost.move(pacman_x, pacman_y)
                    ghost.follow_path()
            # Nếu không phải level 6 thì cho ghost tính toán đường đi 1 lần
            else:
                for ghost in self.ghosts:
                    ghost.follow_path()
            # Kiểm tra va chạm với Ghost
            for ghost in self.ghosts:
                if ghost.x == self.pacman.x and ghost.y == self.pacman.y:
                    expanded_nodes = ghost.expanded_nodes
                    self.performance_monitor.stop_monitoring(expanded_nodes)

    def render(self, screen):
        """Vẽ mê cung"""
        self.screen.fill((0, 0, 0))  
        self.maze.draw()

        # Vẽ Pacman
        self.pacman.draw(self.screen, Config.TILE_HEIGHT)

        # Vẽ các Ghost
        for ghost in self.ghosts:
            ghost.draw(self.screen, Config.TILE_HEIGHT)

        # Vẽ các nút test nếu level cho phép
        if self.level_config["show_test_buttons"]:
            for button in self.buttons:
                button.draw(self.screen)

        # Vẽ nút thoát
        self.quit_button.draw(screen)

        # Vẽ thông báo bắt đầu nếu game chưa bắt đầu
        if not self.game_started:
            # Vẽ hiệu ứng mờ (không bao gồm khu vực nút bấm)
            screen.blit(self.blur_surface, (0, 0))

            if self.show_text:
                # Vẽ hướng dẫn bắt đầu
                start_text = self.start_message_font.render("Press SPACE to start", True, (255, 255, 255))
                start_rect = start_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
                screen.blit(start_text, start_rect)

        # Vẽ popup hiệu suất nếu cần
        self.performance_monitor.draw_popup(screen)

        pygame.display.flip()

    def handle_quit_event(self, event):
        """Xử lý sự kiện thoát game"""
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def on_enter(self):
        """Được gọi khi vào scene maze"""
        # Phát nhạc nền
        Sounds().stop_music("menu")
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

    def quit_to_main_menu(self, data):
        self.scene_manager.switch_to("MainMenu")
        print("Đã thoát về Main Menu")

    def reset_test_case(self):
        """Reset test case hiện tại"""
        if self.current_test_case:
            self.set_test_case(self.current_test_case)