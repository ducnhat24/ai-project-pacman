import pygame

class Sounds:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            "click": pygame.mixer.Sound("assets/sounds/click.wav"),
            "hover": pygame.mixer.Sound("assets/sounds/hover.wav"),
            "pacman_death": pygame.mixer.Sound("assets/sounds/pacman_death.wav"),
        }

        self.musics = {
            "menu": pygame.mixer.Sound("assets/sounds/menu.mp3"),
        }

        self.sounds["click"].set_volume(0.3)
        self.sounds["hover"].set_volume(0.1)

        self.musics["menu"].set_volume(0.7)

    def play_sound(self, sound_name):
        """Phát âm thanh theo tên"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def stop_sound(self, sound_name):
        """Dừng âm thanh theo tên"""
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()

    def set_sound_volume(self, sound_name, volume):
        """Chỉnh âm lượng (0.0 - 1.0)"""
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(volume)

    def play_music(self, music_name):
        """Phát nhạc nền theo tên"""
        if music_name in self.musics:
            self.musics[music_name].play(-1)

    def stop_music(self, music_name):
        """Dừng nhạc nền theo tên"""
        if music_name in self.musics:
            self.musics[music_name].stop()

    def set_music_volume(self, music_name, volume):
        """Chỉnh âm lượng nhạc nền (0.0 - 1.0)"""
        if music_name in self.musics:
            self.musics[music_name].set_volume(volume)

    def stop_all(self):
        pygame.mixer.stop()