"""
Independent reproduction of ATTEMPT.md Section 6 item 1's self-caught bug
claim: an earlier version of script 02 Part B used sp.hyper() directly and
got exactly 8 mismatches, all at m=0, n=1..8, due to the confluent
degeneracy 2F1(a,b;a;z)=(1-z)^-b firing when -(n-m)=-n (i.e. m=0).

We reproduce the BUGGY version exactly as described and check: (i) does
it actually mismatch; (ii) are the mismatches EXACTLY the m=0 rows and
nothing else, for n=1..8.
"""
import sympy as sp

def T_direct(n_val, m_val, g_val):
    return sum(
        sp.binomial(jj + m_val, m_val) * sp.binomial(n_val - jj, m_val) * (1 - g_val) ** jj
        for jj in range(0, n_val - m_val + 1)
    )

mismatches = []
checks = 0
for n_val in range(1, 9):
    for m_val in range(0, n_val + 1):
        g_val = sp.Rational(3, 10)
        direct = T_direct(n_val, m_val, g_val)
        a_val, b_val, c_val, z_val = -(n_val - m_val), m_val + 1, -n_val, 1 - g_val
        # THE BUGGY VERSION: sp.hyper() called directly (per the self-caught
        # issue description), then multiplied by C(n,m)
        buggy_2f1 = sp.hyper([a_val, b_val], [c_val], z_val)
        buggy_val = sp.binomial(n_val, m_val) * buggy_2f1
        try:
            buggy_val_num = sp.nsimplify(sp.N(buggy_val, 30))
            is_mismatch = sp.simplify(direct - buggy_val) != 0
        except Exception as e:
            is_mismatch = True
        checks += 1
        if is_mismatch:
            mismatches.append((n_val, m_val))

print(f"Total (n,m) pairs checked: {checks}")
print(f"Mismatches found: {len(mismatches)}")
print("Mismatch list:", mismatches)
all_m0 = all(m == 0 for (n, m) in mismatches)
print(f"All mismatches at m=0? {all_m0}")
count_m0_total = sum(1 for n_val in range(1,9) for m_val in range(0,n_val+1) if m_val==0)
print(f"Number of m=0 rows total (n=1..8): {count_m0_total}")
print()
if len(mismatches) == 8 and all_m0:
    print("EXACTLY REPRODUCES the target's self-caught-bug description:")
    print("8 mismatches, all and only at m=0, n=1..8 -- matches ATTEMPT.md")
    print("Sec.6 item 1's account precisely.")
else:
    print(f"DOES NOT exactly match target's claim (expected 8 mismatches, all m=0;")
    print(f"got {len(mismatches)} mismatches: {mismatches})")
