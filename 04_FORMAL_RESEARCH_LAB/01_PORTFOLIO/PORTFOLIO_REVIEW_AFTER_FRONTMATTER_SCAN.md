---
document_id: PORTFOLIO-REVIEW-AFTER-FRONTMATTER-SCAN
reviewed_at: 2026-08-03
selected_work_item: FOUND-BISIMULATION-BOUNDARY-001
alternatives_compared: 5
---

# Revisão de portfólio — depois da correção do scanner

## Estado de entrada

```text
FOUND-FINITE-STATE-ABSTRACTION-001   VERIFIED / APPROVED   ENCERRADA
LAB-GOV-FRONTMATTER-SCAN-001         VERIFIED
varredura de duplicatas              392 arquivos, 335 front matter
claims no ledger                     23
```

O instrumento de validação foi conferido no gate anterior. Só agora faz
sentido abrir frente matemática nova.

## As cinco alternativas

| | Candidato | Veredito |
|---|---|---|
| A | Bissimulação determinística, `ABS-GAP-015` | **SELECIONADO** |
| B | Quocientes, `ABS-GAP-016` | adiado |
| C | Invariância do witness sob recodificação, `ENC-GAP-020` | rejeitado |
| D | Extração nativa, CLI, parser | rejeitado |
| E | Frente matemática independente | adiado |

## Por que A

`ABS-GAP-015` foi deixado aberto pela frente anterior com uma suspeita
explícita: bissimulação seria mais forte que semiconjugação e talvez
refletisse ciclos.

O probe deste gate respondeu, e a resposta é mais nítida do que a
pergunta esperava.

### O colapso, compilado sem axiomas

```lean
theorem bisimulation_iff_semiconj (abstract) (stepC) (stepA) :
    Bisimulation abstract stepC stepA
      ↔ Function.Semiconj abstract stepC stepA
```

Em sistemas determinísticos **totais**, o zag é gratuito: dado `c`, a
testemunha do passo concreto é `stepC c`, e a obrigação que sobra é
exatamente o zig. Bissimulação funcional não é uma condição mais forte;
é a mesma condição.

### A consequência

`BOOL_TO_UNIT` — o contraexemplo já formalizado — **é** uma
bissimulação, e `forgetBool` é **sobrejetiva**. Portanto:

```text
bissimulacao                  NAO reflete ciclos
bissimulacao sobrejetiva      NAO reflete ciclos
```

Ambos como teoremas que compilam, ambos sem pegada axiomática.

### Por que isso importa

O laboratório já proibia "assumir bissimulação onde só há
semiconjugação". A proibição deixava implícito que **obter** bissimulação
resolveria o problema. No recorte determinístico total, não há nada a
obter — e o ciclo continua espúrio.

O que separa não é bissimulação: é injetividade sobre a órbita.

## Por que não B, C, D, E

- **B** — quocientes exigem `Setoid`, `Quotient` e uma teoria de
  representantes; custo alto para um ganho que a frente A já esclarece
  em parte. Continua `NOT_AUTHORIZED`.
- **C** — `ENC-GAP-020` segue com o acoplamento à ordem de enumeração do
  detector que o reprovou duas vezes.
- **D** — extração, CLI e parser distribuem garantia sem contrato
  semântico.
- **E** — abrir frente sem conexão com a cadeia existente perderia a
  reutilização integral que torna A barata.

## Custo de A

```text
3 definicoes
5 teoremas
0 fontes primarias
0 dependencias novas
probe descartavel, exit 0, 5 declaracoes sem pegada
```

## A fronteira que a frente precisa preservar

```text
O colapso vale para bissimulacao FUNCIONAL entre sistemas
DETERMINISTICOS TOTAIS.

Fora desse recorte — sistemas nao deterministicos, relacoes de
transicao gerais, bissimulacao relacional R ⊆ C × A, acoes
rotuladas — zig e zag NAO colapsam, e nada aqui se aplica.
```

Generalizar o colapso além desse recorte é a stop condition principal da
frente.

## Escopo negativo

```text
sistemas nao deterministicos     NOT_AUTHORIZED
bissimulacao relacional          NOT_AUTHORIZED
acoes rotuladas                  NOT_AUTHORIZED
coinducao                        NOT_AUTHORIZED
quocientes                       NOT_AUTHORIZED
extracao, CLI, parser            NOT_AUTHORIZED
alteracao de frente encerrada    PROIBIDA
```
