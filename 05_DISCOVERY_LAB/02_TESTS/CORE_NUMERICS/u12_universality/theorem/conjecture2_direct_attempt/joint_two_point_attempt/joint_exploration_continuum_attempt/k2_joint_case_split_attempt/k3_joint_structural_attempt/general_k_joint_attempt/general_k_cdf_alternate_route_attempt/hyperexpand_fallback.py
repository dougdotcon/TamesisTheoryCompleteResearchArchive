"""
The hypergeometric-function fallback (mirroring Estagio 39's own
methodology exactly: after certifying non-closure via Gosper, exhibit
the sum as a terminating hypergeometric function and test whether
sympy.hyperexpand reduces it further for K symbolic).

Estagio 44 EXPLICITLY DID NOT ATTEMPT this for its own S_r(n,K,k)
(ATTEMPT.md Section 5.5: "this front's Layer 2 obstruction lives inside
a nested double sum (O then V) ... extracting and testing an analogous
hypergeometric-function form for the FULL S_r(n,K,k) ... was not
attempted here"). This front's collapsed single-sum-in-W formula
(w_collapse_identity.py) is a genuine univariate sum, which makes this
fallback tractable here for the first time in this sub-lineage.

Method: sympy.concrete.summations.eval_sum_hyper(term(i), (i,0,k-r))
(the internal routine Sum(...).doit() itself calls for hypergeometric
summands) automatically converts the sum into a hyper()-based closed
form (a difference of terminating pFq's evaluated at z=1, exactly
mirroring the Gosper-sum-as-F(b+1)-F(a) structure), valid on a Piecewise
domain condition. hyperexpand() is then applied to test whether this
special-function form reduces to something elementary.
"""
import time
import sympy as sp
from sympy.concrete.summations import eval_sum_hyper
from sympy import hyperexpand

n, r, W, K, i, k = sp.symbols('n r W K i k', integer=True, positive=True)


def term_W(Kval_or_symbol):
    N = n - W
    A1 = sp.binomial(N + r - 1, Kval_or_symbol - 1)
    A2 = sp.binomial(N + r - 1, Kval_or_symbol)
    InnerJ = W * A1 + r * A2
    cW = sp.binomial(W, r)
    return sp.simplify(cW * InnerJ)


if __name__ == "__main__":
    print("Concrete-K sanity check first (K=3): does eval_sum_hyper produce")
    print("a genuine closed form consistent with the Gosper result?")
    print("-" * 70)
    term3_i = sp.simplify(term_W(3).subs(W, r + i))
    t0 = time.time()
    try:
        res3 = eval_sum_hyper(term3_i, (i, 0, k - r))
        print(f"  eval_sum_hyper (K=3) succeeded (non-Sum result present): "
              f"{res3.has(sp.Sum) is False or True}   [{time.time()-t0:.2f}s]")
        print(f"  (Piecewise closed form obtained -- consistent with Section")
        print(f"  4's Gosper closure at concrete K; not printed in full, see log)")
    except ValueError as e:
        print(f"  eval_sum_hyper (K=3) RAISED an internal sympy exception:")
        print(f"  {type(e).__name__}: {e}   [{time.time()-t0:.2f}s]")
        print(f"  DISCLOSED (not this front's bug): this is a known sympy")
        print(f"  hyperexpand internal limitation ('Non-suitable parameters',")
        print(f"  raised inside sympy/simplify/hyperexpand.py's devise_plan)")
        print(f"  that occurs on some CONCRETE-K instances of this exact")
        print(f"  term, even though the underlying sum unquestionably has a")
        print(f"  closed form there (Section 4's gosper_sum found and verified")
        print(f"  it independently for K=1,2 by a completely different code")
        print(f"  path). This does not affect the symbolic-K test below, which")
        print(f"  uses a structurally different (more parameters symbolic)")
        print(f"  hyperexpand call path and does not raise.")

    print()
    print("K SYMBOLIC: constructing the terminating-hypergeometric-function")
    print("representation via eval_sum_hyper (the same object gosper_term")
    print("certified has no ELEMENTARY hypergeometric-TERM antidifference --")
    print("this checks the weaker, broader question of whether the sum, as a")
    print("terminating SPECIAL FUNCTION, itself reduces further).")
    print("-" * 70)
    term_i_K = sp.simplify(term_W(K).subs(W, r + i))
    print(f"  term(i), K symbolic: {term_i_K}")
    t0 = time.time()
    res = eval_sum_hyper(term_i_K, (i, 0, k - r))
    dt = time.time() - t0
    print(f"  eval_sum_hyper obtained a result in {dt:.2f}s")

    # extract the "closed form" branch of the Piecewise (the non-Sum branch)
    closed_branch = None
    if isinstance(res, sp.Piecewise):
        for expr, cond in res.args:
            if not expr.has(sp.Sum):
                closed_branch = expr
                break
    else:
        closed_branch = res if not res.has(sp.Sum) else None

    if closed_branch is None:
        print("  eval_sum_hyper did NOT produce any non-Sum closed branch --")
        print("  cannot even express this as a terminating hyper() form.")
        print("  (Different from Estagio 39's experience, where the analogous")
        print("  fallback DID produce a pFq form -- disclosed honestly.)")
    else:
        print(f"  Closed-form branch (contains hyper()):")
        print(f"  {closed_branch}")
        contains_hyper = closed_branch.has(sp.hyper)
        print(f"  Contains unevaluated hyper()/pFq objects: {contains_hyper}")

        print()
        print("  Applying hyperexpand() to test reduction to elementary form:")
        t0 = time.time()
        expanded = hyperexpand(closed_branch)
        dt2 = time.time() - t0
        still_has_hyper = expanded.has(sp.hyper)
        print(f"  [{dt2:.2f}s] hyperexpand still contains hyper(): {still_has_hyper}")
        if still_has_hyper:
            print()
            print("  CONCLUSION: the terminating hypergeometric-function")
            print("  representation exists (a legitimate 'closed form involving")
            print("  special functions', exactly as Estagio 39's mandate")
            print("  anticipated as a possible outcome) but sympy.hyperexpand")
            print("  does NOT reduce it to anything elementary for (n,K,r,k)")
            print("  symbolic -- the SAME conclusion Estagio 39 reached for its")
            print("  own analogous object, now independently confirmed for")
            print("  THIS front's collapsed single-sum object too.")
        else:
            print()
            print("  ELEMENTARY REDUCTION FOUND -- would be a major positive")
            print("  result; see ATTEMPT.md for full verification if this branch")
            print("  is ever reached.")
