# FOUND-SEMIGROUP-002 — Plano de contraexemplos

Cada negativa de `ASSUMPTIONS.md` tem aqui um modelo finito planejado.
Nenhuma negativa é afirmada sem exemplo. **Nada foi executado neste gate.**

---

```yaml
- id: CE-001
  refutes: "alcancabilidade eh simetrica"
  finite_types:
    X: "Fin 2  (estados 0, 1)"
    M: "monoide livre gerado por um elemento, agindo por f"
  transition_table:
    f: "0 -> 1 ; 1 -> 1"
  property_refuted: >
    Reachable 0 1 vale (f leva 0 a 1), mas Reachable 1 0 eh falso: a partir
    de 1 toda iteracao permanece em 1. Logo alcancabilidade NAO eh simetrica
    e NAO eh relacao de equivalencia.
  expected_lean_representation: >
    def f : Fin 2 -> Fin 2 := ![1, 1]
    example : f 0 = 1 := by decide
    example : ∀ n, Function.iterate f n 1 = 1 := ...
  expected_python_representation: "dict {0: 1, 1: 1}; fecho transitivo por BFS"
  scientific_value: COUNTEREXAMPLE_TO_OVERGENERALIZATION
  note: >
    Contrasta diretamente com FOUND-SG-013 (transitividade do modelo C3):
    aquilo eh propriedade DO C3, nao de sistemas finitos em geral.

- id: CE-002
  refutes: "toda acao finita eh transitiva"
  finite_types:
    X: "Fin 2"
    M: "monoide trivial"
  transition_table:
    f: "0 -> 0 ; 1 -> 1"
  property_refuted: >
    A acao identidade sobre dois estados tem duas orbitas disjuntas
    {0} e {1}. Nao existe m com m . 0 = 1.
  expected_lean_representation: >
    a acao trivial de PUnit sobre Fin 2, ou id : Fin 2 -> Fin 2
  expected_python_representation: "dict {0: 0, 1: 1}"
  scientific_value: COUNTEREXAMPLE_TO_OVERGENERALIZATION

- id: CE-003
  refutes: >
    "periodicidade eventual implica periodicidade desde n = 0" e
    "minimalPeriod captura o periodo eventual"
  finite_types:
    X: "Fin 3  (estados 0, 1, 2)"
  transition_table:
    f: "0 -> 1 ; 1 -> 2 ; 2 -> 2"
  property_refuted: >
    O estado 0 tem cauda de comprimento 2 antes do ponto fixo 2:
      f^[0] 0 = 0, f^[1] 0 = 1, f^[2] 0 = 2, f^[3] 0 = 2.
    Logo mu = 2, lam = 1 e f^[mu + lam] 0 = f^[mu] 0.
    Mas 0 NAO eh periodico: nao existe n > 0 com f^[n] 0 = 0.
    Consequencia critica: Function.minimalPeriod f 0 = 0, porque
    0 ∉ periodicPts f. Quem tratasse minimalPeriod como "periodo
    eventual" obteria lam = 0, contradizendo 0 < lam.
  expected_lean_representation: >
    def f : Fin 3 -> Fin 3 := ![1, 2, 2]
    example : Function.iterate f 3 0 = Function.iterate f 2 0 := by decide
    example : ¬ ∃ n, 0 < n ∧ Function.iterate f n 0 = 0 := ...
  expected_python_representation: "dict {0: 1, 1: 2, 2: 2}; deteccao de cauda e ciclo"
  scientific_value: COUNTEREXAMPLE_TO_OVERGENERALIZATION
  note: >
    Este eh o contraexemplo mais importante do conjunto: ele justifica
    FSG2-PER-004 (o ponto periodico eh f^[mu] x, nao x) e sustenta
    FSG2-GAP-002b.

- id: CE-004
  refutes: "toda acao finita eh fiel"
  finite_types:
    X: "Fin 2"
    M: "ZMod 4 ou monoide ciclico de ordem 4"
  transition_table:
    acao: "m . x = (x + m) mod 2"
  property_refuted: >
    Os elementos 0 e 2 de ZMod 4 induzem a MESMA funcao em X (a
    identidade), mas sao distintos em M. Logo a acao nao eh fiel e a
    aplicacao M -> (X -> X) nao eh injetiva.
  expected_lean_representation: >
    MulAction/AddAction de ZMod 4 sobre ZMod 2 pelo quociente;
    example : (0 : ZMod 4) ≠ 2 ∧ ∀ x, (0 : ZMod 4) +ᵥ x = (2 : ZMod 4) +ᵥ x
  expected_python_representation: "tabela de acao 4x2; agrupar por funcao induzida"
  scientific_value: COUNTEREXAMPLE_TO_OVERGENERALIZATION
  note: >
    Contrasta com FOUND-SG-012 (apply_faithful): a fidelidade eh
    propriedade do modelo C3, nao de acoes finitas em geral.
    Consequencia registrada: acoes diferentes podem induzir a mesma
    funcao em X, entao a Camada B nao determina a Camada A.

- id: CE-005
  refutes: "um invariante separa orbitas"
  finite_types:
    X: "Fin 2"
    A: "PUnit  (ou Fin 1)"
  transition_table:
    f: "0 -> 0 ; 1 -> 1  (como em CE-002)"
    I: "I x = PUnit.unit  para todo x"
  property_refuted: >
    I eh invariante (trivialmente), mas as duas orbitas {0} e {1} recebem o
    MESMO valor. Logo IsInvariant I nao implica que I separe orbitas, e a
    reciproca de FSG2-INV-001 eh falsa:
      I y = I x  NAO implica  Reachable x y.
  expected_lean_representation: >
    def I : Fin 2 -> PUnit := fun _ => PUnit.unit
    example : IsInvariant I ∧ I 0 = I 1 ∧ ¬ Reachable 0 1
  expected_python_representation: "funcao constante sobre o grafo de CE-002"
  scientific_value: COUNTEREXAMPLE_TO_OVERGENERALIZATION
  note: >
    Impede a leitura errada mais comum: invariante eh condicao NECESSARIA
    para alcancabilidade, nunca suficiente. Um invariante so refuta
    alcancabilidade; nunca a demonstra.
```

