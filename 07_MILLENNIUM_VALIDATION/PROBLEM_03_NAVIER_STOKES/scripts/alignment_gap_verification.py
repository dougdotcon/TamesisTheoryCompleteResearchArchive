"""
ALIGNMENT GAP NUMERICAL VERIFICATION
=====================================
Verificação numérica do gap de alinhamento ω-S para Navier-Stokes

Este script simula um campo de vorticidade simplificado e mede:
1. O alinhamento médio ⟨α₁⟩_Ω = ⟨cos²(ω, e₁)⟩ pesado por |ω|²
2. A distribuição de α₁ nas regiões de alta vorticidade
3. A correlação entre |ω| e desalinhamento

Tamesis Kernel v3.1 — Janeiro 29, 2026
"""

import numpy as np
from scipy.linalg import eigh
from scipy.fft import fftn, ifftn
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# =============================================================================
# PARÂMETROS DA SIMULAÇÃO
# =============================================================================

N = 64           # Resolução (N³ grid)
L = 2 * np.pi    # Tamanho do domínio
nu = 0.01        # Viscosidade
dt = 0.001       # Timestep
T_max = 1.0      # Tempo total
output_every = 100  # Frequência de output

# Grid
x = np.linspace(0, L, N, endpoint=False)
dx = L / N
X, Y, Z = np.meshgrid(x, x, x, indexing='ij')

# Wavenumbers
k = np.fft.fftfreq(N, d=dx) * 2 * np.pi
KX, KY, KZ = np.meshgrid(k, k, k, indexing='ij')
K2 = KX**2 + KY**2 + KZ**2
K2[0, 0, 0] = 1  # Avoid division by zero

# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

def curl(u):
    """Calcula vorticidade ω = ∇ × u"""
    ux, uy, uz = u
    
    # Derivadas espectrais
    ux_hat = fftn(ux)
    uy_hat = fftn(uy)
    uz_hat = fftn(uz)
    
    # ω_x = ∂uz/∂y - ∂uy/∂z
    omega_x = np.real(ifftn(1j * KY * uz_hat - 1j * KZ * uy_hat))
    # ω_y = ∂ux/∂z - ∂uz/∂x
    omega_y = np.real(ifftn(1j * KZ * ux_hat - 1j * KX * uz_hat))
    # ω_z = ∂uy/∂x - ∂ux/∂y
    omega_z = np.real(ifftn(1j * KX * uy_hat - 1j * KY * ux_hat))
    
    return np.array([omega_x, omega_y, omega_z])

def gradient(f):
    """Calcula gradiente ∇f"""
    f_hat = fftn(f)
    df_dx = np.real(ifftn(1j * KX * f_hat))
    df_dy = np.real(ifftn(1j * KY * f_hat))
    df_dz = np.real(ifftn(1j * KZ * f_hat))
    return np.array([df_dx, df_dy, df_dz])

def strain_tensor(u):
    """
    Calcula tensor de strain S = (∇u + ∇uᵀ)/2
    Retorna componentes S_ij para cada ponto do grid
    """
    ux, uy, uz = u
    
    # Gradientes
    grad_ux = gradient(ux)  # [∂ux/∂x, ∂ux/∂y, ∂ux/∂z]
    grad_uy = gradient(uy)
    grad_uz = gradient(uz)
    
    # S_ij = (∂ui/∂xj + ∂uj/∂xi)/2
    S = np.zeros((3, 3, N, N, N))
    
    # Diagonal
    S[0, 0] = grad_ux[0]
    S[1, 1] = grad_uy[1]
    S[2, 2] = grad_uz[2]
    
    # Off-diagonal
    S[0, 1] = S[1, 0] = 0.5 * (grad_ux[1] + grad_uy[0])
    S[0, 2] = S[2, 0] = 0.5 * (grad_ux[2] + grad_uz[0])
    S[1, 2] = S[2, 1] = 0.5 * (grad_uy[2] + grad_uz[1])
    
    return S

