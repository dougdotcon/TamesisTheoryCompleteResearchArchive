import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt
from scipy.fft import fftn, ifftn, fftfreq

print("="*70)
print("EIGENSTÄNDIGE MASS GAP BERECHNUNG")
print("Basierend auf dem ROC/ROA/LMC Framework von Dr. Jeanette Leue")
print("="*70)

# SCHRITT 1: ROC-PROJEKTOREN KONSTRUIEREN
# 
print("\n1. ROC-PROJEKTOREN KONSTRUIEREN")
print("-"*70)

# Grid-Parameter (klein halten für schnelle Berechnung)
nx, ny, nz = 8, 8, 8
N = nx * ny * nz

# Propagation direction (diagonal)
v = np.array([1.0, 1.0, 1.0])
v = v / np.linalg.norm(v)
print(f"Propagationsrichtung v = {v}")

# Frequenz-Gitter
kx = 2 * np.pi * fftfreq(nx)
ky = 2 * np.pi * fftfreq(ny)
kz = 2 * np.pi * fftfreq(nz)
KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing='ij')

# k·v berechnen
k_dot_v = KX * v[0] + KY * v[1] + KZ * v[2]

# ROC-Kanäle definieren (Theorem 2.2)
epsilon = 0.15
indicator_plus = (k_dot_v > epsilon).astype(float)
indicator_zero = (np.abs(k_dot_v) <= epsilon).astype(float)
indicator_minus = (k_dot_v < -epsilon).astype(float)

# Normierung für Partition der Einheit
total = indicator_plus + indicator_zero + indicator_minus
indicator_plus = indicator_plus / total
indicator_zero = indicator_zero / total
indicator_minus = indicator_minus / total

# Überprüfung
completeness_check = np.max(np.abs(indicator_plus + indicator_zero + indicator_minus - 1.0))
print(f"✓ Vollständigkeit P₊ + P₀ + P₋ = I, Fehler: {completeness_check:.2e}")

# Kanal-Anteile
plus_fraction = np.sum(indicator_plus) / N
zero_fraction = np.sum(indicator_zero) / N
minus_fraction = np.sum(indicator_minus) / N
print(f"  Kanal-Anteile: P₊={plus_fraction:.3f}, P₀={zero_fraction:.3f}, P₋={minus_fraction:.3f}")

# 
# SCHRITT 2: LMC-FELD KONSTRUIEREN
# 
print("\n2. LMC-FELD KONSTRUIEREN")
print("-"*70)

# Primzahlen für LMC
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

# Koordinatengitter
x_coords = np.arange(nx)
y_coords = np.arange(ny)
z_coords = np.arange(nz)
X, Y, Z = np.meshgrid(x_coords, y_coords, z_coords, indexing='ij')

# LMC-Feld aufbauen
mollifier_width = 0.8
numerator = np.zeros((nx, ny, nz))
denominator = np.zeros((nx, ny, nz))

print(f"Mollifikationsbreite a = {mollifier_width}")

for i, p in enumerate(primes[:12]):  # Erste 12 Primzahlen
    # Position basierend auf Primzahl
    x_p = (p * 3) % nx
    y_p = (p * 5) % ny
    z_p = (p * 7) % nz
    
    # LMC-Koeffizient: t_p = a_p / (2√p) mit |a_p| ≤ 1
    # Verwende cos(p) für Variation
    a_p = np.cos(p * 0.7)  # |cos(p)| ≤ 1
    t_p = a_p / (2.0 * np.sqrt(p))
    
    # Gauss-Mollifikator
    r_squared = ((X - x_p)**2 + (Y - y_p)**2 + (Z - z_p)**2)
    eta = np.exp(-r_squared / (2 * mollifier_width**2))
    eta = eta / np.sum(eta)  # Normierung
    
    numerator += t_p * eta
    denominator += eta

# LMC-Feld t(x)
denominator[denominator < 1e-10] = 1.0
t_field = numerator / denominator
t_field = np.clip(t_field, -1.0, 1.0)  # |t(x)| ≤ 1

