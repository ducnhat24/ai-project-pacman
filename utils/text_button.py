import pygame
from utils.button import Button


class TextButton(Button):
    def __init__(self, x, y, width, height, text, font, callback=None, data=None):
        super().__init__(x, y, width, height, callback, data)
        self.text = text
        self.font = font
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))  # Render text with black color
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)  # Center text within button

    def update(self, event):
        """Cập nhật trạng thái của nút, xử lý sự kiện"""
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                if self.callback:
                    self.callback(self.data)

    def draw(self, screen):
        """Vẽ nút và văn bản lên màn hình"""
        pygame.draw.rect(screen, "white", self.rect)  # Draw the button rectangle
        screen.blit(self.text_surface, self.text_rect)  # Draw the text centered within the button