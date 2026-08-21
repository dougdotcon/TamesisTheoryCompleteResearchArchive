#!/usr/bin/env python3
"""Parse Ashton-Cantarella-Piatek-Rawdon (arXiv:1002.1723) Tables 3-4
(Appendix A) into a JSON table of ropelengths for all prime KNOTS
(single component) with 3..9 crossings. Links (multi-component entries,
typeset with a component superscript) are excluded.

Text-stream structure (pymupdf extraction of PDF pages idx 37, 38):
  knot row : NAME  ROPP  ROP          (NAME like '31', '819', '949')
  link row : NAME  SUB   ROPP  ROP    (e.g. '92' '41' -> link 9^2_41)
Column/page breaks repeat the last row: dedupe keeps first occurrence.
"""
import json, re, sys
import pymupdf

PDF = sys.argv[1] if len(sys.argv) > 1 else "data/acpr_1002.1723.pdf"
OUT = sys.argv[2] if len(sys.argv) > 2 else "data/knot_ropelength_acpr.json"

FLOAT = re.compile(r"^\d+\.\d{4}$")
INT = re.compile(r"^\d+$")

doc = pymupdf.open(PDF)
tokens = []
for idx in (37, 38):  # Tables 3 and 4 (knots up to 9_49)
    tokens += [t for t in doc[idx].get_text().split() if t not in ("Link", "Ropp", "Rop")]

knots = {}
i = 0
while i < len(tokens):
    t = tokens[i]
    if INT.match(t) and i + 2 < len(tokens):
        a, b = tokens[i + 1], tokens[i + 2]
        if FLOAT.match(a) and FLOAT.match(b):
            # knot row: crossing = first digit(s), index = rest
            if len(t) >= 2 and t[0] in "3456789":
                name = f"{t[0]}_{int(t[1:])}"
                if name not in knots:
                    knots[name] = float(b)  # column Rop (smooth upper bound)
            i += 3
            continue
        if INT.match(a) and i + 3 < len(tokens) and FLOAT.match(tokens[i + 2]) and FLOAT.match(tokens[i + 3]):
            i += 4  # link row (NAME SUB ROPP ROP): skip
            continue
    i += 1

# sanity checks (fail loudly rather than silently mis-parse)
expected_counts = {3: 1, 4: 1, 5: 2, 6: 3, 7: 7, 8: 21, 9: 49}
counts = {}
for k in knots:
    c = int(k.split("_")[0])
    counts[c] = counts.get(c, 0) + 1
assert counts == expected_counts, f"count mismatch: {counts}"
assert abs(knots["3_1"] - 32.7436) < 1e-4, knots["3_1"]
assert abs(knots["4_1"] - 42.0887) < 1e-4, knots["4_1"]
assert abs(knots["5_1"] - 47.2016) < 1e-4, knots["5_1"]
assert abs(knots["8_19"] - 60.9858) < 1e-4, knots["8_19"]
assert abs(knots["9_49"] - 73.9286) < 1e-4, knots["9_49"]

out = {
    "source": "Ashton, Cantarella, Piatek, Rawdon, Exp. Math. 20(1):57-90 (2011), arXiv:1002.1723, Tables 3-4, column Rop",
    "fetched": "2026-08-21",
    "convention": "ropelength Rop = Len/Thi (unit radius); Tamesis L/D = Rop/2",
    "n_knots": len(knots),
    "ropelength": dict(sorted(knots.items(), key=lambda kv: (int(kv[0].split("_")[0]), int(kv[0].split("_")[1])))),
}
json.dump(out, open(OUT, "w"), indent=1)
print(f"wrote {OUT}: {len(knots)} knots; 3_1={knots['3_1']} 4_1={knots['4_1']} 5_1={knots['5_1']}")
