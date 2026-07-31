# Ordem do operador — auditoria de paridade

## O problema descoberto no gate anterior

`OPERATOR_CLASS.md` (Classe W v1) declarava operador **diferencial** de
ordem inteira `m ≥ 1` arbitrária, elíptico e positivo. Mas Hörmander 1968,
p. 193, diz que o símbolo principal `p` é *"a real homogeneous polynomial
of degree `m`"*. Para operador diferencial escalar, `p(x,−ξ) = (−1)^m
p(x,ξ)`; se `p > 0` para `ξ ≠ 0` (elipticidade + positividade), então `m`
tem de ser **par** quando `d ≥ 2`. A classe v1 era, portanto, **vazia para
`m` ímpar** — defeito de formulação (GAP-RH-011).

## Caso diferencial

Nenhuma fonte obtida **restringe explicitamente** `m ∈ 2ℕ`. O que existe:

- Hörmander 1968 p. 193: símbolo principal é polinômio homogêneo **real** de
  grau `m`; positividade formal `(Pu,u) ≥ c(u,u)`, `c > 0`. A paridade é
  **consequência**, não hipótese declarada.
- Ivrii 2016, Example 3.1.1(ii), p. 32: *"Suppose that `A_B` is positive
  definite (**then `m_A ≥ 2`**)"* — a fonte deriva uma restrição de ordem a
  partir da positividade, mas apenas `m ≥ 2`, não paridade.

Estado: a paridade permanece uma **consequência não enunciada** nas fontes
obtidas. Não deve ser mantida silenciosamente como `m ≥ 1` arbitrário.

## Caso pseudodiferencial

Coriasco–Doll 2020, p. 1, enuncia para *"positive elliptic self-adjoint
classical pseudodifferential operator of **order `m > 0`** on a compact
manifold"*.

Aqui `m > 0` é **real**, o símbolo principal é positivo-homogêneo de grau
`m` (não polinomial), e **a questão da paridade desaparece**: não há
restrição `p(x,−ξ) = (−1)^m p(x,ξ)` porque `p` não é polinômio.

Ivrii 2016, Example 3.1.1, também usa `m = m_A` genérico, e a seção
"Fractional Laplacians" trata explicitamente `m > 0` com `m ∉ 2ℤ`,
confirmando que ordens não pares são objeto legítimo da teoria (embora ali
num contexto de domínio com bordo, fora da Boutet de Monvel).

## Decisão

```text
PSEUDODIFFERENTIAL_POSITIVE_ORDER
```

Justificativa:

1. É a única formulação, entre as fontes obtidas, que enuncia a lei
   **global** com hipóteses precisas (Coriasco–Doll).
2. Elimina o defeito de paridade sem introduzir hipótese nova: `m > 0` real.
3. `α = d/m` passa a ser real positivo arbitrário — exatamente a
   generalidade de `ASYM-NOGO-001`, que quantifica sobre `α > 0` real.
4. Contém o caso diferencial de ordem par como caso particular (todo
   operador diferencial elíptico clássico é pseudodiferencial clássico).

`BOTH_WITH_SEPARATE_THEOREMS` seria igualmente defensável — Hörmander
dedica a Seção 5 a operadores diferenciais de ordem `m` — mas exigiria
manter duas classes com dois conjuntos de fontes, sem ganho para o no-go.
Registrado como alternativa rejeitada, não como impossibilidade.

## Efeito sobre a Classe W

`W-ELLIPTIC` v2 adota ordem **real `m > 0`**, sem restrição de paridade.
GAP-RH-011 fica **fechado por reformulação**, não por prova: a classe v1
não foi corrigida — foi substituída.
