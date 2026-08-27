import TamesisLab.ExternalLines.NonclassicalLogicLP.Definitions
import TamesisLab.ExternalLines.NonclassicalLogicLP.ValidTheorems
import TamesisLab.ExternalLines.NonclassicalLogicLP.Countermodels
import TamesisLab.ExternalLines.NonclassicalLogicLP.CollapseTheorem
import TamesisLab.ExternalLines.NonclassicalLogicLP.Audit

/-!
# LP-001 — top-level import shim

Aggregates the standalone Lean4 formalization of Priest's LP (Logic of
Paradox). Tracked under `05_DISCOVERY_LAB` (`DISC-DEC-102`) — **not**
this lab's own portfolio gate (`00_GOVERNANCE/`, `01_PORTFOLIO/`,
`02_FOUNDATIONS/`'s numbered track). The physical `.lean` files live
under `TamesisLab/` only because `lake`'s module resolution requires it;
the governance-style README/RESULTS documentation lives instead at
`04_FORMAL_RESEARCH_LAB/11_EXTERNAL_LINES/NONCLASSICAL_LOGIC_LP/`.
-/

namespace TamesisLab.ExternalLines.NonclassicalLogicLP

theorem nonclassical_logic_lp_smoke : True := by trivial

end TamesisLab.ExternalLines.NonclassicalLogicLP
