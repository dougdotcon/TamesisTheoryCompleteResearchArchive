# Decisão sobre a Classe W

## Opção escolhida

```text
C. REFORMULATE_AS_CLASSICAL_PSEUDODIFFERENTIAL
```

A formulação pseudodiferencial positiva e auto-adjunta é a mais precisa
entre as sustentadas pelas fontes obtidas.

## Justificativa

1. **É a única formulação, entre as fontes obtidas, que enuncia a lei
   global com hipóteses completas.** Coriasco–Doll 2020, p. 1: *"a positive
   elliptic self-adjoint classical pseudodifferential operator of order
   `m > 0` on a compact manifold"* com `N(λ) = #{j : λ_j < λ}` e
   `N(λ) = γλ^{d/m} + O(λ^{(d−1)/m})`.
2. **Resolve o defeito de paridade** (GAP-RH-011) sem hipótese nova: `m > 0`
   real. Ver `ORDER_PARITY_AUDIT.md`.
3. **Resolve a ambiguidade de auto-adjunção** (GAP-RH-010): "self-adjoint"
   = uma realização, não essencial auto-adjunção. Ver
   `SELF_ADJOINT_REALIZATION_DECISION.md`.
4. **Contém o caso diferencial** de ordem par como caso particular, sem
   precisar mantê-lo como classe separada.
5. Alinha `α = d/m` com a quantificação real `α > 0` de `ASYM-NOGO-001`.

## Opções rejeitadas e por quê

| Opção | Por que não |
|---|---|
| **A. PRESERVE_WITH_NEW_SOURCE** | A classe v1 exigia essencial auto-adjunção (não sustentada), fibrados gerais (não sustentados) e ordem inteira `m ≥ 1` (vazia para `m` ímpar). Preservá-la seria manter três hipóteses sem fonte. |
| **B. NARROW_TO_SCALAR_DIFFERENTIAL** | Defensável e seguro, mas estreita demais: descarta a formulação pseudodiferencial, que é a de fato enunciada pela fonte, e mantém a discussão de paridade. |
| **D. SPLIT_INTO_MULTIPLE_CLASSES** | Só se justificaria se houvesse teoremas distintos auditados para escalares, sistemas e fibrados. Não há: os sistemas aparecem em Ivrii (com bordo) e a versão para fibrados sobre variedade compacta fechada **não foi obtida**. |
| **E. SOURCE_STILL_INSUFFICIENT** | Seria excessivo: duas fontes independentes revisadas por pares enunciam a lei global com hipóteses precisas, e a ponte local→global está documentada etapa a etapa. |

## O que a decisão NÃO resolve

- **Fibrados / sistemas (GAP-RH-009):** `W-ELLIPTIC` v2 é **escalar por
  omissão**. A versão para fibrados sobre variedade compacta fechada
  continua sem fonte obtida. A constante correta para sistemas é a de Ivrii
  (3.1.3) com `n(x,ξ)`; ver `GLOBAL_WEYL_CONSTANT.md`.
- **Bordo:** nenhuma fonte obtida diz literalmente "closed manifold" para a
  forma pseudodiferencial. Registrado como `AMBIGUOUS` em
  `W_ELLIPTIC_CLASS.md`.
- **Discretude (GAP-RH-012):** sustentada por analogia com o argumento de
  resolvente compacto de Coriasco–Doll (contexto SG), não por fonte que a
  enuncie para variedades compactas.
- **Positividade de `C_P`:** corolário elementar registrado, não citado.

## Arquitetura resultante

```text
        ASYM-NOGO-001  (VERIFIED em Lean)
              ↑
          W-POWER      (classe abstrata; nenhuma EDP)
              ↑
     GLOBAL-WEYL-BRIDGE   (documentada, NAO formalizada)
              ↑
        W-ELLIPTIC v2  (pseudodiferencial classico, positivo,
                        auto-adjunto, ordem m > 0, M compacta)
```

Este gate **apenas especifica** a inclusão `W-ELLIPTIC ⊆ W-POWER`. Ela não
foi formalizada em Lean, não foi provada, e `ASYM-NOGO-001` não foi
aplicado.

## Status da Classe W v1

`OPERATOR_CLASS.md` **não foi editado**. Fica como registro histórico da
formulação que a auditoria refutou. `W_ELLIPTIC_CLASS.md` é a formulação
vigente e declara explicitamente o que mudou e por quê.
