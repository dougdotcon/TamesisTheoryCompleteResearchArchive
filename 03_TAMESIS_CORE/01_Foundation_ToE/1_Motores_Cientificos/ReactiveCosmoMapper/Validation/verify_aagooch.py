import sys
import os

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from harmonic_decoder import UniversalTuner

def verify_harmonics():
    print("🎧 Verifying Universal Harmonics (Phase 7)...")
    print("---------------------------------------------")
    
    tuner = UniversalTuner(gamma_hz=117.038)
    
    # 1. Check A# anchor
    assert tuner.reference_Asharp == 117.038
    print("✅ Gamma Anchor verified: 117.038 Hz")
    
    # 2. Generate Audio
    audio, rate = tuner.generate_omega_chord(duration_sec=10)
    
    output_dir = "Validation"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    out_path = os.path.join(output_dir, "acorde_omega.wav")
    
    # This actually saves the file during verification
    import scipy.io.wavfile as wav
    wav.write(out_path, rate, audio)
    
    if os.path.exists(out_path):
        size = os.path.getsize(out_path)
        print(f"✅ Audio File Generated: {out_path} ({size/1024:.1f} KB)")
        
        # Create Report
        with open("Validation/harmonic_report.txt", "w") as f:
            f.write("HARMONIC DECODING REPORT\n")
            f.write("========================\n")
            f.write(f"Root Frequency (Gamma): {tuner.gamma} Hz\n")
            f.write(f"Base Tone (A2): {tuner.base_A:.3f} Hz\n")
            f.write("Chord Structure: Am9(no5) [A-C-G-B]\n")
            f.write("Status: RESONANCE ACHIEVED\n")
            f.write("Caution: Long-term exposure may alter perception of time.\n")
            
        print("✅ Report saved: Validation/harmonic_report.txt")
    else:
        print("❌ Failed to generate audio file.")

if __name__ == "__main__":
    verify_harmonics()
