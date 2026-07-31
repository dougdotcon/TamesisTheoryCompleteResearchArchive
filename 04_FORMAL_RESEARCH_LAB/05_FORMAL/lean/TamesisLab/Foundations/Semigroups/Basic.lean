import Mathlib.Algebra.Group.Action.Defs

/-!
# FOUND-SEMIGROUP-001 — Basic: interface abstrata

Camada A do gate. A busca no checkout fixado da Mathlib
(revisão `79d0395a1825a6264ad5d269e35e60537518955e`) encontrou a interface
oficial para ação de semigrupo, adequada inclusive ao caso sem identidade:

- `SemigroupAction (α β) [Semigroup α] extends SMul α β`, com a lei
  `mul_smul : (x * y) • b = x • (y • b)`
  (`Mathlib/Algebra/Group/Action/Defs.lean`);
- `MulAction (α β) [Monoid α] extends SemigroupAction α β`, acrescentando
  `one_smul : (1 : α) • b = b`.

Pela stop condition do gate, nenhuma estrutura local duplicada é criada:
a interface oficial é reutilizada.

## Mapeamento terminológico

| Vocabulário do laboratório | Objeto matemático padrão |
|---|---|
| regime | elemento de um tipo finito `X` |
| transição | elemento de um semigrupo/monoide `S` |
| composição de transições | `*` (multiplicação de `S`) |
| ação da transição sobre o regime | `•` (`SMul S X`) |
| lei de compatibilidade | `mul_smul : (a * b) • x = a • (b • x)` |

## Convenção de ordem

`a * b` significa "aplicar `b` primeiro e depois `a`", exatamente como na
lei `mul_smul` da Mathlib. A composição concreta `Shift3.comp` em
`Regime3.lean` segue essa mesma convenção; ver `DEFINITIONS.md` da frente
`02_FOUNDATIONS/03_SEMIGROUPS`.

Este arquivo não introduz definições novas: registra a decisão de reuso e o
mapeamento, e serve de âncora de import para a camada abstrata.

Valor científico: FOUNDATIONAL_FORMALIZATION_ONLY. Nenhum resultado Tamesis,
Omega ou Braid é usado como premissa.
-/

namespace TamesisLab.Foundations.Semigroups

/-- Registro formal (trivial) de que a camada abstrata está ancorada na
interface oficial da Mathlib; a verificação real é o typecheck dos usos de
`SemigroupAction`/`MulAction` em `Action.lean`. -/
theorem abstract_interface_is_mathlib : True := trivial

end TamesisLab.Foundations.Semigroups
