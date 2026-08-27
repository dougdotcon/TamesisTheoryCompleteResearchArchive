"""
Miscellaneous arithmetic/consistency spot-checks on numbers quoted verbatim
in the target's ATTEMPT.md (its Sec 3, Sec 4 tables), independent of the
main verification scripts. Pure arithmetic, no modeling assumptions.
"""
from fractions import Fraction as F

print("=" * 70)
print("Check 1: c_0(K) = 1/(K+1) exactly, read off the K=7,K=8 closed forms'")
print("leading coefficient ratio (numerator leading term / denominator)")
print("=" * 70)
# P_nn(n,7) = (6435 n^7 + ... )/(51480 n^7); c_0 = 6435/51480
c0_7 = F(6435, 51480)
c0_8 = F(24310, 218790)
print(f"c_0(7) = 6435/51480 = {c0_7}  (expect 1/8): {c0_7 == F(1,8)}")
print(f"c_0(8) = 24310/218790 = {c0_8}  (expect 1/9): {c0_8 == F(1,9)}")
assert c0_7 == F(1, 8) and c0_8 == F(1, 9)

print("\n" + "=" * 70)
print("Check 2: c_1(K) matches the 1/n coefficient of the quoted closed forms")
print("=" * 70)
c1_7_from_poly = F(17548, 51480)
c1_8_from_poly = F(76627, 218790)
c1_7_claimed = F(4387, 12870)
c1_8_claimed = F(76627, 218790)
print(f"c_1(7) from polynomial coeff = {c1_7_from_poly} = {c1_7_from_poly}, claimed = {c1_7_claimed}, "
      f"MATCH: {c1_7_from_poly == c1_7_claimed}")
print(f"c_1(8) from polynomial coeff = {c1_8_from_poly}, claimed = {c1_8_claimed}, "
      f"MATCH: {c1_8_from_poly == c1_8_claimed}")
assert c1_7_from_poly == c1_7_claimed and c1_8_from_poly == c1_8_claimed

print("\n" + "=" * 70)
print("Check 3: Sec 4 bonus table -- decimal values and 'ratio to K-1' column")
print("=" * 70)
c1 = {1: F(1, 6), 2: F(7, 30), 3: F(19, 70), 4: F(187, 630), 5: F(437, 1386),
      6: F(1979, 6006), 7: F(4387, 12870), 8: F(76627, 218790)}
claimed_decimals = {1: 0.16667, 2: 0.23333, 3: 0.27143, 4: 0.29683, 5: 0.31530,
                     6: 0.32950, 7: 0.34087, 8: 0.35023}
claimed_ratios = {2: 1.400, 3: 1.163, 4: 1.094, 5: 1.062, 6: 1.045, 7: 1.035, 8: 1.027}

all_ok = True
for K in range(1, 9):
    dec = round(float(c1[K]), 5)
    dec_ok = abs(dec - claimed_decimals[K]) < 1e-5
    all_ok &= dec_ok
    line = f"K={K}: c1={c1[K]} decimal={dec}  claimed={claimed_decimals[K]}  {'OK' if dec_ok else '*** MISMATCH ***'}"
    if K > 1:
        ratio = float(c1[K] / c1[K - 1])
        ratio_rounded = round(ratio, 3)
        ratio_ok = abs(ratio_rounded - claimed_ratios[K]) < 1e-9
        all_ok &= ratio_ok
        line += f"   ratio_to_K-1(exact)={ratio:.6f} rounded={ratio_rounded}  claimed={claimed_ratios[K]}  " \
                f"{'OK' if ratio_ok else '*** MISMATCH (rounding slip) ***'}"
    print(line)

print(f"\nALL Sec-4-table arithmetic checks pass: {all_ok}")
if not all_ok:
    print("(See REFEREE_REPORT.md 'Named issues' -- expected one LOW-severity")
    print(" rounding slip at K=7's ratio-to-K-1 column: true value rounds to")
    print(" 1.034, table prints 1.035.)")
