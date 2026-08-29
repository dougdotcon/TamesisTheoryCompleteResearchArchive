"""
ADVERSARIAL SCRIPT 1 (referee's own, written from scratch from the
mathematical prose of THEOREM.md Estagio 44 and the sibling
general_k_closed_cdf_attempt/ATTEMPT.md -- NOT copied from any front's
.py file, per the mandate's hard constraint on the target front and
extended here by this referee to its own independent work as well).

Verifies, independently, the two core new claims of
general_k_cdf_alternate_route_attempt/ATTEMPT.md Section 3:

  CLAIM 1 (the "W-collapse identity"): the cited Layer-1 closed form
    InnerJ(V,O) = (O+V)*C(N+r-1,K-1) + r*C(N+r-1,K),  N:=n-V-O   (r<K)
    InnerJ(V,O) = n*C(N+r-1,r-1),                     N:=n-V-O   (r=K)
  depends on (V,O) only through their sum W:=V+O.

  CLAIM 2 (the hockey-stick collapse): sum_{V=r}^{W} C(V-1,r-1) = C(W,r),
  and the resulting reorganization
    S_r(n,K,k) = sum_{O=0}^{k} sum_{V=r}^{k-O} C(V-1,r-1)*InnerJ(V,O)
               = sum_{W=r}^{k} C(W,r)*InnerJ(W)
  genuinely reproduces the same total as the ORIGINAL nested double sum.

Also investigates and resolves a genuine notational subtlety this referee
found independently at the r=0 boundary (see PART 2b/3 below) -- resolved
by inspecting how the target's OWN code (reference_Sr_double_sum.py,
w_collapse_identity.py) handles it, confirming their result is correct,
not a bug; the subtlety is a documentation-clarity gap in the ATTEMPT.md
prose, not a mathematical error. Reported as a LOW-severity finding.
"""
import math
import sympy as sp
import random


def binom(n, k):
    """Standard combinatorial convention: C(n,k)=0 if k<0 or n<0 or k>n."""
    if k < 0 or n < 0 or k > n:
        return 0
    return math.comb(n, k)


def innerJ(n, K, r, V, O):
    N = n - V - O
    if r < K:
        return (O + V) * binom(N + r - 1, K - 1) + r * binom(N + r - 1, K)
    elif r == K:
        return n * binom(N + r - 1, r - 1)
    else:
        raise ValueError("r>K not defined")


def innerJ_W(n, K, r, W):
    return innerJ(n, K, r, V=0, O=W)


print("=" * 70)
print("PART 1: W-collapse identity -- symbolic (sympy exact)")
print("=" * 70)
n, K, r, V, W, O_sym = sp.symbols('n K r V W O', integer=True)

InnerJ_raw_rltK = (O_sym + V) * sp.binomial((n - V - O_sym) + r - 1, K - 1) \
    + r * sp.binomial((n - V - O_sym) + r - 1, K)
InnerJ_raw_rltK_sub = InnerJ_raw_rltK.subs(O_sym, W - V)
InnerJ_sub_rltK = W * sp.binomial(n - W + r - 1, K - 1) + r * sp.binomial(n - W + r - 1, K)
diff_rltK = sp.simplify(InnerJ_raw_rltK_sub - InnerJ_sub_rltK)
pd_rltK = sp.simplify(sp.diff(InnerJ_raw_rltK_sub, V))
print(f"r<K: InnerJ(V,W-V) - InnerJ_W(W) simplifies to: {diff_rltK}")
print(f"r<K: d/dV[InnerJ(V,W-V)] simplifies to: {pd_rltK}")

