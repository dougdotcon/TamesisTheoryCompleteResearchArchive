import numpy as np
import matplotlib.pyplot as plt
from reactive_gravity import ReactiveGravity
import os

# Configuration
N_STARS = 500
T_MAX_GYR = 2.0
DT = 0.01 # Gyr
FRAMES_DIR = "frames/galactic"
os.makedirs(FRAMES_DIR, exist_ok=True)

class GalacticAnimator:
    def __init__(self):
        # 1. Setup Gravity
        self.grav = ReactiveGravity(a0=1.2e-10) 
        self.M_gal_sol = 1e11
        self.M_gal_kg = self.M_gal_sol * 1.989e30
        
        # Units
        self.KPC_TO_M = 3.086e19
        self.GYR_TO_S = 3.154e16
        self.KM_TO_M = 1000.0
        
        # 2. Init Particles (Exponential Disk)
        Rd = 3.0 # kpc
        self.pos_kpc = []
        while len(self.pos_kpc) < N_STARS:
            test_r = np.random.uniform(0.1, 15)
            prob = test_r * np.exp(-test_r/Rd)
            if np.random.uniform(0, 1.5) < prob:
                theta = np.random.uniform(0, 2*np.pi)
                x = test_r * np.cos(theta)
                y = test_r * np.sin(theta)
                self.pos_kpc.append([x, y, 0.0])
        self.pos_kpc = np.array(self.pos_kpc)
        
        # 3. Init Velocities (Circular)
        self.vel_kms = np.zeros_like(self.pos_kpc)
        for i in range(N_STARS):
            r_vec = self.pos_kpc[i]
            r_kpc = np.linalg.norm(r_vec)
            if r_kpc < 0.1: continue
            
            # Use ReactiveGravity to get V (km/s)
            r_m = r_kpc * self.KPC_TO_M
            # calculate_velocity returns km/s
            v_circ = self.grav.calculate_velocity(self.M_gal_kg, r_m)
            
            # Tangent
            tangent = np.array([-r_vec[1], r_vec[0], 0])
            tangent = tangent / np.linalg.norm(tangent)
            
            self.vel_kms[i] = tangent * v_circ

    def run(self):
        print(f"🎥 Rendering Galactic Dynamics ({N_STARS} stars)...")
        t = 0.0
        step = 0
        frame_idx = 0
        
        while t < T_MAX_GYR:
            # 1. Update Position (Half Step for Leapfrog? Or Euler for sim)
            # dx (kpc) = v (km/s) * dt (Gyr) * conversion
            # 1 (km/s) * 1 Gyr = (1e3 m/s) * (3.15e16 s) = 3.15e19 m
            # in kpc: 3.15e19 / 3.08e19 ~ 1.022 kpc
            K_vel_to_pos = (self.KM_TO_M * self.GYR_TO_S) / self.KPC_TO_M # ~1.022
            
            self.pos_kpc += self.vel_kms * DT * K_vel_to_pos
            
            # 2. Update Velocity
            # dv (km/s) = a (m/s^2) * dt (Gyr) * conversion
            # a comes from self.grav.calculate_effective_acceleration (m/s^2)
            
            r_kpc = np.linalg.norm(self.pos_kpc, axis=1, keepdims=True)
            mask = (r_kpc > 0.1).flatten() # Flatten for indexing
            
            # Get Force Magnitude
            # Vectorize call? No, class is scalar. Loop or implement array ops in class?
            # Class uses numpy, so array ops might work if inputs are arrays.
            # let's try array inputs
            r_m = r_kpc * self.KPC_TO_M
            g_eff_ms2 = self.grav.calculate_effective_acceleration(self.M_gal_kg, r_m)
            
            # Direction
            acc_dir = -self.pos_kpc / r_kpc
            acc_vec_ms2 = acc_dir * g_eff_ms2
            
            # Convert acc to delta_v_kms
            # dv (km/s) = acc (m/s^2) * dt (Gyr) * (GYR_TO_S) / 1000
            K_acc_to_vel = self.GYR_TO_S / 1000.0
            
            self.vel_kms[mask] += acc_vec_ms2[mask] * DT * K_acc_to_vel
            
            t += DT
            step += 1
            
            if step % 5 == 0:
                self.plot_frame(frame_idx, t)
                frame_idx += 1
                
    def plot_frame(self, idx, t):
        plt.figure(figsize=(6, 6), dpi=100)
        plt.style.use('dark_background')
        plt.scatter(self.pos_kpc[:,0], self.pos_kpc[:,1], s=2, c='cyan', alpha=0.7)
        plt.xlim(-20, 20)
        plt.ylim(-20, 20)
        plt.title(f"Reactive Galactic Dynamics t={t:.2f} Gyr")
        plt.tight_layout()
        plt.savefig(f"{FRAMES_DIR}/frame_{idx:03d}.png")
        plt.close()

if __name__ == "__main__":
    anim = GalacticAnimator()
    anim.run()
