from visualizer import GalaxyVisualizer
import matplotlib.pyplot as plt
import numpy as np
import os
from mpl_toolkits.mplot3d import Axes3D

FRAMES_DIR = "frames/cosmic_web"
os.makedirs(FRAMES_DIR, exist_ok=True)

def run_animation():
    print("🎥 Rendering Cosmic Web Flythrough...")
    
    # 1. Load Data
    viz = GalaxyVisualizer(data_file="data/sdss_sample.csv")
    df = viz.load_and_transform()
    if df is None:
        print("Error: Could not load data.")
        return
    
    # Downsample for smoother plotting if needed, but 50k points in mpl3d is slow.
    # We'll use 10k for video.
    if len(df) > 10000:
        df_plot = df.sample(10000)
    else:
        df_plot = df
        
    x = df_plot['x'].values
    y = df_plot['y'].values
    z = df_plot['z'].values
    
    # 2. Setup Plot
    fig = plt.figure(figsize=(12, 8), dpi=80) # HD
    ax = fig.add_subplot(111, projection='3d')
    # Pre-scatter (static) - or update view?
    # Updating view is faster.
    
    sc = ax.scatter(x, y, z, s=0.5, c=z, cmap='twilight', alpha=0.6)
    ax.set_axis_off() # Space look
    plt.tight_layout()
    
    # Set background color
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    
    # Camera Path: Spiral Flythrough
    # Azimuth 0->360, Elevation oscillating, Zoom in?
    frames = 180
    
    for i in range(frames):
        angle = i * (360 / frames)
        elev = 10 + 20 * np.sin(np.radians(i * 2))
        dist = 20000 - (i * 50) # Zoom in slightly
        
        ax.view_init(elev=elev, azim=angle)
        # ax.dist = dist / 1000 # MPL 3D dist param is weird
        
        plt.title(f"The Reactive Cosmic Web (Frame {i})", color='white')
        plt.savefig(f"{FRAMES_DIR}/frame_{i:03d}.png", facecolor='black')
        
    print("✅ Cosmic Web frames generated.")

if __name__ == "__main__":
    run_animation()
