import pygame

class Button:
    def __init__(self, x, y, width, height, callback=None, data=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.data = data

    def update(self, event):
        """Cập nhật trạng thái của nút, xử lý sự kiện"""
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                if self.callback:
                    self.callback(self.data)

    def draw(self, screen):
        """Vẽ nút lên màn hình (sử dụng rect làm ví dụ)"""
        pygame.draw.rect(screen, (255, 241, 213), self.rect)  
