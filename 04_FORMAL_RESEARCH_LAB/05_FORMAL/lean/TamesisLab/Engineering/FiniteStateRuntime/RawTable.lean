import Mathlib.Data.Fintype.Card

set_option autoImplicit false

/-!
# ENG-FINITE-STATE-RUNTIME-001 — Tabela bruta e tabela validada

```text
Uma tabela bruta pode conter destinos fora dos limites.
A estrutura representa dados recebidos, nao dados ja validados.
```

Cada **posição** do array é um estado; o **valor** naquela posição é o
índice do sucessor. O espaço de estados é, portanto, `Fin next.size`.

`raw.next.size` é o **único** nome público para o número de estados.
Nenhum accessor `stateCount` é criado, e nenhum campo `size` é
armazenado: ele seria redundante e criaria obrigação de consistência.

A tabela vazia satisfaz `Valid` por vacuidade. Isso é deliberado: a
validade é **estrutural**, e a existência de um estado inicial pertence à
camada de consulta.
-/

namespace TamesisLab.Engineering.FiniteStateRuntime

/-- Tabela de transições recebida em tempo de execução.

Pode conter destinos fora dos limites; é exatamente por isso que ela é a
representação certa para a **entrada**. -/
structure RawTransitionTable where
  /-- `next[i]` é o índice do sucessor do estado `i`. -/
  next : Array Nat
deriving DecidableEq, Repr, BEq

/-- Validade **estrutural**: todo destino permanece dentro do domínio.

Significa que cada estado registrado possui exatamente um sucessor e que
esse sucessor pertence ao mesmo espaço finito.

**Não** significa: tabela não vazia, alcançabilidade de todos os estados,
componente único, ciclo único, estado inicial válido, nem ausência de
estados transitórios. -/
def RawTransitionTable.Valid (t : RawTransitionTable) : Prop :=
  ∀ i : Fin t.next.size, t.next[i] < t.next.size

/-- A validade é decidível, sem qualquer recurso a raciocínio clássico.

A instância se monta a partir da decidibilidade de `<` em `ℕ` e da
finitude de `Fin`. -/
instance RawTransitionTable.decidableValid (t : RawTransitionTable) :
    Decidable t.Valid := by
  unfold RawTransitionTable.Valid
  infer_instance

/-- Tabela cujo fechamento já está provado.

O campo `closed` é uma proposição, e portanto é apagado na execução — é o
que permite `step` ser computável apesar de consumi-lo. -/
structure ValidatedTransitionTable where
  /-- O mesmo array da tabela bruta, preservado sem alteração. -/
  next : Array Nat
  /-- Todo destino permanece dentro do domínio. -/
  closed : ∀ i : Fin next.size, next[i] < next.size

/-- Volta à representação bruta, descartando a prova.

É público **porque** os dois teoremas centrais falam da execução sobre a
tabela original; sem ele, seriam inenunciáveis. -/
def ValidatedTransitionTable.toRaw (t : ValidatedTransitionTable) :
    RawTransitionTable :=
  ⟨t.next⟩

/-- A tabela convertida é válida — imediato, pois `toRaw` só descarta a
prova. -/
theorem ValidatedTransitionTable.toRaw_valid (t : ValidatedTransitionTable) :
    t.toRaw.Valid :=
  t.closed

end TamesisLab.Engineering.FiniteStateRuntime
