#!/usr/bin/env python3
"""HOSTILE REFEREE check 5: the conjectured second-order constant
  C(g) = -(2/(3 sqrt(pi))) sqrt(g) (6-8g+3g^2)/(2-g)^2   (ATTEMPT sec.7.3)
tested by Richardson extrapolation at HIGHER n than the front
(front: n=2^17/2^18; referee: n=2^19/2^20 everywhere, n=2^21/2^22 at
g in {0.2,0.5,1.0}), including fresh gammas 0.25/0.65/0.85 the front
never tested.  Model x_n = C + b/sqrt(n) =>
  C_est = (sqrt2 * x_{2n} - x_n)/(sqrt2 - 1).
Also: the gamma=1 anchor via the referee's own exact-series Q(n) (float,
truncated with certified tail), independent of the A_k route; and the
approach-from-below + err-ratio -> sqrt(2) diagnostics over ALL n.
"""
import json, math

def main():
    out = []
    def log(s):
        print(s, flush=True); out.append(s)
    data = json.load(open('ref02_gamma_grid.json'))
    log("=== ref05: second-order constant C(gamma) (hostile referee) ===")
    worst = 0.0
    for gs, table in data.items():
        g = float(gs)
        ns = sorted(int(n) for n in table)
        n1, n2 = ns[-2], ns[-1]
        assert n2 == 2*n1
        x1 = math.sqrt(n1)*table[str(n1)]['err']
        x2 = math.sqrt(n2)*table[str(n2)]['err']
        Cest = (math.sqrt(2.0)*x2 - x1)/(math.sqrt(2.0)-1.0)
        C = -(2.0/(3.0*math.sqrt(math.pi)))*math.sqrt(g) \
            * (6.0-8.0*g+3.0*g*g)/((2.0-g)**2)
        rel = abs((Cest-C)/C)
        worst = max(worst, rel)
        # below-approach across all n
        below = all(table[str(n)]['err'] < 0 for n in ns)
        # err-ratio monotonic climb to sqrt2?
        ratios = [table[str(ns[i-1])]['err']/table[str(ns[i])]['err']
                  for i in range(1, len(ns))]
        mono = all(ratios[i] <= ratios[i+1] + 5e-4 for i in range(len(ratios)-1))
        log(f"g={g:5}: n_pair=2^{int(math.log2(n1))}/2^{int(math.log2(n2))} "
            f"x_n={x1:+.6f} x_2n={x2:+.6f} C_est={Cest:+.6f} "
            f"C(g)={C:+.6f} rel.dev={rel:.2e} below_all_n={'Y' if below else 'N'} "
            f"ratio[last]={ratios[-1]:.4f} mono={'Y' if mono else 'N'}")
    log(f"worst relative deviation of C_est vs closed form: {worst:.2e} "
        f"(front claimed 5.1e-07 at 2^17/2^18)")
    # gamma=1 anchor by independent exact-series Q(n)
    log("-- gamma=1 anchor via referee's own Q(n) (truncated series, "
        "certified tail):")
    for n in (2**18, 2**20, 2**22):
        # Q(n) = sum_{k>=1} prod_{i=1}^k (n-k+i)/n ; terms ~ e^{-k^2/(2n)}
        Kq = int(10*math.sqrt(n))+10
        s = 0.0
        logt = 0.0
        for k in range(1, Kq+1):
            logt += math.log1p(-(k-1)/n)
            s += math.exp(logt)
            if logt < -60*math.log(10):
                break
        pinf = (math.sqrt(math.pi)/2.0)/math.sqrt(n)*(1.0-math.erfc(math.sqrt(n)))
        R = (s/n)/pinf
        err = R - math.sqrt(2.0)
        log(f"   n=2^{int(math.log2(n))}: Q(n)={s:.10e} R={R:.10f} "
            f"sqrt(n)*(R-sqrt2)={math.sqrt(n)*err:+.6f} "
            f"(C(1)=-2/(3 sqrt pi)={-2/(3*math.sqrt(math.pi)):+.6f})")
        if str(n) in data.get('1.0', {}):
            ra = data['1.0'][str(n)]['R']
            log(f"      A_k-route R={ra:.10f}  |diff|={abs(ra-R):.2e}")
    # Estagio 19 anchor consistency: sqrt(pi n/2)-6 <= Q(n) <= sqrt(pi n/2)
    #   -1/3 + (1/11) sqrt(pi/(2n))
    n = 2**20
    Kq = int(10*math.sqrt(n))+10
    s = 0.0; logt = 0.0
    for k in range(1, Kq+1):
        logt += math.log1p(-(k-1)/n)
        s += math.exp(logt)
    lo = math.sqrt(math.pi*n/2)-6
    hi = math.sqrt(math.pi*n/2)-1.0/3.0+(1.0/11.0)*math.sqrt(math.pi/(2*n))
    log(f"Estagio-19 bounds at n=2^20: {lo:.4f} <= Q={s:.4f} <= {hi:.4f}: "
        f"{'OK' if lo <= s <= hi else 'FAIL'}")
    with open(__file__.replace('.py','.log'), 'w') as fh:
        fh.write('\n'.join(out)+'\n')

if __name__ == '__main__':
    main()
