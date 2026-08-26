"""
h01_gap_characterization.py -- precise characterization of the "abstract
vs real ~30% gap" named by floor_closed_form_attempt/ATTEMPT.md SS4/SS6
and repeatedly flagged as out-of-scope-but-unresolved by every descendant
front (floor_h2_b1_full_closure_attempt, plateau_resummation_attempt).

WHAT THE GAP IS (established, cited from the record, prose only -- no
.py file of any ancestor front opened):

  - "Real engine" side: phi(ell) := P(x0 cyclic | x0 not seed, L(x0)=ell),
    measured by DIRECT SIMULATION of the actual finite n=65536, c=1000
    M-CLUST(1) engine, binned by ell or by L/n. Two already-vetted,
    referee-confirmed tables exist in floor_closed_form_attempt/ATTEMPT.md
    (accepted DISC-DEC-057/062):
      Table T1 (SS2): 6 absolute-ell bins, [500,1000) .. [32768,65536)
      Table T2 (SS4): 9 relative L/n bins spanning the WHOLE far tail,
                       (0.031,0.061] .. (0.875,1.000], PLUS a separate
                       cluster-robust re-measurement of the 3 rightmost
                       bins (proper between-INSTANCE SEM, not the naive,
                       inflated between-POINT SEM) that the front's own
                       replication showed changes two of those three
                       bins substantially.

  - "Abstract" side: Phi(0,t0) for the idealized (s,g) recursive process
    at the SAME (c=1000) parameter, t0 identified with L/n. Originally
    known only to ~2-3 significant figures ("~0.037-0.039", measured by
    Monte Carlo of the abstract process, floor_closed_form_attempt SS4
    T3). floor_h2_b1_full_closure_attempt + its referee (DISC-DEC-071)
    and plateau_resummation_attempt + its referee (DISC-DEC-077)
    subsequently pinned this down to an EXACT, many-times-cross-validated
    121-digit value via the (P,Q)-family closed-form series (re-verified
    fresh in this front's own g01/g02):

        Pi(1000) = Phi(0, t0>=0.02) = 0.0377615983402126188243712025905770479904...

  - The GAP (as named by the ancestor documents): the abstract-process
    plateau sits ABOVE the real engine's plateau. It was characterized
    only as "~30%" (informally, from the ROUGH 2-sig-fig abstract value
    vs. the ROUGH 0.025-0.029 real-engine range) and explicitly NOT
    reconciled; floor_closed_form_attempt SS6 offers exactly two named,
    UNTESTED hypotheses for its source: (H-finite-n) "possibly a
    finite-n effect not captured by the n->infinity idealization", and
    (H-boundary) "possibly a remaining simplification in the abstract
    model's treatment of the s+g<=1 total-mass constraint for t0 near 1".

THIS SCRIPT: uses the now-EXACT abstract value (removing essentially all
abstract-side uncertainty) against the already-published, already-vetted
real-engine bin tables (cited verbatim as data, not re-derived -- these
numbers are matter of record, referee-confirmed, DISC-DEC-057/062) to
compute a bin-resolved relative gap, and tests directly (from the SHAPE
of the resulting table, no new simulation needed for this part) whether
either named hypothesis is consistent with the observed pattern.
"""

import mpmath as mp

mp.mp.dps = 30

PI_ABSTRACT = mp.mpf("0.0377615983402126188243712025905770479904")  # Pi(1000), exact (record + this front's own g02/g04 re-verification)
PHI_U = mp.mpf("0.0280")  # phi_U(1000), reference used throughout the ancestor lineage

# --- Table T1 (floor_closed_form_attempt ATTEMPT.md SS2, "Candidate 1" table) ---
# absolute-ell bins, midpoint used as representative t0=ell/n, n=65536
T1 = [
    # (bin_lo, bin_hi, phi_hat, sem)
    (500, 1000, mp.mpf("0.0298"), mp.mpf("0.0002")),
    (2000, 4000, mp.mpf("0.0265"), mp.mpf("0.00009")),
    (4000, 8000, mp.mpf("0.0253"), mp.mpf("0.00006")),
    (8000, 16384, mp.mpf("0.0258"), mp.mpf("0.00005")),
    (16384, 32768, mp.mpf("0.0266"), mp.mpf("0.00003")),
    (32768, 65536, mp.mpf("0.0273"), mp.mpf("0.00002")),
]
N = mp.mpf(65536)

