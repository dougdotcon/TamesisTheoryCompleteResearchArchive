---
document_id: FOUND-BISIMULATION-BOUNDARY-001-SCOPE-BOUNDARY
work_item_id: FOUND-BISIMULATION-BOUNDARY-001
criticality: HIGHEST
---

# Fronteira de escopo — onde o colapso NÃO vale

Este é o documento mais importante da frente. O resultado é um
**colapso**, e colapsos convidam à generalização indevida.

## Onde o colapso vale

```text
sistemas       deterministicos e TOTAIS      stepC : C → C, stepA : A → A
bissimulacao   FUNCIONAL                     dada pelo grafico de abstract : C → A
transicoes     sem rotulos, sem acoes
```

Nessas três condições, e **somente** nelas.

## De onde vem o colapso

```text
zag:  ∀ c, ∃ c', stepC c = c' ∧ abstract c' = stepA (abstract c)
```

Como `stepC` é **função total**, o `c'` está determinado: só pode ser
`stepC c`. A quantificação existencial não oferece escolha nenhuma, e a
obrigação restante é o zig.

**É a ausência de escolha que produz o colapso.** Qualquer relaxamento
que devolva escolha destrói o argumento.

## Onde o colapso NÃO vale, e por quê

### Sistemas não determinísticos

```text
stepC : C → Set C
```

O zag passa a exigir a existência de **algum** sucessor concreto com a
observação certa. Existe escolha, e o zag deixa de ser consequência do
zig. `NOT_AUTHORIZED`.

### Relações de transição gerais

```text
→C ⊆ C × C
```

Mesmo problema, na forma mais geral. `NOT_AUTHORIZED`.

### Bissimulação relacional

```text
R ⊆ C × A,  em vez do grafico de uma funcao
```

Um estado concreto pode se relacionar com vários abstratos. O argumento
da testemunha obrigatória não se aplica. `NOT_AUTHORIZED`.

### Sistemas com rótulos ou ações

```text
stepC : Label → C → C
```

O zag passa a quantificar sobre rótulos. `NOT_AUTHORIZED`.

### Funções parciais

```text
stepC : C → Option C
```

O zag pode falhar por indefinição, e não por observação. `NOT_AUTHORIZED`.

### Coindução

Nada nesta frente é coindutivo. `Bisimulation` é definido diretamente
como uma conjunção de duas proposições quantificadas, não como o maior
ponto fixo de um funtor. `NOT_AUTHORIZED`.

## A afirmação proibida mais provável

```text
PROIBIDO: "bissimulacao e o mesmo que semiconjugacao"
```

Sem o qualificador, isso é **falso** — e é falso exatamente na teoria de
concorrência onde a palavra "bissimulação" nasceu, que é não
determinística e rotulada. A forma correta é sempre:

```text
Para sistemas deterministicos totais, a bissimulacao FUNCIONAL
coincide com a semiconjugacao.
```

## A segunda afirmação proibida

```text
PROIBIDO: "bissimulacao e inutil"
```

O resultado é que ela não acrescenta **neste recorte**. Em sistemas não
determinísticos ela acrescenta muito. A frente não diz nada sobre isso.

## Stop condition principal

```text
STOP-BIS-001  o colapso e enunciado ou usado fora do recorte
              deterministico total e funcional
```
