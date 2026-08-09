---
session_id: 2026-08-09_FOUND-CZ-MEAN-ZERO-001
date: 2026-08-09
gates_run:
  - RESEARCH (Fourier-multiplier route, no code edits)
  - PORTFOLIO-REVIEW-CZ-MEAN-ZERO-2026-08-09
  - FORMALIZATION (background agent, resumed once after a stall)
  - RESULT-REVIEW (adversarial, independente, escrutínio reforçado)
---

# Sessão: FOUND-CZ-MEAN-ZERO-001 — fechamento do campo mean_zero

## Contexto

Continuação direta de `09_SESSIONS/2026/2026-08-09_FOUND-CZ-KERNEL-DEFINITIONS-001.md`.
Antes de tocar qualquer código, uma pesquisa dedicada (sem edição,
citações verificadas por leitura direta de PDF — Grafakos, *Classical
Fourier Analysis*, 3ª ed., 2014) investigou se a rota de multiplicador
de Fourier (via `FOUND-FOURIER-MULTIPLIER-L2-001`, já formalizado) podia
ser honestamente conectada ao mecanismo de Constantin-Fefferman.
Resposta honesta: não, não sem construir teoria de integral singular
ausente do Mathlib — mas a pesquisa descobriu, como subproduto, que o
campo `mean_zero` de `CZKernelClass` (deixado em aberto pela frente
anterior) é um fato elementar, não o cálculo difícil que se supunha.
Apresentado ao usuário via `AskUserQuestion` com as ressalvas completas;
usuário escolheu formalizar.

## O que foi feito

1. `PORTFOLIO_REVIEW_CZ_MEAN_ZERO_2026_08_09.md` + `DEC-080`: terceira
   extensão nomeada da exceção de `DEC-076` (via `DEC-078`).
2. Agente em segundo plano formalizou a extensão. Travou uma vez
   esperando uma checagem em segundo plano não lida — retomado via
   `SendMessage` com instrução explícita de rodar verificações no
   primeiro plano.
3. Resultado: não apenas fechou `mean_zero` para o `K` concreto, mas
   provou isotropia de `sphereSurfaceMeasure` sob **todo**
   `LinearIsometryEquiv` de `E` (mais forte que o subgrupo finito
   sugerido como alternativa tratável), produzindo
   `czKernelClass_sphereSurfaceMeasure_K` — o primeiro termo COMPLETO de
   `CZKernelClass` no laboratório (384→865 linhas).
4. Verificação independente própria (exit codes diretos, primeiro
   plano): `lake env lean` e `lake build` completo, ambos `exit 0`
   (8825 jobs), zero tokens proibidos, log de 66 linhas lido por inteiro
   (zero `sorryAx` em 38 declarações).
5. Revisão adversarial com escrutínio reforçado (terceira frente ligada
   diretamente a `NS-GAP-001`, a mais sofisticada matematicamente):
   **APPROVED**, sem ressalvas. Recompilou de forma independente no
   primeiro plano, leu o conteúdo matemático completo (não só as
   assinaturas), verificou cada citação Mathlib contra o código-fonte,
   auditou toda a prosa contra overclaiming.
6. `NS-GAP-001` em `GAP_REGISTER.yaml` anotado com cross-referência.

## O que NÃO foi afirmado

```text
que qualquer limitação L² ou L^p de operador foi provada
que qualquer teorema de Calderón-Zygmund foi formalizado
que a integral p.v. real das eq. 2.1/2.2 foi estimada (operador
  não-linear/não-convolução, fundamentalmente diferente do núcleo aqui
  fechado)
que NS-GAP-001/004 foi resolvido, aproximado, ou tem caminho de prova
que Navier-Stokes ficou alcançável
```

## Novidade

```yaml
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_FOUNDATION
```

## Fechamento

`work_status: VERIFIED`, `result_review: APPROVED`. `authorized_action`
volta a `PORTFOLIO_REVIEW_REQUIRED`. `NS-GAP-001` permanece `OPEN`.

## Próxima ação

A camada definicional de Calderón-Zygmund está completa para o núcleo de
coeficiente congelado. O próximo passo genuíno de análise harmônica —
limitação L²/L^p do operador real, ou a integral p.v. das eq. 2.1/2.2
aplicada a um campo de vorticidade genuíno — exige teoria de integral
singular (derivar um multiplicador de Fourier a partir de um núcleo
espacial p.v., ou uma teoria completa de decomposição/tipo-fraco) que
este laboratório ainda não tem, e a pesquisa já conduzida mostrou que
não é alcançável a partir da infraestrutura atual sem construir essa
teoria substancialmente do zero. Nenhuma execução autônoma adicional é
autorizada sem um novo gate de revisão de portfólio.
