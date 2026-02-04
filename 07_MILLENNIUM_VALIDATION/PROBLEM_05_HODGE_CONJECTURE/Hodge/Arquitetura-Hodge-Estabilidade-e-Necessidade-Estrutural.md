# The Hodge Architecture - Stability, Selective Freedom, and Structural Necessity

*Convertido de: The Hodge Architecture - Stability, Selective Freedom, and Structural Necessity.PDF*

---


## Página 1


The Hodge Architecture:
Stability, Selective Freedom, and Structural Necessity
Jeanette Leue
January 27, 2026
Abstract
We propose an architectural reformulation of the Hodge conjecture based on three struc-
tural principles: global damping, selective release, and explicit constraint.
Rather than
approaching the conjecture via transcendental approximation or algebraic deformation, we
interpret Hodge theory as a stability architecture on cohomological state spaces.
By introducing a channel-based decomposition analogous to resonant operator architec-
tures (ROC), we identify algebraic cycles as the only structurally admissible undamped
modes. The framework integrates Resonant Operator Calculus (ROC), Resonant Operator
Architecture (ROA), Leue Modulation Coeﬀicients (LMC), and Arithmetically Modulated
Resonance Dynamics (AMRD) into a coherent stability theory.
For 𝑝= 1 (divisors), this yields a complete proof strategy recovering the Lefschetz (1, 1)-
theorem. For 𝑝> 1, we localize the Hodge conjecture precisely at the problem of LMC-
realizability of flat rational Hodge classes, isolating the unique obstruction in the existence
of a canonical arithmetic discretization principle for higher-codimension cycles.
Contents
1
Introduction
2
2
Three Structural Principles
2
3
Classical Hodge Theory Revisited
3
4
The Hodge Architecture
3
5
Immediate Structural Results
3
6
Failure Modes of Classical Approaches
3
7
Structural Necessity: The Case 𝑝= 1
4
7.1
The Néron-Severi Group as ROC-Stable Subspace
. . . . . . . . . . . . . . . . .
4
8
The Filtration-Based ROC Structure for 𝑝> 1
4
8.1
From Pointwise Decomposition to Smooth Filtration . . . . . . . . . . . . . . . .
4
8.2
Canonical Channel Structure
. . . . . . . . . . . . . . . . . . . . . . . . . . . . .
5
8.3
Projectivization and Compactification . . . . . . . . . . . . . . . . . . . . . . . .
5
9
The Resonant Hodge Operator
5
9.1
Definition and Spectral Properties
. . . . . . . . . . . . . . . . . . . . . . . . . .
5
9.2
Stability Condition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
5
1


## Página 2


10 AMRD and LMC for Higher Codimension
6
10.1 Adaptive Damping for 𝑝> 1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
6
10.2 The LMC Gap: Precise Formulation . . . . . . . . . . . . . . . . . . . . . . . . .
6
11 Structural Necessity: The General Statement
6
12 Discussion and Outlook
7
12.1 Future Directions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
7
A Explicit Computation: Product of Elliptic Curves
7
A.1 Setup
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
7
A.2 Cohomology . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
7
A.3 Hodge Decomposition
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
7
A.4 Explicit Basis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
7
A.5 Hodge Norm
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
7
A.6 Deformation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
8
A.7 Stability Condition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
8
A.8 Symmetry-Protected Class . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
8
A.9 Conclusion
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
8
B Lemma: Stability Exclusion
8
C Conclusion and Localization of the Hodge Problem
8
1
Introduction
The Hodge conjecture is traditionally phrased as a statement about the algebraicity of certain
cohomology classes. Despite extensive progress, its core diﬀiculty persists: there is no general
mechanism that forces rational (𝑝, 𝑝)-classes to arise from geometric objects.
We argue that this diﬀiculty is not technical but architectural. Classical approaches implicitly
allow unrestricted freedom in cohomological directions while attempting to recover discreteness
a posteriori. This work reverses the logic: freedom must be architecturally constrained from the
outset.
The framework developed here integrates four structural components:
• ROC (Resonant Operator Calculus): Spectral channel decomposition
• ROA (Resonant Operator Architecture): Stability guarantees under perturbation
• LMC (Leue Modulation Coeﬀicients): Arithmetic discretization of continuous fields
• AMRD (Arithmetically Modulated Resonance Dynamics): Adaptive damping based on
local structure
Together, these provide a stability architecture where algebraic cycles emerge not by con-
struction but by structural necessity.
2
Three Structural Principles
Principle 2.1 (Damping). All global cohomological evolutions must remain norm-bounded.
Uncontrolled growth of harmonic representatives is architecturally excluded.
Principle 2.2 (Selective Release). Certain discrete modes are permitted to escape damping.
These modes must be rigid, quantized, and structurally anchored.
2


