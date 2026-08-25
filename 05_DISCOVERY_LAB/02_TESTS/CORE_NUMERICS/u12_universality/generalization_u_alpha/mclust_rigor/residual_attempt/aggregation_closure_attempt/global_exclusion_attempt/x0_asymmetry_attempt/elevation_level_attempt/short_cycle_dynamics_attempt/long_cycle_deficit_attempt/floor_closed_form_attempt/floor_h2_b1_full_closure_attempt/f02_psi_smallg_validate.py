"""
f02_psi_smallg_validate.py -- direct Monte Carlo test of the g->0 closed
form for Psi(s,g) derived in f01 (Part B): Psi(s,g) = g*psi1(s) + g^2*b2(s) +
O(g^3), with psi1(s)=sqrt(pi c/2) erfcx(s sqrt(c/2)) in EXACT closed form and
b2(s) computed via one numerical quadrature layer.

Seeds: SeedSequence(20260856000) (this front's reserved range,
20260856000+, confirmed unused via grep before this dispatch).
"""
import numpy as np
import json
from scipy.special import erfcx
from scipy import integrate
import sys, time

sys.path.insert(0, ".")
from abstract_proc import psi_hat

C = 1000.0


def psi1(sv):
    return np.sqrt(np.pi * C / 2.0) * erfcx(sv * np.sqrt(C / 2.0))


def f2_of_sigma(sigma, a1):
    return -C * a1 / 2.0 + C * psi1(sigma)


def b2_of_s(sv, a1, upper=None):
    if upper is None:
        upper = sv + 12.0 / np.sqrt(C)
    integrand = lambda sigma: np.exp(-C * sigma ** 2 / 2.0) * f2_of_sigma(sigma, a1)
    val, err = integrate.quad(integrand, sv, upper, limit=400, epsabs=1e-16, epsrel=1e-12)
    return -np.exp(C * sv ** 2 / 2.0) * val


a1 = -C

s0_values = [0.0, 0.01, 0.03, 0.05, 0.08]
g0_values = [0.0001, 0.0003]
N = 300000

ss = np.random.SeedSequence(20260856000)
children = ss.spawn(len(s0_values) * len(g0_values))

print(f"{'s0':>6} {'g0':>8} {'N':>7} {'psi_hat':>10} {'SE':>9} "
      f"{'lin-only pred':>14} {'z(lin)':>8} {'lin+quad pred':>14} {'z(lin+quad)':>12}")

rows = []
idx = 0
t_start = time.time()
for s0 in s0_values:
    p1 = psi1(s0)
    b2 = b2_of_s(s0, a1)
    for g0 in g0_values:
        child = children[idx]
        idx += 1
        rng = np.random.default_rng(child)
        p, se = psi_hat(s0, g0, C, N, rng)
        pred_lin = g0 * p1
        pred_quad = g0 * p1 + g0 ** 2 * b2
        z_lin = (p - pred_lin) / se
        z_quad = (p - pred_quad) / se
        rows.append(dict(s0=s0, g0=g0, N=N, psi_hat=p, se=se, psi1_s0=p1, b2_s0=b2,
                          pred_lin=pred_lin, z_lin=z_lin, pred_quad=pred_quad, z_quad=z_quad))
        print(f"{s0:6.3f} {g0:8.5f} {N:7d} {p:10.6f} {se:9.6f} "
              f"{pred_lin:14.6f} {z_lin:8.2f} {pred_quad:14.6f} {z_quad:12.2f}")

print(f"\nelapsed: {time.time()-t_start:.1f}s")

with open("f02_results.json", "w") as fh:
    json.dump(rows, fh, indent=2)
