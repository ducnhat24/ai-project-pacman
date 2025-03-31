import pygame
from settings import *

class ImageButton:
    """Class đại diện cho một nút với hình ảnh"""
    def __init__(self, x, y, normal_width, normal_height, image_path,  hover_width=None, hover_height=None, hover_image_path=None, scale=1.0, callback=None, data=None):
        # Load normal image
        self.normal_image = pygame.image.load(image_path).convert_alpha()
        self.normal_image = pygame.transform.smoothscale(self.normal_image, (normal_width, normal_height))
        self.normal_rect = self.normal_image.get_rect()
        self.normal_rect.topleft = (x, y)
        
        # Load hover image
        if hover_image_path is not None:
            self.hover_image = pygame.image.load(hover_image_path).convert_alpha()
            self.hover_image = pygame.transform.smoothscale(self.hover_image, (hover_width, hover_height))
        else:
            # Create default hover effect
            self.hover_image = self.normal_image.copy()    
            bright_surface = pygame.Surface((normal_width, normal_height), pygame.SRCALPHA)
            bright_surface.fill((50, 50, 50, 0))
            self.hover_image.blit(bright_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        
        # Create hover rect aligned with normal rect
        self.hover_rect = self.hover_image.get_rect()
        
        # Store the center of the normal image as the reference point
        self.center_x = self.normal_rect.centerx
        self.center_y = self.normal_rect.centery
        
        # Initialize with normal state
        self.current_image = self.normal_image
        self.current_rect = self.normal_rect.copy()
        
        # Other properties
        self.callback = callback
        self.data = data
        self.scale = scale
        self.is_hovered = False
        
        # Cursor settings
        self.default_cursor = pygame.mouse.get_cursor()
        self.hover_cursor = pygame.SYSTEM_CURSOR_HAND  # Use system hand cursor
        
    def update(self):
        """Cập nhật trạng thái nút"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Check previous hover state
        was_hovered = self.is_hovered
        
        # Use the current rect for collision detection
        self.is_hovered = self.current_rect.collidepoint(mouse_pos)
        
        # Change cursor when hover state changes
        if self.is_hovered != was_hovered:
            if self.is_hovered:
                pygame.mouse.set_cursor(self.hover_cursor)
            else:
                pygame.mouse.set_cursor(self.default_cursor)
        
        # Update image and rect based on hover state
        if self.is_hovered:
            self.current_image = self.hover_image
            # Update hover rect position to maintain the same center
            self.hover_rect.centerx = self.center_x
            self.hover_rect.centery = self.center_y
            self.current_rect = self.hover_rect
        else:
            self.current_image = self.normal_image
            # Update normal rect position to maintain the same center
            self.normal_rect.centerx = self.center_x
            self.normal_rect.centery = self.center_y
            self.current_rect = self.normal_rect
    
    def draw(self, screen):
        """Vẽ nút lên màn hình"""
        screen.blit(self.current_image, self.current_rect)
    
    def handle_event(self, event):
        """Xử lý sự kiện click chuột"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if self.current_rect.collidepoint(event.pos) and self.callback:
                self.callback(self.data)
                return True
        return False