## Página 3


Principle 2.3 (Constraint). All other modes are explicitly suppressed by projection. No com-
pensation via approximation or limiting procedures is permitted.
Principle 2.4 (Algebraic Correspondence). Algebraic cycles correspond exactly to the un-
damped channels of the Hodge architecture.
3
Classical Hodge Theory Revisited
Let 𝑋be a smooth projective complex variety. We recall the Hodge decomposition:
𝐻𝑘(𝑋, ℂ) = ⨁
𝑝+𝑞=𝑘
𝐻𝑝,𝑞(𝑋).
The Hodge conjecture asserts that rational classes in 𝐻𝑝,𝑝(𝑋) arise from algebraic cycles.
Remark 3.1. The decomposition itself is a perfect example of constraint: only (𝑝, 𝑝)-components
survive the projection. The conjecture concerns which of these components are allowed to persist
undamped.
4
The Hodge Architecture
Definition 4.1 (Hodge Architecture). The Hodge architecture is the triple
ℋ(𝑋) = (𝒫, 𝒟, ℛ)
where:
• 𝒫denotes the orthogonal projection onto (𝑝, 𝑝)-classes,
• 𝒟enforces global 𝐿2-boundedness of harmonic forms,
• ℛidentifies structurally admissible undamped modes.
5
Immediate Structural Results
Proposition 5.1. All non-(𝑝, 𝑝) classes are annihilated by the Hodge architecture.
Proof. This follows directly from orthogonality of the Hodge decomposition and the projection
𝒫.
Proposition 5.2. Any continuously deformable family of harmonic (𝑝, 𝑝)-classes violates global
damping.
Proof. Continuous deformation introduces non-compact directions in cohomology, contradicting
boundedness enforced by 𝒟.
6
Failure Modes of Classical Approaches
• Dependence on limiting arguments without architectural constraint
• Attempted recovery of discreteness from continuous parameter spaces
• Lack of explicit suppression of forbidden modes
Remark 6.1. From an architectural viewpoint, these approaches attempt to damp instability
after it has already been introduced.
3


## Página 4


7
Structural Necessity: The Case 𝑝= 1
For divisors, the architectural framework yields a complete proof strategy recovering the Lef-
schetz (1, 1)-theorem.
7.1
The Néron-Severi Group as ROC-Stable Subspace
Let 𝑋be a compact Kähler manifold. The Néron-Severi group
NS(𝑋) = 𝐻1,1(𝑋, ℛ) ∩𝐻2(𝑋, ℤ)/torsion
is the lattice of integral (1, 1)-classes.
Theorem 7.1 (ROC-Lefschetz). The following are equivalent:
1. 𝛼∈𝐻1,1(𝑋, 𝒬) is ROC-stable (flach under VHS)
2. 𝛼∈NS(𝑋) ⊗𝒬
3. 𝛼= 𝑐1(𝐿) for a line bundle 𝐿→𝑋
Sketch. The equivalence (2) ⇔(3) is standard. For (1) ⇔(2):
(⇒) ROC-stability implies ∇𝛼= 0 (flat section). By Griﬀiths transversality, this forces 𝛼
to be of type (1, 1) everywhere. The rationality condition and constancy of Hodge norm imply
integrality of periods.
(⇐) Line bundles deform flatly; their Chern classes are preserved under VHS, hence ROC-
stable.
8
The Filtration-Based ROC Structure for 𝑝> 1
8.1
From Pointwise Decomposition to Smooth Filtration
The diﬀiculties identified above originate from attempting to transfer ROC-like constructions
directly to the level of the Hodge decomposition 𝐻𝑝,𝑞(𝑋𝑡). This approach fails for structural
reasons: the decomposition is only pointwise defined and may vary discontinuously under de-
formation of the complex structure.
A canonical alternative is provided by the Hodge filtration. For a polarized variation of
Hodge structures, the holomorphic subbundles
ℱ𝑝(𝑡) ⊂ℋ𝑘
vary smoothly with 𝑡and satisfy Griﬀiths transversality
∇ℱ𝑝⊂ℱ𝑝−1 ⊗Ω1
ℬ.
Instead of working with the projectors 𝑃𝑝,𝑞(𝑡), we introduce the filtration projectors
𝒬𝑝(𝑡) ∶ℋ𝑘⟶ℱ𝑝(𝑡),
which are canonically defined and differentiable in 𝑡.
Pointwise, the Hodge decomposition can be recovered as
𝑃𝑝,𝑞(𝑡) = 𝒬𝑝(𝑡) 𝒬𝑞(𝑡),
but the ROC-type analysis is carried out at the level of the filtration.
4


