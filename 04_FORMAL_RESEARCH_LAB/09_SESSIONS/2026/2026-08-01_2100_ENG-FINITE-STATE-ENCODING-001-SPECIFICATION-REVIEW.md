---
session_id: 2026-08-01-ENG-FINITE-STATE-ENCODING-001-SPECIFICATION-REVIEW
date: 2026-08-01
gate: ENG_FINITE_STATE_ENCODING_001_SPECIFICATION_REVIEW
authorized_action: ENG_FINITE_STATE_ENCODING_001_SPECIFICATION_REVIEW_AUTHORIZED
agent: claude-opus-5
commit_before: 2066edc165ace0fbf4e183303e30c4ced246aaaa
decision: A_ENG_FINITE_STATE_ENCODING_001_SPECIFICATION_REVIEW_APPROVED
lean_files_created: 0
---

# Sessão — revisão da especificação da codificação certificada

## Preflight

```text
HEAD                  2066edc165ace0fbf4e183303e30c4ced246aaaa
historico             confere com os seis commits esperados
arvore                limpa
processos             nenhum
cat-file -e           0
merge-base ancestor   0
canonical_commit      4c15d4a -> 2066edc
```

## Pergunta 1 — `encode_decode` é necessário?

Respondida **por construção**, não por leitura. O probe contém uma
estrutura `WeakEncoding` com apenas `decode_encode`, e nela foram
reprovados `encodedStep`, a tabela, o tamanho, a leitura, o índice, a
preservação do valor, a semiconjugação, a correspondência de `run?`, a
análise e a **soundness tipada**.

```text
tudo compilou.
```

Logo `encode_decode` **não é dependência de prova de nenhum resultado
CORE**. E ainda assim fica, porque é a única coisa que separa dois
contratos:

```text
com as duas leis:  n eh a cardinalidade de S; todo indice eh um estado
                   real; a tabela representa exatamente o sistema.

com uma lei so:    n eh um limite superior; a tabela pode conter linhas
                   que nao correspondem a estado nenhum.
```

A frente promete o primeiro. Enfraquecer para `LeftInverse` seria trocar
o contrato sem dizer — e o gate é explícito: isso seria outra frente.

## Pergunta 2 — `encodedStep` é público?

**Sim, mas por um motivo novo.**

A especificação justificava a exposição dizendo que ele aparece no
enunciado de `buildTransitionTable_getElem`, que era público. Esta
revisão tornou aquele auxiliar **interno**, e o argumento caiu junto.

O que sobrou é suficiente: com o auxiliar interno, `encodedStep` é o
**único nome público capaz de descrever o conteúdo da tabela**. Sem ele,
nada na API diz o que `next[i]` contém. E ele não depende de axioma
nenhum.

## Pergunta 3 — a pegada axiomática é aceitável?

**Sim**, e a medição foi mais informativa do que a especificação supunha.

```text
encode_injective     does not depend on any axioms
encode_surjective    does not depend on any axioms
encodedStep          does not depend on any axioms
```

A especificação relatava pegada uniforme. **Estava errado.** A primeira
declaração a carregar os três axiomas é `buildTransitionTable`, pelo
campo `closed`, via `Array.getElem_ofFn`.

A rota leve foi tentada:

```lean
theorem sizeB1 (f : Fin n → Nat) : (Array.ofFn f).size = n := rfl
```

```text
error: Not a definitional equality:
  (Array.ofFn f).size is not definitionally equal to n
```

Com tamanho **literal**, passa. Com `n` genérico, não. `Array.ofFn` é um
laço, e a API é polimórfica em `n`. Não é preferência de estilo: é
impossibilidade medida.

E o argumento que encerra a discussão:

```text
analyzeTransitionTable            [propext, Classical.choice, Quot.sound]
analyzeTransitionTable_sound      [propext, Classical.choice, Quot.sound]
analyzeTransitionTable_complete   [propext, Classical.choice, Quot.sound]
```

A definição reutilizada **já carrega os três**. Uma prova de `closed`
mais leve não mudaria nada a jusante.

## A correção que mais muda o código

A especificação provava `table_step_commutes` e derivava a
semiconjugação como `.symm`. A revisão **inverteu**: a semiconjugação é
provada diretamente, e a comutação é o corolário.

Motivo: a forma que Mathlib consome é a semiconjugação, e inverter a cada
uso era ruído. O probe confirmou que a prova direta tem exatamente o
mesmo tamanho — seis linhas.

## O limite novo

```text
codificacao identidade   tabela #[1, 2, 3, 2]
codificacao i ↦ 3 - i    tabela #[1, 0, 1, 2]
witness nos dois casos   ⟨2, 2⟩
```

A coincidência dos witnesses é **observação**, não teorema. Provar
invariância exigiria provar que a ordem de busca do detector não importa,
o que não é resultado desta frente. Registrado como `ENC-GAP-020` e
`STOP-ENC-019`.

O que **é** preservado por qualquer codificação correta é a validade
semântica do witness no sistema tipado — e isso é a própria soundness.

## Evidência

```text
probe principal   exit 0, 33 s, zero erros, zero tokens proibidos
probe de axiomas  exit 1 por desenho, contendo as tentativas da rota leve
probes removidos  sim
lake build        NAO executado
```

## Estado final

```text
work_status              READY
specification_status     APPROVED
specification_review     APPROVED
formalization_status     NOT_STARTED
authorized_action        ENG_FINITE_STATE_ENCODING_001_FORMALIZATION_AUTHORIZED
declaracoes publicas     14  (eram 16)
auxiliares internos      1
documentos               39
lacunas                  20
stop conditions          19, zero disparadas
arquivos Lean            0
claims                   21, nenhuma promovida
```

## Próxima ação única

Formalizar. Uma única tabela pública, dois pontos controlados de
transporte, zero escolha clássica produzindo dado executável.
