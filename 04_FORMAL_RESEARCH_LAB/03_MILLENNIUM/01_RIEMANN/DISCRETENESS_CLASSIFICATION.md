---
document_id: DISCRETENESS-CLASSIFICATION
obligations: [GWB-001, GWB-002]
status: CLASSIFIED
related_gaps: [GAP-RH-012, SB-GAP-002]
---

# Classificação honesta da discretude (GWB-001, GWB-002)

O gate pede que a discretude seja classificada sem inflação. A classificação
adotada é a mista, **`EXPLICIT_CLASS_ASSUMPTION` + `SOURCE_CITED_RESULT`**,
porque as duas obrigações têm status diferentes.

## GWB-001 — o espectro é discreto, com multiplicidades finitas

```yaml
evidence_status: EXPLICIT_CLASS_ASSUMPTION
```

Motivo, dito sem rodeio: **nenhuma fonte obtida enuncia a discretude para
operadores pseudodiferenciais elípticos positivos em variedade compacta.**

O que existe:

- **Coriasco–Doll 2020, §3** estabelecem a cadeia
  *resolvente compacto → base ortonormal de autofunções →
  `0 < λ₁ ≤ λ₂ ≤ … → +∞`*, mas **no contexto SG deles**, que não é o de
  variedade compacta. Usar isso como fonte para o caso compacto seria
  transportar um enunciado entre contextos — exatamente o erro que
  `GAP-RH-013` registrou na atribuição da lei global a Hörmander.
- **Hörmander 1968** não enuncia nem prova discretude. A p.193 fala em
  *"at least one self-adjoint extension"* (Friedrichs), não em espectro.

Para `M` compacta o análogo é teoria elíptica padrão. Isso é
provavelmente verdade e certamente **não foi lido**. Portanto entra na
definição da classe, visivelmente, como hipótese incorporada — não como
consequência.

Consequência prática: o enunciado do no-go, quando for escrito, carrega a
discretude **no rosto**, e não escondida atrás de "por elipticidade".

## GWB-002 — `N_P(Λ) = #{j : λ_j < Λ}` é bem definida e finita

```yaml
evidence_status: SOURCE_CITED_RESULT
```

Aqui há fonte literal: **Coriasco–Doll 2020, p.1, eq. (1)** define

```text
N(lambda) = #{ j : lambda_j < lambda }
```

com desigualdade **estrita**. A finitude para cada `Λ` finito é imediata da
enumeração `λ_j → +∞` **dado GWB-001**.

Ou seja: a *definição* e a *convenção de fronteira* são de fonte; a
*finitude* é corolário elementar de uma hipótese incorporada. Registrar as
duas coisas com o mesmo rótulo seria inflação.

## Por que não `SOURCE_CITED_RESULT` para GWB-001

Foi considerado e rejeitado. Promover GWB-001 a resultado citado exigiria
uma destas duas coisas, e nenhuma existe:

1. uma fonte obtida que enuncie a discretude **para variedade compacta**; ou
2. uma prova, neste laboratório, da cadeia
   *elíptico + compacto ⟹ resolvente compacto ⟹ espectro discreto*.

A rota (2) exigiria formalizar teoria pseudodiferencial — proibido neste
gate. A rota (1) permanece como trabalho de recuperação bibliográfica
futura.

## Por que não `UNRESOLVED`

Porque a hipótese **está** na definição da classe e é usada
explicitamente. Chamá-la de irresolvida sugeriria um buraco silencioso na
cadeia; ela não é um buraco, é uma hipótese declarada que estreita a
classe. O custo é que a classe é menor do que a fonte sugere — e esse custo
está registrado.

## Efeito no gap register

| Gap | Antes | Depois |
|---|---|---|
| `GAP-RH-012` | `PARTIALLY_SUPPORTED` | `EXPLICIT_CLASS_ASSUMPTION_CLASSIFIED` |
| `SB-GAP-002` | `EXPLICIT_CLASS_ASSUMPTION` | inalterado; ganha referência a este documento |

**Nenhum dos dois foi fechado.** A classificação torna o estado explícito;
não o resolve.
