import TamesisLab.Foundations.CycleDetection.Candidates

set_option autoImplicit false

/-!
# FOUND-CYCLE-DETECTION-001 — Detector executável

O núcleo executável: percorrer a lista finita de candidatos e devolver o
primeiro que satisfaça o contrato.

A definição é computável, não recorre a escolha clássica para construir o
certificado e não menciona objeto de ciclo quociente algum.

A lista completa de proibições está em
`FOUND_CYCLE_DETECTION_001/COMPUTABILITY_RESULT.md`, deliberadamente fora
dos arquivos Lean: mantê-la aqui faria a auditoria de tokens e de imports
proibidos encontrar as próprias menções documentais.

`DecidableEq X` entra **aqui**, e só aqui: o detector compara dois estados
produzidos por iteradas distintas. As camadas proposicionais não a
recebem.

A API pública desta versão é `Option CycleWitness`. A função total está
diferida — ver `TOTALIZATION_DECISION.md`.
-/

namespace TamesisLab.Foundations.CycleDetection

/-- Busca limitada por certificado.

Percorre `cycleCandidates (Fintype.card X)` e devolve o primeiro `w` com
`CycleWitness.Valid f x w`. Devolve `none` apenas se nenhum candidato for
válido — o que `detectCycleWitness?_complete` mostra não ocorrer. -/
def detectCycleWitness? {X : Type*} [Fintype X] [DecidableEq X]
    (f : X → X) (x : X) : Option CycleWitness :=
  (cycleCandidates (Fintype.card X)).find? fun w =>
    decide (CycleWitness.Valid f x w)

end TamesisLab.Foundations.CycleDetection