def compute_alignment_stats(omega, S):
    """
    Calcula estatísticas de alinhamento ω-S
    
    Returns:
        alpha_1_weighted: ⟨cos²(ω, e₁)⟩ pesado por |ω|²
        alpha_2_weighted: ⟨cos²(ω, e₂)⟩ pesado por |ω|²
        alpha_3_weighted: ⟨cos²(ω, e₃)⟩ pesado por |ω|²
        omega_mag_max: |ω|_max
        enstrophy: Ω = (1/2)∫|ω|² dx
    """
    omega_mag2 = omega[0]**2 + omega[1]**2 + omega[2]**2
    omega_mag = np.sqrt(omega_mag2 + 1e-10)  # Avoid division by zero
    
    # Normalizar direção
    omega_hat = omega / (omega_mag + 1e-10)
    
    # Arrays para armazenar α_i
    alpha_1 = np.zeros((N, N, N))
    alpha_2 = np.zeros((N, N, N))
    alpha_3 = np.zeros((N, N, N))
    
    # Calcular autovalores e autovetores para cada ponto
    # (Isso é lento, mas correto)
    for i in range(N):
        for j in range(N):
            for k in range(N):
                S_local = S[:, :, i, j, k]
                
                # Autovalores e autovetores (ordenados crescente)
                eigenvalues, eigenvectors = eigh(S_local)
                
                # Reordenar para λ₁ ≥ λ₂ ≥ λ₃
                idx = np.argsort(eigenvalues)[::-1]
                eigenvalues = eigenvalues[idx]
                eigenvectors = eigenvectors[:, idx]
                
                e1 = eigenvectors[:, 0]
                e2 = eigenvectors[:, 1]
                e3 = eigenvectors[:, 2]
                
                omega_hat_local = omega_hat[:, i, j, k]
                
                alpha_1[i, j, k] = np.dot(omega_hat_local, e1)**2
                alpha_2[i, j, k] = np.dot(omega_hat_local, e2)**2
                alpha_3[i, j, k] = np.dot(omega_hat_local, e3)**2
    
    # Peso por |ω|²
    total_weight = np.sum(omega_mag2) * dx**3
    
    if total_weight < 1e-10:
        return 1/3, 1/3, 1/3, 0, 0
    
    alpha_1_weighted = np.sum(alpha_1 * omega_mag2) * dx**3 / total_weight
    alpha_2_weighted = np.sum(alpha_2 * omega_mag2) * dx**3 / total_weight
    alpha_3_weighted = np.sum(alpha_3 * omega_mag2) * dx**3 / total_weight
    
    enstrophy = 0.5 * total_weight
    omega_max = np.max(omega_mag)
    
    return alpha_1_weighted, alpha_2_weighted, alpha_3_weighted, omega_max, enstrophy

def initial_velocity_taylor_green():
    """
    Condição inicial Taylor-Green modificada para 3D
    """
    A = 1.0
    ux = A * np.sin(X) * np.cos(Y) * np.cos(Z)
    uy = -A * np.cos(X) * np.sin(Y) * np.cos(Z)
    uz = np.zeros_like(X)
    return np.array([ux, uy, uz])

def project_divergence_free(u_hat):
    """
    Projeção de Leray: remove componente com divergência
    u → u - ∇(∇⁻²(∇·u))
    """
    ux_hat, uy_hat, uz_hat = u_hat
    
    # Divergência em Fourier
    div_hat = 1j * (KX * ux_hat + KY * uy_hat + KZ * uz_hat)
    
    # Pressão (Poisson)
    p_hat = -div_hat / K2
    p_hat[0, 0, 0] = 0
    
    # Subtrair gradiente de pressão
    ux_hat_new = ux_hat - 1j * KX * p_hat
    uy_hat_new = uy_hat - 1j * KY * p_hat
    uz_hat_new = uz_hat - 1j * KZ * p_hat
    
    return np.array([ux_hat_new, uy_hat_new, uz_hat_new])

