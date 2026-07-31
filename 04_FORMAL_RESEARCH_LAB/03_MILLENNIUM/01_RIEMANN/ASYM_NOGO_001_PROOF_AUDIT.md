# ASYM-NOGO-001 — Auditoria da prova

Revisão adversarial do núcleo formalizado, conforme a Fase 5 da skill
`/goal`. Cada item pergunta como o resultado poderia estar errado ou ser
mais fraco do que parece.

## Auditoria de axiomas do kernel

```text
#print axioms TamesisLab.RHNogo.AsymptoticCore.asym_nogo_001
  → [propext, Classical.choice, Quot.sound]
#print axioms TamesisLab.RHNogo.AsymptoticCore.eventually_normalization_identity
  → [propext, Classical.choice, Quot.sound]
#print axioms ...tendsto_powerLogFactor_atTop_of_lt_one   → idem
#print axioms ...tendsto_powerLogFactor_atTop_of_eq_one   → idem
#print axioms ...tendsto_powerLogFactor_nhds_zero_of_one_lt → idem
#print axioms TamesisLab.RHNogo.asymNogoStatement_holds   → idem
```

Nenhum `sorryAx` e nenhum axioma local. Os três axiomas listados são os
axiomas padrão do Lean/Mathlib, presentes em qualquer resultado de análise
real da biblioteca.

## Checklist adversarial

| Risco auditado | Verificação | Resultado |
|---|---|---|
| **Hipótese oculta** | as únicas hipóteses são `0 < α`, `0 < c`, `0 < C` e os dois limites; nenhuma hipótese de monotonicidade, integralidade, positividade ou não nulidade de `N` | OK |
| **Divisão por `N(T)`** | proibida pelo gate; a identidade eventual divide apenas por `T`, `log T` e `T^α`, todos não nulos para `T > 1` | OK — nenhuma divisão por `N(T)` |
| **Conclusão mais forte que a prova** | a conclusão é `False` a partir das duas hipóteses; nada é afirmado sobre existência de funções com uma só das assintóticas | OK |
| **Quantificador incorreto** | `α`, `c`, `C` são universalmente quantificados; a contradição vale para cada escolha, não para uma escolha particular | OK |
| **Caso não coberto** | `lt_trichotomy α 1` cobre `α < 1`, `α = 1`, `α > 1` exaustivamente; `α ≤ 0` é excluído pela hipótese `0 < α` | OK |
| **Fatos globais falsos sobre `log`** | `Real.log T ≤ 0` para `0 < T ≤ 1` e `Real.log` é definido como 0 em `T ≤ 0`; todas as afirmações sobre positividade de `log` são feitas sob `T > 1` ou `T ≥ 1` via `filter_upwards` | OK — nenhuma afirmação global |
| **`T^α` para `T ≤ 0`** | `Real.rpow` tem convenção própria em bases não positivas; a identidade só é afirmada eventualmente, sob `T > 1` | OK |
| **Dependência circular** | o grafo de dependências é acíclico: Definitions → Normalization/PowerLog → Incompatibility → Audit; nenhum lema usa o teorema principal | OK |
| **Teorema trivial apresentado como descoberta** | `scientific_novelty` fixado em `STANDARD_ASYMPTOTIC_INCOMPATIBILITY_FORMALIZED_FOR_LOCAL_USE` em todos os itens; o `README` da frente e a claim repetem que não há novidade | OK |
| **Import mascarando dependência** | os imports são apenas `Log.Basic`, `Pow.Real`, `Pow.Asymptotics`, `Order.Filter.AtTopBot.Basic` e `Topology.Algebra.Order.Field`; nenhum import de teoria analítica dos números, PDE, geometria ou legado | OK |
| **Resultado computacional tratado como prova** | nenhum `decide`, `native_decide` ou verificação numérica é usado; a proposição é infinitária e a prova é analítica | OK |
| **Generalização física não autorizada** | nenhum enunciado menciona operador, espectro, física ou zeta | OK |
| **`sorry` disfarçado** | nenhum `by_contra` sem fechamento, nenhuma declaração opaca, nenhum postulado, nenhum teorema importado fictício; auditoria de axiomas acima confirma | OK |
| **Autoimplícitos silenciosos** | `set_option autoImplicit false` em `Audit.lean`; a falta desse guarda no primeiro rascunho fez `AsymNogoStatement` ser capturado como variável universal, erro detectado pelo compilador e corrigido com o import correto | Corrigido |

## Falha real ocorrida e corrigida

1. `Definitions.lean` falhou com *"failed to compile definition, consider
   marking it as noncomputable"* — as quatro definições dependem de
   `Real.log` e da divisão real. Corrigido com `noncomputable def`. Isso é
   herança da Mathlib e não introduz axioma.
2. `Audit.lean` falhou com *"type of theorem is not a proposition"*: o
   arquivo não importava `SignatureProbe`, e `AsymNogoStatement` foi
   auto-vinculado como `Sort u_1`. Corrigido com o import explícito e
   `set_option autoImplicit false`.
3. `Normalization.lean` falhou com *"No goals to be solved"*: `field_simp`
   já fechava o objetivo, tornando o `ring` seguinte inválido. Removido.

Nenhuma dessas falhas foi contornada com token proibido.

## Alcance — o que foi e o que não foi provado

```text
Foi provado:
uma incompatibilidade abstrata entre duas normalizações
assintóticas de uma função real.

Não foi provado:
a fórmula de Riemann–von Mangoldt;
a lei de Weyl;
a aplicação dessas fórmulas a uma classe de operadores;
RH-NOGO-001 completo;
inexistência de operador de Hilbert–Pólya;
verdade ou falsidade da Hipótese de Riemann.
```

A ponte entre o lema e as duas leis de contagem permanece aberta
(GAP-RH-002, GAP-RH-003) e depende da leitura integral das fontes
primárias, ainda `TO_FETCH` (ver `EPISTEMIC_CORRECTIONS.md`).
