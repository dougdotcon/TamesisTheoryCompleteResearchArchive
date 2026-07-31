---
session_id: 2026-08-01-PORTFOLIO-REVIEW-AFTER-RUNTIME-ADAPTER
date: 2026-08-01
gate: PORTFOLIO_REVIEW
authorized_action: PORTFOLIO_REVIEW_AUTHORIZED
agent: claude-opus-5
commit_before: 861dc6bf24b4e1f8da88af138554556e644a3b49
decision: A_PORTFOLIO_REVIEW_APPROVED_CERTIFIED_STATE_ENCODING_SELECTED
selected_work_item: ENG-FINITE-STATE-ENCODING-001
lean_files_created: 0
---

# Sessão — revisão de portfólio após o adaptador de runtime

## Preflight

```text
HEAD                  861dc6bf24b4e1f8da88af138554556e644a3b49
historico             confere com os seis commits esperados
arvore                limpa
processos             nenhum
cat-file -e           0
merge-base ancestor   0
canonical_commit      746102f -> 861dc6b
```

## A pergunta do gate

Não *qual funcionalidade falta*, e sim *qual lacuna falta*.

```text
A tabela eh analisada corretamente,
mas nada prova que ela representa o sistema que a originou.
```

A entrada do adaptador é um `Array Nat` **anônimo**. Um erro de
codificação — dois estados no mesmo índice, uma transição no destino
errado — produz uma tabela válida, um certificado correto e uma conclusão
**falsa** sobre o sistema real. Extração, CLI e JSON distribuem essa
lacuna; não a fecham.

## Seis alternativas, uma escolhida

```text
A  codificacao certificada    SELECIONADA
B  extracao nativa            depende de um consumidor que nao existe
C  CLI e formato externo      depende de B, e amplifica a lacuna
D  diagnostico detalhado      barato, seguro, e nao muda nada
E  abstracao e simulacao      a resposta completa, e a mais perigosa agora
F  nova frente matematica     sem produto verificavel em 30 dias
```

O argumento decisivo entre `A` e `E`:

```text
com bijecao, a correspondencia eh EXATA e nao ha ciclos espurios;
com simulacao, ciclo abstrato NAO implica ciclo concreto.
```

Um laboratório que prioriza resultados parciais verdadeiros começa pelo
caso exato. E, com `A` pronta, `E` ganha o ponto de comparação que hoje
lhe falta.

## Auditoria de API — dois probes, ambos removidos

O achado que **encurta** o plano:

```lean
Function.Semiconj.iterate_right :
  Semiconj f ga gb → ∀ n, Semiconj f ga^[n] gb^[n]
```

Axiomas `[propext]`. `Semiconj encode stepS tableStep` é exatamente a
comutação de um passo; a comutação de iteradas vira `.iterate_right n`.
A condição 8 da regra de decisão passa por um caminho mais curto do que a
proposta previa.

O achado que **restringe** o plano:

```text
Fintype.equivFin eh noncomputable.
```

Logo a codificação não pode ser derivada de `[Fintype S]`. Ela tem de ser
**recebida** como campo. Isso virou `STOP-ENC-006` e é a razão de a
estrutura candidata ter quatro campos.

E a base da construção está sólida:

```text
Array.ofFn                 [propext],  #eval -> #[1, 2, 3]
Array.size_ofFn            [propext]
Array.getElem_ofFn         enunciado sobre (ofFn f).size
```

## O risco que vai custar tempo

```text
Array.ofFn f tem size igual a n por TEOREMA, nao por definicao.
```

`Fin table.next.size` e `Fin n` não são o mesmo tipo sintaticamente.
`ENC-GAP-004`, e `STOP-ENC-005` se a correspondência exigir `cast` não
controlado. Há precedente favorável: a frente anterior eliminou
transporte dependente inteiro escolhendo a tabela concreta cujo campo era
sintaticamente igual. Mesma técnica, decisão do gate de especificação.

## Dez de dez

As dez condições da regra de decisão foram verificadas uma a uma, três
delas por medição no checkout. Nenhuma falhou. Nenhuma stop condition
material disparada.

## A fronteira que não pode ser apagada

```text
Uma codificacao certificada prova correspondencia entre um sistema
TIPADO e sua tabela.

Ela NAO prova que um sistema fisico, servico, workflow ou programa
real foi modelado corretamente.
```

`RT-GAP-017` será fechado **apenas** no recorte em que o sistema já é um
objeto Lean tipado. No caso geral, permanece aberto — e provavelmente
permanecerá.

```yaml
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_SOFTWARE_BRIDGE
```

Codificar um tipo finito como `Fin n` é rotina desde os anos 1950.

## Estado final

```text
active_work_item     ENG-FINITE-STATE-ENCODING-001
work_status          SCOPED
current_blocker      null
authorized_action    ENG_FINITE_STATE_ENCODING_001_SPECIFICATION_PREPARATION_AUTHORIZED
allowlist            uma entrada literal, sem wildcard
gaps                 16, nenhum fechado
stop conditions      14
arquivos Lean        0
provas               0
lake build           NAO executado
```

## Próxima ação única

Preparar a especificação da codificação certificada. Nada de
formalização, extração, CLI, parser ou integração.