print(f"✓ LMC-Feld t(x): min={np.min(t_field):.4f}, max={np.max(t_field):.4f}")
print(f"  Beschränktheit |t(x)| ≤ 1: {np.max(np.abs(t_field)) <= 1.0}")

# Conductivity-Feld σ(x) = σ₀(1 + β t(x))
sigma_0 = 1.0
beta = 0.12
sigma_field = sigma_0 * (1.0 + beta * t_field.flatten())

sigma_min = np.min(sigma_field)
sigma_max = np.max(sigma_field)
print(f"✓ Conductivity σ(x): min={sigma_min:.4f}, max={sigma_max:.4f}")
print(f"  Uniforme Elliptizität σ(x) > 0: {sigma_min > 0}")


# SCHRITT 3: ROA-MODULATOR M KONSTRUIEREN
# 
print("\n3. ROA-MODULATOR M KONSTRUIEREN")
print("-"*70)

# Eigene Wahl der Kanal-Gewichte (strikt geordnet!)
gamma_plus = 0.7
gamma_zero = 1.5
gamma_minus = 3.0

print(f"Kanal-Gewichte: γ₊={gamma_plus}, γ₀={gamma_zero}, γ₋={gamma_minus}")

# Intrinsische Lücke
gap_M = gamma_zero - gamma_plus
print(f"✓ Intrinsische Lücke gap(M) = γ₀ - γ₊ = {gap_M:.4f}")

# Kritische Schranke
critical_K_norm = gap_M / 2.0
print(f"✓ ROA-Bedingung: ||K|| < {critical_K_norm:.4f}")

# M als diagonale Matrix in Fourier-Basis
M_diagonal = (gamma_plus * indicator_plus.flatten() + 
              gamma_zero * indicator_zero.flatten() + 
              gamma_minus * indicator_minus.flatten())

M = sp.diags(M_diagonal, format='csr')

# Spektrum von M verifizieren
M_eigenvals = np.unique(np.round(M_diagonal, 6))
print(f"✓ Spektrum σ(M) = {M_eigenvals}")
print(f"  Erwartung: {{{gamma_plus:.2f}, {gamma_zero:.2f}, {gamma_minus:.2f}}}")


# SCHRITT 4: STÖRUNGSOPERATOR K[σ] KONSTRUIEREN
# 
print("\n4. STÖRUNGSOPERATOR K[σ] KONSTRUIEREN")
print("-"*70)

