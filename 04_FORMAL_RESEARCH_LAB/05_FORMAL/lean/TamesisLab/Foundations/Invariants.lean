import TamesisLab.Foundations.Invariants.Definitions
import TamesisLab.Foundations.Invariants.Unreachability
import TamesisLab.Foundations.Invariants.CollapseLimit
import TamesisLab.Foundations.Invariants.Instance

/-!
# FOUND-INVARIANT-UNREACHABILITY-001

Abstração usada para **separar**, e não para colapsar.

```text
Definitions.lean     Invariant, a ponte definicional, Reachable
Unreachability.lean  a ferramenta, a composicao, a ponte com a cadeia
CollapseLimit.lean   o teorema negativo
Instance.lean        TEST_ONLY, sobre Int x Int
```

Oito declarações públicas, duas `TEST_ONLY` residentes. Zero typeclasses,
zero `Fintype`, zero `DecidableEq`.
-/
