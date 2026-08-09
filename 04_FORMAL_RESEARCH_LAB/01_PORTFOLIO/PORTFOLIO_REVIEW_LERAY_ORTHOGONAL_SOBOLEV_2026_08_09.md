---
document_id: PORTFOLIO-REVIEW-LERAY-ORTHOGONAL-SOBOLEV-2026-08-09
reviewed_at: 2026-08-09
selected_work_item: FOUND-LERAY-PROJECTOR-SOBOLEV-ORTHOGONAL-001
closes_gap: LP-GAP-005
---

# Revisão de portfólio — LP-GAP-005, continuação direta da frente anterior

## Por que esta frente

`LP-GAP-005` foi aberto por esta mesma sessão, no gate imediatamente
anterior (`FOUND-LERAY-PROJECTOR-SOBOLEV-001`), como um corte de escopo
deliberado — não uma lacuna descoberta em outro lugar. Fechar um gap que
a própria sessão acabou de abrir, com escopo já delimitado e pequeno, é
uma continuação direta, não uma frente nova inventada.

## A decisão de escopo, e por que ela existe

`Hs E F s` carrega `NormedSpace`/`CompleteSpace`, mas não uma instância
`InnerProductSpace`. O Mathlib tem uma ferramenta genérica de transporte,
`InnerProductSpace.induced`, mas ela exige que a norma **já instalada**
no domínio seja definicionalmente a instância específica
`SeminormedAddCommGroup.induced` construída a partir do **mesmo** mapa
usado para induzir o produto interno. A norma de `Hs` foi instalada em
`SobolevSpace.lean` via `NormedAddCommGroup.induced` usando um
`AddMonoidHom` (`toL2AddHom`), e verificar que isso bate exatamente com
o que `InnerProductSpace.induced` espera — sem introduzir um diamante de
tipo silencioso entre duas instâncias `SeminormedAddCommGroup (Hs E F s)`
definicionalmente iguais mas não sintaticamente idênticas — exigiria
investigação cuidadosa da definição interna de `NormedAddCommGroup.induced`
no Mathlib.

**Decisão**: em vez de arriscar esse diamante, o conteúdo matemático
(auto-adjunção, ortogonalidade do complemento, Pitágoras) é provado
através de um **pareamento pullback explícito**, `hsInner f g := inner
(toL2 f) (toL2 g)` — uma função `ℂ`-valorada comum, não uma instância de
classe de tipo concorrente. Isso é uma afirmação matematicamente fiel de
auto-adjunção (`⟪Tf,g⟫ = ⟪f,Tg⟫` para todo `f g`), só não expressa pela
API `IsSelfAdjoint`/`ContinuousLinearMap.adjoint` do Mathlib, que exigiria
instalar essa instância. Instalar `InnerProductSpace (Hs E F s)`
globalmente **não é feito aqui** e continua como trabalho em aberto, se
algum dia for desejado.

## O que foi provado

`TamesisLab/Foundations/LerayOrthogonalSobolev.lean` (compilado, `lake
env lean` e `lake build` completo do projeto, ambos `exit 0`, 8821 jobs,
`#print axioms` em todas as declarações confirma `[propext,
Classical.choice, Quot.sound]`, sem `sorryAx`):

```text
toL2_sub                           toL2 respeita subtracao (nao dado em SobolevSpace.lean)
hsInner                            pareamento pullback, funcao comum
hsInner_self_eq_normSq             o pareamento representa genuinamente a norma H^s ao quadrado
hsInner_lerayOpHs_symm             auto-adjuncao, transferida de LerayOrthogonal.inner_lerayOpL2_symm
hsInner_self_lerayOpHs             idempotencia + auto-adjuncao combinadas
hsInner_lerayOpHs_sub              ortogonalidade do complemento, transferida
norm_sq_lerayOpHs_pythagoras       Pitagoras em H^s, via transferencia direta de norma
lerayOpHs_orthogonal_package       pacote fechado, combina com o pacote da frente anterior
concrete_lerayOpHs_orthogonal_R3   instancia concreta, sem hipoteses livres, R^3, s=5/2
```

## Erros de sintaxe corrigidos (não de matemática)

Três erros no rascunho inicial: `inner_self_eq_norm_sq` (versão que
retorna a parte real, tipo errado) trocado por `inner_self_eq_norm_sq_to_K`
(retorna o valor em `𝕜`, tipo certo); a armadilha já documentada em
`ORTHOGONAL_CLOSURE.md` — `RCLike.ofReal` não é sintaticamente
`Complex.ofReal`, então `ring` falhava numa igualdade trivial `x = x`
disfarçada por casts diferentes, trocado por `simp`; e `map_sub` não se
aplica diretamente a `toL2` (uma função comum, não um hom empacotado) —
precisou de um lema auxiliar `toL2_sub`, derivado de `toL2ₗ` (a versão
`LinearMap` já empacotada, para a qual `map_sub` é genérico).

## O que esta frente explicitamente NÃO afirma

```text
que Hs E F s tem uma instancia global InnerProductSpace
que ContinuousLinearMap.adjoint (lerayOpHs b s) = lerayOpHs b s (a forma da API Mathlib)
que Navier-Stokes ficou alcancavel
```

## Trava

`authorized_action` para esta frente: `RESULT_REVIEW_REQUIRED` — revisão
adversarial independente pendente antes de fechamento final.
