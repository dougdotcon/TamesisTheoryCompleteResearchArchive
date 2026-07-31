---
document_id: WEYL-COEFFICIENT-POSITIVITY
obligations: [GWB-008A, GWB-008B, GWB-008C]
status: DOCUMENTED_NOT_PROVED
lean_core: "05_FORMAL/lean/TamesisLab/RHNogo/Geometry/PositiveCoefficient.lean"
---

# Positividade e finitude do coeficiente de Weyl escalar

`GWB-008` da v2 dizia apenas `C_P > 0` e estava marcada
`ELEMENTARY_COROLLARY_PENDING_FORMAL_ARGUMENT`. Isso misturava três
afirmações de naturezas diferentes. Este documento as separa.

| Id | Afirmação | Natureza |
|---|---|---|
| `GWB-008A` | `vol(B_x) > 0` para cada `x`, e `∫_M vol(B_x) dx > 0` | geométrica + teoria da medida |
| `GWB-008B` | `C_P = (2π)^{−d} ∫_M vol(B_x) dx > 0` | aritmética trivial dado 008A |
| `GWB-008C` | `C_P < ∞` | geométrica, **exige fonte** |

onde `B_x = {ξ ∈ T*_x M : p_m(x,ξ) < 1}`.

---

## Camada 1 — argumento geométrico (documental, **não** formalizado)

### GWB-008A — os seis passos

```text
1.  Elipticidade (S4) da p_m(x,xi) != 0 para xi != 0.
    Com a hipotese B5 (simbolo principal real e positivo fora da secao
    nula), tem-se p_m(x,xi) > 0 para todo xi != 0.

2.  p_m(x, .) eh continua na fibra T*_x M (parte da definicao de simbolo
    classico).

3.  B_x = p_m(x, .)^{-1}( (-infinito, 1) ) eh ABERTO em T*_x M, por ser
    pre-imagem de um aberto por funcao continua.

4.  p_m(x, .) eh homogenea de grau m > 0 (B5), logo p_m(x, 0) = 0 < 1.
    Portanto 0 ∈ B_x: o conjunto eh uma vizinhanca aberta NAO VAZIA da
    origem da fibra. (Equivalentemente: p_m(x, t xi) = t^m p_m(x, xi) -> 0
    quando t -> 0+, de modo que t xi ∈ B_x para t pequeno.)

5.  A medida de Lebesgue da fibra — que tem dimensao d >= 1 por B4 — eh
    positiva em abertos nao vazios. Logo vol(B_x) > 0 para cada x.
    [Este eh o passo que o nucleo Lean cobre: GWB-008A-CORE.]

6.  M eh compacta (S6) e NAO VAZIA (B3), e x |-> vol(B_x) eh continua e
    estritamente positiva. A integral de uma funcao continua positiva sobre
    um espaco de medida nao vazia eh positiva:
        integral_M vol(B_x) dx > 0.
```

### Estado de cada passo

```yaml
- step: 1
  status: EXPLICIT_BRIDGE_ASSUMPTION
  note: "depende de B5; NAO derivado de S2 ('positive' eh dito do operador)"
- step: 2
  status: STANDARD_DEFINITION
  note: "parte da definicao de simbolo classico; nao lido literalmente"
- step: 3
  status: ELEMENTARY_TOPOLOGY
- step: 4
  status: ELEMENTARY_ALGEBRA
  note: "usa homogeneidade de grau m > 0 (B5)"
- step: 5
  status: FORMALIZED_CORE
  lean: "measure_pos_of_isOpen_subset"
- step: 6
  status: DOCUMENTED_STANDARD_ARGUMENT
  note: >
    A CONTINUIDADE de x |-> vol(B_x) nao foi lida em fonte obtida. Ela eh
    plausivel (dependencia suave do simbolo) mas NAO esta demonstrada aqui.
    Ver GAP-RH-015.
```

**Nenhum dos seis passos foi demonstrado neste laboratório.** O passo 5 tem
um núcleo abstrato verificado em Lean; os demais são documentais.

### GWB-008B

Dado `GWB-008A`, e sendo `(2π)^{−d} > 0`:

```text
C_P = (2pi)^{-d} * integral_M vol(B_x) dx  >  0.
```

