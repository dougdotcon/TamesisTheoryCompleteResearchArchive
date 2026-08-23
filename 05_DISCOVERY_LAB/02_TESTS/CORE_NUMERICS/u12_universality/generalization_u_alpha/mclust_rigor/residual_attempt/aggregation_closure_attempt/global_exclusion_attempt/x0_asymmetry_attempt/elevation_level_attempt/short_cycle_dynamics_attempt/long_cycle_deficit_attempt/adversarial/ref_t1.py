import sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import ref_common as R

n = 65536
cells = [
    dict(label="A(target)", c=1000, threshold=2000, seed=20260828101, N=5000),
    dict(label="B",         c=100,  threshold=8000, seed=20260828102, N=5000),
    dict(label="C",         c=150,  threshold=4000, seed=20260828103, N=5000),
]

t_start = time.time()
for cell in cells:
    t0 = time.time()
    res = R.run_cell(n, 1, cell["c"], cell["threshold"], N=cell["N"],
                      seed_base=cell["seed"], n_workers=4, label="T1-" + cell["label"])
    phiU = R.phi_ref(1, cell["c"], n)
    print(R.report_line(res, phiU))
    print(f"  [elapsed {time.time()-t0:.1f}s]\n", flush=True)

print(f"TOTAL T1 elapsed: {time.time()-t_start:.1f}s")
