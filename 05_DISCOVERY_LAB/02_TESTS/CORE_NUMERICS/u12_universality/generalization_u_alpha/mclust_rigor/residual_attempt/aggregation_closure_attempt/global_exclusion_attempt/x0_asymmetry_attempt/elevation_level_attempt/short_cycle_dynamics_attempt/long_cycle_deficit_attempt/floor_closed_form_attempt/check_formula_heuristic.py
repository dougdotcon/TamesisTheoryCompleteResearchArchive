import numpy as np

def phi_t0(t0, c):
    beta = c / t0
    disc = c**2 + 4*beta
    sq = np.sqrt(disc)
    s1 = (-c + sq)/2
    s2 = (-c - sq)/2
    g = t0
    # Phi(g) = [s1 e^{s1 g} - s2 e^{s2 g}] / (s1-s2)
    return (s1*np.exp(s1*g) - s2*np.exp(s2*g)) / (s1 - s2)

c = 1000
for t0 in [1/65536, 25/65536, 125/65536, 350/65536, 750/65536, 1500/65536, 3000/65536,
           6000/65536, 12000/65536, 24500/65536, 49000/65536]:
    print(f"t0={t0:.6f} (L={t0*65536:.0f})  Phi_predicted={phi_t0(t0,c):.5f}")

print()
print("phi_U(c) via naive continuum avg check: integral_0^1 Phi(t0) dt0 -- numeric")
ts = np.linspace(1e-6, 1, 200000)
vals = phi_t0(ts, c)
print("numeric avg:", np.trapz(vals, ts))
import math
from scipy.special import erf
print("phi_U(1000) formula:", (np.sqrt(np.pi)/(2*np.sqrt(c)))*erf(np.sqrt(c)))
