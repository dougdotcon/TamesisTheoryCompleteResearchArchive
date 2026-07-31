---
class_id: W-ELLIPTIC-SCALAR
version: 3
status: SPECIFIED_NOT_PROVED
supersedes: W_ELLIPTIC_SCALAR_V2.md
split:
  - W-ELLIPTIC-SCALAR-SOURCE
  - W-ELLIPTIC-SCALAR-BRIDGE
---

# W-ELLIPTIC-SCALAR (v3) — classe refinada e dividida

A v2 tratava como um bloco só duas coisas que precisam ficar separadas: o
que a fonte **literalmente diz** e o que este laboratório **acrescentou**
para que a ponte até `W-POWER` feche. A v3 divide a classe em duas.

```text
W-ELLIPTIC-SCALAR-SOURCE   ⊇   W-ELLIPTIC-SCALAR-BRIDGE
(o que Coriasco–Doll enuncia)   (SOURCE + acréscimos deste laboratório)
```

Toda condição presente apenas na segunda é marcada
`EXPLICIT_BRIDGE_ASSUMPTION`. Nenhuma delas é atribuída a fonte alguma.

## Os quatro objetos (mantido da v2)

| # | Objeto | Descrição |
|---|---|---|
| 1 | **operador formal** `p` | expressão pseudodiferencial clássica elíptica de ordem `m > 0` sobre `M`, sem domínio fixado |
| 2 | **domínio** `D` | subespaço denso de `L²(M)` no qual se define uma extensão |
| 3 | **realização auto-adjunta** | o par `(p, D)` tal que o operador resultante é auto-adjunto |
| 4 | **operador realizado `P`** | o operador auto-adjunto concreto em `L²(M)` resultante de 3 |

**A classe é propriedade do objeto 4.**

## Forma de quantificação — obrigatória

Correta:

```text
Para todo operador realizado P que satisfaça individualmente
as hipóteses de W-ELLIPTIC-SCALAR-BRIDGE, …
```

Proibida:

```text
Para todas as realizações auto-adjuntas de uma expressão formal p, …
```

Motivo (inalterado desde a v2): nenhuma fonte obtida garante que toda
realização auto-adjunta de um `p` fixo permaneça na classe
pseudodiferencial auditada. Afirmar isso importaria um teorema não lido.

---

## `W-ELLIPTIC-SCALAR-SOURCE`

Somente o que **Coriasco–Doll 2020, p. 1**, enuncia literalmente:

> *"Hörmander [15] proved, for a positive elliptic self-adjoint classical
> pseudodifferential operator of order m > 0 on a compact manifold, the
> Weyl law N(λ) = γ·λ^{d/m} + O(λ^{(d−1)/m})"*

```yaml
source_conditions:
  - id: S1
    condition: "P eh auto-adjunto"
    literal_words: "self-adjoint"
  - id: S2
    condition: "P eh positivo"
    literal_words: "positive"
  - id: S3
    condition: "P eh pseudodiferencial classico"
    literal_words: "classical pseudodifferential operator"
  - id: S4
    condition: "P eh eliptico"
    literal_words: "elliptic"
  - id: S5
    condition: "ordem m > 0"
    literal_words: "of order m > 0"
  - id: S6
    condition: "M variedade compacta"
    literal_words: "on a compact manifold"
```

Seis condições. **Nada além disso** está na fonte. Em particular a fonte
**não** diz: escalar, sem bordo, `M` não vazia, `d ≥ 1`, espectro discreto,
`γ > 0`, forma do símbolo principal.

---

## `W-ELLIPTIC-SCALAR-BRIDGE`

`P ∈ W-ELLIPTIC-SCALAR-BRIDGE` quando `P` satisfaz **individualmente** S1–S6
**e** todos os acréscimos abaixo.

