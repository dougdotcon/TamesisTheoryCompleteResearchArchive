import mpmath as mp
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ref01_fresh_family import build_family, comb_eval, erfcx

mp.mp.dps = 60

c = 1000

# check E' identity independently first
s = mp.mpf('0.37')
h = mp.mpf('1e-25')
E = lambda ss: erfcx(ss*mp.sqrt(mp.mpf(c)/2))
num = (E(s+h)-E(s-h))/(2*h)
sc = mp.sqrt(2*mp.mpf(c)/mp.pi)
pred = c*s*E(s) - sc
print("E' check: numeric deriv - predicted =", num-pred)

a, b = build_family(c, 6)

def a0(k):
    return comb_eval(a[k], mp.mpf(0), c)

def b0(k):
    return comb_eval(b[k], mp.mpf(0), c)

print("a_2(0) =", a0(2), " expect ~520316.636488")
print("a_3(0) =", a0(3), " expect ~-180730907.6285")
print("a_4(0) =", a0(4), " expect ~47146963944.14")
print("b_2(0) =", b0(2), " expect ~-20816.636488")
print("b_1(0) =", b0(1), " expect sqrt(pi*c/2) =", mp.sqrt(mp.pi*c/2))
