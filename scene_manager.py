import pygame
import sys

class SceneManager:
    """Quản lý các scene trong game"""
    def __init__(self):
        self.scenes = {}
        self.current_scene = None

    def add_scene(self, name, scene):
        """Thêm scene vào quản lý"""
        self.scenes[name] = scene

    def switch_to(self, scene_name):
        """Chuyển đổi giữa các scene"""
        if scene_name in self.scenes:
            if self.current_scene:
                self.current_scene.on_exit()
            
            self.current_scene = self.scenes[scene_name]
            self.current_scene.on_enter()

    def handle_events(self, events):
        """Xử lý sự kiện cho scene hiện tại"""
        if self.current_scene:
            self.current_scene.handle_events(events)

    def update(self, dt):
        """Cập nhật scene hiện tại"""
        if self.current_scene:
            self.current_scene.update(dt)

    def render(self, screen):
        """Vẽ scene hiện tại"""
        if self.current_scene:
            self.current_scene.render(screen)

    