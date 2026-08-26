"""
Symbolic closed-form derivation of P_nn(n,2) := P(0,1 both cyclic | K=2 reroute
sources fixed at two OTHER indices, non-rerouted), via exact resummation
(sympy) of the case-split derived from scratch in ATTEMPT.md.

Assembly (see ATTEMPT.md sections 3-5 for the full derivation):

  P_nn(n,2) = sum_{p=1}^{n-1} sum_{q=1}^{n-p} [2/(n(n-1))] * T(p,q) / [(n-2)(n-3)]

where (p,q) is the (proved) uniform joint law of the two "arc lengths"
(source-1's-forward-arc length p, source-0's-forward-arc length q), and

  O := n - p - q
  S1(p,q) := (n+q)*p*(p-1) / (2*n^2)         [= sum_i P(arc1 pos i cyclic)]
  S2(p,q) := (n+p)*q*(q-1) / (2*n^2)         [= sum_i P(arc2 pos i cyclic)]
  T(p,q)  := O*(O-1)
             + O*(n+q)*p*(p-1)/n^2 + O*(n+p)*q*(q-1)/n^2
             + (n+q)*p*(p-1)*(p-2)/(3*n^2) + (n+p)*q*(q-1)*(q-2)/(3*n^2)
             + p*(p-1)*q*(q-1)/n^2

This script (a) simplifies T(p,q) symbolically, (b) performs the double sum
over the triangle p>=1,q>=1,p+q<=n exactly in sympy, (c) simplifies the
result to a closed form P_nn(n,2)(n), and (d) evaluates it at small n to
compare against independent brute-force enumeration (brute_force_k2.py).
"""
import sympy as sp

n, p, q = sp.symbols('n p q', positive=True, integer=True)

O = n - p - q
S1 = (n + q) * p * (p - 1) / (2 * n**2)
S2 = (n + p) * q * (q - 1) / (2 * n**2)

T = (O * (O - 1)
     + O * (n + q) * p * (p - 1) / n**2
     + O * (n + p) * q * (q - 1) / n**2
     + (n + q) * p * (p - 1) * (p - 2) / (3 * n**2)
     + (n + p) * q * (q - 1) * (q - 2) / (3 * n**2)
     + p * (p - 1) * q * (q - 1) / n**2)

T = sp.expand(T)
print("T(p,q) expanded:")
sp.pprint(T)

# Double sum over p=1..n-1, q=1..n-p  (i.e. p+q<=n, p,q>=1)
qq = sp.symbols('qq', integer=True)
inner = sp.summation(T, (q, 1, n - p))
inner = sp.simplify(inner)
print("\nInner sum over q (fixed p, symbolic) simplified:")
sp.pprint(inner)

outer = sp.summation(inner, (p, 1, n - 1))
outer = sp.simplify(outer)
print("\nOuter sum (= sum_{p,q} T(p,q)) simplified:")
sp.pprint(outer)

Pnn2 = sp.simplify(sp.Rational(2, 1) * outer / (n * (n - 1) * (n - 2) * (n - 3)))
Pnn2 = sp.simplify(Pnn2)
print("\nP_nn(n,2) closed form:")
sp.pprint(Pnn2)
print("\nFactored / together:")
sp.pprint(sp.factor(sp.together(Pnn2)))

print("\nExpanded as series in 1/n (for sanity, leading terms):")
x = sp.symbols('x', positive=True)  # x = 1/n
expr_x = Pnn2.subs(n, 1 / x)
print(sp.series(expr_x, x, 0, 4))

# Numeric evaluation at n=4..10
print("\nNumeric evaluation:")
for nv in range(4, 12):
    val = Pnn2.subs(n, nv)
    val = sp.nsimplify(val)
    print(f"n={nv}: P_nn(n,2) = {val} = {float(val):.6f}")
