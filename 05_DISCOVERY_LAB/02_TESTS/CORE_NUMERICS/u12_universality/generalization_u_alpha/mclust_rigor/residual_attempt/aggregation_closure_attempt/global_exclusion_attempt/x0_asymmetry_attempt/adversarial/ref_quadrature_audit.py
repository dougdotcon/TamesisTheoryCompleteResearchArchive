"""REFEREE: audit of the TARGET's quadrature against high-precision values.

Runs the target's own `x0_asym_candidate.phi_CAND / phi_EPS` (400x250 uniform
trapezoid) and this referee's adaptive Gauss-Kronrod on a closed-form H, on
the 18-cell grid, and reports the relative difference.  A quadrature error
comparable to the claimed phi_EPS effect (~0.1-2.3%) would invalidate the
comparison; we need it to be orders of magnitude smaller.

This is the ONLY place the target's code is executed (as an object under
test).  Nothing is imported from it into the referee's own measurement or
formula pipeline.
"""
import os
import sys

TARGET = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import ref_formula as R                                   # noqa: E402

CELLS = ([(32768, 8, c) for c in (10.0, 40.0, 160.0)]
         + [(65536, 50, c) for c in (10.0, 50.0, 150.0, 400.0)]
         + [(65536, 100, c) for c in (10.0, 50.0, 150.0, 400.0)]
         + [(65536, 200, c) for c in (5.0, 20.0, 60.0, 150.0)]
         + [(65536, 300, 150.0), (65536, 100, 600.0), (65536, 400, 100.0)])


def main():
    sys.path.insert(0, TARGET)
    import x0_asym_candidate as tgt                       # target under test

    print("%6s %4s %7s %8s | %-38s | %-38s | %9s" %
          ("n", "b", "c", "rho", "phi_CAND  target / referee / rel",
           "phi_EPS   target / referee / rel", "EPS-CAND%"))
    worst_c = worst_e = 0.0
    for (n, b, c) in CELLS:
        rho = R.rho_of(c, n, b)
        tc, te = tgt.phi_CAND(c, n, b), tgt.phi_EPS(c, n, b)
        rc, re_ = R.phi_CAND(c, n, b), R.phi_EPS(c, n, b)
        dc, de = abs(tc - rc) / rc, abs(te - re_) / re_
        worst_c = max(worst_c, dc)
        worst_e = max(worst_e, de)
        print("%6d %4d %7.1f %8.4f | %.7f %.7f %8.1e | %.7f %.7f %8.1e | %+8.3f%%"
              % (n, b, c, rho, tc, rc, dc, te, re_, de, 100 * (re_ - rc) / rc))
    print()
    print("worst relative quadrature disagreement:  phi_CAND %.2e   phi_EPS %.2e"
          % (worst_c, worst_e))


if __name__ == "__main__":
    main()