```yaml
bridge_additions:
  - id: B1
    condition: "acao escalar; sem fibrado vetorial, sem sistema"
    status: EXPLICIT_BRIDGE_ASSUMPTION
    why: >
      A identidade local->global de Ivrii (3.1.11) que a ponte usa eh
      ESCALAR. A versao com traco fibrado nao foi lida em fonte alguma.
      Ver W_ELLIPTIC_SYSTEM_DEFERRED.md; GAP-RH-009 permanece ABERTO.

  - id: B2
    condition: "M sem bordo"
    status: EXPLICIT_BRIDGE_ASSUMPTION
    why: >
      Coriasco-Doll dizem "compact manifold", NAO "closed". Ivrii formula o
      Example 3.1.1 COM problema de contorno, o que exigiria elipticidade do
      par (A,B). Excluir o bordo eh o unico modo de nao importar tacitamente
      Boutet de Monvel ou condicoes (A,B).

  - id: B3
    condition: "M eh NAO VAZIA"
    status: EXPLICIT_BRIDGE_ASSUMPTION
    why: >
      Com M vazia, L^2(M) = {0}, o espectro eh vazio, N_P == 0 e nenhuma
      constante positiva existe. A condicao eh necessaria e nao eh dita por
      fonte alguma. Corresponde ao passo 6 de GWB-008A.

  - id: B4
    condition: "d = dim M >= 1"
    status: EXPLICIT_BRIDGE_ASSUMPTION
    why: >
      W-POWER exige expoente alpha > 0. Como alpha = d/m e m > 0, seria
      alpha = 0 caso d = 0. Com d = 0, M compacta eh um conjunto finito de
      pontos, o espectro eh finito e N_P eh eventualmente constante: nao ha
      lei de potencia com expoente positivo. Formalizado como
      dimension_div_order_pos: 0 < d -> 0 < m -> 0 < d/m.

  - id: B5
    condition: >
      O simbolo principal p_m eh real, positivo fora da secao nula
      (p_m(x,xi) > 0 para todo xi != 0) e homogeneo de grau m > 0 em xi.
    status: EXPLICIT_BRIDGE_ASSUMPTION
    why: >
      "elliptic" (S4) da p_m(x,xi) != 0 para xi != 0; "positive" (S2) eh
      afirmado do OPERADOR, nao do simbolo. A passagem de "operador
      positivo" para "simbolo principal positivo" NAO foi lida em fonte
      obtida. Ela eh assumida explicitamente, nao derivada.
      A homogeneidade de grau m eh parte da definicao padrao de
      "classical pseudodifferential of order m", mas o texto de
      Coriasco-Doll nao a escreve; por prudencia entra aqui.

  - id: B6
    condition: "espectro discreto com multiplicidades finitas"
    status: EXPLICIT_CLASS_ASSUMPTION
    why: "ver DISCRETENESS_CLASSIFICATION.md; GAP-RH-012 permanece aberto."
```

## Tabela de proveniência

| Condição | Classe | Estado |
|---|---|---|
| auto-adjunto | SOURCE | `SOURCE_CITED_RESULT` |
| positivo (operador) | SOURCE | `SOURCE_CITED_RESULT` |
| pseudodiferencial clássico | SOURCE | `SOURCE_CITED_RESULT` |
| elíptico | SOURCE | `SOURCE_CITED_RESULT` |
| ordem `m > 0` | SOURCE | `SOURCE_CITED_RESULT` |
| `M` compacta | SOURCE | `SOURCE_CITED_RESULT` |
| escalar (B1) | BRIDGE | `EXPLICIT_BRIDGE_ASSUMPTION` |
| sem bordo (B2) | BRIDGE | `EXPLICIT_BRIDGE_ASSUMPTION` |
| `M ≠ ∅` (B3) | BRIDGE | `EXPLICIT_BRIDGE_ASSUMPTION` |
| `d ≥ 1` (B4) | BRIDGE | `EXPLICIT_BRIDGE_ASSUMPTION` |
| `p_m > 0` fora de `ξ = 0`, homogêneo de grau `m` (B5) | BRIDGE | `EXPLICIT_BRIDGE_ASSUMPTION` |
| espectro discreto (B6) | BRIDGE | `EXPLICIT_CLASS_ASSUMPTION` |

Seis condições de fonte, seis acréscimos. **A metade da classe é deste
laboratório.** Registrar isso é o ponto do gate.

## O que a v3 muda em relação à v2

1. Divisão `SOURCE` / `BRIDGE`, com proveniência linha a linha.
2. Novas condições explícitas `M ≠ ∅` (B3) e `d ≥ 1` (B4).
3. A condição sobre o símbolo principal (B5) deixa de ser tácita: a v2
   escrevia "elíptico" e usava `p_m > 0` em `GLOBAL_WEYL_CONSTANT.md` sem
   marcar a passagem. Isso era uma lacuna de registro e está corrigido.
4. Nada foi removido; nada foi promovido a fonte.

## O que a v3 **não** muda

- Sistemas e fibrados continuam fora. `GAP-RH-009` **não** foi fechado.
- Bordo continua fora.
- Nenhuma prova foi executada. `RH-NOGO-001` permanece `SCOPED`.
