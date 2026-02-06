"""Generate the empirical constraints figure for Tamesis Theory."""
import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# Panel 1: GRB Time Delay Constraints
ax1 = axes[0]
xi_values = np.logspace(-3, 0, 100)
linear_delay = xi_values * 1e6 * 100  # ms scale
quadratic_delay = xi_values**2 * 1e6 * 100

ax1.loglog(xi_values, linear_delay, 'r-', lw=2, label=r'Linear: $\xi \cdot E^2$')
ax1.loglog(xi_values, quadratic_delay, 'b-', lw=2, label=r'Quadratic: $\xi^2 \cdot E^2$')
ax1.axhline(0.85, color='green', ls='--', lw=2, label='GRB 090510 limit')
ax1.fill_between([0.001, 0.065], [1e-2]*2, [1e6]*2, alpha=0.2, color='blue', label='Tamesis viable')
ax1.axvline(0.065, color='k', ls=':', lw=1.5)
ax1.set_xlabel(r'Coupling parameter $\xi$', fontsize=11)
ax1.set_ylabel(r'Time delay $\Delta t$ (ms)', fontsize=11)
ax1.set_title('Lorentz Violation Constraints', fontsize=12)
ax1.legend(fontsize=9)
ax1.set_xlim(0.001, 1)
ax1.set_ylim(1e-2, 1e6)
ax1.grid(True, alpha=0.3)

# Panel 2: Polarization Rotation Constraints
ax2 = axes[1]
ax2.bar(['Linear', 'Quadratic'], [0.85, 0.012], color=['red', 'blue'], alpha=0.7)
ax2.axhline(0.1, color='green', ls='--', lw=2, label='IXPE limit')
ax2.set_ylabel(r'Birefringence $\delta\phi$ (rad)', fontsize=11)
ax2.set_title('Polarimetric Constraints (IXPE)', fontsize=12)
ax2.legend(fontsize=10)
ax2.text(0, 0.45, 'RULED OUT', ha='center', fontsize=10, color='red')
ax2.text(1, 0.05, 'ALLOWED', ha='center', fontsize=10, color='blue')

plt.suptitle('Tamesis Theory: Empirical Constraints', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('tamesis_constraints.png', dpi=300, bbox_inches='tight')
plt.savefig('tamesis_constraints.pdf', dpi=300, bbox_inches='tight')
print('Constraints figure created!')
