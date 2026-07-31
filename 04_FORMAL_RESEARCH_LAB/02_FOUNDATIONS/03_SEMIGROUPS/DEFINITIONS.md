# FOUND-SEMIGROUP-001 — Definições

## Auditoria de escopo (respostas obrigatórias)

1. **O que é um regime?** Um elemento do tipo finito `Regime3`
   (`alpha`, `beta`, `gamma`). Nenhum significado físico é atribuído.
2. **O que é uma transição?** Um elemento do tipo finito `Shift3`
   (`identity`, `forward`, `forward2`).
3. **A transição é função, relação ou símbolo?** Um símbolo (elemento de
   `Shift3`) cuja semântica é dada pela função total
   `Shift3.apply : Shift3 → Regime3 → Regime3`. A ação é funcional e
   determinística; não há relação não determinística neste modelo.
4. **Qual é a operação de composição?**
   `Shift3.comp : Shift3 → Shift3 → Shift3`, tabela finita explícita.
5. **Qual é a ordem da composição?** `comp a b` aplica **`b` primeiro** e
   depois `a` — a mesma convenção da lei `mul_smul` da Mathlib:
   `(a * b) • r = a • (b • r)`. A convenção está declarada nos módulos Lean
   e verificada por FOUND-SG-005; nada é escondido.
6. **Associatividade ou também identidade?** Ambas: o modelo forma um
   monoide (`identity` é identidade bilateral provada). A camada abstrata
   sem identidade é coberta pela `SemigroupAction` da Mathlib.
7. **A ação é fiel?** Sim, provado em FOUND-SG-012 (`apply_faithful`).
8. **O modelo é determinístico?** Sim: `Shift3.apply` é uma função total.
9. **Propriedades do exemplo:** transitividade (FOUND-SG-013),
   cardinalidades 3/3, ciclo de ordem 3, comutatividade da tabela (não
   formalizada — não requerida pelo gate).
10. **Propriedades da estrutura abstrata:** associatividade, identidades e
    compatibilidade da ação — são as leis de `Monoid`/`MulAction` da
    Mathlib, instanciadas após provadas.

## Distinção estrutural

```text
SEMIGROUP:
operação associativa, sem identidade obrigatória.

MONOID:
semigrupo com identidade.

ACTION:
compatibilidade entre composição de transições e aplicação aos regimes.

FINITE MODEL:
instância concreta, sem pretensão de universalidade.
```

## Camada A — interface abstrata

Nenhuma estrutura local foi criada. A busca no checkout fixado da Mathlib
(revisão `79d0395a1825a6264ad5d269e35e60537518955e`) encontrou:

- `SemigroupAction (α β) [Semigroup α] extends SMul α β` com
  `mul_smul (x y : α) (b : β) : (x * y) • b = x • y • b`
  — exatamente a interface para ação de semigrupo, sem exigir identidade
  (`Mathlib/Algebra/Group/Action/Defs.lean`);
- `MulAction (α β) [Monoid α] extends SemigroupAction α β` com
  `one_smul`.

Pela stop condition do gate ("se a interface abstrata apenas duplicar
Mathlib, use a estrutura oficial"), a interface oficial é reutilizada. O
mapeamento terminológico está em `Semigroups/Basic.lean`.

## Camada B — modelo concreto

| Símbolo | Semântica sobre `(alpha, beta, gamma)` |
|---|---|
| `identity` | `(alpha, beta, gamma)` |
| `forward` | `(beta, gamma, alpha)` |
| `forward2` | `(gamma, alpha, beta)` |

Tabela de composição (`comp a b`, linha = `a`, coluna = `b`):

| `comp` | `identity` | `forward` | `forward2` |
|---|---|---|---|
| `identity` | `identity` | `forward` | `forward2` |
| `forward` | `forward` | `forward2` | `identity` |
| `forward2` | `forward2` | `identity` | `forward` |

A estrutura é a do monoide cíclico C3 (na verdade um grupo, mas o gate só
requer e só registra as leis de monoide) agindo regularmente sobre um
conjunto de três elementos.

## Independência do benchmark

Os tipos `Regime3`/`Shift3` são redefinições independentes (opção B da
seção 8 do gate). Nenhum objeto de `TamesisLab/Benchmark/` é importado pela
frente de semigrupos; o benchmark permanece fixture de infraestrutura.

## Vocabulário não usado

Tamesis, TRI, TDTR, Omega, Hamiltoniano Omni-Computacional e Braid P/NP não
aparecem como premissas nem como conclusões. Ver `KNOWN_RESULTS_MATRIX.md`.