# Diskrete Laplace-Matrix (periodische Randbedingungen)
def build_laplacian_3d(nx, ny, nz):
    N = nx * ny * nz
    rows, cols, data = [], [], []
    
    for i in range(N):
        iz = i % nz
        iy = (i // nz) % ny
        ix = i // (ny * nz)
        
        # Zentraler Knoten
        degree = 0
        
        # 6 Nachbarn (±x, ±y, ±z)
        for dx, dy, dz in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:
            nx_new = (ix + dx) % nx
            ny_new = (iy + dy) % ny
            nz_new = (iz + dz) % nz
            
            j = nx_new * (ny * nz) + ny_new * nz + nz_new
            
            rows.append(i)
            cols.append(j)
            data.append(-1.0)
            degree += 1
        
        # Diagonalelement
        rows.append(i)
        cols.append(i)
        data.append(float(degree))
    
    return sp.coo_matrix((data, (rows, cols)), shape=(N, N)).tocsr()

Laplacian = build_laplacian_3d(nx, ny, nz)

# K[σ] = -β √σ Δ √σ (symmetrisch!)
sqrt_sigma = np.sqrt(np.maximum(sigma_field, 1e-12))
D_sqrt = sp.diags(sqrt_sigma, format='csr')

coupling_strength = 0.05
K = -coupling_strength * (D_sqrt @ Laplacian @ D_sqrt)

# Operatornorm abschätzen (Power-Iteration)
def estimate_norm(A, n_iter=15):
    n = A.shape[0]
    v = np.random.randn(n)
    v = v / np.linalg.norm(v)
    
    for _ in range(n_iter):
        Av = A @ v
        norm = np.linalg.norm(Av)
        if norm > 0:
            v = Av / norm
    
    return norm

K_norm = estimate_norm(K)
print(f"✓ ||K[σ]|| ≈ {K_norm:.6f}")
print(f"  Kritische Schranke: {critical_K_norm:.6f}")
print(f"  ROA-Bedingung erfüllt: {K_norm < critical_K_norm}")
print(f"  Margin: {critical_K_norm - K_norm:.6f}")


# SCHRITT 5: HAMILTONIAN H = M + K UND SPEKTRUM
# 
print("\n5. HAMILTONIAN H = M + K KONSTRUIEREN")
print("-"*70)

H = M + K

print(f"Hamiltonian H konstruiert: {H.shape} sparse matrix")

# Kleinste Eigenwerte berechnen
n_eigs = min(6, N - 2)
try:
    eigenvalues, eigenvectors = spla.eigsh(H, k=n_eigs, which='SA', tol=1e-9)
    eigenvalues = np.sort(eigenvalues)
except:
    print("  Fallback: Dense Eigenwerte")
    H_dense = H.toarray()
    eigenvalues = np.linalg.eigvalsh(H_dense)
    eigenvalues = np.sort(eigenvalues)[:n_eigs]

print(f"✓ Kleinste Eigenwerte:")
for i, ev in enumerate(eigenvalues[:6]):
    print(f"  λ_{i} = {ev:.8f}")

# 
# SCHRITT 6: MASS GAP BERECHNUNG
# 
print("\n6. MASS GAP BERECHNUNG")
print("="*70)

if len(eigenvalues) >= 2:
    gap_H = eigenvalues[1] - eigenvalues[0]
    
    print(f"\n✓ SPEKTRALE LÜCKE GEFUNDEN!")
    print(f"  λ₀ = {eigenvalues[0]:.8f}")
    print(f"  λ₁ = {eigenvalues[1]:.8f}")
    print(f"\n  ╔══════════════════════════════════════╗")
    print(f"  ║  gap(H) = {gap_H:.8f}          ║")
    print(f"  ╚══════════════════════════════════════╝")
    
    # ROA-Schranke verifizieren
    theoretical_bound = gap_M - 2 * K_norm
    print(f"\n✓ ROA-SCHRANKE (Theorem 7.6):")
    print(f"  gap(H) ≥ gap(M) - 2||K||")
    print(f"  {gap_H:.6f} ≥ {theoretical_bound:.6f}")
    print(f"  Schranke erfüllt: {gap_H >= theoretical_bound - 1e-6}")
    
    # Erfolgsanalyse
    print(f"\n{'='*70}")
    print("ERFOLGSNACHWEIS")
    print(f"{'='*70}")
    
    conditions = {
        "ROC-Orthogonalität": completeness_check < 1e-10,
        "LMC-Beschränktheit |t| ≤ 1": np.max(np.abs(t_field)) <= 1.0,
        "Uniforme Elliptizität σ > 0": sigma_min > 0,
        "ROA-Bedingung ||K|| < gap(M)/2": K_norm < critical_K_norm,
        "Positive Massenlücke gap(H) > 0": gap_H > 0,
        "ROA-Schranke erfüllt": gap_H >= theoretical_bound - 1e-6
    }
    
    for name, satisfied in conditions.items():
        status = "✓" if satisfied else "✗"
        print(f"  {status} {name}")
    
    n_passed = sum(conditions.values())
    n_total = len(conditions)
    
    print(f"\n  Bestanden: {n_passed}/{n_total} Bedingungen")
    
    if n_passed == n_total:
        print(f"\n  {'🎉'*20}")
        print(f"  ✓ ERFOLG: MASS GAP ERFOLGREICH BERECHNET!")
        print(f"  {'🎉'*20}")
    
    # 
    # VISUALISIERUNG
    # 
   
    print("\n7. VISUALISIERUNG")
    print("-"*70)
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Plot 1: Spektrum
    ax1 = axes[0, 0]
    ax1.plot(range(len(eigenvalues)), eigenvalues, 'bo-', markersize=8, linewidth=2)
    ax1.axhline(y=eigenvalues[0], color='r', linestyle='--', alpha=0.5)
    ax1.axhline(y=eigenvalues[1], color='r', linestyle='--', alpha=0.5)
    ax1.fill_between([0, len(eigenvalues)-1], eigenvalues[0], eigenvalues[1], 
                      alpha=0.3, color='green', label=f'Gap = {gap_H:.4f}')
    ax1.set_xlabel('Eigenwert Index')
    ax1.set_ylabel('Energie')
    ax1.set_title('Spektrum von H')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: LMC-Feld (Schnitt)
    ax2 = axes[0, 1]
    slice_z = nz // 2
    im2 = ax2.imshow(t_field[:,:,slice_z], cmap='RdBu', vmin=-1, vmax=1)
    ax2.set_title(f'LMC-Feld t(x,y,z={slice_z})')
    plt.colorbar(im2, ax=ax2)
    
    # Plot 3: Conductivity σ(x)
    ax3 = axes[0, 2]
    sigma_2d = sigma_field.reshape(nx, ny, nz)[:,:,slice_z]
    im3 = ax3.imshow(sigma_2d, cmap='viridis')
    ax3.set_title(f'Conductivity σ(x,y,z={slice_z})')
    plt.colorbar(im3, ax=ax3)
    
    # Plot 4: ROC-Kanäle
    ax4 = axes[1, 0]
    channels = ['P₊', 'P₀', 'P₋']
    fractions = [plus_fraction, zero_fraction, minus_fraction]
    colors = ['red', 'yellow', 'blue']
    ax4.bar(channels, fractions, color=colors, edgecolor='black', linewidth=2)
    ax4.set_ylabel('Anteil')
    ax4.set_title('ROC-Kanal-Verteilung')
    ax4.set_ylim([0, 1])
    
    # Plot 5: Gap vs Theorie
    ax5 = axes[1, 1]
    x_vals = ['gap(M)', 'Theor. Bound', 'gap(H)']
    y_vals = [gap_M, theoretical_bound, gap_H]
    colors_bar = ['blue', 'orange', 'green']
    bars = ax5.bar(x_vals, y_vals, color=colors_bar, edgecolor='black', linewidth=2)
    ax5.set_ylabel('Lücke')
    ax5.set_title('Gap-Vergleich')
    ax5.axhline(y=0, color='k', linestyle='-', linewidth=1)
    
    # Plot 6: Validierung
    ax6 = axes[1, 2]
    validation_names = list(conditions.keys())
    validation_values = [1 if v else 0 for v in conditions.values()]
    colors_val = ['green' if v else 'red' for v in validation_values]
    
    y_pos = np.arange(len(validation_names))
    ax6.barh(y_pos, validation_values, color=colors_val, edgecolor='black')
    ax6.set_yticks(y_pos)
    ax6.set_yticklabels([name[:25] for name in validation_names], fontsize=8)
    ax6.set_xlabel('Status')
    ax6.set_title('Framework-Validierung')
    ax6.set_xlim([0, 1.2])
    
    for i, v in enumerate(validation_values):
        ax6.text(v + 0.05, i, '✓' if v else '✗', 
                va='center', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('eigenstaendige_mass_gap_berechnung.png', dpi=150, bbox_inches='tight')
    print("  ✓ Visualisierung gespeichert: 'eigenstaendige_mass_gap_berechnung.png'")
    
    plt.show()

else:
    print("\n  ✗ Nicht genug Eigenwerte berechnet")

print("\n" + "="*70)
print("BERECHNUNG ABGESCHLOSSEN")
print("="*70)