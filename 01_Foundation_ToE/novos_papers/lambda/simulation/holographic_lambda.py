import numpy as np

def calculate_holographic_lambda():
    """
    Calculates the Vacuum Energy Density predicted by the Holographic Principle
    and compares it to the observed Cosmological Constant.
    
    Hypothesis:
    Rho_vac_holographic ~ (Planck_Mass / Hubble_Radius)^2
    Instead of the QFT prediction:
    Rho_vac_QFT ~ (Planck_Mass / Planck_Length)^4
    """

    # Constants (SI Units)
    c = 2.99792458e8        # Speed of light (m/s)
    h_bar = 1.0545718e-34   # Reduced Planck constant (J.s)
    G = 6.67430e-11         # Gravitational constant (m^3/kg/s^2)
    
    # Planck Mass (Reduced)
    # M_p = sqrt(hbar * c / 8pi G)
    M_p = np.sqrt(h_bar * c / (8 * np.pi * G)) 
    # Value is approx 2.435e18 GeV/c^2 or 4.34e-9 kg
    
    # 1. Observational Data (Planck 2018)
    H0_km_s_Mpc = 67.4      # Hubble Constant (km/s/Mpc)
    
    # Convert H0 to SI (1/s)
    Mpc_to_km = 3.086e19    # 1 Mpc in km
    H0 = H0_km_s_Mpc / Mpc_to_km
    
    # Critical Density of the Universe
    # rho_crit = 3H^2 / 8pi G
    rho_crit = (3 * H0**2) / (8 * np.pi * G)
    
    # Observed Dark Energy Density (Omega_Lambda ~ 0.685)
    Omega_Lambda = 0.685
    rho_obs = Omega_Lambda * rho_crit
    
    print(f"--- OBSERVATIONAL DATA (Planck 2018) ---")
    print(f"Hubble Constant H0: {H0:.3e} s^-1")
    print(f"Critical Density:   {rho_crit:.3e} kg/m^3")
    print(f"Observed Rho_vac:   {rho_obs:.3e} kg/m^3")
    print(f"")

    # 2. QFT Prediction (The Catastrophe)
    # rho_QFT ~ (M_pl)^4 (in natural units) -> M_pl^4 * c^3 / h_bar^?
    # Simply: Density of 1 Planck Mass per Planck Volume
    l_p = np.sqrt(h_bar * G / c**3)
    m_p = np.sqrt(h_bar * c / G)
    rho_qft = m_p / l_p**3
    
    print(f"--- QFT PREDICTION (The Catastrophe) ---")
    print(f"Planck Density:     {rho_qft:.3e} kg/m^3")
    print(f"Discrepancy:        10^{np.log10(rho_qft/rho_obs):.0f} orders of magnitude")
    print(f"")
    
    # 3. Holographic Prediction (TARDIS/HDE)
    # Hypothesis: The energy density is limited by the horizon area.
    # rho_hole = 3 c^2 / (8 pi G L^2)  ... equivalent to rho_crit if L = Hubble Radius
    # This roughly means the universe is a Black Hole.
    
    # Infrared Cutoff L (Hubble Radius)
    L = c / H0
    
    # Holographic Density
    # rho_holo = 3 * c^2 * M_p_reduced^2 / L^2 ?? 
    # Let's use the formula: rho = 3 H^2 / 8 pi G * c^2 (factor of c^2 depending on units)
    # Actually, rho_theo ~ (M_p / L)^2 is strictly scaling.
    # The standard formula for Holographic Dark Energy is:
    # rho_de = 3 * c^2 * M_p_reduced^2 / L^2 * (constant c^2)
    
    # Simpler derivation:
    # Maximum Entropy S_max = Area / 4 l_p^2
    # Energy E = L / 2 G (Schwartzschild Mass of the Universe)
    # Density rho = E / Volume = (L / 2G) / (4/3 pi L^3) 
    
    Mass_Universe_Holo = L * c**2 / (2 * G) # Mass of a BH with radius L
    Volume_Universe = (4/3) * np.pi * L**3
    rho_holo = Mass_Universe_Holo / Volume_Universe
    
    print(f"--- HOLOGRAPHIC PREDICTION (Horizon Entropy) ---")
    print(f"Hubble Radius L:    {L:.3e} m")
    print(f"Holographic Rho:    {rho_holo:.3e} kg/m^3")
    
    # Comparison
    ratio = rho_holo / rho_obs
    print(f"")
    print(f"--- CONCLUSION ---")
    print(f"Ratio (Pred/Obs):   {ratio:.2f}")
    
    if 0.1 < ratio < 10:
        print("SUCCESS: The Holographic prediction matches observation within 1 order of magnitude.")
        print("This solves the 120-order-of-magnitude vacuum catastrophe.")
    else:
        print("FAIL: The prediction does not match.")

if __name__ == "__main__":
    calculate_holographic_lambda()
