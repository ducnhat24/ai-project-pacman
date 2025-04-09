import pygame

class Sounds:
    def __init__(self):
        pygame.mixer.init()  # Khởi tạo mixer của pygame
        self.sounds = {}     # Sử dụng dict để lưu trữ âm thanh
        self.load_sounds()   # Gọi phương thức tải âm thanh

        self.sounds["click"].set_volume(0.3)
        self.sounds["hover"].set_volume(0.3)

    def load_sounds(self):
        """Tải tất cả âm thanh cần thiết."""
        self.sounds = {
            "click": pygame.mixer.Sound("assets/sounds/click.wav"),
            "hover": pygame.mixer.Sound("assets/sounds/hover.wav"),
            "pacman_death": pygame.mixer.Sound("assets/sounds/pacman_death.wav"),
        }

    def play_sound(self, sound_name):
        """Phát âm thanh theo tên."""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def stop_sound(self, sound_name):
        """Dừng âm thanh theo tên."""
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()

    def play_music(self, music_name, loops=-1, volume=0.5):
        """Phát nhạc nền theo tên."""
        if music_name == "menu":
            pygame.mixer.music.load("assets/sounds/menu.mp3")
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loops=loops)

    def stop_music(self, music_name):
        """Dừng nhạc nền theo tên."""
        if music_name == "menu":
            pygame.mixer.music.stop()
 