---

## Cobertura das negativas

| Negativa de `ASSUMPTIONS.md` | Contraexemplo |
|---|---|
| alcançabilidade não é simétrica | `CE-001` |
| ação finita não precisa ser transitiva | `CE-002` |
| órbita pode ter cauda antes do ciclo | `CE-003` |
| periodicidade eventual ≠ periodicidade desde `n = 0` | `CE-003` |
| ação finita não precisa ser fiel | `CE-004` |
| ações diferentes podem induzir a mesma função em `X` | `CE-004` |
| invariante pode ser constante em mais de uma órbita | `CE-005` |
| invariante não precisa separar órbitas | `CE-005` |

### Negativa ainda sem contraexemplo planejado

```yaml
- negativa: "o periodo pode depender do estado inicial"
  status: SEM_MODELO_PLANEJADO
  gap: FSG2-GAP-007
  nota: >
    Exige um sistema com pelo menos duas orbitas de periodos distintos,
    por exemplo X = Fin 3 com 0 -> 0 (periodo 1) e 1 -> 2 -> 1 (periodo 2).
    O modelo eh obvio, mas nao foi incluido nos cinco pedidos pelo gate.
    Registrado aqui em vez de ser afirmado sem exemplo.
```

## Estratégia de codificação

`FSG2-GAP-007` cobre a decisão pendente entre:

```text
A. Fin n com ![...] (Matrix.cons notation) e prova por `decide`
B. tipos indutivos proprios, como Regime3 em FOUND-SEMIGROUP-001
```

Vantagem de A: `decide` funciona imediatamente, sem instâncias manuais.
Vantagem de B: coerência com a frente anterior. A decisão fica para a
execução; nenhum código foi escrito.
