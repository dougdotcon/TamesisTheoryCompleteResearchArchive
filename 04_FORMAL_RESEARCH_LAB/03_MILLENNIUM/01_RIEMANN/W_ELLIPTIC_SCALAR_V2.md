---
class_id: W-ELLIPTIC-SCALAR
version: 2
status: SPECIFIED_NOT_PROVED
---

# W-ELLIPTIC-SCALAR (v2) — classe geométrica estreita

## Os quatro objetos, distinguidos

A imprecisão que os gates anteriores expuseram vinha de tratar como um só
objeto quatro coisas diferentes. A especificação as separa:

| # | Objeto | Descrição |
|---|---|---|
| 1 | **operador formal** `p` | expressão pseudodiferencial clássica elíptica de ordem `m > 0` sobre `M`, sem domínio fixado |
| 2 | **domínio** `D` | subespaço denso de `L²(M)` no qual se define uma extensão |
| 3 | **realização auto-adjunta** | o par `(p, D)` tal que o operador resultante é auto-adjunto |
| 4 | **operador realizado `P`** | o operador auto-adjunto concreto em `L²(M)` que resulta de 3 |

**A classe é uma propriedade do objeto 4.** Nem do 1, nem do conjunto de
todas as realizações do 1.

## Definição

`P ∈ W-ELLIPTIC-SCALAR` quando `P` é um **operador realizado** que satisfaz
**individualmente** todas as condições:

```yaml
operator_realization:
  self_adjoint: true          # P eh auto-adjunto em L^2(M)
  positive: true              # espectro contido em (0, +infinito)

symbol_class:
  classical_pseudodifferential: true
  elliptic: true
  order: "m > 0 (real)"

base:
  smooth: true
  compact: true
  boundary: EXCLUDED_IN_V2

action:
  scalar: true
  vector_bundle_or_system: EXCLUDED_IN_V2

spectrum:
  discrete: true              # ver "Hipoteses incorporadas"
  finite_multiplicity: true
```

## Forma de quantificação — obrigatória

Correta:

```text
Para todo operador realizado P que satisfaça individualmente
as hipóteses de W-ELLIPTIC-SCALAR, …
```

**Proibida:**

```text
Para todas as realizações auto-adjuntas de uma expressão formal p, …
```

Motivo: quantificar sobre *todas* as realizações de uma expressão formal
incluiria realizações que **não** satisfazem a classe pseudodiferencial
auditada — por exemplo realizações cujo domínio destrói a estrutura de
símbolo, ou que não sejam positivas. Nenhuma fonte obtida garante que toda
realização auto-adjunta de um `p` fixo permaneça na classe. Afirmar isso
seria importar um teorema não auditado.

Consequência prática: o no-go, quando enunciado, exclui **cada `P` da
classe**, um a um. Não afirma nada sobre operadores formais nem sobre
realizações fora da classe.

## Hipóteses diretas versus incorporadas

Estados: `SOURCE_DIRECT`, `SOURCE_CITED_RESULT`, `BRIDGE_DOCUMENTED`,
`EXPLICIT_CLASS_ASSUMPTION`, `UNRESOLVED`.

| Hipótese | Estado | Origem |
|---|---|---|
| `P` auto-adjunto | `SOURCE_CITED_RESULT` | Coriasco–Doll p. 1 ("self-adjoint") |
| `P` positivo | `SOURCE_CITED_RESULT` | Coriasco–Doll p. 1 ("positive") |
| pseudodiferencial clássico | `SOURCE_CITED_RESULT` | Coriasco–Doll p. 1 |
| elíptico | `SOURCE_CITED_RESULT` | Coriasco–Doll p. 1 |
| ordem `m > 0` real | `SOURCE_CITED_RESULT` | Coriasco–Doll p. 1 |
| `M` suave compacta | `SOURCE_CITED_RESULT` | Coriasco–Doll p. 1 ("compact manifold") |
| **sem bordo** | `EXPLICIT_CLASS_ASSUMPTION` | estreitamento deliberado deste laboratório |
| **ação escalar** | `EXPLICIT_CLASS_ASSUMPTION` | estreitamento deliberado |
| **espectro discreto, multiplicidade finita** | `EXPLICIT_CLASS_ASSUMPTION_OR_CITED_RESULT` | ver abaixo |
| `C_P > 0` | `ELEMENTARY_COROLLARY_PENDING_FORMAL_ARGUMENT` | `GLOBAL_WEYL_CONSTANT.md` |

### Sobre o espectro discreto

`Coriasco–Doll` estabelecem a cadeia *resolvente compacto → base ortonormal
de autofunções → `0 < λ₁ ≤ λ₂ ≤ … → +∞`* **no contexto SG deles**, não para
variedades compactas. Para `M` compacta o análogo é teoria elíptica padrão,
mas **não foi lido em fonte obtida**.

Decisão: a discretude entra na classe como **hipótese incorporada
explícita** (`EXPLICIT_CLASS_ASSUMPTION`), não como consequência derivada.
Se um gate futuro obtiver a fonte, ela passa a `SOURCE_CITED_RESULT` e a
hipótese pode ser removida da definição. Enquanto isso, o enunciado do
no-go carrega a hipótese visivelmente. `GAP-RH-012` permanece aberto.

## Por que o bordo foi excluído

```text
A classe foi estreitada ao contexto sem bordo para evitar importar
resultados de problemas elipticos de bordo nao auditados.
```

Fatos registrados:

- Coriasco–Doll dizem "compact manifold" e **não** usam a palavra "closed".
  Este laboratório **não** afirma que a fonte diz "closed".
- Hörmander 1968 não formula condição de bordo alguma.
- Ivrii formula o Example 3.1.1 **com** problema de contorno
  (`D(A) = {u : Bu|∂X = 0}`), o que exige elipticidade do par `(A,B)` —
  hipótese adicional não auditada.

Excluir o bordo é, portanto, o único modo de não importar tacitamente a
teoria de Boutet de Monvel ou condições `(A,B)` elípticas.

## Por que sistemas e fibrados foram excluídos

Ver `W_ELLIPTIC_SYSTEM_DEFERRED.md`. Resumo: a constante correta para
sistemas é a de Ivrii (3.1.3) com `n(x,ξ)`, e a identidade de traço
matricial da etapa local→global (GWB-004) não foi auditada. `GAP-RH-009`
permanece **aberto** e **não** é fechado por este gate.

## Relação com a Classe W v1

`OPERATOR_CLASS.md` (v1) não foi editado; permanece como registro do que a
auditoria refutou. `W_ELLIPTIC_CLASS.md` (v2, em `08_REVIEWS/`) é a versão
intermediária; **este documento é a versão vigente**, que acrescenta a
exclusão explícita de bordo e de sistemas e a distinção dos quatro objetos.
