"""
POST-HOC (declared as such): one supplementary confirmatory run, triggered
by an unexplained |z|=2.51 outlier at M-MIX0.3, c=18 in the locked B1
battery (all other cells fine, and the c=220 outlier was already
explained by the known +p*c/n finite-n term). Fresh seed, larger N, same
mechanism/c/n -- checks fluctuation vs bug BEFORE writing the verdict.
Not part of the pre-registered battery; does not replace it.
"""
import numpy as np, time, json
import adv_sim as A

rng = np.random.default_rng(np.random.SeedSequence(555000111))
n = 65536
K = 17
N = 6000
t0 = time.time()
vals = np.empty(N)
for k in range(N):
    vals[k] = A.run_MIX(n, 18.0, 0.3, rng, K)
mean = vals.mean()
sem = vals.std(ddof=1) / np.sqrt(N)

P = json.load(open("/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/adv_predictions.json"))
target = P["M-MIX_p0.3"]["18.0"]
z = (mean - target) / sem
out = {"mean": mean, "sem": sem, "N": N, "target": target, "z": z, "time_s": time.time() - t0,
       "seed": 555000111, "purpose": "post-hoc confirmatory re-check of M-MIX0.3 c=18 outlier from locked B1 battery"}
print(json.dumps(out, indent=2))
with open("/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/adv_posthoc_check.json", "w") as fh:
    json.dump(out, fh, indent=2)