# --- Table T2 (floor_closed_form_attempt ATTEMPT.md SS4, point-level) ---
T2_POINT = [
    # (lo, hi) as L/n, phi_hat, sem
    (mp.mpf("0.031"), mp.mpf("0.061"), mp.mpf("0.02781"), mp.mpf("0.00007")),
    (mp.mpf("0.061"), mp.mpf("0.122"), mp.mpf("0.02716"), mp.mpf("0.00005")),
    (mp.mpf("0.122"), mp.mpf("0.250"), mp.mpf("0.02747"), mp.mpf("0.00003")),
    (mp.mpf("0.250"), mp.mpf("0.375"), mp.mpf("0.02673"), mp.mpf("0.00003")),
    (mp.mpf("0.375"), mp.mpf("0.500"), mp.mpf("0.02722"), mp.mpf("0.00003")),
    (mp.mpf("0.500"), mp.mpf("0.625"), mp.mpf("0.02781"), mp.mpf("0.00003")),
    (mp.mpf("0.625"), mp.mpf("0.750"), mp.mpf("0.02692"), mp.mpf("0.00003")),
    (mp.mpf("0.750"), mp.mpf("0.875"), mp.mpf("0.02866"), mp.mpf("0.00003")),  # flagged unreliable, see T2_CLUSTER
    (mp.mpf("0.875"), mp.mpf("1.000"), mp.mpf("0.02577"), mp.mpf("0.00003")),  # flagged unreliable, see T2_CLUSTER
]

# --- Table T2, cluster-robust re-measurement of the 3 rightmost bins ---
# (floor_closed_form_attempt ATTEMPT.md SS4, "cluster-robustness check")
# instance-averaged phi_hat with proper between-instance SEM -- the front's
# OWN replication showed the point-level SEM badly understates the true
# uncertainty for these bins (2 of 3 point-level values do not replicate).
T2_CLUSTER = [
    # (lo_ell, hi_ell) absolute L, L/n range, phi_hat_cluster, cluster_sem
    (24576, 32768, mp.mpf("0.375"), mp.mpf("0.500"), mp.mpf("0.02672"), mp.mpf("0.00060")),
    (49152, 57344, mp.mpf("0.750"), mp.mpf("0.875"), mp.mpf("0.02637"), mp.mpf("0.00070")),
    (57344, 65536, mp.mpf("0.875"), mp.mpf("1.000"), mp.mpf("0.02747"), mp.mpf("0.00068")),
]


def rel_gap(abstract, real):
    return (abstract - real) / real * 100