Produto de dois reais positivos. Núcleo Lean:
`coefficient_pos_of_factors`.

Observação de escopo: a **fórmula** de `C_P` é a escalar, tirada de
Hörmander 1968 (1.1) p.193 e comparável a Ivrii (3.1.3). Ela **não** é
aplicada a sistemas — para sistemas a constante correta envolve `n(x,ξ)`,
o número de autovalores de `A⁰(x,ξ)` em `(0,1)`. Ver
`W_ELLIPTIC_SYSTEM_DEFERRED.md`.

### GWB-008C — finitude

`W-POWER` exige que o limite seja um número real; portanto `C_P < ∞` é
obrigação **separada** e não decorre de `GWB-008A`.

Argumento padrão:

```text
Elipticidade + compacidade do fibrado cosferico S*M (compacto porque M eh
compacta) + continuidade e positividade de p_m dao uma cota inferior
uniforme c > 0 com p_m(x, xi) >= c |xi|^m. Logo

    B_x  subset  { |xi| < c^{-1/m} },

um conjunto limitado, de volume finito, uniformemente em x. Integrando
sobre M compacta, C_P < infinito.
```

```yaml
- id: GWB-008C
  evidence_status: DOCUMENTED_STANDARD_ARGUMENT_REQUIRING_SOURCE
  gap: GAP-RH-015
  note: >
    A cota inferior uniforme c > 0 sobre o fibrado cosferico eh um
    argumento de compacidade padrao, mas NENHUMA fonte obtida o enuncia.
    Nao foi formalizado; formaliza-lo exigiria definir fibrado cosferico e
    simbolo, o que este gate PROIBE.
```

---

## Camada 2 — núcleo formalizável (Lean, verificado)

O que efetivamente foi para Lean, em
`TamesisLab/RHNogo/Geometry/PositiveCoefficient.lean`:

| Lean | Cobre | Enunciado |
|---|---|---|
| `measure_pos_of_isOpen_subset` | passo 5 | `IsOpen U → U.Nonempty → U ⊆ S → 0 < μ S` para `μ` positiva em abertos |
| `coefficient_pos_of_factors` | GWB-008B | `0 < a → 0 < b → 0 < a * b` |
| `PositiveWeylCoefficient.ofFactors` | interface | produz o dado que `PowerCountingLaw` consome |
| `dimension_div_order_pos` | B4 | `0 < d → 0 < m → 0 < d/m` |
| `integral_pos_of_nonneg_of_support_measure_pos` | variante integral do passo 6 | reexporta `integral_pos_iff_support_of_nonneg` |

### O que o núcleo Lean **não** faz

```text
NAO define variedade, fibrado cotangente, operador pseudodiferencial,
simbolo principal, medida de Liouville nem coeficiente de Weyl concreto.

NAO prova que B_x eh aberto — isso exigiria p_m.
NAO prova que x |-> vol(B_x) eh continua.
NAO prova a lei de Weyl.
NAO prova que existe operador algum na classe.

Um wrapper de teoria da medida NAO prova a lei de Weyl. O nucleo aqui
cobre exatamente o passo 5 e a aritmetica de GWB-008B, e nada mais.
```

---

## Estado consolidado

| Obrigação | Estado após este gate |
|---|---|
| `GWB-008A` | `DOCUMENTED_ARGUMENT_WITH_FORMALIZED_CORE` — passos 1–4 e 6 documentais; passo 5 verificado |
| `GWB-008B` | `ELEMENTARY_COROLLARY_WITH_FORMALIZED_CORE` |
| `GWB-008C` | `DOCUMENTED_STANDARD_ARGUMENT_REQUIRING_SOURCE` — `GAP-RH-015` **aberto** |

`GAP-RH-014` (`C_P > 0` sem fonte) passa a
`RESOLVED_DOCUMENTALLY_FOR_SCALAR_BRIDGE_CLASS_ONLY`: o argumento está
escrito e auditável, e seu núcleo de medida está verificado — mas **nenhuma
fonte obtida afirma `C_P > 0`**, e a resolução vale apenas dentro de
`W-ELLIPTIC-SCALAR-BRIDGE`, cuja metade das hipóteses é deste laboratório.
