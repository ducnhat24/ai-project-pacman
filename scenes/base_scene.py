import pygame
import abc
from settings import *

class BaseScene(abc.ABC):
    """Lớp cơ sở cho các scene"""
    def __init__(self, scene_manager, screen):
        self.scene_manager = scene_manager
        self.screen = screen  # Thêm screen vào constructor
        self.screen_width = Config.SCREEN_WIDTH
        self.screen_height = Config.SCREEN_HEIGHT

        # Màu sắc
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 255, 0)
        self.BLUE = (100, 149, 237)

        # Font chữ
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 64)
        self.level_font = pygame.font.Font(None, 36)

    @abc.abstractmethod
    def on_enter(self):
        """Được gọi khi vào scene"""
        pass

    @abc.abstractmethod
    def on_exit(self):
        """Được gọi khi rời scene"""
        pass

    @abc.abstractmethod
    def handle_events(self, events):
        """Xử lý sự kiện"""
        pass

    @abc.abstractmethod
    def update(self, dt):
        """Cập nhật logic scene"""
        pass

    @abc.abstractmethod
    def render(self, screen):
        """Vẽ scene"""
        pass
