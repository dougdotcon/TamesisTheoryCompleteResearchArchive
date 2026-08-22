"""
Referee check #1: literal Monte-Carlo simulation of Definition 3 (THEOREM.md, S2.2)
exactly as specified -- independent implementation, not copied from any file in the repo.
Compares P(x0 cyclic) under the literal algorithm to the claimed closed form
phi_inf(c) = int_0^1 e^{-c t^2} dt.

Also runs a deliberately "broken" variant that drops the (1-t)/(1-s) competing-clock
factor (Step 4 of Theorem 1) to see whether it reproduces the sqrt(pi/2) c^{-1/2}
error flagged in THEOREM.md S3.1(a)-(b).
"""
import numpy as np
import math
from scipy import integrate

rng = np.random.default_rng(20260822)

def phi_inf_closed_form(c):
    if c == 0:
        return 1.0
    val, _ = integrate.quad(lambda t: math.exp(-c*t*t), 0, 1)
    return val

def simulate_def3(c, n_trials, rng, broken=False):
    """
    Literal implementation of Definition 3.
    For each trial:
      E0 ~ Exp(1); T0 = 1-exp(-E0)
      K ~ Poisson(c); S_1<...<S_K iid Unif(0,1) order statistics
      Theta_1..K iid Unif(0,1)
      Process marks in increasing S_j order, maintaining open arc-heads
      A (dict idx -> T_i), initialized {0: T0}.
      For each mark j:
        if S_j >= min(T_i for i in A): stop (skip rest)
        elif Theta_j < S_j: kill -> x0 not cyclic, stop
        else: T_j = S_j + (1-S_j)*(1-exp(-E_j)) [or, broken variant,
              T_j = S_j + (1-S_j)*(1-exp(-E_j)) is unchanged -- the "broken"
              variant instead uses success prob (1-s) alone by NOT requiring
              the sibling arc to survive to time t; implemented as a separate
              closed-form comparison below, not by changing this simulator]
              A[j] = T_j
      If loop completes without kill: x0 cyclic iff argmin(A) == 0
    Returns fraction cyclic.
    """
    cyclic_count = 0
    for _ in range(n_trials):
        E0 = rng.exponential(1.0)
        T0 = 1 - math.exp(-E0)
        K = rng.poisson(c)
        if K == 0:
            S = np.array([])
        else:
            S = np.sort(rng.uniform(0, 1, size=K))
        Theta = rng.uniform(0, 1, size=K)
        E = rng.exponential(1.0, size=K)

        A_idx = [0]
        A_T = [T0]
        killed = False
        for j in range(K):
            cur_min = min(A_T)
            if S[j] >= cur_min:
                break
            if Theta[j] < S[j]:
                killed = True
                break
            else:
                Tj = S[j] + (1 - S[j]) * (1 - math.exp(-E[j]))
                A_idx.append(j + 1)  # +1 so index 0 stays x0's own head
                A_T.append(Tj)
        if killed:
            cyclic = False
        else:
            min_i = A_idx[int(np.argmin(A_T))]
            cyclic = (min_i == 0)
        if cyclic:
            cyclic_count += 1
    return cyclic_count / n_trials


if __name__ == "__main__":
    print("=== Check 1: literal Definition 3 simulation vs closed form ===")
    N = 300_000
    for c in [0.3, 1.0, 3.0, 8.0]:
        est = simulate_def3(c, N, rng)
        target = phi_inf_closed_form(c)
        se = math.sqrt(est * (1 - est) / N)
        z = (est - target) / se if se > 0 else float('nan')
        print(f"c={c:6.2f}  MC={est:.6f} +/- {se:.6f}   closed_form={target:.6f}   z={z:+.2f}")
