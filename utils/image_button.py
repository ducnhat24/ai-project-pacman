import pygame
from settings import *
from utils.sounds import Sounds

# Tạo instance Sounds duy nhất để sử dụng cho tất cả các button
sounds_instance = Sounds()

class ImageButton:
    """Class đại diện cho một nút với hình ảnh"""
    def __init__(self, x, y, normal_width, normal_height, image_path, 
                 hover_width=None, hover_height=None, hover_image_path=None, 
                 scale=1.0, callback=None, data=None):
        # Load normal image
        self.normal_image = pygame.image.load(image_path).convert_alpha()
        self.normal_image = pygame.transform.smoothscale(self.normal_image, (normal_width, normal_height))
        self.normal_rect = self.normal_image.get_rect(topleft=(x, y))
        
        # Load hover image
        if hover_image_path is not None:
            self.hover_image = pygame.image.load(hover_image_path).convert_alpha()
            self.hover_image = pygame.transform.smoothscale(self.hover_image, (hover_width, hover_height))
        else:
            # Create default hover effect bằng cách tăng độ sáng
            self.hover_image = self.normal_image.copy()    
            bright_surface = pygame.Surface((normal_width, normal_height), pygame.SRCALPHA)
            bright_surface.fill((50, 50, 50, 0))
            self.hover_image.blit(bright_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        
        # Tạo rect cho hover image và đặt vị trí ban đầu
        self.hover_rect = self.hover_image.get_rect(topleft=(x, y))
        
        # Lưu center để dễ dàng cập nhật vị trí khi thay đổi ảnh
        self.center = self.normal_rect.center
        
        # Khởi tạo trạng thái ban đầu
        self.current_image = self.normal_image
        self.current_rect = self.normal_rect.copy()
        self.callback = callback
        self.data = data
        self.scale = scale
        self.is_hovered = False

    def update(self):
        """Cập nhật trạng thái nút dựa trên vị trí chuột."""
        mouse_pos = pygame.mouse.get_pos()
        was_hovered = self.is_hovered
        self.is_hovered = self.current_rect.collidepoint(mouse_pos)
        
        # Nếu mới hover, phát âm thanh hover
        if self.is_hovered and not was_hovered:
            sounds_instance.play_sound("hover")
        
        # Cập nhật ảnh và vị trí rect dựa trên trạng thái hover
        if self.is_hovered:
            self.current_image = self.hover_image
            self.hover_rect.center = self.center
            self.current_rect = self.hover_rect
        else:
            self.current_image = self.normal_image
            self.normal_rect.center = self.center
            self.current_rect = self.normal_rect
    
    def draw(self, screen):
        """Vẽ nút lên màn hình."""
        screen.blit(self.current_image, self.current_rect)
    
    def handle_event(self, event):
        """Xử lý sự kiện click chuột."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if self.current_rect.collidepoint(event.pos) and self.callback:
                sounds_instance.play_sound("click")
                self.callback(self.data)
                return True
        return False