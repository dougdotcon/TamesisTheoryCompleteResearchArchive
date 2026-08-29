import mpmath as mp
mp.mp.dps = 25

def f_rational(xv):
    return 1/(1+xv)

def theta(hprime, z, x, f):
    def integrand(v):
        u = v/z
        return mp.e**(-u**2/2 - v) * f(x + hprime + u) / z
    bpts = [0, mp.mpf('0.5'), 2, 5, 15, 40, 80]
    return mp.quad(integrand, bpts)

def K_A_raw(y, t, x, eps, f):
    z = x + y
    h = y - t
    if h <= 0:
        return mp.mpf(0)
    def outer(hp):
        return mp.e**(-hp/eps) * theta(hp, z, x, f)
    cand = [eps/10, eps/2, eps, 2*eps, 5*eps, 10*eps, 25*eps, 50*eps]
    bpts = sorted(set([mp.mpf(0)] + [c for c in cand if c < h] + [h]))
    return mp.quad(outer, bpts)

def K_B(h, x, eps, f):
    if h <= 0:
        return mp.mpf(0)
    def integrand(v):
        return mp.e**(-v/eps) * f(x + v)
    cand = [eps/10, eps/2, eps, 2*eps, 5*eps, 10*eps, 25*eps, 50*eps]
    bpts = sorted(set([mp.mpf(0)] + [c for c in cand if c < h] + [h]))
    return mp.quad(integrand, bpts)

def M_y_val(z, eps):
    return (1 - eps*z)/eps

def K_full(y, t, x, eps, f):
    z = x + y
    h = y - t
    A = K_A_raw(y, t, x, eps, f)
    return M_y_val(z, eps)*A + K_B(h, x, eps, f)

def closed_form(y, t, x, eps, f):
    z = x + y
    h = y - t
    return (f(x) - mp.e**(-h/eps)*f(x+h)) / z

print("PART 3: spot check x=3 (s02c regime) -- eps=0.1, z in {200,1000}, ratios {0.1,0.5,0.9}")
eps3 = mp.mpf('0.1')
x3 = mp.mpf(3)
for zt in [mp.mpf(200), mp.mpf(1000)]:
    y3 = zt - x3
    for r in [mp.mpf('0.1'), mp.mpf('0.5'), mp.mpf('0.9')]:
        h = r*y3
        t = y3 - h
        Kv = K_full(y3, t, x3, eps3, f_rational)
        cf = closed_form(y3, t, x3, eps3, f_rational)
        err = Kv - cf
        z2err = zt**2 * err
        print(f"z={float(zt):6.0f} h/y={float(r):5.2f}  z^2*err = {mp.nstr(z2err,6)}")
        import sys; sys.stdout.flush()
print("\nTarget's claimed table (Sec 4.3): z^2*err approx -0.039 at z=200, -0.038 at z=1000, constant across ratios.")
