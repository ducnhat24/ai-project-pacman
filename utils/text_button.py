import pygame
from utils.button import Button
from utils.sounds import Sounds

class TextButton(Button):
    def __init__(self, x, y, width, height, text, font, callback=None, data=None, 
                 normal_color=(255, 255, 255), hover_color=(150, 150, 150), selected_color=(0, 255, 0)):
        super().__init__(x, y, width, height, callback, data)
        self.text = text
        self.font = font
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))  # Render text with black color
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)  # Center text within button
        
        # Thêm các màu sắc cho các trạng thái
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.selected_color = selected_color
        self.is_hovered = False
        self.was_hovered = False  # Thêm biến để theo dõi trạng thái hover trước đó
        self.is_selected = False
        self.sounds_instance = Sounds()

    def update(self, event):
        """Cập nhật trạng thái của nút, xử lý sự kiện"""
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # Chỉ phát âm thanh hover khi mới hover vào
        if self.is_hovered and not self.was_hovered:
            self.sounds_instance.play_sound("hover")
        
        if self.is_hovered and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            self.sounds_instance.play_sound("click")
            if self.callback:
                self.callback(self.data)
                
        # Cập nhật trạng thái hover trước đó
        self.was_hovered = self.is_hovered

    def draw(self, screen):
        """Vẽ nút và văn bản lên màn hình"""
        # Chọn màu dựa trên trạng thái
        if self.is_selected:
            color = self.selected_color
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.normal_color
            
        pygame.draw.rect(screen, color, self.rect)  # Draw the button rectangle
        screen.blit(self.text_surface, self.text_rect)  # Draw the text centered within the button