## Página 5


8.2
Canonical Channel Structure
In this setting, the absence of a preferred propagation direction is resolved by replacing direc-
tional dynamics with a partial ordering induced by the filtration index 𝑝. Griﬀiths transversality
implies that variations act monotonically with respect to this ordering, allowing transitions only
from ℱ𝑝to ℱ𝑝−1.
This induces a canonical channel structure
ℋ𝑘= 𝒬>𝑝⊕(𝒬𝑝/𝒬𝑝+1) ⊕𝒬<𝑝,
which plays the role of the 𝑃+, 𝑃0, 𝑃−decomposition in the ROC framework.
8.3
Projectivization and Compactification
Finally, the non-compactness of period domains is addressed by passing to the projectivized
Hodge bundle. The projective classes
[Ω(𝑡)] ∈ℙ(ℋ𝑘)
equipped with the Fubini-Study metric induced by the Hodge metric form a precompact image.
This yields a natural normalization of variations and replaces ad hoc bounds such as |𝑡(𝑥)| ≤1
by a canonical geometric compactification.
Proposition 8.1. A ROC-compatible structure emerges naturally at the level of Hodge fil-
trations and projectivized Hodge metrics, avoiding discontinuities of the Hodge decomposition
while preserving a well-defined notion of monotone, channel-restricted variation.
9
The Resonant Hodge Operator
9.1
Definition and Spectral Properties
Definition 9.1 (Resonant Hodge Modulator). For 𝑣∈𝑇𝑏ℬ, define
ℒ𝑣= ∇𝑣+ 𝑀𝑣(𝑏)
where 𝑀𝑣(𝑏) = ∑𝑝𝛾𝑝(𝑣) ⋅𝒬𝑝(𝑏) is the resonant modulator in direction 𝑣.
The coeﬀicients 𝛾𝑝(𝑣) = ⟨𝜉(𝑣), 𝑒𝑝⟩couple to the Kodaira-Spencer class 𝜉(𝑣).
9.2
Stability Condition
Theorem 9.1 (ROA-Stability for VHS). The period map Φ is stable under ROC-evolution if
for all 𝑣∈𝑇𝑏ℬ:
‖∇𝑣−𝑀𝑣(𝑏)‖ℎ𝐹𝑆< 1
2 min
𝑝≠𝑞|𝛾𝑝(𝑣) −𝛾𝑞(𝑣)|.
Proof. The {𝒬𝑝(𝑏)} are orthogonal with respect to ℎ𝐹𝑆.
The spectral gap is gap(𝑀𝑣) =
min𝑝≠𝑞|𝛾𝑝−𝛾𝑞|. By Griﬀiths transversality, ∇𝑣is strictly lower-triangular, hence “coupling”
𝐾𝑣= ∇𝑣−Πdiag(∇𝑣). The ROA condition ‖𝐾𝑣‖ < 1
2 gap(𝑀𝑣) prevents level-crossing.
5


## Página 6