def main():
    print("=" * 78)
    print("PART A -- Table T1 (absolute-ell bins), gap = (Pi_abstract - phi_real)/phi_real")
    print("=" * 78)
    print(f"{'ell bin':>16s} {'t0=mid/n':>10s} {'phi_real':>10s} {'gap%':>8s} {'gap_vs_U%':>10s}")
    gaps_t1 = []
    for lo, hi, phat, sem in T1:
        mid = (lo + hi) / 2
        t0 = mid / N
        g = rel_gap(PI_ABSTRACT, phat)
        gU = rel_gap(PHI_U, phat)
        gaps_t1.append((float(t0), float(g)))
        print(f"[{lo:>6d},{hi:>6d}) {float(t0):>10.4f} {float(phat):>10.4f} {float(g):>7.2f}% {float(gU):>9.2f}%")

    print()
    print("=" * 78)
    print("PART B -- Table T2 (relative L/n bins, point-level, WHOLE far tail)")
    print("=" * 78)
    print(f"{'L/n bin':>16s} {'phi_real':>10s} {'gap%':>8s}   note")
    gaps_t2 = []
    for lo, hi, phat, sem in T2_POINT:
        g = rel_gap(PI_ABSTRACT, phat)
        note = ""
        if (lo, hi) in [(T2_POINT[7][0], T2_POINT[7][1]), (T2_POINT[8][0], T2_POINT[8][1])]:
            note = "<- point-level UNRELIABLE at this z (see cluster-robust below)"
        gaps_t2.append((float((lo + hi) / 2), float(g)))
        print(f"({float(lo):.3f},{float(hi):.3f}] {float(phat):>10.5f} {float(g):>7.2f}%   {note}")

    print()
    print("=" * 78)
    print("PART C -- Table T2, cluster-robust re-measurement of the 3 rightmost bins")
    print("(replaces the two unreliable point-level tail bins)")
    print("=" * 78)
    gaps_t2c = []
    for lo_ell, hi_ell, lo_r, hi_r, phat, sem in T2_CLUSTER:
        g = rel_gap(PI_ABSTRACT, phat)
        gaps_t2c.append((float((lo_r + hi_r) / 2), float(g)))
        print(f"({float(lo_r):.3f},{float(hi_r):.3f}] (cluster) phi_real={float(phat):.5f}+-{float(sem):.5f}  gap={float(g):.2f}%")

    # honest composite: T2 bins 1-6 (point-level, reliable, low individual z
    # against cluster-robust replication per the front's own SS4 finding)
    # + T2_CLUSTER for bins 7-9 (cluster-robust replacing point-level)
    print()
    print("=" * 78)
    print("PART D -- honest composite gap-vs-t0 table (best available real-engine")
    print("value at each t0 bin: point-level where reliable, cluster-robust for")
    print("the 3 rightmost/tail bins)")
    print("=" * 78)
    composite = []
    for i, (lo, hi, phat, sem) in enumerate(T2_POINT[:6]):
        composite.append((float((lo + hi) / 2), float(phat), float(rel_gap(PI_ABSTRACT, phat))))
    # bin 7 = (0.625,0.750] point-level (not in cluster re-check list -> keep point-level)
    lo, hi, phat, sem = T2_POINT[6]
    composite.append((float((lo + hi) / 2), float(phat), float(rel_gap(PI_ABSTRACT, phat))))
    # bins 8,9 -> cluster-robust
    for lo_ell, hi_ell, lo_r, hi_r, phat, sem in T2_CLUSTER[1:]:
        composite.append((float((lo_r + hi_r) / 2), float(phat), float(rel_gap(PI_ABSTRACT, phat))))

    composite.sort()
    gaps_only = [g for (_, _, g) in composite]
    for t0mid, phat, g in composite:
        print(f"t0~{t0mid:.3f}   phi_real={phat:.5f}   gap={g:6.2f}%")
    mean_gap = sum(gaps_only) / len(gaps_only)
    spread = max(gaps_only) - min(gaps_only)
    print()
    print(f"mean gap (composite, N={len(gaps_only)} bins) = {mean_gap:.2f}%")
    print(f"range: [{min(gaps_only):.2f}%, {max(gaps_only):.2f}%]   spread = {spread:.2f} pp")

    # Trend test: correlation of gap% vs t0 (composite table) -- crude
    # Pearson correlation, no scipy dependency
    xs = [t for (t, _, _) in composite]
    ys = [g for (_, _, g) in composite]
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / n
    sx = (sum((x - mx) ** 2 for x in xs) / n) ** 0.5
    sy = (sum((y - my) ** 2 for y in ys) / n) ** 0.5
    r = cov / (sx * sy)
    print(f"\nPearson r(gap%, t0) across composite bins = {r:.3f}  (n={n})")

    print()
    print("=" * 78)
    print("PART E -- magnitude/scaling argument against a naive vanishing")
    print("O(n^-1) or O(n^-1/2) finite-n-effect hypothesis")
    print("=" * 78)
    n_val = 65536
    print(f"n = {n_val}")
    print(f"  1/n        = {1/n_val:.3e}  ({100/n_val:.4f}% )")
    print(f"  1/sqrt(n)  = {1/n_val**0.5:.3e}  ({100/n_val**0.5:.2f}% )")
    c_val = 1000
    print(f"  c/n        = {c_val/n_val:.4f}  ({100*c_val/n_val:.2f}% )")
    print(f"  sqrt(c/n)  = {(c_val/n_val)**0.5:.4f}  ({100*(c_val/n_val)**0.5:.2f}% )")
    print(f"observed composite mean gap = {mean_gap:.1f}%  (O(1), NOT vanishing)")


if __name__ == "__main__":
    main()
