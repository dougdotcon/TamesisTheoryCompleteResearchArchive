import json, math

with open("/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/adv_sim_results.json") as fh:
    R = json.load(fh)
with open("/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/adv_predictions.json") as fh:
    P = json.load(fh)

def z(mean, sem, target):
    return (mean - target) / sem

def chi2(cells, targets):
    s = 0.0
    for c in cells:
        s += ((cells[c]["mean"] - targets[c]) / cells[c]["sem"]) ** 2
    return s

def slope(c1, m1, c2, m2):
    return math.log(m1 / m2) / math.log(c2 / c1)

print("=== C1: M-U ===")
cells = R["B1_M-U"]
targ = P["M-U"]
chi = chi2(cells, targ)
for c in sorted(cells, key=float):
    print(c, "mean", cells[c]["mean"], "target", targ[c], "z", round(z(cells[c]["mean"], cells[c]["sem"], targ[c]), 2))
print("chi2_5 =", chi)

print("=== C1: M-MIX0.3 ===")
cells = R["B1_M-MIX0.3"]
targ = P["M-MIX_p0.3"]
chi = chi2(cells, targ)
for c in sorted(cells, key=float):
    print(c, "mean", cells[c]["mean"], "target", targ[c], "z", round(z(cells[c]["mean"], cells[c]["sem"], targ[c]), 2))
print("chi2_5 =", chi)

print("=== C1: M-PREV ===")
cells = R["B1_M-PREV"]
targ = P["M-PREV"]
chi = chi2(cells, targ)
for c in sorted(cells, key=float):
    print(c, "mean", cells[c]["mean"], "target", targ[c], "z", round(z(cells[c]["mean"], cells[c]["sem"], targ[c]), 2))
print("chi2_5 =", chi)

print("=== C1: M-CLUST13 (finite-n c_eff target) ===")
cells = R["B1_M-CLUST13"]
targ = {c: P["M-CLUST13"][c]["target"] for c in P["M-CLUST13"]}
chi = chi2(cells, targ)
for c in sorted(cells, key=float):
    band = P["M-CLUST13"][c]["band_2bc_over_n"]
    print(c, "mean", cells[c]["mean"], "target", targ[c], "z", round(z(cells[c]["mean"], cells[c]["sem"], targ[c]), 2), "band", round(band,4))
print("chi2_5 =", chi)

print("=== B2: M-CLUST50 stress ===")
cells = R["B2_M-CLUST50"]
targ = {c: P["M-CLUST50_stress"][c]["target"] for c in P["M-CLUST50_stress"]}
chi = chi2(cells, targ)
for c in sorted(cells, key=float):
    band = P["M-CLUST50_stress"][c]["band_2bc_over_n"]
    print(c, "mean", cells[c]["mean"], "target", targ[c], "z", round(z(cells[c]["mean"], cells[c]["sem"], targ[c]), 2), "band", round(band,4))
print("chi2_4 =", chi)

print("=== B4: M-SHARED (exploratory, no target) ===")
cells = R["B4_M-SHARED"]
for c in sorted(cells, key=float):
    print(c, "mean", cells[c]["mean"], "phiU", P["M-SHARED_comparison_phiU"][c], "baseline(1-e^-c)/c", P["M-SHARED_baseline_untouched_cycles"][c])
cs = sorted(cells, key=float)
for i in range(len(cs)-1):
    c1, c2 = float(cs[i]), float(cs[i+1])
    m1, m2 = cells[cs[i]]["mean"], cells[cs[i+1]]["mean"]
    print(f"local slope {c1}->{c2}: alpha_hat = {slope(c1,m1,c2,m2):.4f}")

print("=== B3: M-INTRA extended ===")
cells = R["B3_M-INTRA"]
heur = P["M-INTRA_heuristic_descriptive"]
for c in sorted(cells, key=float):
    print(c, "mean", cells[c]["mean"], "sem", cells[c]["sem"], "heuristic(descriptive)", heur.get(c, "NA"))
cs = sorted(cells, key=float)
for i in range(len(cs)-1):
    c1, c2 = float(cs[i]), float(cs[i+1])
    m1, m2 = cells[cs[i]]["mean"], cells[cs[i+1]]["mean"]
    print(f"local slope {c1}->{c2}: alpha_hat = {slope(c1,m1,c2,m2):.4f}")
c1, c2 = float(cs[0]), float(cs[-1])
m1, m2 = cells[cs[0]]["mean"], cells[cs[-1]]["mean"]
print(f"overall slope {c1}->{c2}: alpha_hat = {slope(c1,m1,c2,m2):.4f}")

print("=== K=1 battery ===")
k1targets = P.get("K1_exact_own", None)
for key in ["K1_M-U", "K1_M-MIX0.3", "K1_M-PREV", "K1_M-INTRA"]:
    if key in R:
        d = R[key]
        print(key, d)