def ns_rhs(u):
    """
    Lado direito de Navier-Stokes: -u·∇u + ν∇²u
    (projetado para ser divergence-free)
    """
    ux, uy, uz = u
    
    # Convecção: (u·∇)u
    grad_ux = gradient(ux)
    grad_uy = gradient(uy)
    grad_uz = gradient(uz)
    
    conv_x = ux * grad_ux[0] + uy * grad_ux[1] + uz * grad_ux[2]
    conv_y = ux * grad_uy[0] + uy * grad_uy[1] + uz * grad_uy[2]
    conv_z = ux * grad_uz[0] + uy * grad_uz[1] + uz * grad_uz[2]
    
    # Difusão em Fourier
    u_hat = np.array([fftn(ux), fftn(uy), fftn(uz)])
    diff_hat = -nu * K2 * u_hat
    
    # RHS em físico (sem pressão ainda)
    rhs_x = -conv_x + np.real(ifftn(diff_hat[0]))
    rhs_y = -conv_y + np.real(ifftn(diff_hat[1]))
    rhs_z = -conv_z + np.real(ifftn(diff_hat[2]))
    
    rhs = np.array([rhs_x, rhs_y, rhs_z])
    
    # Projetar para divergence-free
    rhs_hat = np.array([fftn(rhs_x), fftn(rhs_y), fftn(rhs_z)])
    rhs_hat = project_divergence_free(rhs_hat)
    
    rhs = np.real(np.array([ifftn(rhs_hat[0]), ifftn(rhs_hat[1]), ifftn(rhs_hat[2])]))
    
    return rhs

# =============================================================================
# SIMULAÇÃO PRINCIPAL
# =============================================================================

def run_simulation():
    """
    Executa simulação de NS e coleta estatísticas de alinhamento
    """
    print("="*70)
    print("VERIFICAÇÃO NUMÉRICA DO GAP DE ALINHAMENTO")
    print("Tamesis Kernel v3.1 — Navier-Stokes Attack")
    print("="*70)
    print(f"\nParâmetros: N={N}, ν={nu}, dt={dt}, T_max={T_max}")
    print("\nIniciando simulação...")
    
    # Condição inicial
    u = initial_velocity_taylor_green()
    
    # Arrays para armazenar resultados
    times = []
    alpha_1_history = []
    alpha_2_history = []
    alpha_3_history = []
    omega_max_history = []
    enstrophy_history = []
    
    # Loop temporal
    n_steps = int(T_max / dt)
    
    for step in range(n_steps + 1):
        t = step * dt
        
        # Output periódico
        if step % output_every == 0:
            omega = curl(u)
            S = strain_tensor(u)
            alpha_1, alpha_2, alpha_3, omega_max, enstrophy = compute_alignment_stats(omega, S)
            
            times.append(t)
            alpha_1_history.append(alpha_1)
            alpha_2_history.append(alpha_2)
            alpha_3_history.append(alpha_3)
            omega_max_history.append(omega_max)
            enstrophy_history.append(enstrophy)
            
            print(f"t = {t:.3f}: α₁ = {alpha_1:.4f}, α₂ = {alpha_2:.4f}, "
                  f"α₃ = {alpha_3:.4f}, |ω|_max = {omega_max:.2f}, Ω = {enstrophy:.4f}")
        
        # Integração temporal (Euler explícito simples)
        if step < n_steps:
            rhs = ns_rhs(u)
            u = u + dt * rhs
            
            # Re-projetar para garantir divergence-free
            u_hat = np.array([fftn(u[0]), fftn(u[1]), fftn(u[2])])
            u_hat = project_divergence_free(u_hat)
            u = np.real(np.array([ifftn(u_hat[0]), ifftn(u_hat[1]), ifftn(u_hat[2])]))
    
    return (times, alpha_1_history, alpha_2_history, alpha_3_history, 
            omega_max_history, enstrophy_history)

