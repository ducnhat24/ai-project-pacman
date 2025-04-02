import pygame

class Sounds:
    def __init__(self):
        pygame.mixer.init()  # Khởi tạo mixer của pygame
        self.sounds = {}     # Sử dụng dict để lưu trữ âm thanh
        self.musics = {}     # Sử dụng dict để lưu trữ nhạc nền
        self.load_sounds()   # Gọi phương thức tải âm thanh
        self.load_music()    # Gọi phương thức tải nhạc nền

    def load_sounds(self):
        """Tải tất cả âm thanh cần thiết."""
        self.sounds = {
            "click": pygame.mixer.Sound("assets/sounds/click.wav"),
            "hover": pygame.mixer.Sound("assets/sounds/hover.wav"),
            "pacman_death": pygame.mixer.Sound("assets/sounds/pacman_death.wav"),
        }

    def load_music(self):
        """Tải nhạc nền."""
        self.musics = {
            "menu": pygame.mixer.Sound("assets/sounds/menu.mp3"),
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
        if music_name in self.musics:
            self.musics[music_name].set_volume(volume)  # Điều chỉnh âm lượng
            self.musics[music_name].play(loops=loops)

    def stop_music(self, music_name):
        """Dừng nhạc nền theo tên."""
        if music_name in self.musics:
            self.musics[music_name].stop()
 