import time
import psutil
import pygame
from settings import Config

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
        self.current_algorithm = None  # Thêm biến lưu thuật toán hiện tại

    def start_monitoring(self, algorithm_name=None):
        """Bắt đầu theo dõi hiệu suất"""
        self.start_time = time.time()
        self.initial_memory = self.process.memory_info().rss / 1024  # Convert to KB
        self.is_monitoring = True
        self.expanded_nodes = 0
        self.show_popup = False
        self.current_algorithm = algorithm_name  # Lưu tên thuật toán

    def stop_monitoring(self):
        """Dừng theo dõi hiệu suất"""
        if self.is_monitoring:
            self.end_time = time.time()
            self.current_memory = self.process.memory_info().rss / 1024  # Convert to KB
            self.is_monitoring = False
            self.show_popup = True

    def increment_expanded_nodes(self, count=1):
        """Tăng số lượng node đã mở rộng"""
        if self.is_monitoring:
            self.expanded_nodes += count

    def get_metrics(self):
        """Lấy các thông số hiệu suất"""
        if not self.start_time or not self.end_time:
            return None

        total_time = self.end_time - self.start_time
        memory_used = self.current_memory - self.initial_memory

        return {
            "total_time": total_time,
            "expanded_nodes": self.expanded_nodes,
            "memory_used": memory_used,
            "algorithm": self.current_algorithm  # Thêm thông tin về thuật toán
        }

    def draw_popup(self, screen):
        """Vẽ popup hiển thị thông tin hiệu suất"""
        if not self.show_popup:
            return

        metrics = self.get_metrics()
        if not metrics:
            return

        # Tạo surface cho popup
        popup_width = 400
        popup_height = 300
        popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
        popup_surface.fill((0, 0, 0, 200))  # Màu đen với độ trong suốt

        # Vẽ viền
        pygame.draw.rect(popup_surface, (255, 255, 255), (0, 0, popup_width, popup_height), 2)

        # Vẽ tiêu đề
        title = self.font.render("Performance Metrics", True, (255, 255, 255))
        title_rect = title.get_rect(centerx=popup_width//2, y=20)
        popup_surface.blit(title, title_rect)

        # Vẽ các thông số
        y_offset = 70
        metrics_text = [
            f"Algorithm: {metrics['algorithm']}",
            f"Total Time: {metrics['total_time']:.2f} seconds",
            f"Expanded Nodes: {metrics['expanded_nodes']}",
            f"Memory Used: {metrics['memory_used']:.2f} KB"
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

        # Vẽ popup lên màn hình
        screen.blit(popup_surface, ((Config.SCREEN_WIDTH - popup_width) // 2, 
                                  (Config.SCREEN_HEIGHT - popup_height) // 2))

    def handle_events(self, event):
        """Xử lý sự kiện cho popup"""
        if self.show_popup and event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            self.show_popup = False
            return True
        return False 
