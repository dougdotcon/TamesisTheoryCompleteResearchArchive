"""Surface (a): EXACT finite-n expectation of cyclic fraction.

Ensemble: uniform permutation pi of [n]; each point independently
rerouted with prob p=c/n to a uniform destination in [n].
E[frac cyclic] computed exactly two ways:

 (1) Map-sum: E = sum over all n^n maps f of  weight(f) * cyc(f)/n,
     weight(f) = P(F=f) = E_pi prod_i [(1-p)1{f(i)=pi(i)} + p/n]
               = sum_{A subset, f|_A injective} (1-p)^{|A|}(p/n)^{n-|A|}(n-|A|)!/n!
     The count of injective subsets of size k depends only on preimage
     class sizes m(f): it's the elementary symmetric polynomial e_k(m).

 (2) Direct triple enumeration (n<=5 check): sum over all n! perms,
     all reroute subsets S, all destination vectors d in [n]^{|S|},
     with exact probability weights.

Adversarial agent, wave 2. Own code, from scratch.
"""
import itertools, json, math, sys
from fractions import Fraction

def cyclic_count(f, n):
    # f: tuple, 0-indexed. Standard iterative coloring.
    color = [0]*n  # 0 unvisited, 1 in progress stack id stored separately, 2 done
    oncycle = [False]*n
    state = [0]*n   # 0 unseen, 1 on stack, 2 finished
    order = [0]*n
    for start in range(n):
        if state[start] != 0:
            continue
        stack = []
        v = start
        while state[v] == 0:
            state[v] = 1
            order[v] = len(stack)
            stack.append(v)
            v = f[v]
        if state[v] == 1:
            # found new cycle from v to top of stack
            for w in stack[order[v]:]:
                oncycle[w] = True
        for w in stack:
            state[w] = 2
    return sum(oncycle)

def exact_mapsum(n, c, use_fractions=False):
    """Method 1. Returns E[frac cyclic] as float (or Fraction if p rational)."""
    if use_fractions:
        p = Fraction(c) / n
        one = Fraction(1)
    else:
        p = c / n
        one = 1.0
    q = one - p
    pn = p / n
    fact = [math.factorial(k) for k in range(n+1)]
    nfact = fact[n]
    # precompute (1-p)^k * (p/n)^(n-k) * (n-k)!/n!
    coef = [ (q**k) * (pn**(n-k)) * Fraction(fact[n-k], nfact) if use_fractions
             else (q**k) * (pn**(n-k)) * (fact[n-k]/nfact) for k in range(n+1)]
    total = Fraction(0) if use_fractions else 0.0
    # cache elementary symmetric polys by sorted preimage-size multiset
    ek_cache = {}
    for f in itertools.product(range(n), repeat=n):
        # preimage class sizes
        cnt = [0]*n
        for v in f:
            cnt[v] += 1
        m = tuple(sorted(x for x in cnt if x > 0))
        ek = ek_cache.get(m)
        if ek is None:
            # e_k over the multiset m via DP
            ek = [1] + [0]*len(m)
            for mm in m:
                for k in range(len(ek)-1, 0, -1):
                    ek[k] += ek[k-1]*mm
            ek_cache[m] = ek
        w = sum(ek[k]*coef[k] for k in range(len(ek)))
        cyc = cyclic_count(f, n)
        total += w * cyc
    return total / n

def exact_triple(n, c):
    """Method 2: direct enumeration over perms x reroute subsets x destinations."""
    p = c / n
    total = 0.0
    pts = list(range(n))
    nfact = math.factorial(n)
    for pi in itertools.permutations(pts):
        for r in range(n+1):
            for S in itertools.combinations(pts, r):
                wS = (p**r) * ((1-p)**(n-r))
                # average over destinations
                acc = 0.0
                for d in itertools.product(pts, repeat=r):
                    f = list(pi)
                    for idx, dest in zip(S, d):
                        f[idx] = dest
                    acc += cyclic_count(tuple(f), n)
                total += wS * acc / (n**r)
    return total / (n * nfact)

if __name__ == "__main__":
    cs = [0.5, 1.0, 2.0, 3.0]
    out = {"cs": cs, "exact": {}, "crosscheck": {}}
    # cross-check n=4 both methods, and n=5 for c=0.5
    for (n, c) in [(4, 0.5), (4, 2.0)]:
        a = exact_mapsum(n, c)
        b = exact_triple(n, c)
        out["crosscheck"][f"n{n}_c{c}"] = {"mapsum": a, "triple": b, "absdiff": abs(a-b)}
        print(f"crosscheck n={n} c={c}: mapsum={a:.12f} triple={b:.12f} diff={abs(a-b):.2e}", flush=True)
    for n in [4, 5, 6, 7]:
        out["exact"][str(n)] = {}
        for c in cs:
            v = exact_mapsum(n, c)
            out["exact"][str(n)][str(c)] = v
            phi = 0.5*math.sqrt(math.pi/c)*math.erf(math.sqrt(c))
            print(f"n={n} c={c}: E[frac cyclic] = {v:.10f}   (claimed limit {phi:.10f}, dev {v-phi:+.6f})", flush=True)
    with open(sys.path[0] + "/adv2_exact.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print("saved adv2_exact.json")