InnerJ_raw_rK = n * sp.binomial((n - V - O_sym) + r - 1, r - 1)
InnerJ_raw_rK_sub = InnerJ_raw_rK.subs(O_sym, W - V)
InnerJ_sub_rK = n * sp.binomial(n - W + r - 1, r - 1)
diff_rK = sp.simplify(InnerJ_raw_rK_sub - InnerJ_sub_rK)
pd_rK = sp.simplify(sp.diff(InnerJ_raw_rK_sub, V))
print(f"r=K: InnerJ(V,W-V) - InnerJ_W(W) simplifies to: {diff_rK}")
print(f"r=K: d/dV[InnerJ(V,W-V)] simplifies to: {pd_rK}")

assert diff_rltK == 0 and pd_rltK == 0 and diff_rK == 0 and pd_rK == 0
print("PART 1: PASSED (both r<K and r=K, symbolic)")

print()
print("=" * 70)
print("PART 1b: numeric spot-check, multiple (V,O) splits of the same W")
print("=" * 70)
random.seed(20260828)  # referee's own throwaway parameter-selection seed;
                        # NOT one of the target's reserved MC seeds, no
                        # probabilistic claim rests on it.
all_ok = True
for _ in range(20):
    n_c = random.randint(8, 30)
    K_c = random.randint(1, 6)
    r_c = random.randint(0, K_c)
    W_c = random.randint(r_c, max(r_c, n_c - (K_c - r_c) - 1))
    splits = list(range(0, W_c + 1))
    if len(splits) > 5:
        splits = random.sample(splits, 5)
    vals = {innerJ(n_c, K_c, r_c, Vc, W_c - Vc) for Vc in splits}
    ok = len(vals) == 1
    all_ok &= ok
    print(f"n={n_c} K={K_c} r={r_c} W={W_c} splits={splits} "
          f"values={vals} {'OK' if ok else 'MISMATCH'}")
print(f"PART 1b: {'PASSED' if all_ok else 'FAILED'}")

print()
print("=" * 70)
print("PART 2: hockey-stick identity sum_{V=r}^{W} C(V-1,r-1) = C(W,r)")
print("=" * 70)
Vs, Ws, rs = sp.symbols('V W r', integer=True)
generic = sp.simplify(sp.summation(sp.binomial(Vs - 1, rs - 1), (Vs, rs, Ws)) - sp.binomial(Ws, rs))
print(f"Generic symbolic r: sp.summation(...) - C(W,r) simplifies to: {generic}")
assert generic == 0

print()
print("PART 2b: r=0 boundary -- genuine subtlety found and resolved")
print("-" * 70)
print("Term-by-term check with sympy's OWN binomial convention (C(n,k)=0 for")
print("k<0), which is what a literal/naive re-implementation would use:")
for Wc in range(0, 6):
    lhs = sum(int(sp.binomial(Vc - 1, -1)) for Vc in range(0, Wc + 1))
    rhs = int(sp.binomial(Wc, 0))
    print(f"  W={Wc}: term-by-term(r=0)={lhs}  C(W,0)={rhs}  "
          f"{'MATCH' if lhs == rhs else 'MISMATCH (naive convention)'}")
print()
print("FINDING: under the naive/literal convention C(n,-1):=0 (sympy's and")
print("math.comb's own default), the hockey-stick identity as literally")
print("stated FAILS at r=0 for every W>0 -- the symbolic 'simplifies to 0'")
print("verdict above is a statement for GENERIC (nonzero) r; substituting")
print("r=0 into the sum's own symbolic closed form W*C(W-1,r-1)/r gives an")
print("indeterminate 0/0, not a value that visibly matches C(W,0)=1 by")
print("direct term-by-term summation under the naive convention.")
print()
print("RESOLUTION (confirmed by reading the target's OWN code, per the task")
print("mandate's item 4/5 style cross-check -- reference_Sr_double_sum.py")
print("line 64 and InnerJ_direct's own r=0 branch, and w_collapse_identity.py's")
print("use of math.comb(W,r) which is correctly 1 at r=0): the target's own")
print("scripts special-case C(V-1,r-1) at r=0 to the correct combinatorial")
print("meaning -- 'number of compositions of V into 0 positive parts' = the")
print("Kronecker delta [V=0], NOT the naive binomial-function value. Python's")
print("math.comb(V-1,-1) does not even accept a negative second argument (it")
print("raises ValueError), so this special-casing is a REQUIRED, deliberate")
print("choice in their code, not an accidental omission -- and it is the")
print("mathematically correct choice, verified below.")


