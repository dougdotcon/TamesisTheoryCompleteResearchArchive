"""
Fresh, from-scratch exhaustive brute-force enumeration of THEOREM.md's
Definition 4 (finite conditional-K model), written WITHOUT reading any
.py script from this front, the parent joint_two_point_attempt/ front
(including its adversarial/), or any other prior front -- per the
referee mandate. Rebuilt from the prose of THEOREM.md Sec 7.2 and
.../joint_two_point_attempt/ATTEMPT.md Sec 1 only.

Definition 4 recap (from prose):
  - pi: uniform random permutation of [n] = {0,...,n-1}.
  - R subset of [n], |R|=K, uniform random K-subset, independent of pi.
  - U_i, i in R: i.i.d. Uniform([n]), independent of (pi,R).
  - f(i) := U_i if i in R, f(i) := pi(i) otherwise.
  - i is "cyclic" iff its forward f-orbit returns to i in finitely many
    steps (automatic on a finite set).

This script enumerates ALL (pi, R, {U_i}) triples with EQUAL weight
(pi ranges over all n! permutations, R ranges over all C(n,K) subsets,
{U_i} ranges over all n^K destination tuples aligned to R in sorted
order) -- this exactly represents the uniform/independent joint law
Definition 4 specifies, since pi, R, and the U_i's are each drawn
uniformly and independently. All arithmetic is exact (Python ints and
fractions.Fraction) -- no floating point anywhere in the counting.

No random sampling is used anywhere in this file (fully deterministic
enumeration), so no seed is needed per the mandate's seed-range
instructions.
"""
import itertools
import json
import time
from fractions import Fraction


def analyze(f, n):
    """Given f as a list (f[i] = image of i), return:
       cyclic: list[bool], cyclic[i] True iff i is on a directed cycle of f
       cycle_id: list[int], the cycle index of i if cyclic[i], else -1
    Linear time (each node visited O(1) times, standard "rho-shape"
    functional-graph decomposition).
    """
    state = [0] * n  # 0 unvisited, 1 on current path (in progress), 2 done
    cyclic = [False] * n
    cycle_id = [-1] * n
    next_id = 0
    for start in range(n):
        if state[start] != 0:
            continue
        path = []
        pos_in_path = {}
        cur = start
        while state[cur] == 0:
            state[cur] = 1
            pos_in_path[cur] = len(path)
            path.append(cur)
            cur = f[cur]
        if state[cur] == 1:
            idx = pos_in_path[cur]
            cid = next_id
            next_id += 1
            for node in path[idx:]:
                cyclic[node] = True
                cycle_id[node] = cid
        for node in path:
            state[node] = 2
    return cyclic, cycle_id


def enumerate_definition4(n, K, r_fixed=None):
    """Enumerate Definition 4's full (pi,R,{U}) space for given (n,K).

    If r_fixed is None: R ranges over all C(n,K) subsets (the genuine
    Definition-4 model, R averaged/marginalized as specified).
    If r_fixed is an int (only meaningful for K=1): R is held fixed at
    {r_fixed} instead of averaged -- this reproduces the document's
    "R fixed, not averaged" isolation checks for the K=1 sub-cases.
    Returns a dict of exact Fraction probabilities:
      P_both_cyclic (0,1 both cyclic)
      P_same_cycle  (0,1 both cyclic AND same final cycle)
      P_diff_cycle  (0,1 both cyclic AND different final cycles)
    """
    assert n >= 2
    both_count = 0
    same_count = 0
    diff_count = 0
    total = 0

    perms = itertools.permutations(range(n))
    if r_fixed is not None:
        assert K == 1
        R_choices = [(r_fixed,)]
    else:
        R_choices = list(itertools.combinations(range(n), K))

    for pi in perms:
        for R in R_choices:
            for U in itertools.product(range(n), repeat=K):
                f = list(pi)
                for idx, i in enumerate(R):
                    f[i] = U[idx]
                cyclic, cycle_id = analyze(f, n)
                total += 1
                if cyclic[0] and cyclic[1]:
                    both_count += 1
                    if cycle_id[0] == cycle_id[1]:
                        same_count += 1
                    else:
                        diff_count += 1

    assert both_count == same_count + diff_count
    return {
        "n": n, "K": K, "r_fixed": r_fixed, "total": total,
        "P_both_cyclic": Fraction(both_count, total),
        "P_same_cycle": Fraction(same_count, total),
        "P_diff_cycle": Fraction(diff_count, total),
    }


