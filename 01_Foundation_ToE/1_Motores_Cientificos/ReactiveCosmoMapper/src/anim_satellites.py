from satellite_plane import SatelliteDynamics
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import os

FRAMES_DIR = "frames/satellites"
os.makedirs(FRAMES_DIR, exist_ok=True)

class SatelliteAnimator(SatelliteDynamics):
    def run_animation(self, t_gyr=5.0):
        print("🎥 Rendering Satellite Plane Formation...")
        
        # Init
        r_scale = 100.0
        u_rand = np.random.uniform(0, 1, self.N)
        v_rand = np.random.uniform(0, 1, self.N)
        theta = 2 * np.pi * u_rand
        phi = np.arccos(2 * v_rand - 1)
        x = r_scale * np.sin(phi) * np.cos(theta)
        y = r_scale * np.sin(phi) * np.sin(theta)
        z = r_scale * np.cos(phi)
        
        # Pos and Vel
        pos = np.column_stack([x,y,z])
        vel = np.zeros_like(pos)
        
        # G Calculation for Init
        g_int_at_r = self.G * self.M_sol / (r_scale**2)
        self.g_ext_mag = g_int_at_r * 0.3 # Strong EFE
        
        # Tangential velocities
        for i in range(self.N):
            p = pos[i]
            v_mag = 150.0 
            rand_v = np.random.randn(3)
            tangent = np.cross(p, rand_v)
            tangent = tangent / np.linalg.norm(tangent) * v_mag
            vel[i] = tangent
            
        # Integration Loop (Manual Leapfrog for easy plotting)
        dt = 0.05
        t = 0.0
        frame_idx = 0
        
        # Integration constant K for units (see anim_galactic)
        K = 1.022 
        
        while t < t_gyr:
            # Drift
            pos += vel * dt * K
            
            # Kick
            acc = self.relative_acceleration(pos, model='reactive')
            vel += acc * dt * K
            
            t += dt
            
            # Plot
            self.plot_frame(pos, frame_idx, t)
            frame_idx += 1
            
    def plot_frame(self, pos, idx, t):
        fig = plt.figure(figsize=(10, 6), dpi=80)
        plt.style.use('dark_background')
        
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(pos[:,0], pos[:,1], pos[:,2], c='orange', s=10)
        
        # Draw Ext Field Arrow
        ax.quiver(0, 0, 0, 0, 0, 100, color='red', length=1.0, pivot='tail')
        
        ax.set_xlim(-150, 150)
        ax.set_ylim(-150, 150)
        ax.set_zlim(-150, 150)
        ax.set_title(f"Satellite Plane Evolution (EFE) t={t:.2f} Gyr")
        
        plt.savefig(f"{FRAMES_DIR}/frame_{idx:03d}.png")
        plt.close()

if __name__ == "__main__":
    anim = SatelliteAnimator(n_satellites=100)
    anim.run_animation()
