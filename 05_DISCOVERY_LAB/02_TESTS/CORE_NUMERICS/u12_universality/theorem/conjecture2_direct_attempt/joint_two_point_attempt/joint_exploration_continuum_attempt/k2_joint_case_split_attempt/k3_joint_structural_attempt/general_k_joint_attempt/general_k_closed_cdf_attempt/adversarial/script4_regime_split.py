"""
ADVERSARIAL SCRIPT 4 -- probing the "no regime-splitting on k needed"
claim (target ATTEMPT.md Executive Summary / Section 3.1 / Scorecard #4).

Two distinct things are tested:
  (I) The literal claim as stated: does the exchangeability-reduced S_r
      REORGANIZATION (an exact algebraic rewrite, Section 2-3 of the
      target) match brute force / the raw engine at EVERY k without
      needing case-splits? -- re-verified independently at K=3 (already
      done more broadly in script1; here every single k, 0..n, several
      n, is checked explicitly and printed).
  (II) Whether this is a FAIR comparison to Estagio 40's own three
      regimes: Estagio 40's regimes arose while deriving an actual
      CLOSED ALGEBRAIC FORMULA in n (not a raw/definitional identity)
      by symbolically summing the O-range (which is where Estagio 40's
      3 regimes actually come from -- see THEOREM.md Estagio 40 Sec.
      4.3: "because the O-sum's valid range is 0<=O<=min(k,n-3)").
      Here we test directly: does attempting the SAME kind of symbolic
      closure (via sp.summation, at concrete K=3, using Layer 1's own
      closed InnerJ for the V-sum, then trying to close the O-sum too)
      run into the SAME kind of k-vs-(n-3)-boundary regime-split
      structure, i.e. is the "no regime split" bonus actually about a
      LATER, harder step this front never reached (Layer 3, explicitly
      marked NOT ATTEMPTED in Section 5.2), or does it also avoid that?
"""
from math import comb
from fractions import Fraction
import sympy as sp
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/adv")
import script1_exchangeability as s1


def safe_comb(n_, k_):
    if n_ < 0 or k_ < 0 or k_ > n_:
        return 0
    return comb(n_, k_)


def InnerJ_closed(n, K, r, V, O):
    N = n - V - O
    if r == K:
        return n * safe_comb(N + r - 1, r - 1)
    return (O + V) * safe_comb(N + r - 1, K - 1) + r * safe_comb(N + r - 1, K)


def S_r_via_layer1(n, K, k, r):
    total = 0
    for O in range(0, k + 1):
        t = k - O
        for V in range(r, t + 1):
            if n - V - O < 0:
                continue
            cV = safe_comb(V - 1, r - 1) if r >= 1 else (1 if V == 0 else 0)
            total += cV * InnerJ_closed(n, K, r, V, O)
    return total


def cdf_via_layer1(n, K, k):
    from math import factorial
    tot = Fraction(0, 1)
    for r in range(K + 1):
        Sr = S_r_via_layer1(n, K, k, r)
        tot += Fraction(comb(K, r) * factorial(r), n ** (r + 1)) * Sr
    return tot / comb(n, K)


if __name__ == "__main__":
    print("=" * 70)
    print("(I) literal claim: exchangeability-reduced S_r reorganization")
    print("    (via closed Layer-1 InnerJ + raw O,V double loop -- NOT a")
    print("    closed-form-in-n, just the reorganized sum) matches D3")
    print("    at EVERY k=0..n for several n, K=3 -- no case-split logic")
    print("    anywhere in cdf_via_layer1's own code.")
    print("=" * 70)
    ok = True
    for n in range(3, 12):
        for k in range(0, n + 1):
            c = cdf_via_layer1(n, 3, k)
            if k <= n - 1:
                d = s1.D3(n, k)
            else:
                d = Fraction(1, 1)
            if c != d:
                ok = False
                print(f"  MISMATCH n={n} k={k}: {c} vs {d}")
    print("ALL k=0..n MATCH, single uniform code path, K=3:", ok)
    print("(This confirms the reorganization ITSELF needs no case analysis")
    print(" to be numerically correct -- but note this is a claim about an")
    print(" un-collapsed double sum over O,V, not a closed rational")
    print(" function of n, so it is not testing the same kind of")
    print(" 'regime' Estagio 40 needed -- see part (II) below.)")

    print()
    print("=" * 70)
    print("(II) Attempting the SAME symbolic-in-n closure Estagio 40 did,")
    print("     via this front's own Layer-1-based S_r, concrete K=3,")
    print("     r=0,1,2,3 -- does sp.summation's OWN attempt to close the")
    print("     O-sum (Layer 3, 'NOT ATTEMPTED' per the target's Section")
    print("     5.2) hit the same k-vs-(n-3) boundary structure, i.e. is")
    print("     a regime split latent in the very layer this front never")
    print("     reached?")
    print("=" * 70)
    n_, k_, O_, r_ = sp.symbols('n k O r', positive=True, integer=True)
    K_ = 3
    N_ = n_ - O_  # V summed out already at fixed r via Layer 1 closure;
    # here we directly attempt: for r<3, sum over V of C(V-1,r-1)*InnerJ(V,O)
    # from V=r to V=k-O (Layer 2, symbolic in n,k,O,r) via sp.summation,
    # then attempt the O-sum (Layer 3) symbolically in n,k -- exactly
    # mirroring what Estagio 40 needed to do to get a real closed form.
    V_ = sp.symbols('V', positive=True, integer=True)
    for r_val in (0, 1, 2):
        Kv = 3
        Nexpr = n_ - V_ - O_
        InnerJ_sym = (O_ + V_) * sp.binomial(Nexpr + r_val - 1, Kv - 1) + r_val * sp.binomial(Nexpr + r_val - 1, Kv)
        summand = sp.binomial(V_ - 1, r_val - 1) * InnerJ_sym if r_val >= 1 else InnerJ_sym.subs(V_, 0)
        if r_val == 0:
            # V is forced to 0; Layer-2 V-sum is trivial (single term)
            print(f"r={r_val}: V forced to 0 (no touched sources) -- Layer 2 trivial, skip sp.summation.")
            continue
        t0 = sp.Symbol('t0')
        print(f"--- r={r_val}: attempting sp.summation over V (Layer 2), symbolic O,n,k ---")
        try:
            Vsum = sp.summation(summand, (V_, r_val, k_ - O_))
            Vsum = sp.simplify(Vsum)
            print("  Layer-2 V-sum (symbolic O,n,k) closed via sp.summation:")
            print("   ", Vsum)
        except Exception as e:
            print("  sp.summation raised:", e)
            continue
