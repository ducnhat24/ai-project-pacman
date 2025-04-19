import pygame
from settings import Config
from scenes.base_scene import BaseScene  # giả sử bạn đặt BaseScene trong scenes/
from utils.sounds import Sounds

class WinScene(BaseScene):
    def __init__(self, scene_manager, screen):
        super().__init__(scene_manager, screen)
        self.quit_button_rect = pygame.Rect(
            (self.screen_width - 200) // 2,
            self.screen_height // 2 + 50,
            200,
            60
        )
        self.button_hover = False
        self.sounds = Sounds()

    def on_enter(self):
        self.sounds.play_sound("win") 
        print("Entered WinScene")

    def on_exit(self):
        print("Exited WinScene")

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        self.button_hover = self.quit_button_rect.collidepoint(mouse_pos)

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.button_hover:
                    # Quay lại menu chính
                    self.scene_manager.switch_to("MainMenu")  # Giả sử bạn có scene tên là 'menu'

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill(self.BLACK)

        # Vẽ dòng chữ "YOU WIN!"
        text_surface = self.title_font.render("YOU WIN!", True, self.YELLOW)
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        screen.blit(text_surface, text_rect)

        # Vẽ nút Quit
        button_color = self.BLUE if not self.button_hover else (70, 130, 180)
        pygame.draw.rect(screen, button_color, self.quit_button_rect, border_radius=10)

        button_text = self.level_font.render("Quit", True, self.WHITE)
        text_rect = button_text.get_rect(center=self.quit_button_rect.center)
        screen.blit(button_text, text_rect)