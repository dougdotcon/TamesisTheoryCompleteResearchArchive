"""V1/V2 validation of the adversarial simulator.

V1: exact E[phi] by full enumeration over maps f in [n]^n with
    P(f) = sum_{S subset [n]} (1-p)^|S| (p/n)^(n-|S|) (n-|S|)!/n! * 1{f injective on S}
    (uniform permutation integrated out analytically). Internal
    cross-check of that formula for n=4,5 against brute-force average
    over all n! permutations. Then MC z-test of the simulator.

V2: classical benchmarks: c=0 => phi=1; c=n (p=1) => pure uniform random
    map, P(x cyclic) = sum_{k=1}^n (n-1)...(n-k+1)/n^k, tested at n=1000.
"""
import itertools
import json
import math
import numpy as np
from adv_sim import run_cell

OUT = {}
rng_master = np.random.default_rng(np.random.SeedSequence(1234321))


def phi_of_maps(F, n):
    """F: (M, n) array of maps. Return phi per map via composition power."""
    m = 1
    steps = 0
    while m < n:
        m <<= 1
        steps += 1
    g = F.copy()
    for _ in range(steps):
        g = np.take_along_axis(g, g, axis=1)
    M = F.shape[0]
    present = np.zeros((M, n), dtype=bool)
    rows = np.repeat(np.arange(M), n)
    present[rows, g.ravel()] = True
    return present.sum(axis=1) / n


def exact_phi_subset_formula(n, c):
    p = c / n
    maps = np.array(list(itertools.product(range(n), repeat=n)), dtype=np.int64)
    phis = phi_of_maps(maps, n)
    total = np.zeros(len(maps))
    for S in itertools.chain.from_iterable(
            itertools.combinations(range(n), k) for k in range(n + 1)):
        k = len(S)
        w = (1 - p) ** k * (p / n) ** (n - k) * math.factorial(n - k) / math.factorial(n)
        if k == 0:
            inj = np.ones(len(maps), dtype=bool)
        else:
            sub = np.sort(maps[:, list(S)], axis=1)
            inj = np.all(np.diff(sub, axis=1) != 0, axis=1) if k > 1 else np.ones(len(maps), dtype=bool)
        total += w * inj
    # sanity: total must sum to 1 over all maps
    Z = total.sum()
    return float((total * phis).sum()), float(Z)


def exact_phi_bruteforce_perms(n, c):
    """Direct average over all n! permutations (independent check of formula)."""
    p = c / n
    maps = np.array(list(itertools.product(range(n), repeat=n)), dtype=np.int64)
    phis = phi_of_maps(maps, n)
    acc = np.zeros(len(maps))
    for perm in itertools.permutations(range(n)):
        pa = np.array(perm)
        match = maps == pa[None, :]
        w = np.prod(np.where(match, (1 - p) + p / n, p / n), axis=1)
        acc += w
    acc /= math.factorial(n)
    return float((acc * phis).sum()), float(acc.sum())


def random_map_cyclic_fraction_exact(n):
    """P(x cyclic) for a uniform random map on [n]."""
    s = 0.0
    term = 1.0
    for k in range(1, n + 1):
        # term for length-k: (n-1)(n-2)...(n-k+1)/n^k
        s += term / n  # term currently = prod_{j=1}^{k-1}(n-j)/n^{k-1}; divide by n
        term *= (n - k) / n
    return s


print("=== V1: exact enumeration vs simulator ===")
OUT["V1"] = []
for n in (4, 5):
    for c in (0.5, 2.0):
        e_sub, Z = exact_phi_subset_formula(n, c)
        e_bf, Zbf = exact_phi_bruteforce_perms(n, c)
        print(f"n={n} c={c}: subset-formula={e_sub:.10f} (Z={Z:.12f}) "
              f"bruteforce={e_bf:.10f} (Z={Zbf:.12f}) diff={abs(e_sub-e_bf):.2e}")
        assert abs(e_sub - e_bf) < 1e-10 and abs(Z - 1) < 1e-10
        OUT["V1"].append(dict(n=n, c=c, exact=e_sub, bruteforce=e_bf))

for n in (6,):
    for c in (0.5, 2.0):
        e_sub, Z = exact_phi_subset_formula(n, c)
        assert abs(Z - 1) < 1e-10
        OUT["V1"].append(dict(n=n, c=c, exact=e_sub))
        print(f"n={n} c={c}: subset-formula={e_sub:.10f} (Z ok)")

# MC z-tests against exact values
print("--- MC z-tests ---")
N = 400_000
for rec in OUT["V1"]:
    n, c, exact = rec["n"], rec["c"], rec["exact"]
    mean, std, sem, _, _ = run_cell(n, c, N, rng_master.spawn(1)[0])
    z = (mean - exact) / sem
    rec.update(mc=mean, sem=sem, z=z)
    print(f"n={n} c={c}: exact={exact:.6f} mc={mean:.6f}±{sem:.6f} z={z:+.2f}")

print("=== V2: classical benchmarks ===")
# c=0 -> permutation -> phi = 1 exactly
mean, _, sem, _, _ = run_cell(50, 0.0, 200, rng_master.spawn(1)[0])
print(f"c=0, n=50: phi={mean} (expect exactly 1.0)")
OUT["V2_c0"] = dict(n=50, phi=mean)
assert mean == 1.0

# c=n -> p=1 -> uniform random map, exact P(cyclic)
n = 1000
exact_rm = random_map_cyclic_fraction_exact(n)
mean, std, sem, _, _ = run_cell(n, float(n), 20_000, rng_master.spawn(1)[0])
z = (mean - exact_rm) / sem
print(f"c=n={n} (pure random map): exact={exact_rm:.6f} mc={mean:.6f}±{sem:.6f} z={z:+.2f}")
OUT["V2_randommap"] = dict(n=n, exact=exact_rm, mc=mean, sem=sem, z=z)

with open("adv_validation.json", "w") as fh:
    json.dump(OUT, fh, indent=2)
print("saved adv_validation.json")
