---
document_id: PORTFOLIO-REVIEW-INVARIANT-TOOLKIT
reviewed_at: 2026-08-04
selected_work_item: FOUND-INVARIANT-UNREACHABILITY-001
alternatives_compared: 5
selection_criterion: TRANSFERABILITY
probes_compiled_in_this_gate: 10
probe_exit: 0
---

# Revisão de portfólio — o critério muda para transferência

## O critério

As revisões anteriores escolheram por **impacto local**: qual resultado
fecha a lacuna mais visível. Esta escolhe por **transferência**: qual
peça se encaixa em tabuleiros que ainda não foram abertos.

Uma frente que só serve à cadeia que a gerou não vale a jogada, ainda que
seu teorema seja mais bonito.

## A lacuna que o critério revela

```text
dez frentes encerradas usam abstracao para COLAPSAR
  semiconjugacao, codificacao, deteccao de ciclo, bissimulacao

ZERO usam abstracao para SEPARAR
```

Separar é o mecanismo de **toda** prova de impossibilidade em
combinatória: paridade, coloração, monovariante, argumento de invariante.
O laboratório não tem nenhuma peça dessas, e a peça é quase gratuita no
frame existente.

```text
um invariante E uma semiconjugacao com stepA = id
```

Isso não é analogia. É igualdade definicional: `Invariant.semiconj` é o
próprio termo `h`, sem conversão.

## As cinco alternativas

| | Candidato | Transferência | Veredito |
|---|---|---|---|
| A | **Invariantes e inalcançabilidade** | **alta** | **SELECIONADO** |
| B | Finitude da órbita concreta, `ABS-GAP-021` | média | adiado |
| C | Quocientes, `ABS-GAP-016` | baixa | adiado |
| D | Invariância sob recodificação, `ENC-GAP-020` | nenhuma | rejeitado |
| E | Extração, CLI, parser | nenhuma | rejeitado |

**B perdeu por pouco.** Seu teorema é mais forte, mas transfere só para
argumentos que já tenham abstração finita certificada em mãos — ou seja,
para dentro da própria cadeia. A vai para fora dela.

## O negativo afiado, já compilado

Esta é a razão de A não ser reescrita de nada:

```lean
theorem invariant_orbitSeparating_iff_fixedPoint
    (h : Invariant abstract stepC) (start : C) :
    OrbitSeparating abstract stepC start ↔ stepC start = start
```

Para uma abstração invariante, a condição de reflexão da frente anterior
vale **exatamente nos pontos fixos**. Portanto:

```text
invariantes certificam IMPOSSIBILIDADE
invariantes NUNCA certificam recorrencia
os dois usos da mesma maquina sao incompativeis fora dos pontos fixos
```

O laboratório passou dez frentes construindo o lado do colapso. Este
teorema mede a distância exata até o outro lado, e a distância não é
zero.

## Evidência deste gate

Probe descartável, `exit 0`, árvore versionada intocada:

```text
Invariant                                def
Invariant.semiconj                       ponte definicional
Invariant.iterate                        [propext]
Reachable                                def
unreachable_of_invariant_ne              [propext]     A FERRAMENTA
Invariant.pair                           composicao
invariantAbstraction                     ponte para a cadeia
invariant_orbitSeparating_iff_fixedPoint [propext, Quot.sound]
diagStep_invariant                       instancia sobre Int x Int
diag_unreachable                         impossibilidade PROVADA
constant_invariant_proves_nothing        o limite honesto
```

`diag_unreachable` roda sobre um sistema concreto **infinito** e prova
que `(1,0)` não é alcançável a partir de `(0,0)` por nenhum número de
passos. Nenhuma finitude é usada em lugar nenhum.

## O limite, declarado antes de começar

```text
a ferramenta e SUFICIENTE, nunca NECESSARIA
```

`constant_invariant_proves_nothing` está no probe exatamente para impedir
a leitura ao contrário. Um invariante que não separa não prova nada, e a
existência de um invariante separador não é consequência da
inalcançabilidade — é o que se precisa exibir.

## Escopo negativo

```text
sistemas nao deterministicos      NAO AUTORIZADOS
monovariantes e boa ordem         NAO AUTORIZADOS  (frente propria)
invariantes completos             NAO AUTORIZADOS
quocientes                        NAO AUTORIZADOS
extracao, CLI, parser             NAO AUTORIZADOS
qualquer conexao com Clay ou TOE  PROIBIDA
alteracao de frente encerrada     PROIBIDA
```

**Nenhum problema de milênio é atacado nesta frente.** A frente constrói
uma peça. Atacar tabuleiro antes de ter peça é como o laboratório
perdeu `RH-NOGO-001` para o congelamento.

## Próxima ação

```text
FOUND_INVARIANT_UNREACHABILITY_001_SPECIFICATION_PREPARATION_AUTHORIZED
```
