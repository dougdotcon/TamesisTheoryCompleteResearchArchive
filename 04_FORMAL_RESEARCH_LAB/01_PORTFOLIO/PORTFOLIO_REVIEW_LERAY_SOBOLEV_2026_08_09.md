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
espaço de Banach). Isso não é um gate autônomo decidindo por conta
própria que "agora vale a pena" — proibido explicitamente por
`RH_NOGO_REACTIVATION_CRITERIA.md` — é o reconhecimento de que o
bloqueador especificamente nomeado no registro deixou de existir.

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

`TamesisLab/Foundations/LerayProjectorSobolev.lean`, compilado
(`lake env lean` e `lake build` completo, ambos `exit 0`, `#print axioms`
em todas as 9 declarações confirma `[propext, Classical.choice,
Quot.sound]`, sem `sorryAx`):

```text
lerayOpHs                operador em H^s, por conjugacao com lerayOpL2
toL2_lerayOpHs            a acao no representante L^2 e exatamente lerayOpL2
lerayOpHs_idem            idempotente, transferido (nao reprovado do zero)
norm_lerayOpHs_eq         norma EXATA (nao so cota) igual a norma em L^2
norm_lerayOpHs_le_one     ‖P‖ <= 1
lerayOpHs_ne_zero         nao-nulo para n >= 2
norm_lerayOpHs_eq_one     ‖P‖ = 1 (para n >= 2)
lerayOpHs_package         pacote fechado das quatro propriedades acima
concrete_lerayOpHs_R3     instancia concreta, sem hipoteses livres, em R^3, s=5/2
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

## Trava

`authorized_action` para esta frente: `RESULT_REVIEW_REQUIRED` — revisão
adversarial independente pendente antes de `VERIFIED` ser afirmado como
fechamento final do ciclo.