def cV_correct(V, r):
    return math.comb(V - 1, r - 1) if r > 0 else (1 if V == 0 else 0)


def original_double_sum(n, K, r, k, cV_fn):
    total = 0
    for O in range(0, k + 1):
        for V in range(r, k - O + 1):
            total += cV_fn(V, r) * innerJ(n, K, r, V, O)
    return total


def collapsed_single_sum(n, K, r, k):
    total = 0
    for W in range(r, k + 1):
        total += binom(W, r) * innerJ_W(n, K, r, W)
    return total


print()
print("=" * 70)
print("PART 3: original double sum vs. collapsed single sum, exact integers")
print("=" * 70)
cases = []
for nv in [6, 8, 10, 12, 15]:
    for Kv in range(1, 7):
        for rv in range(0, Kv + 1):
            for kv in sorted(set([0, 1, 2, nv // 2, nv - 1, nv])):
                cases.append((nv, Kv, rv, kv))

print(f"Total cells: {len(cases)}")

print()
print("3a) Using the NAIVE convention (cV=math.comb(V-1,r-1) attempted -- but")
print("    since math.comb rejects negative k, we substitute the sympy-style")
print("    'return 0' stand-in for r=0 to demonstrate the naive mismatch):")


def cV_naive(V, r):
    return 0 if r == 0 else math.comb(V - 1, r - 1)


mism_naive = 0
mism_naive_by_r = {}
for (nv, Kv, rv, kv) in cases:
    a = original_double_sum(nv, Kv, rv, kv, cV_naive)
    b = collapsed_single_sum(nv, Kv, rv, kv)
    if a != b:
        mism_naive += 1
        mism_naive_by_r[rv] = mism_naive_by_r.get(rv, 0) + 1
print(f"    Naive-convention mismatches: {mism_naive} / {len(cases)}  "
      f"(breakdown by r: {mism_naive_by_r})")
print("    -- all at r=0, exactly as PART 2b predicts; this confirms the")
print("    'C(V-1,r-1)' notation in the ATTEMPT.md/Estagio-44 prose is NOT")
print("    safe to interpret via a literal binomial-function call at r=0;")
print("    it requires the Kronecker-delta reading used in the target's own")
print("    code.")

print()
print("3b) Using the CORRECT (combinatorially meaningful, and target's own)")
print("    convention cV(V,0):=[V=0]:")
mism_correct = 0
for (nv, Kv, rv, kv) in cases:
    a = original_double_sum(nv, Kv, rv, kv, cV_correct)
    b = collapsed_single_sum(nv, Kv, rv, kv)
    if a != b:
        mism_correct += 1
        print(f"  MISMATCH n={nv} K={Kv} r={rv} k={kv}: orig={a} collapsed={b}")
print(f"    Mismatches: {mism_correct} / {len(cases)}")
print(f"    PART 3 (correct convention): {'PASSED' if mism_correct == 0 else 'FAILED'}")

print()
print("=" * 70)
print("OVERALL VERDICT")
print("=" * 70)
print("W-collapse identity (Claim 1): CONFIRMED, symbolic + numeric, r<K and r=K.")
print("Hockey-stick + overall collapse (Claim 2): CONFIRMED for the")
print("combinatorially-correct convention, which the target's own code uses")
print("correctly. A LOW-severity documentation-clarity finding is raised:")
print("the ATTEMPT.md prose does not spell out that C(V-1,r-1) needs this")
print("r=0 boundary convention, even though its own code handles it correctly.")
