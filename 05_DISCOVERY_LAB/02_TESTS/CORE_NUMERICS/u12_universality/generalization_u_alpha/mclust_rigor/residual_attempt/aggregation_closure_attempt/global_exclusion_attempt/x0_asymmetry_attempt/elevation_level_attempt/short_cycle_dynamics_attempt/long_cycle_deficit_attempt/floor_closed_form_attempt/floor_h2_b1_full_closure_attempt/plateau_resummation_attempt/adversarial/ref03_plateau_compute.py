"""
Referee (adversarial) computation of Pi(c) at several c values, using ONLY
this referee's own fresh (P,Q)-family implementation (ref01_fresh_family.py)
-- built independently from ATTEMPT.md's prose (Sec 0/1.1), with NO script
of the front under review ever opened. Same 3-way-error-control philosophy
as ATTEMPT.md Sec 2.1 (approach / truncation / roundoff), applied
independently:
  - approach error: |S(260/c) - S(290/c)|
  - truncation: last-term/S magnitude, required tiny
  - roundoff: not separately re-run at higher dps here (budget); instead,
    cross-c consistency (matching to all quoted ATTEMPT.md digits at 3
    different c values, Sec 3 below) serves as the roundoff sanity check.

Usage: python3 ref03_plateau_compute.py <c> <K> <dps>
Writes ref03_result_c<c>.json in this directory.
"""
import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mpmath as mp
from ref01_fresh_family import build_family, comb_eval

def compute(c, K, dps):
    mp.mp.dps = dps
    t0 = time.time()
    a, b = build_family(c, K)
    build_t = time.time() - t0
    a0 = [comb_eval(a[k], mp.mpf(0), c) for k in range(K + 1)]
    eval_t = time.time() - t0 - build_t

    def S(t0v):
        s = mp.mpf(0)
        for k in range(K, -1, -1):
            s = s * t0v + a0[k]
        return s

    results = {}
    for ct0 in [230, 260, 290]:
        t0v = mp.mpf(ct0) / c
        val = S(t0v)
        last_term_rel = abs(a0[K] * t0v ** K) / abs(val)
        results[ct0] = (val, last_term_rel)

    diff_260_290 = abs(results[260][0] - results[290][0])
    diff_230_290 = abs(results[230][0] - results[290][0])
    stable_digits = int(-mp.log10(diff_260_290)) if diff_260_290 > 0 else dps

    out = {
        "c": c, "K": K, "dps": dps,
        "S230": mp.nstr(results[230][0], 130),
        "S260": mp.nstr(results[260][0], 130),
        "S290": mp.nstr(results[290][0], 130),
        "last_term_rel_290": mp.nstr(results[290][1], 6),
        "diff_260_290": mp.nstr(diff_260_290, 8),
        "diff_230_290": mp.nstr(diff_230_290, 8),
        "stable_digits_est": stable_digits,
        "build_time_s": build_t, "eval_time_s": eval_t,
        "total_time_s": time.time() - t0,
    }
    return out


if __name__ == "__main__":
    c = int(sys.argv[1]); K = int(sys.argv[2]); dps = int(sys.argv[3])
    out = compute(c, K, dps)
    print(json.dumps(out, indent=2))
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"ref03_result_c{c}.json")
    with open(fn, "w") as f:
        json.dump(out, f, indent=2)
    print("wrote", fn)
