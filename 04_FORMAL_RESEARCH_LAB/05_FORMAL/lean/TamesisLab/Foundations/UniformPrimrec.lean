import TamesisLab.Foundations.UniformPrimrec.Execution
import TamesisLab.Foundations.UniformPrimrec.Validity
import TamesisLab.Foundations.UniformPrimrec.Candidates
import TamesisLab.Foundations.UniformPrimrec.Witness
import TamesisLab.Foundations.UniformPrimrec.Analysis
import TamesisLab.Foundations.UniformPrimrec.Instance

/-!
# FOUND-UNIFORM-PRIMREC-001

```text
Execution.lean   run? como iterada — a peca que destrava
Validity.lean    validade da tabela, com if e nao decide
Candidates.lean  flatMap por foldr
Witness.lean     o casamento com o detector tipado
Analysis.lean    Primrec2 analyzeTransitionTable — o fechamento
Instance.lean    TEST_ONLY
```

Trinta e uma declaracoes publicas. Fecha `CB-GAP-001`: o nivel uniforme,
sobre dominio **infinito**, onde a conclusao depende do algoritmo.

`Primrec` **nao** significa eficiente.
-/
