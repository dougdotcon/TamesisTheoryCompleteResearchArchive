"""ref2_pool_moments.py -- exact/measured first and second moments of the
image pool |U_rem| and of the world |R^c| for M-CLUST(b) at (c,n).

Why this matters for the reduction claim (4.1).  The reduction matches the
MEAN world and the MEAN pool of M-CLUST(b) to the (deterministic) world and
pool of M-U at (c',n').  But M-CLUST's pool is RANDOM (it is a function of the
seed count k), while M-U's pool N is a constant.  Since phi_U is convex in its
argument, a mixture over a random pool sits ABOVE phi_U at the mean pool:

    phi(cyclic | x0 notin R)  ~  E_k[ phi_U( (c/n) |U_rem| ) ]
                              ~  phi_U(c'') * ( 1 + (3/8) CV(|U_rem|)^2 )

with c'' = (c/n) E|U_rem| = c(1-c/n)^(b-1)  (E|U_rem| = n(1-c/n)^(b-1), exact).
This script measures CV(|U_rem|) and evaluates the mixture integral directly.
Seeds 20260824950+.
"""
import sys

import mpmath as mp
import numpy as np

import ref2_formula as F
import ref2_mc as M

CELLS = [(65536, 50, 400), (65536, 100, 400), (65536, 100, 600),
         (65536, 200, 150), (65536, 400, 100), (65536, 100, 1000),
         (65536, 200, 600), (65536, 800, 100), (65536, 400, 300),
         (32768, 8, 40), (32768, 8, 160), (65536, 300, 150),
         (131072, 200, 800), (131072, 400, 400)]

NI = 3000
OUT = []


def say(*a):
    s = " ".join(str(x) for x in a)
    OUT.append(s)
    print(s, flush=True)


say("ref2_pool_moments.py -- pool/world fluctuation of M-CLUST(b)")
say("%-24s %10s %10s %10s %10s %10s %10s"
    % ("cell", "E|U|/n th", "E|U|/n mc", "CV(|U|)", "CV(|Rc|)",
       "Jensen%", "c''"))
rng = np.random.default_rng(np.random.SeedSequence(20260824950))
res = []
for (n, b, c) in CELLS:
    p = c / n
    pool = np.empty(NI)
    world = np.empty(NI)
    for i in range(NI):
        pi = rng.permutation(n).astype(np.int64)
        sm = rng.random(n) < p
        R = M.build_R(pi, sm, b)
        I = np.zeros(n, dtype=bool)
        cur = np.flatnonzero(sm)
        for _ in range(b - 1):
            cur = pi[cur]
            I[cur] = True
        pool[i] = n - I.sum()
        world[i] = n - R.sum()
    cv = pool.std(ddof=1) / pool.mean()
    cvw = world.std(ddof=1) / world.mean()
    cpp = c * (1 - p) ** (b - 1)
    # direct mixture:  E[phi_U((c/n) * pool)]  vs phi_U(c'')
    mix = float(np.mean([float(F.phi_U(p * x)) for x in pool]))
    base = float(F.phi_U(cpp))
    say("n=%6d b=%4d c=%5d %10.6f %10.6f %10.5f %10.5f %+9.4f %10.4f"
        % (n, b, c, (1 - p) ** (b - 1), pool.mean() / n, cv, cvw,
           100 * (mix / base - 1), cpp))
    res.append(dict(n=n, b=b, c=c, cv=cv, cvw=cvw, mix=mix, base=base,
                    cpp=cpp, poolmean=pool.mean(), Ntheory=n * (1 - p) ** (b - 1)))

say("")
say("Jensen%% is 100*(E[phi_U((c/n)|U_rem|)]/phi_U(c'') - 1), i.e. the amount by")
say("which the RANDOM-pool mixture exceeds the fixed-pool M-U value.  It is a")
say("term the reduction (4.1) does not carry, because M-U's pool is a constant.")
say("Analytic check: (3/8)CV^2 in %% =")
for r in res:
    say("   n=%6d b=%4d c=%5d   (3/8)CV^2 = %+.4f%%   measured mixture "
        "excess = %+.4f%%"
        % (r["n"], r["b"], r["c"], 100 * 0.375 * r["cv"] ** 2,
           100 * (r["mix"] / r["base"] - 1)))

with open("ref2_pool_moments.log", "w") as fh:
    fh.write("\n".join(OUT) + "\n")
