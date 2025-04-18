import pygame
from typing import Dict, Optional


class Sounds:
    def __init__(self):
        """Initialize the sound system."""
        pygame.mixer.init()
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.load_sounds()
        
        # Set default volumes
        self._set_default_volumes()
        
    def _set_default_volumes(self) -> None:
        """Set default volumes for specific sounds."""
        volume_settings = {
            "click": 0.3,
            "hover": 0.3,
            "pacman_death": 0.5
        }
        
        for sound_name, volume in volume_settings.items():
            if sound_name in self.sounds:
                self.sounds[sound_name].set_volume(volume)
    
    def load_sounds(self) -> None:
        """Load all required sound effects."""
        sound_files = {
            "click": "assets/sounds/click.wav",
            "hover": "assets/sounds/hover.wav",
            "pacman_death": "assets/sounds/pacman_death.wav",
            "pacman_eat": "assets/sounds/eating_dot.wav",
            "win": "assets/sounds/win.mp3"
        }
        
        # Load all sounds at once
        for name, path in sound_files.items():
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
            except pygame.error as e:
                print(f"Could not load sound {name}: {e}")
    
    def play_sound(self, sound_name: str) -> None:
        """Play a sound effect by name."""
        sound = self.sounds.get(sound_name)
        if sound:
            sound.play()
        else:
            print(f"Warning: Sound '{sound_name}' not found")
    
    def stop_sound(self, sound_name: str) -> None:
        """Stop a sound effect by name."""
        sound = self.sounds.get(sound_name)
        if sound:
            sound.stop()
            
    def set_volume(self, sound_name: str, volume: float) -> None:
        """Set the volume for a specific sound (0.0 to 1.0)."""
        sound = self.sounds.get(sound_name)
        if sound:
            sound.set_volume(max(0.0, min(1.0, volume)))  # Clamp volume between 0.0 and 1.0
    
    def play_music(self, music_name: str, loops: int = -1, volume: float = 0.5) -> None:
        """ music_name: tên nhạc (menu, game)
            loops: số lần lặp (-1 là lặp vô hạn)
            volume: Volume from 0.0 to 1.0
        """
        music_files = {
            "menu": "assets/sounds/menu.mp3",
            "game": "assets/sounds/game_background_music.wav "
        }
        
        if music_name in music_files:
            try:
                pygame.mixer.music.load(music_files[music_name])
                pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))  # Clamp volume
                pygame.mixer.music.play(loops=loops)
            except pygame.error as e:
                print(f"Could not play music '{music_name}': {e}")
    
    def stop_music(self) -> None:
        pygame.mixer.music.stop()
    
    def pause_music(self) -> None:
        pygame.mixer.music.pause()
        
    def unpause_music(self) -> None:
        pygame.mixer.music.unpause()
        
    def fade_out_music(self, time_ms: int = 500) -> None:
        pygame.mixer.music.fadeout(time_ms)