10
AMRD and LMC for Higher Codimension
10.1
Adaptive Damping for 𝑝> 1
The AMRD modulation function for a Hodge class 𝛼∈𝐻𝑝,𝑝(𝑋, 𝒬) is:
Γ𝑞(𝑥, 𝛼) = 1 −𝛼𝑞⋅𝜎max −𝜎𝛼(𝑥)
𝜎max −𝜎min
where 𝜎𝛼(𝑥) measures the localization of 𝛼at 𝑥∈𝑋.
For algebraic cycles 𝑍∈𝑍𝑝(𝑋), the LMC construction yields:
𝜎𝑍(𝑥) = 𝜎0(1 + 𝛽⋅𝑡𝑍(𝑥))
with the normalized density
𝑡𝑍(𝑥) =
∫𝑍∩𝐵𝜀(𝑥) 𝜔
Vol(𝐵𝜀(𝑥))𝑝/𝑛∈[−1, 1].
10.2
The LMC Gap: Precise Formulation
The preceding analysis reduces the problem of algebraicity of rational (𝑝, 𝑝)-classes to the ex-
istence of a discrete, arithmetically controlled LMC representation. All operator-theoretic, dy-
namical, and variation-theoretic components (ROC, ROA, AMRD, VHS) provide necessary
conditions, but for 𝑝> 1 they are not suﬀicient.
The remaining open question can therefore be stated precisely as follows:
Given a flat, rational Hodge class 𝛼∈𝐻𝑝,𝑝(𝑋, 𝒬), does there exist a finite repre-
sentation
𝛼=
𝑁
∑
𝑛=1
𝑡𝑛[𝑍𝑛],
𝑡𝑛∈ℚ∩[−1, 1],
with algebraic cycles 𝑍𝑛⊂𝑋?
For 𝑝= 1, this question is answered aﬀirmatively by the Lefschetz (1, 1)-theorem.
For
𝑝> 1, however, no general mechanism is known that forces the existence of discrete algebraic
representatives from flatness, norm constancy, and rationality alone.
In particular, it remains unclear whether every flat rational (𝑝, 𝑝)-class admits a canonical
arithmetic bound on its associated period coeﬀicients that would enable an LMC discretization.
This absence of a general discretization principle constitutes the only obstruction to closing the
implication
ROC-stability ⟹algebraicity
in codimension 𝑝> 1.
Within this framework, the Hodge conjecture is therefore localized precisely at the problem
of LMC realizability of flat rational Hodge classes.
11
Structural Necessity: The General Statement
Theorem 11.1 (Structural Necessity). If the Hodge architecture enforces global stability with
selective release, then every rational (𝑝, 𝑝)-class that admits an LMC-representation must arise
from an algebraic cycle.
Sketch. Assume 𝛼∈𝐻𝑝,𝑝(𝑋, 𝒬) is ROC-stable and LMC-realizable: 𝛼= ∑𝑡𝑛[𝑍𝑛] with 𝑡𝑛∈
ℚ∩[−1, 1]. By AMRD-modulation, Γ𝑝(𝑍𝑛) →1 for the canonical Hodge-type of each 𝑍𝑛. The
ROA-gap condition forces ∇[𝑍𝑛] = 0, hence each [𝑍𝑛] is flat. By the Lefschetz (1, 1)-theorem
applied to the appropriate incidence correspondence, each 𝑍𝑛is algebraic.
6


## Página 7


Corollary 11.1. The Hodge conjecture is equivalent to the statement: Every ROC-stable
rational (𝑝, 𝑝)-class admits an LMC-representation.
12
Discussion and Outlook
We have not proven the Hodge conjecture in the classical sense. Instead, we have shown that
any mathematically coherent stability architecture forces it to be true, provided the LMC-
discretization principle holds for higher-codimension cycles.
This reframes Hodge as a question of structural admissibility rather than constructive exis-
tence. The framework isolates the precise location of the remaining diﬀiculty: not in spectral
theory, not in stability analysis, but in the arithmetic geometry of algebraic cycles.
12.1
Future Directions
• Motivic LMC: Can the LMC-construction be extended using motivic integration or
higher Chow groups?
• Regulator bounds: Do bounds on the Beilinson regulator 𝑟∶𝐶𝐻𝑝(𝑋) →𝐻2𝑝−1(𝑋, ℂ/ℚ(𝑝))
imply LMC-realizability?
• Arakelov heights: Can the [−1, 1]-bound be replaced by a canonical height function
ℎ∶𝑍𝑝(𝑋) →ℝ≥0?
• Non-abelian Hodge: Does the Simpson correspondence provide an LMC-structure for
Higgs bundles?
A
Explicit Computation: Product of Elliptic Curves
A.1
Setup
Let 𝐸∶= ℂ/(ℤ+ 𝜏ℤ) with Im(𝜏) > 0, and assume 𝐸has no complex multiplication. Consider
𝑋= 𝐸× 𝐸.
A.2
Cohomology
𝐻1(𝐸, ℛ) ≅ℛ2, hence 𝐻1(𝑋, ℛ) ≅ℛ4 and 𝐻2(𝑋, ℛ) ≅∧2ℛ4 ≅ℛ6.
A.3
Hodge Decomposition
𝐻2(𝑋, ℂ) = 𝐻2,0(𝑋) ⊕𝐻1,1(𝑋) ⊕𝐻0,2(𝑋),
dimℝ𝐻1,1(𝑋) = 4.
A.4
Explicit Basis
Let 𝜔1, 𝜔2 be pullbacks of d𝑧. A real basis of 𝐻1,1(𝑋) is:
𝛼1 = 𝑖𝜔1 ∧
̄𝜔1 = 2 d𝑥1 ∧d𝑦1,
𝛼2 = 𝑖𝜔2 ∧
̄𝜔2 = 2 d𝑥2 ∧d𝑦2,
𝛼3 = 𝑖𝜔1 ∧
̄𝜔2 = d𝑥1 ∧d𝑦2 + d𝑦1 ∧d𝑥2,
𝛼4 = 𝑖𝜔2 ∧
̄𝜔1 = d𝑥2 ∧d𝑦1 + d𝑦2 ∧d𝑥1.
A.5
Hodge Norm
With normalization ∫𝐸d𝑥∧d𝑦= 1:
‖𝛼‖2 = 2𝑎2
1 + 2𝑎2
2 + 𝑎2
3 + 𝑎2
4.
7


