---
session_id: 2026-08-09_0828_FOUND-LERAY-PROJECTOR-SOBOLEV-001
date: 2026-08-09
gates_run:
  - PORTFOLIO-REVIEW-LERAY-SOBOLEV-2026-08-09
  - FORMALIZATION (self-specified)
  - RESULT-REVIEW (adversarial, independent agent)
---

# Sessão: LP-GAP-004 fecha — o projetor de Leray em H^s

## Contexto

A sessão anterior concluiu, corretamente, que a fila de pesquisa estava
esgotada (`PORTFOLIO_REVIEW_QUEUE_EXHAUSTED_2026_08_09.md`). O usuário
pediu para continuar. Em vez de forçar uma frente nova sem motivo, ou
atacar um problema de pesquisa genuinamente aberto (risco de produzir
matemática não confiável sem laço de revisão humana), esta sessão
verificou se algum gap já registrado tinha deixado de estar bloqueado.

## O que foi encontrado

`LP-GAP-004` ("versão H^s matricial [do projetor de Leray], bloqueada
por FM-GAP-001") — e `FM-GAP-001` ("Mathlib não tem TIPO de espaço de
Sobolev") tinha fechado nesta mesma sessão de trabalho, via
`FOUND-SOBOLEV-SPACE-001`. Confirmado por três `STATUS.yaml`
independentes, não apenas pela narrativa.

## O que foi feito

1. Leitura de `SobolevSpace.lean`, `LerayProjector.lean`,
   `LerayOrthogonal.lean` por inteiro. Achado: o padrão de construção
   necessário (conjugação por isometria linear, `Hs E F s ≃ₗᵢ[ℂ] Lp F 2`)
   já estava demonstrado no arquivo para um multiplicador escalar —
   inclusive especificamente para o componente escalar do símbolo de
   Leray. Não era preciso inventar técnica nova.
2. Escrito `TamesisLab/Foundations/LerayProjectorSobolev.lean` (12
   declarações): `lerayOpHs` por conjugação, com limitação, idempotência
   e norma exatamente 1 (n≥2, não nulo) transferidas — não reprovadas do
   zero — do resultado já verificado em L².
3. Dois erros de sintaxe (não de matemática) no rascunho inicial,
   corrigidos: excesso de `rw` idênticos; parênteses ausentes fazendo
   `toL2` aplicar-se ao equivalente linear em vez de ao seu resultado.
4. **Quase-incidente**: um `head`/`tail` no meio de um pipe mascarava o
   código de saída real do processo `lean` — o mesmo defeito de classe
   de `LAB-CORR-VALIDATION-BLINDNESS-001`. Capturado antes de qualquer
   registro de sucesso; a partir daí, todo `lake env lean` desta sessão
   teve o exit code conferido separadamente, sem pipe.
5. Registrado em `TamesisLab/Foundations.lean`; `lake build` completo do
   projeto: 8820 jobs, exit 0.
6. Revisão adversarial independente (agente que rodou `lake env lean` de
   novo por conta própria): `APPROVED_WITH_NOTES`. Zero problemas de
   corretude matemática ou lógica. Dois nits cosméticos corrigidos:
   contagem de declarações (9→12) e escopo da citação de
   `RH_NOGO_REACTIVATION_CRITERIA.md` (é sobre RH-NOGO-001, citada aqui
   só analogicamente).

## O que NÃO foi afirmado

```text
que o operador em H^s e auto-adjunto
que o operador em H^s e projecao ortogonal
que Hs E F s tem produto interno
que Navier-Stokes ficou alcancavel
```

`LP-GAP-005` (auto-adjunção/projeção ortogonal em H^s, requer
transportar o produto interno de L² através de `toL2ₗᵢ`) abre de
propósito, não tentado.

## Novidade

```yaml
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_FOUNDATION
```

## Fechamento

`work_status: VERIFIED`, `result_review: APPROVED_WITH_NOTES`.
`authorized_action` volta a `PORTFOLIO_REVIEW_REQUIRED`.

## Próxima ação

Nenhuma execução autônoma adicional está autorizada sem um novo gate de
revisão de portfólio.