def fmt(fr):
    return f"{fr.numerator}/{fr.denominator} = {float(fr):.6f}"


def main():
    log_lines = []

    def log(s=""):
        print(s)
        log_lines.append(s)

    t_start = time.time()

    # ------------------------------------------------------------------
    # 1. K=0 trivial sanity check: P_n^{(0)}(both) = 1 for all n
    # ------------------------------------------------------------------
    log("=" * 78)
    log("SECTION 1: K=0 trivial check")
    log("=" * 78)
    for n in range(2, 6):
        res = enumerate_definition4(n, 0)
        log(f"n={n} K=0: P(both)={fmt(res['P_both_cyclic'])} "
            f"P(same)={fmt(res['P_same_cycle'])} "
            f"P(diff)={fmt(res['P_diff_cycle'])}")
        assert res["P_both_cyclic"] == 1
        assert res["P_same_cycle"] == Fraction(1, 2)
        assert res["P_diff_cycle"] == Fraction(1, 2)
    log("K=0: P(both)=1 exactly, P(same)=P(diff)=1/2 exactly, for all "
        "tested n. Matches document Sec 3.1 and Theorem J's Corollary.")
    log("")

    # ------------------------------------------------------------------
    # 2. K=1 sub-case isolation, R FIXED (not averaged) -- reproduces
    #    the document's claimed V_a(n), V_b(n) sub-case checks, and the
    #    false-start reproduction at n=3.
    # ------------------------------------------------------------------
    log("=" * 78)
    log("SECTION 2: K=1 sub-case isolation (R fixed), independent re-derivation")
    log("=" * 78)

    def Va_formula(n):
        return Fraction(3 * n + 1, 6 * n)

    def Vb_formula(n):
        return Fraction(n + 1, 3 * n)

    va_results = {}
    vb_results = {}
    for n in range(3, 7):  # need n>=3 for a genuine "r not in {0,1}" third point
        r_other = 2  # any label not in {0,1}
        res_a = enumerate_definition4(n, 1, r_fixed=r_other)
        va_pred = Va_formula(n)
        match_a = res_a["P_both_cyclic"] == va_pred
        log(f"n={n} Case(a) r={r_other} (r not in {{0,1}}): "
            f"brute={fmt(res_a['P_both_cyclic'])}  "
            f"hand-formula V_a(n)=(3n+1)/(6n)={fmt(va_pred)}  "
            f"MATCH={match_a}")
        assert match_a
        va_results[n] = str(res_a["P_both_cyclic"])

        res_b = enumerate_definition4(n, 1, r_fixed=0)
        vb_pred = Vb_formula(n)
        match_b = res_b["P_both_cyclic"] == vb_pred
        log(f"n={n} Case(b) r=0 (r IS query point 0): "
            f"brute={fmt(res_b['P_both_cyclic'])}  "
            f"hand-formula V_b(n)=(n+1)/(3n)={fmt(vb_pred)}  "
            f"MATCH={match_b}")
        assert match_b
        vb_results[n] = str(res_b["P_both_cyclic"])

        # symmetric check: r=1 (the OTHER query point) should give the
        # identical V_b(n) value by the 0<->1 relabeling symmetry
        res_b1 = enumerate_definition4(n, 1, r_fixed=1)
        match_b1 = res_b1["P_both_cyclic"] == vb_pred
        log(f"n={n} Case(c) r=1 (r IS query point 1, symmetric check): "
            f"brute={fmt(res_b1['P_both_cyclic'])}  MATCH V_b(n)={match_b1}")
        assert match_b1
    log("")

    # ------------------------------------------------------------------
    # 3. The false-start reproduction at n=3
    # ------------------------------------------------------------------
    log("=" * 78)
    log("SECTION 3: False-start reproduction at n=3")
    log("=" * 78)
    va3 = Va_formula(3)
    log(f"V_a(3) [the false-start value, i.e. treating Case(a) as if it "
        f"were the WHOLE unconditional answer] = {fmt(va3)}")
    assert va3 == Fraction(5, 9)
    log("Confirmed: the false-start value IS exactly 5/9 at n=3, matching "
        "the document's self-disclosure. This is Case(a)'s CONDITIONAL "
        "value only, wrongly reported as unconditional in the document's "
        "disclosed first attempt.")
    log("")

    # ------------------------------------------------------------------
    # 4. K=1 full closed form (R averaged over all n choices) -- the
    #    genuine Definition-4 model -- vs. hand-reassembled formula AND
    #    vs. the document's claimed closed form (3n^2-n+2)/(6n^2).
    # ------------------------------------------------------------------
    log("=" * 78)
    log("SECTION 4: K=1 full closed form, R averaged (genuine Definition 4)")
    log("=" * 78)

    def P_both_K1_reassembled(n):
        # my own from-scratch reassembly: (n-2)/n * V_a(n) + 2/n * V_b(n)
        return Fraction(n - 2, n) * Va_formula(n) + Fraction(2, n) * Vb_formula(n)

    def P_both_K1_document(n):
        return Fraction(3 * n * n - n + 2, 6 * n * n)

    k1_full_results = {}
    for n in range(2, 8):
        res = enumerate_definition4(n, 1, r_fixed=None)
        reassembled = P_both_K1_reassembled(n)
        doc_formula = P_both_K1_document(n)
        assert reassembled == doc_formula, (
            f"MY reassembly disagrees with document's closed form at n={n}: "
            f"{reassembled} vs {doc_formula}"
        )
        match = res["P_both_cyclic"] == doc_formula
        log(f"n={n}: brute(R averaged)={fmt(res['P_both_cyclic'])}  "
            f"my-reassembly=(n-2)/n*Va+2/n*Vb={fmt(reassembled)}  "
            f"document-closed-form=(3n^2-n+2)/(6n^2)={fmt(doc_formula)}  "
            f"ALL MATCH={match}")
        assert match
        k1_full_results[n] = str(res["P_both_cyclic"])

        # also verify the same-cycle / diff-cycle exact 1/2 split
        # (Theorem J's Corollary, cited, re-verified as a sanity check
        # on our own brute-force harness's cycle_id logic)
        half_both = Fraction(res["P_both_cyclic"], 1) if False else None
        assert res["P_same_cycle"] == res["P_diff_cycle"] == res["P_both_cyclic"] / 2, (
            f"Theorem J Corollary sanity check FAILED at n={n},K=1: "
            f"same={res['P_same_cycle']} diff={res['P_diff_cycle']} "
            f"both/2={res['P_both_cyclic']/2}"
        )
    log("Theorem J's Corollary (P(same)=P(diff)=P(both)/2 EXACTLY, every "
        "n) independently re-confirmed by our own harness at K=1, n=2..7.")
    log("")

    # ------------------------------------------------------------------
    # 5. Rate check: n*(P_n^{(1)}(both) - 1/2) -> -1/6
    # ------------------------------------------------------------------
    log("=" * 78)
    log("SECTION 5: Rate check")
    log("=" * 78)
    for n in [10, 100, 1000, 10 ** 6]:
        val = P_both_K1_document(n)
        rate = n * (val - Fraction(1, 2))
        log(f"n={n}: n*(P_n^(1)(both)-1/2) = {fmt(rate)}  "
            f"(exact = -1/6 + 1/(3n) -> -1/6 as n->infty)")
        assert rate == Fraction(-1, 6) + Fraction(1, 3 * n)
    log("Confirmed: n*(P-1/2) = -1/6 + 1/(3n) exactly, algebra is correct, "
        "limit is exactly -1/6.")
    log("")

    # ------------------------------------------------------------------
    # 6. K=2 spot checks against the document's own table
    # ------------------------------------------------------------------
    log("=" * 78)
    log("SECTION 6: K=2 exact enumeration, spot-checking document's table")
    log("=" * 78)
    doc_k2_table = {
        3: Fraction(10, 27),
        4: Fraction(49, 144),
        5: Fraction(33, 100),
        6: Fraction(44, 135),
        7: Fraction(143, 441),
    }
    k2_results = {}
    for n in sorted(doc_k2_table.keys()):
        t0 = time.time()
        res = enumerate_definition4(n, 2, r_fixed=None)
        dt = time.time() - t0
        doc_val = doc_k2_table[n]
        match = res["P_both_cyclic"] == doc_val
        log(f"n={n} K=2: brute={fmt(res['P_both_cyclic'])}  "
            f"document table value={fmt(doc_val)}  MATCH={match}  "
            f"[{dt:.1f}s, {res['total']} configs enumerated]")
        assert match, f"K=2 n={n} MISMATCH vs document table!"
        k2_results[n] = str(res["P_both_cyclic"])
        # Theorem J corollary sanity re-check at K=2 too
        assert res["P_same_cycle"] == res["P_diff_cycle"] == res["P_both_cyclic"] / 2
    log("")

    # ------------------------------------------------------------------
    # 7. K=3 spot checks (bonus, beyond mandate minimum)
    # ------------------------------------------------------------------
    log("=" * 78)
    log("SECTION 7: K=3 exact enumeration, spot-checking document's table")
    log("=" * 78)
    doc_k3_table = {
        4: Fraction(19, 64),
        5: Fraction(3383, 12500),
        6: Fraction(233, 900),
    }
    k3_results = {}
    for n in sorted(doc_k3_table.keys()):
        t0 = time.time()
        res = enumerate_definition4(n, 3, r_fixed=None)
        dt = time.time() - t0
        doc_val = doc_k3_table[n]
        match = res["P_both_cyclic"] == doc_val
        log(f"n={n} K=3: brute={fmt(res['P_both_cyclic'])}  "
            f"document table value={fmt(doc_val)}  MATCH={match}  "
            f"[{dt:.1f}s, {res['total']} configs enumerated]")
        assert match, f"K=3 n={n} MISMATCH vs document table!"
        k3_results[n] = str(res["P_both_cyclic"])
        assert res["P_same_cycle"] == res["P_diff_cycle"] == res["P_both_cyclic"] / 2
    log("")

    t_total = time.time() - t_start
    log("=" * 78)
    log(f"ALL CHECKS PASSED. Total wall time: {t_total:.1f}s")
    log("=" * 78)

    results = {
        "K1_case_a_Va": va_results,
        "K1_case_b_Vb": vb_results,
        "K1_false_start_n3": "5/9",
        "K1_full_closed_form": k1_full_results,
        "K2_full": k2_results,
        "K3_full": k3_results,
        "wall_time_s": t_total,
    }
    with open(
        "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/"
        "CORE_NUMERICS/u12_universality/theorem/conjecture2_direct_attempt/"
        "joint_two_point_attempt/joint_exploration_continuum_attempt/adversarial/"
        "bruteforce_definition4_results.json",
        "w",
    ) as fh:
        json.dump(results, fh, indent=2)

    with open(
        "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/"
        "CORE_NUMERICS/u12_universality/theorem/conjecture2_direct_attempt/"
        "joint_two_point_attempt/joint_exploration_continuum_attempt/adversarial/"
        "bruteforce_definition4.log",
        "w",
    ) as fh:
        fh.write("\n".join(log_lines) + "\n")


if __name__ == "__main__":
    main()
