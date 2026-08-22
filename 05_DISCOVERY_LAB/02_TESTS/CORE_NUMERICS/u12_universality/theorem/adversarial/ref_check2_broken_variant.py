"""
Referee check #2: simulate the "broken" (size-biasing-forgetting) variant of
Definition 3 that THEOREM.md S3.1(a) claims would arise from computing only
the "does not kill" factor (1-s) for each surviving mark, instead of the
correct joint success probability (1-t) = (1-s)*(1-t)/(1-s).

Concretely: instead of requiring the *sibling* arc-head spawned at s to also
survive past t (T_j > t), the broken variant only requires "not a kill"
(Theta_j >= s) and otherwise ignores the sibling's own closure clock.
This should reproduce int_0^1 e^{-c t^2/2} dt, NOT the claimed correct
int_0^1 e^{-c t^2} dt.
"""
import numpy as np
import math
from scipy import integrate

rng = np.random.default_rng(99001)

def closed_form(c, exponent_power):
    val, _ = integrate.quad(lambda t: math.exp(-c*(t**exponent_power)), 0, 1)
    return val

def simulate_broken(c, n_trials, rng):
    """
    Broken variant: a surviving mark at s "always" behaves as if it never
    threatens x0 again after surviving the kill check (Theta_j >= s) --
    i.e. it does NOT get its own closure clock T_j at all, so there is no
    second race. Formally this is: x0 is cyclic at T0=t iff no mark before
    t is a kill (Theta_j < s), full stop -- ignoring competing closures
    entirely. This is *exactly* using probability (1-s) instead of (1-t)
    at each mark in the thinning step (Step 5 of the correct proof),
    which the document claims gives Poisson(c*t^2/2) failures.
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

        killed = False
        for j in range(K):
            if S[j] >= T0:
                break
            if Theta[j] < S[j]:
                killed = True
                break
            # else: survives, but (broken variant) contributes NO further
            # closure-clock risk to x0 -- this is the dropped-factor error.
        cyclic = not killed
        if cyclic:
            cyclic_count += 1
    return cyclic_count / n_trials


if __name__ == "__main__":
    print("=== Check 2: broken (size-biasing-forgetting) variant ===")
    N = 300_000
    for c in [1.0, 3.0, 8.0]:
        est = simulate_broken(c, N, rng)
        target_wrong = closed_form(c, 1)      # int e^{-c t} dt -- NOT what text predicts either
        target_half  = closed_form(c, 2) if False else None
        # correct prediction per THEOREM.md S3.1(a): int_0^1 e^{-c t^2/2} dt
        target_half_t2 = integrate_half = __import__('scipy.integrate', fromlist=['quad']).quad(
            lambda t: math.exp(-c*t*t/2.0), 0, 1)[0]
        target_correct = closed_form(c, 2)    # the TRUE closed form int e^{-c t^2} dt
        se = math.sqrt(est*(1-est)/N)
        print(f"c={c:5.2f}  MC(broken)={est:.6f}+/-{se:.6f}  "
              f"predicted-broken(int e^-ct^2/2)={target_half_t2:.6f}  "
              f"true-correct(int e^-ct^2)={target_correct:.6f}")
