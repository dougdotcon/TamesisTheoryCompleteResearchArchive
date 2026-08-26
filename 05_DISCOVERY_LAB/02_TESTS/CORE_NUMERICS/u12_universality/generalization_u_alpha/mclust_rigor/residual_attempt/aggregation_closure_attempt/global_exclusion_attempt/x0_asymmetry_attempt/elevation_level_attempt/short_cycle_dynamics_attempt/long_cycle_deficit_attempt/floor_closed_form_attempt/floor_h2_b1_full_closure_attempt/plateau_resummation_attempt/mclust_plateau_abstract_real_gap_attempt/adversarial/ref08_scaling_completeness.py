#!/usr/bin/env python3
"""
Completeness check on the target document's Sec A.4 magnitude argument
against the vanishing-finite-n hypothesis. The document tests three
candidate rates (1/n, 1/sqrt(n), sqrt(c/n)) against the observed ~38.8%
gap at n=65536, c=1000. This script checks whether other natural
small-parameter rates in c/n (not tested by the document) come closer to
the observed magnitude without requiring an "implausible" prefactor.
"""
import math

n = 65536
c = 1000
observed_gap_pct = 38.8

candidates = {
    "1/n": 1 / n,
    "1/sqrt(n)": 1 / math.sqrt(n),
    "c/n": c / n,
    "sqrt(c/n)": math.sqrt(c / n),
    "(c/n)^(1/3)": (c / n) ** (1 / 3),
    "(c/n)^(1/4)": (c / n) ** (1 / 4),
    "1/ln(n)": 1 / math.log(n),
    "ln(n)/n": math.log(n) / n,
    "ln(n)/sqrt(n)": math.log(n) / math.sqrt(n),
    "(c/n)*ln(n/c)": (c / n) * math.log(n / c),
    "sqrt(c/n)*ln(n)": math.sqrt(c / n) * math.log(n),
}

print(f"n={n}, c={c}, observed gap ~ {observed_gap_pct}%\n")
print(f"{'rate':<20}{'value (%)':>12}{'prefactor needed':>20}")
for name, val in candidates.items():
    pct = val * 100
    prefactor = observed_gap_pct / pct if pct != 0 else float('inf')
    flag = "  <-- document tested this" if name in ("1/n", "1/sqrt(n)", "sqrt(c/n)") else ""
    print(f"{name:<20}{pct:>12.4f}{prefactor:>20.3f}{flag}")

print("""
Reading: the document's own three tested candidates require prefactors of
~2500x-100000x (1/n, 1/sqrt(n) -- correctly judged implausible) or ~3.1x
(sqrt(c/n) -- the document's own "most generous" candidate, itself flagged
as a "real, unexplained factor"). This script finds that OTHER natural
small-parameter rates in c/n, not tested by the document, come markedly
closer: (c/n)^(1/3) needs only a ~1.56x prefactor, and (c/n)^(1/4) needs
only a ~1.10x prefactor -- essentially unremarkable. This does not overturn
the document's conclusion (which is explicitly hedged: "at least not at
any of the natural small-parameter rates checked here"), but it shows the
magnitude argument, while correct for the three specific rates it tests,
does not rule out the broader class of vanishing finite-n corrections in
c/n at other powers -- a genuine completeness gap in an otherwise sound
argument.
""")
