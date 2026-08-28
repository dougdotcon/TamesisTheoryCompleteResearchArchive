"""
ADVERSARIAL CHECK 3 -- fully independent sanity check of Check 1/2's key
algebraic simplification (x'+w = x+y), via RAW double numerical quadrature
of the literal double integral definition, WITHOUT using the closed-form
R(z) shortcut anywhere. If this matches Check 1/2's closed-form route, the
simplification (and hence the refutation of Sec 4.4) is confirmed via a
second, structurally independent computation path.

(K_A^raw(y,t) f)(x) = int_t^y e^{-(y-w)/eps} * (T_w f)(x+y-w) dw
(T_w f)(x') = int_0^inf e^{-u^2/2-u(x'+w)} f(x'+u) du

For f=1: (T_w f)(x') = int_0^inf e^{-u^2/2-u(x'+w)} du  -- computed here by
DIRECT quadrature (mpmath.quad), NOT via the erfcx closed form.
"""
import mpmath as mp
mp.mp.dps = 30

def T_w_of_1(xprime, w):
    xprime = mp.mpf(xprime); w = mp.mpf(w)
    f = lambda u: mp.e**(-u*u/2 - u*(xprime+w))
    return mp.quad(f, [0, mp.inf])

def K_A_raw_of_1(x, y, t, eps):
    x = mp.mpf(x); y = mp.mpf(y); t = mp.mpf(t); eps = mp.mpf(eps)
    def integrand(w):
        xprime = x + y - w
        return mp.e**(-(y-w)/eps) * T_w_of_1(xprime, w)
    return mp.quad(integrand, [t, y])

def M_y_at(x, y, eps):
    x = mp.mpf(x); y = mp.mpf(y); eps = mp.mpf(eps)
    return (1 - eps*(x+y))/eps

eps = mp.mpf('0.1')
print("Direct double-quadrature check (no R(z) shortcut used):")
print(f"{'x':>6} {'y':>6}   raw K_A^raw[1](x)     M_y*K_A^raw[1](x)")
for (x, y) in [(0,1),(0,5),(0,20),(5,20),(20,20),(0,100),(50,100),(100,100),(0,1000),(500,1000)]:
    kv = K_A_raw_of_1(x, y, 0, eps)
    my = M_y_at(x, y, eps)
    print(f"{x:>6} {y:>6}   {float(kv):.10f}         {float(my*kv):.10f}")

print()
print("Cross-check against closed-form route (h_eps(x+y)*(1-e^{-(y-t)/eps})):")
def R_closed(z):
    z = mp.mpf(z)
    return mp.sqrt(mp.pi/2) * mp.erfc(z/mp.sqrt(2)) * mp.e**(z*z/2)
for (x, y) in [(0,1),(0,5),(0,20),(5,20),(20,20),(0,100),(50,100),(100,100)]:
    x=mp.mpf(x); y=mp.mpf(y); t=mp.mpf(0)
    z = x+y
    closed = abs(1-eps*z)*R_closed(z)*(1-mp.e**(-(y-t)/eps))
    print(f"x={x},y={y}: closed-form M_y*K_A^raw[1] = {float(closed):.10f}")
