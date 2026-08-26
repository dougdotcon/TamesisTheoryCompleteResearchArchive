# Pre-registration -- GENERAL-P-DSTAR-EXTENSION3-ATTEMPT

Written before any non-throwaway verification run, per this lineage's
standing convention.

**Governance.** Wave 19, front (c), authorized by `DISC-DEC-083`.

**Target.** Confirm the wave-18 reduced-scale exploratory push (`p=41..60`,
`r<=60,b<=10`, `general_p_dstar_extension2_attempt/ATTEMPT.md` Sec.3.3(a))
at FULL scale (`r<=200,b<=30`), and extend further to `p=61,...,80` at full
scale too -- matching the scale ceiling every predecessor in this lineage
has used since wave 16.

**Route.** No new mathematical ingredient. Reuse, cited as PROVED:
Corollary A3 (ground truth); the general-p assembly formula (waves 15/16);
the `H_k(r,b)` machine's correctness for every `k` (wave-15 referee's
induction); the closed factorization `S_{2k-1}=A_k*C(N,m+1)` and proved
degree bound `deg_r H_{2k-1}=k-1` (wave-16 referee).

**Scripts, written fresh, no predecessor `.py` opened:** `ground_truth.py`,
`ingredients.py`, `odd_part.py`, `assemble.py`, `run_full_sweep.py`,
`random_spotcheck.py`, `print_closed_forms.py`.

**Exactness.** `fractions.Fraction` throughout the verification path; no
floating point.

**Randomness.** `numpy.random.SeedSequence`, seeded from this front's
reserved range `20260884000-20260884999` (`DISC-DEC-083`, front (c)).
Confirmed unused elsewhere before first use. Referee range `20260885000+`
not touched.

**Honesty commitments.**
1. If full-scale exhaustive verification for the entire `p=41..80` range
   proves computationally intractable in practice, disclose exactly what
   scale was actually reached and why -- not silently reduce scope.
2. Disclose every bug caught during development, whether in the main
   verification path or in self-test/throwaway code, exactly as every
   predecessor in this lineage has.
3. No claim beyond what is checked: closed forms are printed only where
   cross-validated against ground truth at concrete points; "no new
   mathematical ingredient" is asserted only if actually true on
   inspection of every non-trivial fact used.
4. No `adversarial/` subdirectory is created and no referee is dispatched
   from this front -- reserved for the orchestrating session.