def analyze_results(times, alpha_1_history, alpha_2_history, alpha_3_history,
                   omega_max_history, enstrophy_history):
    """
    Analisa e plota resultados
    """
    print("\n" + "="*70)
    print("ANÁLISE DOS RESULTADOS")
    print("="*70)
    
    alpha_1_mean = np.mean(alpha_1_history)
    alpha_2_mean = np.mean(alpha_2_history)
    alpha_3_mean = np.mean(alpha_3_history)
    
    print(f"\nMÉDIAS TEMPORAIS:")
    print(f"  ⟨α₁⟩ = {alpha_1_mean:.4f} (alinhamento com e₁, máximo stretching)")
    print(f"  ⟨α₂⟩ = {alpha_2_mean:.4f} (alinhamento com e₂, intermediário)")
    print(f"  ⟨α₃⟩ = {alpha_3_mean:.4f} (alinhamento com e₃, compressão máxima)")
    
    # Verificar gap
    gap = 1 - alpha_1_mean
    print(f"\nGAP DE ALINHAMENTO: δ = 1 - ⟨α₁⟩ = {gap:.4f}")
    
    if gap > 0.1:
        print("✅ GAP SIGNIFICATIVO DETECTADO!")
        print("   ω NÃO se alinha perfeitamente com e₁")
        print("   Isso suporta a tese de auto-regularização")
    else:
        print("⚠️ Gap pequeno - pode indicar problema numérico ou regime especial")
    
    # Verificar preferência por e₂
    if alpha_2_mean > alpha_1_mean and alpha_2_mean > alpha_3_mean:
        print("\n✅ PREFERÊNCIA POR e₂ DETECTADA!")
        print("   Consistente com DNS (Ashurst 1987, Tsinober 2009)")
    
    # Plotar
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot 1: Alinhamentos
    ax1 = axes[0, 0]
    ax1.plot(times, alpha_1_history, 'r-', label=r'$\alpha_1 = \cos^2(\omega, e_1)$')
    ax1.plot(times, alpha_2_history, 'g-', label=r'$\alpha_2 = \cos^2(\omega, e_2)$')
    ax1.plot(times, alpha_3_history, 'b-', label=r'$\alpha_3 = \cos^2(\omega, e_3)$')
    ax1.axhline(1/3, color='k', linestyle='--', alpha=0.5, label='Isotrópico (1/3)')
    ax1.set_xlabel('Tempo')
    ax1.set_ylabel(r'$\langle \alpha_i \rangle_\Omega$')
    ax1.set_title('Estatísticas de Alinhamento ω-S')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Vorticidade máxima
    ax2 = axes[0, 1]
    ax2.plot(times, omega_max_history, 'k-')
    ax2.set_xlabel('Tempo')
    ax2.set_ylabel(r'$\|\omega\|_\infty$')
    ax2.set_title('Vorticidade Máxima')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Enstrofia
    ax3 = axes[1, 0]
    ax3.plot(times, enstrophy_history, 'purple')
    ax3.set_xlabel('Tempo')
    ax3.set_ylabel(r'$\Omega = \frac{1}{2}\|\omega\|_{L^2}^2$')
    ax3.set_title('Enstrofia')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Gap de alinhamento
    ax4 = axes[1, 1]
    gap_history = 1 - np.array(alpha_1_history)
    ax4.plot(times, gap_history, 'orange')
    ax4.axhline(np.mean(gap_history), color='r', linestyle='--', 
                label=f'Média = {np.mean(gap_history):.3f}')
    ax4.set_xlabel('Tempo')
    ax4.set_ylabel(r'Gap $= 1 - \alpha_1$')
    ax4.set_title('Gap de Alinhamento (Deve ser > 0)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('alignment_gap_verification.png', dpi=150)
    plt.show()
    
    print("\n" + "="*70)
    print("CONCLUSÃO")
    print("="*70)
    print(f"""
O gap de alinhamento médio é δ = {gap:.4f}

INTERPRETAÇÃO PARA NAVIER-STOKES:
- Se δ > 0 uniformemente → stretching efetivo < máximo
- Stretching reduzido → enstrofia controlada
- Enstrofia controlada → regularidade global

EVIDÊNCIA NUMÉRICA:
- α₁ ≈ {alpha_1_mean:.2f} (esperado ~0.15 em DNS)
- α₂ ≈ {alpha_2_mean:.2f} (esperado ~0.50 em DNS)  
- α₃ ≈ {alpha_3_mean:.2f} (esperado ~0.35 em DNS)

STATUS: {'✅ SUPORTA A TESE' if gap > 0.1 else '⚠️ VERIFICAR'}
""")

# =============================================================================
# EXECUÇÃO
# =============================================================================

if __name__ == "__main__":
    results = run_simulation()
    analyze_results(*results)
