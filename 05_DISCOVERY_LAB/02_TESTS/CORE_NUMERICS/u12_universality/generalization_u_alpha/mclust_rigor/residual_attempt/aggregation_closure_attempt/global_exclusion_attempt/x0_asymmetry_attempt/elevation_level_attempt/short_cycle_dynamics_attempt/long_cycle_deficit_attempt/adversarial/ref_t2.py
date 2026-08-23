import sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import ref_common as R

n = 65536
c = 1000
threshold = 2000
bvals = [
    dict(b=1,   seed=20260828110, N=2500),
    dict(b=5,   seed=20260828111, N=2500),
    dict(b=20,  seed=20260828112, N=2500),
    dict(b=50,  seed=20260828113, N=2500),
    dict(b=100, seed=20260828114, N=2500),
]

t_start = time.time()
rows = []
for bv in bvals:
    t0 = time.time()
    res = R.run_cell(n, bv["b"], c, threshold, N=bv["N"], seed_base=bv["seed"],
                      n_workers=4, label=f"T2-b{bv['b']}")
    phiU = R.phi_ref(bv["b"], c, n)
    print(R.report_line(res, phiU))
    dev = 100 * (res["phi_far"] - phiU) / phiU
    z = (res["phi_far"] - phiU) / res["se_delta"]
    rows.append((bv["b"], res["rho_measured"], phiU, res["phi_far"], res["se_delta"], dev, z))
    print(f"  [elapsed {time.time()-t0:.1f}s]\n", flush=True)

print(f"TOTAL T2 elapsed: {time.time()-t_start:.1f}s\n")

print("=== T2 summary table ===")
print(f"{'b':>4} {'rho':>8} {'phi_U(cpp)':>11} {'phi_far':>10} {'SEM':>10} {'dev%':>8} {'z':>7}")
for (b, rho, phiU, phifar, sem, dev, z) in rows:
    print(f"{b:>4} {rho:>8.4f} {phiU:>11.6f} {phifar:>10.6f} {sem:>10.6f} {dev:>+8.2f} {z:>+7.2f}")

devs = [abs(r[5]) for r in rows]
print(f"\nmax|dev%|/min|dev%| = {max(devs):.2f}/{min(devs):.2f} = {max(devs)/min(devs):.3f}x")
print(f"|dev%| at b=100 / |dev%| at b=1 = {devs[-1]:.2f}/{devs[0]:.2f} = {devs[-1]/devs[0]:.3f}x")
