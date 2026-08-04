---
document_id: PORTFOLIO-REVIEW-MONOVARIANT
reviewed_at: 2026-08-04
selected_work_item: FOUND-MONOVARIANT-DESCENT-001
alternatives_compared: 4
selection_criterion: TRANSFERABILITY
probes_compiled_in_this_gate: 10
probe_exit: 0
---

# Revisão de portfólio — a segunda metade do par clássico

## O critério continua sendo transferência

A frente anterior deu ao laboratório a peça que prova que algo **não
muda**. Falta a que prova que algo **decresce**.

```text
invariante    quantidade conservada    prova IMPOSSIBILIDADE
monovariante  quantidade decrescente   prova TERMINACAO
```

Juntas são o par com que se ataca sistema dinâmico discreto. Ter uma sem
a outra é ter meia ferramenta.

## As quatro alternativas

| | Candidato | Veredito |
|---|---|---|
| A | **Monovariantes e descida bem-fundada**, `INV-GAP-003` | **SELECIONADO** |
| B | Finitude da órbita concreta, `ABS-GAP-021` | adiado |
| C | Invariantes relacionais, `INV-GAP-002` | adiado |
| D | Quocientes, `ABS-GAP-016` | adiado |

## O negativo, já compilado, e é mais forte que o de ontem

```lean
theorem monovariant_not_orbitSeparating
    (hmono : Monovariant measure stepC)
    (h : analyzeAbstractSystem abstraction encoding start = .ok witness) :
    ¬ OrbitSeparating abstraction.abstract stepC start
```

Compare com o resultado da frente anterior:

```text
invariante     OrbitSeparating vale EXATAMENTE nos pontos fixos
monovariante   OrbitSeparating NAO VALE EM LUGAR NENHUM
```

A razão é direta: um monovariante exclui recorrência concreta em qualquer
número positivo de passos, enquanto a análise abstrata **sempre** devolve
um ciclo com período positivo. Logo **todo ciclo abstrato de um sistema
monovariante é espúrio**, sem exceção.

## A lacuna de API que a frente fecha de passagem

`detectCycle?_sound` prova `0 < period`, mas
`analyzeTransitionTable_sound` devolve apenas três cláusulas e **a
positividade se perde** antes de chegar ao consumidor.

O probe recupera as duas, re-derivando a redução em namespace novo com
API exclusivamente pública, **sem tocar em frente encerrada**:

```text
analyzeTransitionTable_period_pos     0 < period, recuperado
analyzeAbstractSystem_period_pos      idem, no nivel da abstracao
```

É o que torna o negativo **livre de hipótese inventada**.

## Evidência deste gate

```text
probe descartavel      exit 0, 0 erros, arvore intocada
Monovariant.iterate_lt              propext, Quot.sound
Monovariant.no_periodic_point       propext, Quot.sound
analyzeAbstractSystem_period_pos    propext, Classical.choice, Quot.sound
monovariant_not_orbitSeparating     propext, Classical.choice, Quot.sound
```

`Classical.choice` aparece **apenas** no que atravessa
`analyzeEncodedSystem`, que é pegada infraestrutural já aceita e cuja
remoção é explicitamente proibida.

## Os dois registros honestos

O probe inclui **duas negações** que impedem a leitura da ferramenta como
universal:

```text
downStep_not_monovariant     sistema crescente NAO tem monovariante
strictDown_not_monovariant   boa fundacao NAO basta sem decrescimo estrito
```

A segunda importa: `Nat` é bem fundado, e ainda assim `k - 1` **não** é
monovariante, porque falha em zero. Boa fundação do contradomínio não
substitui decrescimento estrito.

## Escopo negativo

```text
ordens gerais e WellFoundedRelation   NAO AUTORIZADOS (medida em Nat)
ordinais                              NAO AUTORIZADOS
terminacao de programas               NAO AUTORIZADA
sistemas nao deterministicos          NAO AUTORIZADOS
monovariante completo ou necessario   NAO AUTORIZADO
qualquer conexao com Clay ou TOE      PROIBIDA
```

**Nenhum problema de milênio é atacado.** A frente constrói a segunda
peça do par.

## Próxima ação

```text
FOUND_MONOVARIANT_DESCENT_001_SPECIFICATION_PREPARATION_AUTHORIZED
```
