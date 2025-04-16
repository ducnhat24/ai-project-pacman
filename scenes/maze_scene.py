from copy import deepcopy
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
        self.maze = MazeDrawing(screen)

        self.game_map = MazeDrawing._shared_map
        
        # Lưu level hiện tại
        self.level_id = level_id
        self.level_config = LEVELS[level_id]
        
        # Test case hiện tại
        self.current_test_case = "test1"

        # Khởi tạo Pacman
        self.pacman = Pacman(3, 2, self.game_map) 
        
        # Khởi tạo PerformanceMonitor
        self.performance_monitors = {}
        
        # Khởi tạo Ghosts theo cấu hình level
        self.ghosts = []
        i = 0
        for ghost_config in self.level_config["ghosts"]:
            ghost_type = ghost_config["type"]
            ghost_color = ghost_config["color"]
            ghost_pos = ghost_config["pos"]
            ghost = Ghost(ghost_pos[0], ghost_pos[1], self.board.game_map, ghost_type, ghost_color, self.pacman.y, self.pacman.x, map=self.current_map, level_id=self.level_id)
            # Gán id cho ghost
            ghost.id = i
            i += 1
        
            monitor = PerformanceMonitor()
            self.performance_monitors[ghost.id] = monitor
            
            self.ghosts.append(ghost)
        
        # Kích thước nút bấm
        self.button_width = 100
        self.button_height = 50
        button_font = pygame.font.Font(None, 28)

        self.screen_height = Config.SCREEN_HEIGHT
        self.screen_width = Config.SCREEN_WIDTH

        spacing = 15

        self.end = False

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

        self.last_pacman_move_time = pygame.time.get_ticks()
        self.last_ghost_path_time = 0
        self.ghost_path_delay = 2000  # mỗi 300ms mới cho ghost tính toán lại đường đi
        self.game_over = False
        self.expanded_nodes = []  # Danh sách lưu số lượng node đã mở rộng của từng ghost

    def set_test_case(self, test_case_name):
        """Cấu hình vị trí Ghost theo test case"""
        # Đóng popup hiệu suất nếu đang mở
        for monitor in self.performance_monitors.values():
            if monitor:
                monitor.close_popup()
        
        self.end = False

        self.board = BoardInfo()
        self.current_map = self.board.game_map
        
        if test_case_name in TEST_CASES:
            self.current_test_case = test_case_name
            test_case = TEST_CASES[test_case_name]
            x, y = test_case["ghost_pos"]
            
            # Reset trạng thái game
            self.game_started = False
            self.show_text = True
            self.last_blink_time = time.time()

            # Reset vị trí Pacman về vị trí ban đầu
            self.pacman = Pacman(3, 2, self.board.game_map)
            
            # Tạo lại danh sách Ghosts với vị trí mới
            self.ghosts = []
            self.performance_monitors = {}
            i = 0
            for ghost_config in self.level_config["ghosts"]:
                ghost_type = ghost_config["type"]
                ghost_color = ghost_config["color"]
                if self.level_id >= 5:
                    ghost_pos = ghost_config["pos"]
                    x = ghost_pos[0]
                    y = ghost_pos[1]
                ghost = Ghost(x, y, self.board.game_map, ghost_type, ghost_color, self.pacman.x, self.pacman.y, map=self.current_map, level_id=self.level_id)
                # Gán id cho ghost
                ghost.id = i
                i += 1
                monitor = PerformanceMonitor()
                self.performance_monitors[ghost.id] = monitor
                
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
            for monitor in self.performance_monitors.values():
                if monitor and monitor.handle_events(event):
                    print("current_test_case", self.current_test_case)
                    self.reset_test_case()
                    break
            # if self.performance_monitor.handle_events(event):
            #     # Nếu popup được đóng, reset test case
            #     print("current_test_case", self.current_test_case)
            #     self.reset_test_case()
            #     continue

            if event.type == pygame.QUIT:
                self.handle_quit_event(event)
            # Bắt những sự kiện nhấn phím
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_started:
                    self.game_started = True
                    self.game_over = False
                    # Cho ghost tính toán đường đi
                    for ghost in self.ghosts:
                        monitor = self.performance_monitors.get(ghost.id)
                        monitor.init(ghost.ghost_type)
                        # Find Path
                        ghost.move(self.pacman.y, self.pacman.x)
                        #  
                        
                    # Bắt đầu đo thông số
                    #self.performance_monitor.start_monitoring()

                elif self.game_started and self.level_id == 6:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.pacman.set_next_direction(-1, 0)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.pacman.set_next_direction(1, 0)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.pacman.set_next_direction(0, -1)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.pacman.set_next_direction(0, 1)

                    # print("current map:",self.current_map)

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

        if self.game_started and not self.game_over:
            # Nếu là level 6 thì cho ghost tính toán đường đi liên tục
            if self.level_id == 6:
                self.pacman.update()
                if self.pacman._score == 558:
                    # switch to win scene
                    sleep_time = 0.2  # Thời gian chờ trước khi chuyển cảnh
                    time.sleep(sleep_time)  # Chờ trong 2 giây
                    self.scene_manager.switch_to("WinScene")



            # Kiểm tra va chạm với Ghost
            for ghost in self.ghosts:
                # print(self.current_map)
                ghost.follow_path(self.pacman.y, self.pacman.x, self.current_map)
                if ghost.x == self.pacman.y and ghost.y == self.pacman.x:
                    self.game_over = True
                    expanded_nodes = ghost.total_expanded_nodes
                    # self.expanded_nodes.append(ghost.expanded_nodes)
                    # self.performance_monitor.stop_monitoring(expanded_nodes)
                    monitor = self.performance_monitors.get(ghost.id)
                    if monitor:
                        monitor.stop_monitoring(expanded_nodes)  # Dừng monitor cho ghost tương ứng
                    for monitor in self.performance_monitors.values():
                        if monitor:
                            monitor.stop_monitoring(expanded_nodes)


    def render(self, screen):
        if not self.end: 
            
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
            # self.performance_monitor.draw_popup(screen)
            if (self.game_over):
                for ghost in self.ghosts:
                    monitor = self.performance_monitors.get(ghost.id)
                    # monitor.init(ghost.ghost_type)
            
                    monitor.set_memory(ghost.memory)
                    monitor.set_time(ghost.total_time)
                    monitor.set_expanded_nodes(ghost.total_expanded_nodes)
            # Đếm số monitor hợp lệ
            active_monitors = [m for m in self.performance_monitors.values() if m]
            check_total_monitor = len(active_monitors) > 1
            # Lặp và truyền biến check vào draw_popup
            for i, monitor in enumerate(active_monitors, start=1):
                status = monitor.draw_popup(screen, position=i, check=check_total_monitor)
                pygame.display.flip()
                if status:
                    self.end = True

            # Render text hiển thị số điểm của pacman
            score_text = self.start_message_font.render(f"Score: {self.pacman._score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height - 30))
            screen.blit(score_text, score_rect)

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
        board = BoardInfo()
        MazeDrawing._shared_map = deepcopy(board.initMaze)  # Lấy ma trận cho level
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