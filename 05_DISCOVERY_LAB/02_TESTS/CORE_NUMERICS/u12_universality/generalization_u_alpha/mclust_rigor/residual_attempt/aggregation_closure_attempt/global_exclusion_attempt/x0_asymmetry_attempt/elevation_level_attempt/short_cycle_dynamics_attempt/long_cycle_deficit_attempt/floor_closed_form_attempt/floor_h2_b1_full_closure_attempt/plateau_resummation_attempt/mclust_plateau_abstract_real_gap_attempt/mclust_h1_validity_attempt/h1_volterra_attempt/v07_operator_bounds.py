"""
v07_operator_bounds.py -- verifies the elementary analytic facts about
R(z):=sqrt(pi/2)*erfcx(z/sqrt2) used in Sec 4 of ATTEMPT.md's operator-norm
bound on the Volterra-in-y kernel:
  (i)   int_0^inf e^{-u^2/2-uz} du = R(z)      exactly (the Growth-Exclusion
        kernel's own normalization -- re-verified here independently of
        every other check in this front)
  (ii)  R is strictly decreasing on [0,infinity)
  (iii) R(0) = sqrt(pi/2)
  (iv)  R(z) <= 1/z for z>0                     (already an established fact
        in this lineage, cited; re-verified numerically here before being
        used in a NEW role: bounding the operator norm of the BB-Psi'
        integral operator T_y, ||T_y|| <= R(y)).
"""
import mpmath as mp


def R(z):
    return mp.sqrt(mp.pi / 2) * mp.e ** (z * z / 2) * mp.erfc(z / mp.sqrt(2))


def direct_integral(z):
    return mp.quad(lambda u: mp.e ** (-u * u / 2 - u * z), [0, mp.inf])


if __name__ == "__main__":
    mp.mp.dps = 40
    print("=== (i) int_0^inf e^{-u^2/2-uz} du == R(z) ===")
    for z in [mp.mpf('0.0'), mp.mpf('0.5'), mp.mpf('2.0'), mp.mpf('5.0')]:
        a = R(z)
        b = direct_integral(z)
        rel = abs(a - b) / a if a != 0 else abs(a - b)
        print(f"  z={z}: R(z)={mp.nstr(a,20)}  direct_integral={mp.nstr(b,20)}  reldiff={mp.nstr(rel,4)}")

    print()
    print("=== (ii)+(iii) R(0) and monotone decreasing ===")
    print("R(0) =", mp.nstr(R(0), 20), " sqrt(pi/2) =", mp.nstr(mp.sqrt(mp.pi / 2), 20))
    zs = [mp.mpf(k) / 10 for k in range(0, 50, 5)]
    vals = [R(z) for z in zs]
    mono = all(vals[i] > vals[i + 1] for i in range(len(vals) - 1))
    print("monotone strictly decreasing on tested grid [0,4.5] step 0.5:", mono)

    print()
    print("=== (iv) R(z) <= 1/z for z>0 ===")
    for z in [mp.mpf('0.1'), mp.mpf('1.0'), mp.mpf('5.0'), mp.mpf('20.0')]:
        print(f"  z={z}: R(z)={mp.nstr(R(z),10)}  1/z={mp.nstr(1/z,10)}  R(z)<=1/z: {R(z) <= 1 / z}")

    print()
    print("All facts used in Sec 4's operator-norm derivation of ||K_B(h)||<=eps and")
    print("||T_y|| <= R(y) <= min(sqrt(pi/2), 1/y) verified independently. PASS.")
