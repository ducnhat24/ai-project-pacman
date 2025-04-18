import time
import psutil
import pygame
from settings import Config
import tracemalloc

class PerformanceMonitor:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.expanded_nodes = 0
        self.process = psutil.Process()
        self.initial_memory = None
        self.current_memory = None
        self.is_monitoring = False
        self.font = pygame.font.Font(None, 28)
        self.show_popup = False
        self.current_algorithm = None
        self.memory = 0
        self.total_time_algorithm = 0
        self.total_time_move = 0
        self.current_test_case = "test1"  # Giá trị mặc định

    def init(self, algorithm, test_case=None):
        self.current_algorithm = algorithm
        if test_case:
            self.current_test_case = test_case
        self.total_time_algorithm = 0
        self.total_time_move = 0
        self.memory = 0
        self.start_monitoring()

    def set_test_case(self, test_case):
        """Thiết lập test case hiện tại"""
        self.current_test_case = test_case

    def set_expanded_nodes(self, expanded_nodes):
        self.expanded_nodes = expanded_nodes

    def set_memory(self, memory):
        self.memory = memory

    def set_time(self, time):
        self.total_time_algorithm = time

    def set_add_memory(self, memory):
        self.memory = self.memory + memory

    def set_add_time(self, time):
        self.total_time_algorithm = self.total_time_algorithm + time
        
    def start_monitoring(self):
        """Bắt đầu theo dõi hiệu suất"""
        self.start_time = time.time()
        self.initial_memory = self.process.memory_info().rss / 1024  # Convert to KB
        self.is_monitoring = True
        self.expanded_nodes = 0
        self.show_popup = False

    def stop_monitoring(self, expanded_nodes=0):
        """Dừng theo dõi hiệu suất"""
        if self.is_monitoring:
            self.end_time = time.time()
            self.current_memory = self.process.memory_info().rss / 1024  # Convert to KB
            self.is_monitoring = False
            self.show_popup = True
            self.expanded_nodes = expanded_nodes

    def get_metrics(self):
        """Lấy các thông số hiệu suất"""
        if not self.start_time or not self.end_time:
            return None

        self.total_time_move = self.end_time - self.start_time
        #memory_used = self.current_memory - self.initial_memory
        memory_used = self.memory
        if memory_used is None:
            memory_used = 0.0
        return {
            "time_algorithm": self.total_time_algorithm,
            "time_move": self.total_time_move,
            "expanded_nodes": self.expanded_nodes,
            "memory_used": memory_used,
            "algorithm": self.current_algorithm,
            "test_case": self.current_test_case
        }

    def draw_popup(self, screen, position=1, check=False):
        """Vẽ popup hiển thị thông tin hiệu suất"""
        if not self.show_popup:
            return False

        metrics = self.get_metrics()
        if not metrics:
            return False

        # Tạo surface cho popup
        popup_width = 400
        popup_height = 320
        if check:
            popup_height = 250
        popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
        popup_surface.fill((0, 0, 0, 200))  # Màu đen với độ trong suốt

        # Vẽ viền
        pygame.draw.rect(popup_surface, (255, 255, 255), (0, 0, popup_width, popup_height), 2)

        # Vẽ tiêu đề với tên test case
        test_case_display = metrics['test_case'].replace('test', 'Test Case ')
        title = self.font.render(f"Performance Metrics - {test_case_display}", True, (255, 255, 255))
        title_rect = title.get_rect(centerx=popup_width//2, y=20)
        popup_surface.blit(title, title_rect)

        # Vẽ các thông số
        y_offset = 70
        metrics_text = []
        if (check):
            metrics_text = [
                f"Algorithm: {metrics['algorithm']}",
                f"Time Algorithm: {metrics['time_algorithm'] * 1000:.4f} ms",
                f"Expanded Nodes: {metrics['expanded_nodes']}",
            ]
        else:
            metrics_text = [
                f"Algorithm: {metrics['algorithm']}",
                f"Time Algorithm: {metrics['time_algorithm'] * 1000:.4f} ms",
                f"Expanded Nodes: {metrics['expanded_nodes']}",
                f"Memory Used: {metrics['memory_used']:.2f} KB",
                f"Total Time: {metrics['time_move']:.2f} seconds"
            ]

        for text in metrics_text:
            text_surface = self.font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(centerx=popup_width//2, y=y_offset)
            popup_surface.blit(text_surface, text_rect)
            y_offset += 40

        # Vẽ hướng dẫn
        instruction = self.font.render("Press X to close", True, (255, 255, 255))
        instruction_rect = instruction.get_rect(centerx=popup_width//2, y=popup_height - 40)
        popup_surface.blit(instruction, instruction_rect)
       
        # Xác định vị trí popup dựa vào `position`
        screen_w, screen_h = Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT

        if not check:
            pos = ((screen_w - popup_width) // 2, (screen_h - popup_height) // 2 - 10)
        elif position == 1:  # Top-left
            pos = (220, 80)
        elif position == 2:  # Top-right
            pos = (screen_w - popup_width - 220, 80)
        elif position == 3:  # Bottom-left
            pos = (220, screen_h - popup_height - 100)
        elif position == 4:  # Bottom-right
            pos = (screen_w - popup_width - 220, screen_h - popup_height - 100)
        
        # Vẽ lên màn hình
        screen.blit(popup_surface, pos)
        return True

    def handle_events(self, event):
        """Xử lý sự kiện cho popup"""
        if self.show_popup and event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            self.show_popup = False
            return True
        return False 

    def close_popup(self):
        self.show_popup = False