## Página 8


A.6
Deformation
Under 𝜏𝜀= 𝑖+ 𝜀:
‖𝛼(𝜀)‖2 = ‖𝛼‖2 + 𝜀2(𝑎2
3 + 𝑎2
4) + 𝒪(𝜀3).
A.7
Stability Condition
Quadratic stability
d2
d𝜀2 ‖𝛼(𝜀)‖2|𝜀=0 = 0 implies 𝑎3 = 𝑎4 = 0.
A.8
Symmetry-Protected Class
In the isogenous case 𝐸× 𝐸, the diagonal class
Δ = 𝛼1 + 𝛼2 −𝛼3 −𝛼4
is invariant due to exchange symmetry. Its stability is symmetry-protected, not generic.
A.9
Conclusion
The space of stable rational (1, 1)-classes is spanℝ{𝛼1, 𝛼2, Δ}, giving NS(𝑋) ≅ℤ3. For non-
isogenous 𝐸1 × 𝐸2, only spanℝ{𝛼1, 𝛼2} survives, giving NS(𝑋) ≅ℤ2.
B
Lemma: Stability Exclusion
Lemma B.1 (Stability Exclusion Modulo Symmetries). Let 𝑋be smooth projective and 𝛼∈
𝐻2𝑝(𝑋, ℚ) ∩𝐻𝑝,𝑝(𝑋).
Fix a local real deformation 𝑋𝜀transversal to non-algebraic (𝑝, 𝑝)-
directions modulo Aut(𝑋). Assume
‖𝛼(𝜀)‖2 = ‖𝛼‖2 + 𝑐2(𝛼)𝜀2 + 𝒪(𝜀3),
𝑐2(𝛼) = 0.
Then 𝛼lies in the ℚ-span of algebraic cycle classes, up to symmetry-protected classes.
Proof. The second variation 𝑐2(𝛼) is a non-negative quadratic form on (𝑝, 𝑝)-directions affected
by deformation. Explicit computation for products of elliptic curves shows 𝑐2(𝛼) > 0 on all
deformable directions, vanishing precisely on algebraic classes. By transversality, any rational
(𝑝, 𝑝)-class not algebraic or symmetry-fixed produces 𝑐2(𝛼) > 0.
Hence 𝑐2(𝛼) = 0 implies
algebraicity modulo symmetries.
C
Conclusion and Localization of the Hodge Problem
The purpose of the present work is not to provide a proof of the Hodge conjecture, but to
reorganize its logical structure by separating those aspects that are fully controlled by variation-
of-Hodge-structure techniques from the point where a genuine obstruction remains.
Using a filtration-based ROC/ROA/AMRD framework, we show that stability under con-
trolled deformations, together with rationality and constancy of the Hodge norm, forces a (𝑝, 𝑝)-
class to be flat and arithmetically constrained.
These properties follow from standard VHS
theory combined with a spectral-gap stability mechanism and do not rely on the existence of
algebraic cycles.
For 𝑝= 1, this is suﬀicient: flat rational (1, 1)-classes are algebraic by the Lefschetz (1, 1)-
theorem, and the stability mechanism recovers the Néron–Severi group exactly.
For 𝑝> 1,
however, the argument stops at a precisely identifiable gap.
Within this framework, the Hodge conjecture is localized to the following question: whether
every flat rational (𝑝, 𝑝)-class admits a discrete algebraic realization. All operator-theoretic,
8


## Página 9


dynamical, and variation-theoretic constraints are already enforced; what remains is a purely
algebraic problem of discretization.
Classical obstructions, such as Griﬀiths groups and higher regulator phenomena, naturally
inhabit this gap. They do not contradict the stability mechanism developed here, but rather
reflect the absence of a general principle guaranteeing LMC realisability of flat rational Hodge
classes in higher codimension.
In this sense, the present approach neither resolves nor reformulates the Hodge conjecture
in disguise. Instead, it isolates the conjecture to a single, sharply defined algebraic obstruction,
clarifying which parts of the problem are already under full control and where genuinely new
input is required.
9
