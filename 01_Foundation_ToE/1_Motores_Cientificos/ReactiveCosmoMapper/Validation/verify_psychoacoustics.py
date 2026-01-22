import sys
import os

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from harmonic_composer import PsychoAcousticComposer
import scipy.io.wavfile as wav

def verify_psychoacoustics():
    print("🧠 Generating Psycho-Acoustics (Phase 8)...")
    composer = PsychoAcousticComposer(gamma_hz=117.038)
    
    output_dir = "Validation"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. Generate PLEASURE (The Request)
    print("   > Synthesizing Dopaminergic Layer (Lydian Mode)...")
    audio_pleasure, sr = composer.generate_chord_mode("PLEASURE", duration_sec=60)
    out_pleasure = os.path.join(output_dir, "algoritmo_prazer.wav")
    wav.write(out_pleasure, sr, audio_pleasure)
    
    # 2. Generate FOCUS (Control Group)
    print("   > Synthesizing Nootropic Layer (Agcho Mode)...")
    audio_focus, sr = composer.generate_chord_mode("FOCUS", duration_sec=60)
    out_focus = os.path.join(output_dir, "algoritmo_foco.wav")
    wav.write(out_focus, sr, audio_focus)
    
    # Verify
    if os.path.exists(out_pleasure):
        size = os.path.getsize(out_pleasure)
        print(f"✅ PLEASURE Artifact Created: {out_pleasure} ({size/1024/1024:.1f} MB)")
    
    print("✅ Psycho-acoustic generation complete.")

if __name__ == "__main__":
    verify_psychoacoustics()
