"""
Harmonic Decoder - The Sound of TARDIS
Generates the AAGOOCH chord keyed to the Universal Frequency Gamma (117.038 Hz).
"""
import numpy as np
import scipy.io.wavfile as wav
import os

class UniversalTuner:
    def __init__(self, gamma_hz=117.038):
        self.gamma = gamma_hz
        # Define A# (La Sustenido) as the Gamma anchor (117 Hz)
        # In standard 440Hz tuning, A#2 is ~116.54 Hz.
        # We are shifting reality slightly up to 117.038.
        self.reference_Asharp = self.gamma
        
        # Calculate Base A (A2) from the reference A# (A2#)
        # A is one semitone below A#
        self.base_A = self.reference_Asharp * (2 ** (-1/12))
        
    def get_frequency(self, note_interval_from_A):
        """
        Returns frequency based on semitone distance from Base A.
        """
        return self.base_A * (2 ** (note_interval_from_A/12))

    def generate_tone(self, freq, duration, sr=44100):
        t = np.linspace(0, duration, int(sr * duration), False)
        # Add harmonics for richness (Organ-like sound)
        wave = 0.5 * np.sin(2 * np.pi * freq * t) + \
               0.2 * np.sin(2 * np.pi * freq * 2 * t) + \
               0.1 * np.sin(2 * np.pi * freq * 3 * t) + \
               0.05 * np.sin(2 * np.pi * freq * 4 * t)
        return wave

    def generate_omega_chord(self, duration_sec=30):
        """
        Generates the A-A-G-O-O-C-H chord (Am9 no5).
        Notes:
        A (0) - Root
        G (10) - Minor 7th
        C (3) - Minor 3rd
        H (14) - Major 9th (B)
        Omega - The 117Hz Drone
        """
        sr = 44100
        
        # Calculate Frequencies
        f_A2 = self.base_A                    # Root Low
        f_A3 = self.get_frequency(12)         # Root High
        f_C3 = self.get_frequency(3 + 12)     # Minor 3rd (Emotional)
        f_G3 = self.get_frequency(10 + 12)    # Minor 7th (Tension)
        f_H3 = self.get_frequency(14 + 12)    # Major 9th (Mystery) - "H" is B
        f_Omega = self.gamma                  # The Anchor (A# drone)
        
        print(f"🎵 Tuning Orchestra to Gamma = {self.gamma:.3f} Hz")
        print(f"  A2: {f_A2:.2f} Hz")
        print(f"  A3: {f_A3:.2f} Hz")
        print(f"  G3: {f_G3:.2f} Hz")
        print(f"  C4: {f_C3:.2f} Hz")
        print(f"  H4: {f_H3:.2f} Hz (Si/B)")
        print(f"  Ω : {f_Omega:.2f} Hz (Drone)")

        # Generate Waves
        w_A2 = self.generate_tone(f_A2, duration_sec)
        w_A3 = self.generate_tone(f_A3, duration_sec) * 0.8
        w_C = self.generate_tone(f_C3, duration_sec) * 0.7
        w_G = self.generate_tone(f_G3, duration_sec) * 0.7
        w_H = self.generate_tone(f_H3, duration_sec) * 0.6
        w_Om = self.generate_tone(f_Omega, duration_sec) * 0.4 # Subtle dissonance of A# against A
        
        # Mix: A+A+G+C+H + Omega
        # Note: Omega (A#) vs A is highly dissonant (minor second). 
        # Ideally, Omega acts as the "carrier".
        # Let's make the chord pure AAGOOCH first.
        
        mix = (w_A2 + w_A3 + w_C + w_G + w_H) / 5
        
        # Fade in/out
        fade_len = int(sr * 2)
        fade_in = np.linspace(0, 1, fade_len)
        fade_out = np.linspace(1, 0, fade_len)
        
        mix[:fade_len] *= fade_in
        mix[-fade_len:] *= fade_out
        
        # Normalize
        mix = np.int16(mix / np.max(np.abs(mix)) * 32767)
        
        return mix, sr

if __name__ == "__main__":
    tuner = UniversalTuner()
    audio, rate = tuner.generate_omega_chord(duration_sec=15)
    
    out_path = "Validation/acorde_omega.wav"
    wav.write(out_path, rate, audio)
    print(f"✅ Generated: {out_path}")
