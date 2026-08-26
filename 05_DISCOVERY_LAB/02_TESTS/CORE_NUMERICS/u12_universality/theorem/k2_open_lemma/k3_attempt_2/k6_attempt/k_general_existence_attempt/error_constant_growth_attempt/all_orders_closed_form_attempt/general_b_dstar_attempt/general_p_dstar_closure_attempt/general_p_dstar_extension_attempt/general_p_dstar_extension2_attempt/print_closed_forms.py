"""
print_closed_forms.py -- prints, and cross-validates, the new b=0,1
closed forms for D^{*(p)}_r(b), p=21,...,40, via assemble.py's own
pure-Fraction printed_form_b0/b1 routines. Writes the full list to
printed_forms.log.
"""

from ingredients import poly_eval
from assemble import printed_form_b0, printed_form_b1, _format_poly
import ground_truth as gt


def main():
    checks = 0
    fails = 0
    for p in range(21, 41):
        for b, fn in ((0, printed_form_b0), (1, printed_form_b1)):
            coef, rem = fn(p)
            print(f"--- D^{{*({p})}}_r({b}) ---")
            print(f"coef(r) = {_format_poly(coef)}")
            print(f"rem(r)  = {_format_poly(rem)}")
            for r in (0, 1, 5, 17, 50, 150, 200):
                val = poly_eval(coef, r) * gt.phi_r(r) + poly_eval(rem, r)
                want = gt.D_star(p, r, b)
                checks += 1
                if val != want:
                    fails += 1
                    print(f"  MISMATCH r={r}: got {val} want {want}")
            print()
    print(f"print_closed_forms: {checks} cross-checks, {fails} fails")
    return fails == 0


if __name__ == "__main__":
    ok = main()
    print("print_closed_forms: OK" if ok else "print_closed_forms: FAILURES")
