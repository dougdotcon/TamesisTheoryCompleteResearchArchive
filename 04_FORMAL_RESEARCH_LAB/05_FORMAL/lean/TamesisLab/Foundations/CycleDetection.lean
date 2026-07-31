import TamesisLab.Foundations.CycleDetection.Witness
import TamesisLab.Foundations.CycleDetection.Candidates
import TamesisLab.Foundations.CycleDetection.Detector
import TamesisLab.Foundations.CycleDetection.Correctness
import TamesisLab.Foundations.CycleDetection.Periodicity

/-!
# FOUND-CYCLE-DETECTION-001 — agregador

Detecção executável de ciclos em sistemas determinísticos finitos, por
**busca limitada por certificado**.

```text
Witness.lean       CycleWitness, Valid, instancia decidivel explicita
Candidates.lean    cycleCandidates e sua caracterizacao
                   sem X, sem Fintype, sem DecidableEq
Detector.lean      detectCycleWitness? — unico arquivo com DecidableEq
                   na definicao executavel
Correctness.lean   soundness e completeness
Periodicity.lean   pontes proposicionais, sem DecidableEq
```

O algoritmo é a implementação ingênua contra a qual Floyd e Brent foram
propostos como melhorias. **Nenhuma novidade matemática, nenhuma novidade
algorítmica.** O valor é a execução dentro do Lean com correção e
completude verificadas, e a reutilização de
`FOUND-SEMIGROUP-002` sem repetir a casa dos pombos.

A API pública desta versão é `Option CycleWitness`. A função total, Floyd,
Brent, a tabela de visitados, a minimalidade, a complexidade formal e a
extração permanecem fora do escopo.

scientific_value: FORMAL_ALGORITHM_FOUNDATION
mathematical_novelty: NONE
algorithmic_novelty: NONE
-/
