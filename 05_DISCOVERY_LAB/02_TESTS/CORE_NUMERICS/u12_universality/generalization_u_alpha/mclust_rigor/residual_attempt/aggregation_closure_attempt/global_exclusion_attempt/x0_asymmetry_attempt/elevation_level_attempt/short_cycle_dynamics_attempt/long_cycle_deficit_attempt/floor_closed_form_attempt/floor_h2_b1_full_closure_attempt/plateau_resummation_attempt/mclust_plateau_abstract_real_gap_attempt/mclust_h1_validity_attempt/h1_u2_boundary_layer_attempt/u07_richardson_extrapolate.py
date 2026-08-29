"""
u07_extrapolate.py

Richardson-extrapolate the resid5(x;c) = (W_inf_numeric - W_pred4)/eps^5
data from u06 (pickled) to eps->0 at each fixed test point (bridge x=1,
and boundary-layer u=0,1,2,4), and compare the extrapolated limit against
this front's OWN candidate 5th-order term

    chi_5(x) := (gamma_5 - gamma_4) * R''''(x),  gamma_5 := 209/24

-- i.e. EXTENDING (speculatively, NOT claimed as proved) the pattern
psi_n(x) = gamma_n R^{(n-1)}(x), verified for n=1..4 in
u01_symbolic_outer_expansion.py, to n=5, using the record's own CONJECTURED (not
derived) gamma_5 = 209/24 (plateau_resummation_attempt/ATTEMPT.md
Section 4.4b, "gamma_5=209/24 onward is a PATTERN CONJECTURE"). This is
explicitly a SPECULATIVE comparison, reported as such -- it does NOT
independently establish gamma_5, since it feeds the SAME conjectured
value in as an input, not a fresh derivation.
"""
import pickle
from mpmath import mp, mpf, sqrt, pi

mp.dps = 50

with open("u06_results.pkl", "rb") as f:
    raw = pickle.load(f)

results = [{k: mpf(v) if k not in ("label",) else v for k, v in r.items()} for r in raw]
# fix c and label back to int/str
for r, r0 in zip(results, raw):
    r["c"] = int(r0["c"])
    r["label"] = r0["label"]

labels = sorted(set(r["label"] for r in results), key=lambda s: (s != "bridge x=1", s))

print("=" * 90)
print("Richardson extrapolation of resid5(x;c) to eps->0, at each fixed test point")
print("=" * 90)

R44_pred = {}
for label in labels:
    rows = sorted([r for r in results if r["label"] == label], key=lambda r: r["c"])
    cs = [r["c"] for r in rows]
    eps_list = [r["eps"] for r in rows]
    vals = [r["resid5"] for r in rows]
    print(f"\n{label}:")
    for c, eps, v in zip(cs, eps_list, vals):
        print(f"  c={c:6d}  eps={float(eps):.6e}  resid5={v}")

    # simple two-point Richardson assuming resid5(eps) ~= L + A*eps + O(eps^2):
    # use the last two points (smallest eps), eps and eps/2 (since c ladder is
    # x4 each step, eps ratio is exactly 1/2)
    e2, e1 = eps_list[-2], eps_list[-1]  # e2 > e1 (e1 is smaller eps, later c)
    v2, v1 = vals[-2], vals[-1]
    ratio = e2 / e1
    assert abs(ratio - 2) < mpf('1e-20'), f"expected eps ratio 2, got {ratio}"
    # v(e) = L + A e + O(e^2);  v1 = L + A e1,  v2 = L + A*2*e1
    # => v2 - v1 = A*e1  => A = (v2-v1)/e1 ;  L = v1 - A*e1 = v1-(v2-v1) = 2v1-v2
    L_extrap = 2 * v1 - v2
    print(f"  Richardson extrapolation (last 2 points, assuming O(eps) next "
          f"correction): L = 2*v(eps_min) - v(2*eps_min) = {L_extrap}")

    # also do it with the OTHER pair (c=1000,4000) for a stability check
    if len(vals) >= 3:
        e3, e2b = eps_list[-3], eps_list[-2]
        v3, v2b = vals[-3], vals[-2]
        L_extrap_alt = 2 * v2b - v3
        print(f"  same extrapolation from the PREVIOUS pair (c=1000,4000): "
              f"L' = {L_extrap_alt}   (L-L')={L_extrap - L_extrap_alt}")

    # x value for this label at, say, the largest c (should be the SAME x
    # only for "bridge x=1"; for u-labels x itself shrinks with c, so report
    # the u value and note x->0 as c->infinity along this row)
    if label.startswith("u="):
        u = int(label.split("=")[1])
        # chi_5 prediction evaluated in the LIMIT x->0 (u fixed, eps->0 =>
        # x=eps*u->0 too) -- i.e. compare against chi_5(0), not chi_5(x) at
        # any finite grid point, since the boundary-layer x itself ->0.
        x_pred = mpf(0)
    else:
        x_pred = mpf(1)

    # R'''' (x) via closure identity R^{(4)}=xR'''+3R''
    z = x_pred / sqrt(2)
    from mpmath import erfc, exp
    def erfcx(zz):
        return exp(zz * zz) * erfc(zz)
    R0 = sqrt(pi / 2) * erfcx(z)
    R1 = x_pred * R0 - 1
    R2 = x_pred * R1 + R0
    R3 = x_pred * R2 + 2 * R1
    R4 = x_pred * R3 + 3 * R2
    gamma5 = mpf(209) / 24
    gamma4 = mpf(17) / 3
    chi5_pred = (gamma5 - gamma4) * R4
    print(f"  SPECULATIVE comparison: chi_5(x={float(x_pred)}) via conjectured "
          f"gamma_5=209/24 => (gamma5-gamma4)*R''''(x) = {chi5_pred}")
    print(f"    extrapolated numeric L = {L_extrap}")
    print(f"    L - chi5_pred = {L_extrap - chi5_pred}   "
          f"relative = {(L_extrap - chi5_pred)/chi5_pred}")
