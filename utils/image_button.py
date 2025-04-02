import pygame
from utils.button import Button
from utils.sounds import Sounds  # Đảm bảo import đúng

class ImageButton(Button):
    def __init__(self, x, y, normal_width, normal_height, image_path, 
                 hover_width=None, hover_height=None, hover_image_path=None, 
                 scale=1.0, callback=None, data=None, sounds_instance=None):
        # Khởi tạo sounds_instance bên trong ImageButton
        self.sounds_instance = sounds_instance if sounds_instance else Sounds()

        # Tải hình ảnh bình thường
        self.normal_image = pygame.image.load(image_path).convert_alpha()
        self.normal_image = pygame.transform.smoothscale(self.normal_image, (normal_width, normal_height))
        self.normal_rect = self.normal_image.get_rect(topleft=(x, y))
        
        # Tải hình ảnh hover nếu có
        if hover_image_path is not None:
            self.hover_image = pygame.image.load(hover_image_path).convert_alpha()
            self.hover_image = pygame.transform.smoothscale(self.hover_image, (hover_width, hover_height))
        else:
            # Tạo hiệu ứng hover mặc định
            self.hover_image = self.normal_image.copy()
            bright_surface = pygame.Surface((normal_width, normal_height), pygame.SRCALPHA)
            bright_surface.fill((50, 50, 50, 0))
            self.hover_image.blit(bright_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        
        # Khởi tạo trạng thái ban đầu
        self.current_image = self.normal_image
        self.current_rect = self.normal_rect.copy()

        # Gọi hàm khởi tạo của Button
        super().__init__(x, y, normal_width, normal_height, callback, data)
        self.scale = scale
        self.is_hovered = False

    def handle_event(self, event):
        """Xử lý sự kiện click chuột"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if self.current_rect.collidepoint(event.pos) and self.callback:
                self.sounds_instance.play_sound("click")
                self.callback(self.data)
                return True
        return False

    def update(self, event):
        """Cập nhật trạng thái hover và xử lý sự kiện click"""
        mouse_pos = pygame.mouse.get_pos()
        was_hovered = self.is_hovered
        self.is_hovered = self.current_rect.collidepoint(mouse_pos)
        
        # Nếu mới hover, phát âm thanh hover
        if self.is_hovered and not was_hovered:
            self.sounds_instance.play_sound("hover")
        
        # Cập nhật ảnh và vị trí rect dựa trên trạng thái hover
        if self.is_hovered:
            self.current_image = self.hover_image
            self.current_rect.center = self.normal_rect.center
        else:
            self.current_image = self.normal_image
            self.current_rect.center = self.normal_rect.center
    
    def draw(self, screen):
        """Vẽ nút lên màn hình"""
        screen.blit(self.current_image, self.current_rect)
