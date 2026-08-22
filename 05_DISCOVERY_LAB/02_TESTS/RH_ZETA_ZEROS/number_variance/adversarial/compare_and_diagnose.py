"""
Comparacao celula a celula: meu grid completo (adv_primary_result.json) vs
primary_result.json, e diagnostico terceiro-bug (coincidencia de fronteira
ponto-flutuante no bloco 0 / ultimo bloco de estimator.py::_exact_window_integral).

So roda DEPOIS que meus proprios numeros ja estao travados (adv_primary_result.json
existe). Le estimator.py do primario apenas para reproduzir/diagnosticar (nao
para copiar logica nova).
"""
import json
import sys
import numpy as np

sys.path.insert(0, "..")
from estimator import N_absolute, local_density, block_number_variance as primary_bnv

with open("adv_primary_result.json") as f:
    adv = json.load(f)
with open("../primary_result.json") as f:
    prim = json.load(f)


def load_zeros1():
    vals = np.array([float(x) for x in open("../../data/zeros1.txt").read().split()])
    return vals


def load_offset_file(path, expected_n=10000):
    offsets = []
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        try:
            offsets.append(float(line))
        except ValueError:
            continue
    offsets = np.array(offsets)
    assert len(offsets) == expected_n
    return offsets


g1 = load_zeros1()
x1 = N_absolute(g1)
x1.sort()

base3 = 267653395647.0
off3 = load_offset_file("../../data/zeros3.txt")
dens3 = local_density(base3)
x3 = off3 * dens3
x3.sort()

DATASETS = {"zeros1": x1, "zeros3": x3}

print("=" * 100)
print(f"{'dataset':8} {'mult':>6} {'L':>10} {'B':>4}  {'V_hat(adv)':>10} {'V_hat(prim)':>11} "
      f"{'SE(adv)':>9} {'SE(prim)':>10}  {'blk0_fp_diff':>13}  {'block0_bug?':>11}")
print("=" * 100)

n_bug_triggered = 0
n_total = 0
for dsname in ["zeros1", "zeros3"]:
    x = DATASETS[dsname]
    adv_rows = {round(e["L"], 6): e for e in adv[dsname]["grid"]}
    prim_rows = {round(e["L"], 6): e for e in prim[dsname]["rows"]}
    for Lkey in sorted(set(adv_rows) & set(prim_rows)):
        ea = adv_rows[Lkey]
        ep = prim_rows[Lkey]
        L = ea["L"]
        B = ea["B_design"]
        edges = np.linspace(x[0], x[-1], B + 1)
        a0 = edges[0]
        y_lo0 = a0 + L / 2.0
        fp_diff0 = (y_lo0 - L / 2.0) - x[0]
        bug0 = fp_diff0 < 0  # negative => boundary point erroneously retained -> inflates that block
        n_total += 1
        if bug0:
            n_bug_triggered += 1
        vh_diff = abs(ea["V_hat"] - ep["V_hat"])
        flag = "***BUG0***" if bug0 else ""
        print(f"{dsname:8} {ea['mult']:>6} {L:10.2f} {B:4d}  {ea['V_hat']:10.4f} {ep['V_hat']:11.4f}  "
              f"{ea['SE']:9.4f} {ep['SE']:10.4f}  {fp_diff0:13.2e}  {flag:>11}")

print(f"\nTotal grid points: {n_total}, bloco-0 fp-bug triggered (negative diff) in: {n_bug_triggered}")
