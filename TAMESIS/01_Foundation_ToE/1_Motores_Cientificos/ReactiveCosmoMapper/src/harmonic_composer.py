"""
Harmonic Composer - Psycho-Acoustic Engine
Generates specific emotional states using TAMESIS Gamma Tuning (117 Hz).
"""
import numpy as np
import scipy.io.wavfile as wav
import os
import sys

# Add src to path if running directly
sys.path.append(os.path.dirname(__file__))
from harmonic_decoder import UniversalTuner

class PsychoAcousticComposer(UniversalTuner):
    def generate_chord_mode(self, mode="PLEASURE", duration_sec=60):
        """
        Generates audio based on emotional target.
        """
        sr = 44100
        
        print(f"🎹 Composing for Mode: {mode}")
        print(f"🎵 Base Tuning: A# = {self.gamma} Hz")
        
        # Base Frequencies
        f_A2 = self.base_A
        f_A3 = self.get_frequency(12)
        
        waves = []
        
        if mode == "PLEASURE":
            # MAJOR 9th / LYDIAN feel
            # Structure: Root - Maj3 - Perf5 - Maj7 - Maj9
            # Frequencies relative to A
            f_C_sharp = self.get_frequency(4 + 12)  # Maj 3rd (Hope)
            f_E       = self.get_frequency(7 + 12)  # Perf 5th (Stability)
            f_G_sharp = self.get_frequency(11 + 12) # Maj 7th (Dreamy)
            f_B       = self.get_frequency(14 + 12) # Maj 9th (Floating)
            
            print("  Chord: A Major 9 (A - C# - E - G# - B)")
            
            # Generate Waves (Rich Palette)
            waves.append(self.generate_tone(f_A2, duration_sec) * 0.9)
            waves.append(self.generate_tone(f_A3, duration_sec) * 0.7)
            waves.append(self.generate_tone(f_C_sharp, duration_sec) * 0.6)
            waves.append(self.generate_tone(f_E, duration_sec) * 0.6)
            waves.append(self.generate_tone(f_G_sharp, duration_sec) * 0.5)
            waves.append(self.generate_tone(f_B, duration_sec) * 0.5)
            
            # The Gamma Drone (117Hz) - Kept low to ground the euphoria
            waves.append(self.generate_tone(self.gamma, duration_sec) * 0.25)
            
        elif mode == "FOCUS":
            # THE CLASSIC AAGOOCH (Minor 9 no 5)
            # Structure: Root - Min3 - Min7 - Maj9
            f_C = self.get_frequency(3 + 12)      # Min 3rd (Focus/Deep)
            f_G = self.get_frequency(10 + 12)     # Min 7th (Tension)
            f_H = self.get_frequency(14 + 12)     # Maj 9th (Mystery)
            
            print("  Chord: Am9 no5 (AAGOOCH)")
            
            waves.append(self.generate_tone(f_A2, duration_sec) * 1.0)
            waves.append(self.generate_tone(self.gamma, duration_sec) * 0.4) # Stronger Drone for Focus
            waves.append(self.generate_tone(f_C, duration_sec) * 0.7)
            waves.append(self.generate_tone(f_G, duration_sec) * 0.7)
            waves.append(self.generate_tone(f_H, duration_sec) * 0.6)
            
        # Mixing
        mix = np.zeros_like(waves[0])
        for w in waves:
            mix += w
            
        mix = mix / len(waves) # Average
        
        # Envelope (Smooth Fade In/Out)
        fade_len = int(sr * 3) # 3 sec fade
        fade_in = np.linspace(0, 1, fade_len)
        fade_out = np.linspace(1, 0, fade_len)
        
        mix[:fade_len] *= fade_in
        mix[-fade_len:] *= fade_out
        
        # Normalize
        mix = np.int16(mix / np.max(np.abs(mix)) * 32767)
        
        return mix, sr

if __name__ == "__main__":
    composer = PsychoAcousticComposer()
    audio, rate = composer.generate_chord_mode("PLEASURE", duration_sec=30)
    wav.write("algoritmo_prazer_preview.wav", rate, audio)
