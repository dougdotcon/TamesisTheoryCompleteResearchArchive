---
document_id: PORTFOLIO-REVIEW-LERAY-SOBOLEV-2026-08-09
reviewed_at: 2026-08-09
selected_work_item: FOUND-LERAY-PROJECTOR-SOBOLEV-001
closes_gap: LP-GAP-004
opens_gap: LP-GAP-005
---

# Revisão de portfólio — LP-GAP-004 deixou de estar bloqueada

## Por que esta frente, e por que agora

`LP-GAP-004` ("versão H^s matricial [do projetor de Leray], bloqueada
por FM-GAP-001") estava registrada como bloqueada desde o fechamento de
`FOUND-LERAY-PROJECTOR-001`. `FM-GAP-001` era exatamente "o Mathlib não
tem TIPO de espaço de Sobolev" — e essa lacuna fechou **nesta mesma
sessão**, via `FOUND-SOBOLEV-SPACE-001` (`Hs E F s`, construído como
espaço de Banach). A cadeia está corroborada de forma independente em
três `STATUS.yaml` distintos (`FOUND-LERAY-PROJECTOR-001`,
`FOUND-SOBOLEV-SPACE-001`, e o desta frente), não apenas afirmada aqui.

**Correção pós-revisão adversarial**: `RH_NOGO_REACTIVATION_CRITERIA.md`
está escopado explicitamente a `work_item_id: RH-NOGO-001` e não rege
literalmente esta trilha — citá-lo abaixo é analógico, pelo princípio
geral que ele registra (um gate decidir sozinho que "agora vale a pena"
não basta), não como regra de controle sobre `FOUND-LERAY-PROJECTOR-001`.
A justificativa real desta frente não depende dessa analogia: repousa
sobre o fato concreto e verificável de que o bloqueador especificamente
nomeado (`FM-GAP-001`) deixou de existir.

## O que a sondagem encontrou antes de escrever qualquer prova nova

`SobolevSpace.lean` já continha, no Step 6 (`fourierMultiplierSobolevCLM`),
exatamente o padrão de construção necessário: um multiplicador de Fourier
com símbolo `L∞` arbitrário, definido em `H^s` por **conjugação** através
da isometria `toL2ₗᵢ : Hs E F s ≃ₗᵢ[ℂ] Lp F 2`, com norma transferida do
lado `L²`. O arquivo até prova esse padrão especificamente para o
componente escalar do símbolo de Leray (`fourierMultiplierSobolevCLM_leray`).
O que faltava era aplicar o mesmo padrão ao operador **matricial já
montado** (`lerayOpL2`, que soma `n²` multiplicadores escalares numa
base ortonormal) — não inventar uma construção nova.

## O que foi provado

`TamesisLab/Foundations/LerayProjectorSobolev.lean` (12 declarações: 1
`def` + 11 `theorem`), compilado (`lake env lean` e `lake build`
completo, ambos `exit 0`, `#print axioms` em todas as 12 declarações
confirma `[propext, Classical.choice, Quot.sound]`, sem `sorryAx` —
independentemente reproduzido pela revisão adversarial, que rodou o
build de novo em vez de confiar nesta afirmação):

```text
lerayOpHs                       operador em H^s, por conjugacao com lerayOpL2
toL2_lerayOpHs                   a acao no representante L^2 e exatamente lerayOpL2
lerayOpHs_idem                   idempotente, transferido (nao reprovado do zero)
norm_lerayOpHs_apply             norma pontual = norma do representante L^2
norm_lerayOpHs_le                cota <= norma de lerayOpL2 (uma direcao)
norm_lerayOpL2_le_norm_lerayOpHs  cota na direcao oposta
norm_lerayOpHs_eq                norma EXATA (nao so cota) igual a norma em L^2
norm_lerayOpHs_le_one            ‖P‖ <= 1
lerayOpHs_ne_zero                nao-nulo para n >= 2
norm_lerayOpHs_eq_one            ‖P‖ = 1 (para n >= 2)
lerayOpHs_package                pacote fechado das propriedades acima
concrete_lerayOpHs_R3            instancia concreta, sem hipoteses livres, em R^3, s=5/2
```

## O que esta frente explicitamente NÃO afirma

```text
que o operador em H^s seja auto-adjunto
que o operador em H^s seja projecao ortogonal
que Hs E F s tenha estrutura de produto interno
que Navier-Stokes tenha ficado alcancavel
```

`Hs E F s` em `SobolevSpace.lean` carrega `NormedSpace`/`CompleteSpace`,
não um produto interno — então `ContinuousLinearMap.adjoint` nem sequer
é enunciável sobre ele hoje. Transportar o produto interno de `L²`
através de `toL2ₗᵢ` tornaria isso enunciável; esse transporte **não foi
feito aqui** e fica registrado como `LP-GAP-005`, aberto de propósito —
o mesmo padrão de corte deliberado usado em `SC-GAP-002`.

## Erro de execução encontrado e corrigido antes deste registro

Duas provas do rascunho inicial falharam ao compilar de primeira
(`lerayOpHs_idem`: excesso de `rw` idênticos além do necessário;
`norm_lerayOpL2_le_norm_lerayOpHs`: parênteses ausentes fazendo `toL2`
aplicar-se ao equivalente linear em vez de ao seu resultado — erro de
sintaxe, não de matemática). Corrigidas nesta mesma sessão antes de
qualquer registro de sucesso; a saída de `lake env lean` foi lida sem
truncar, e o código de saída real do processo `lean` foi conferido
separadamente do `head`/`tail` usado para exibir o log — não do `head`
que trunca a saída, o mesmo defeito de classe já corrigido em
`LAB-CORR-VALIDATION-BLINDNESS-001`.

## Revisão adversarial (agente independente)

**Veredito: `APPROVED_WITH_NOTES`.** O revisor rodou `lake env lean` de
novo por conta própria (não confiou na alegação de `exit 0`), leu os
quatro arquivos Lean envolvidos por inteiro, e checou especificamente:
não-vacuidade da conjugação, não-circularidade da prova de igualdade de
norma nas duas direções, uso correto de `toL2_surjective` em
`lerayOpHs_ne_zero`, não-vacuidade de `concrete_lerayOpHs_R3` (confirmou
que `OrthonormalBasis (Fin 3) ℝ (EuclideanSpace ℝ (Fin 3))` tem
habitante real, `TamesisProbe.b3`), ausência de auto-adjunção/projeção
ortogonal disfarçada, ausência de `sorry`/`admit`/`axiom`/escape hatches,
e a cadeia de dependência de gaps corroborada por três `STATUS.yaml`
independentes. Dois achados, ambos corrigidos nesta integração:
contagem de declarações (9 → 12, corrigido acima) e o escopo de
`RH_NOGO_REACTIVATION_CRITERIA.md` (corrigido acima). Nenhum problema de
corretude matemática ou lógica encontrado.

## Fechamento

`FOUND-LERAY-PROJECTOR-SOBOLEV-001` fecha `VERIFIED` / `result_review:
APPROVED_WITH_NOTES`. `LP-GAP-004` fecha. `LP-GAP-005` (auto-adjunção em
`H^s`, requer transportar o produto interno) abre, de propósito, não
tentado nesta frente. `authorized_action` do laboratório volta a
`PORTFOLIO_REVIEW_REQUIRED` — nenhuma frente nova pode abrir sem um novo
gate de revisão de portfólio.
