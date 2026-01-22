import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

# Configuration
OUTPUT_DIR = r"c:\Users\Douglas\Desktop\ToE\assets\animation_frames"
FRAMES = 200
PARTICLES = 500
OMEGA = 117.038

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize random particles
np.random.seed(42)  # For reproducibility
# Random positions between -2 and 2
x = np.random.uniform(-2, 2, PARTICLES)
y = np.random.uniform(-2, 2, PARTICLES)

# Target structure: Golden Spiral
# Points distributed along a golden spiral
indices = np.arange(0, PARTICLES)
golden_angle = np.pi * (3 - np.sqrt(5))
theta_target = indices * golden_angle
radius_target = np.sqrt(indices) / np.sqrt(PARTICLES) * 1.5
x_target = radius_target * np.cos(theta_target)
y_target = radius_target * np.sin(theta_target)

# Setup plot
fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
ax.set_facecolor('black')
scatter = ax.scatter([], [], c='cyan', s=10, alpha=0.6, edgecolors='none')
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.axis('off')

# Text elements
title_text = ax.text(0, 1.8, "ENTROPY", color='white', fontsize=20, ha='center', va='center', alpha=1.0, weight='bold')
omega_text = ax.text(0, -1.8, "", color='#FFD700', fontsize=16, ha='center', va='center', alpha=0.0)

def ease_in_out(t):
    return t * t * (3 - 2 * t)

def update(frame):
    global x, y
    
    # Phase 1: Chaos (0-50)
    if frame < 50:
        # Random Brownian motion
        x += np.random.normal(0, 0.05, PARTICLES)
        y += np.random.normal(0, 0.05, PARTICLES)
        # Keep within bounds mostly
        mask = (x**2 + y**2) > 4
        x[mask] *= 0.95
        y[mask] *= 0.95
        
        title_text.set_text("ENTROPY")
        title_text.set_color("white")
        omega_text.set_alpha(0)
        
        current_x, current_y = x, y
        color = 'cyan'
        
    # Phase 2: Transition to Order (50-150)
    elif frame < 150:
        progress = (frame - 50) / 100.0
        t = ease_in_out(progress)
        
        # Interpolate between current random state and target spiral
        # To make it look continuous, we actually just move towards target each step
        # But for simplicity in this script, let's lerp from the state at frame 50
        # Wait, simple lerp might look artificial. Let's use attraction.
        
        # Attraction force towards target
        dx = x_target - x
        dy = y_target - y
        
        # Strength increases with time
        strength = 0.05 * progress + 0.01
        
        x += dx * strength + np.random.normal(0, 0.01 * (1-progress), PARTICLES)
        y += dy * strength + np.random.normal(0, 0.01 * (1-progress), PARTICLES)
        
        title_text.set_text("EMERGENCE")
        title_text.set_color("#00FFFF")
        omega_text.set_text(f"Ω = {OMEGA}")
        omega_text.set_alpha(progress)
        
        current_x, current_y = x, y
        # Color transition from Cyan to Gold
        color = np.array([0, 1, 1]) * (1-progress) + np.array([1, 0.84, 0]) * progress
        
    # Phase 3: Geometry (150-200)
    else:
        # Stable rotating structure
        progress = (frame - 150) / 50.0
        
        # Slight rotation
        angle = 0.01
        xr = x * np.cos(angle) - y * np.sin(angle)
        yr = x * np.sin(angle) + y * np.cos(angle)
        x, y = xr, yr
        
        title_text.set_text("GEOMETRY")
        title_text.set_color("#FFD700")
        omega_text.set_alpha(1.0)
        
        current_x, current_y = x, y
        color = '#FFD700' # Gold

    scatter.set_offsets(np.c_[current_x, current_y])
    scatter.set_color(color)
    
    # Save frame
    frame_path = os.path.join(OUTPUT_DIR, f"frame_{frame:04d}.png")
    plt.savefig(frame_path, dpi=100, bbox_inches='tight', facecolor='black')
    if frame % 20 == 0:
        print(f"Generated frame {frame}/{FRAMES}")

# Generate all frames
print("Starting frame generation...")
for i in range(FRAMES):
    update(i)
print("Frames generated successfully.")
