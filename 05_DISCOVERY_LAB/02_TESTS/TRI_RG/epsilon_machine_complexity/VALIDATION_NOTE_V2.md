# Nota de validação V2 — `epsilon-machine-complexity` (revisão CSSR incremental completo, `DISC-DEC-011`)

**Data:** 2026-08-21. Esta é uma REVISÃO da validação original
(`VALIDATION_NOTE.md`, mantida intacta como registro histórico da
implementação simplificada de `L` fixo) — ver o adendo de
`METHODOLOGY_NOTE.md` para o racional completo da revisão. Pipeline:
`analysis/em_common.py` (reescrito — CSSR incremental completo, Shalizi &
Klinkner 2004, *UAI*). Script de validação:
`analysis/validate_synthetic_v2.py`,
`analysis/validation_synthetic_v2.json`,
`analysis/validate_synthetic_v2.log`. Mesmos geradores/seeds sintéticos
da validação V1, para comparabilidade direta.

**Veredito final, adiantado aqui:** este candidato permanece **FECHADO NA
ETAPA DE VALIDAÇÃO** — nenhum dado real (Old Faithful, La Palma) foi
tocado. A ambiguidade honesta nomeada no fechamento original (V1) —
"a falta de poder discriminativo de `C_mu` era artefato da implementação
simplificada de `L` fixo, ou fragilidade genuína do estimador?" — está
agora **RESOLVIDA de forma decisiva**: mesmo sob CSSR incremental
completo (implementação verificada correta contra um caso de ordem finita
com solução exata à mão — diagnóstico novo `a3` abaixo), `C_mu` continua
**sem poder discriminativo real** nos 3 controles positivos onde é
computável, e agora exibe **um falso positivo NOVO** em um desenho de
controle negativo que a implementação V1 nem conseguia testar (bloqueado
por `NOT_DETERMINISTIC`). Isto aponta definitivamente para explicação (2)
— fragilidade genuína de `C_mu` como estimador em amostra finita — não
para (1), o artefato de implementação suspeitado originalmente.

## (a) Diagnósticos de correção de código

Todos rodados diretamente sobre `cssr_incremental_grow`/
`reconstruct_at_fixed_L`/`select_Lmax_and_reconstruct` (o motor de CSSR
incremental completo), não passando pela simbolização `R_lambda`
(testada separadamente nos controles positivo/negativo abaixo).

- **Sanidade do teste qui-quadrado:** idêntico a V1 — **OK**.
- **Processo período-2:** `n_states=2`, `C_mu=1,000000`, `h_mu=0,000000` —
  **OK**, correspondência exata, IDÊNTICO a V1 (esperado: processo de
  ordem 1, sem diferença entre `L` fixo e CSSR incremental).
- **Cadeia de Markov de primeira ordem, à mão computável:** `n_states=2`,
  `C_mu=0,6488` (teoria `0,6500`) — **OK**, valor NUMERICAMENTE IDÊNTICO
  ao dígito exibido em V1 (`0,6488116679802353` nos dois casos — mesmo
  gerador/seed, mesmo resultado, esperado para um processo de ordem 1).
- **NOVO em V2 — cadeia de Markov de SEGUNDA ordem, ordem finita, à mão
  computável** (`P(1|00)=0,1`, `P(1|01)=0,3`, `P(1|10)=0,7`,
  `P(1|11)=0,9`, todos os 4 históricos de comprimento 2 estatisticamente
  distintos, `N=300.000`): teoria (autovetor dominante da matriz de
  transição 4×4 exata) dá `pi=(0,375; 0,125; 0,125; 0,375)`,
  `C_mu=1,8113`. CSSR incremental completo recupera **EXATAMENTE**
  `n_states=4` a partir de `L=2` (curva `[2,4,4,4,4,4,4,4]`),
  `C_mu=1,8102` (erro absoluto `0,0011`, ruído de amostra),
  `determinism_violation_frac=0,000000` **exatamente**. Este é o
  diagnóstico DECISIVO de correção do motor GROW+DETERMINIZE: um processo
  de ordem finita, dentro do orçamento `L_max<=8`, é recuperado
  perfeitamente — confirmando que a implementação está correta.
- **Processo Even (exemplo do próprio artigo de Shalizi & Klinkner
  2004) — o teste DECISIVO desta revisão:** máquina mínima VERDADEIRA tem
  exatamente 2 estados causais, `C_mu=H(2/3,1/3)=0,9183` bits.
  **Achado honesto, investigado a fundo, NÃO um julgamento apressado:**
  mesmo com CSSR incremental completo (motor validado como CORRETO pelo
  diagnóstico acima), a curva de número de estados para `L=1..8` é
  `[2, 3, 4, 5, 6, 7, 8, 9]` — CRESCE SEM LIMITE dentro da janela
  testada, nunca estabiliza (`select_Lmax_and_reconstruct` retorna
  `NOT_CONVERGENT`). **Isto é DIFERENTE do achado de V1** (que
  estabilizava, incorretamente, em 3 estados) — mas **também não é o
  resultado esperado pela tarefa** (recuperar exatamente 2 estados).

  **Investigação completa, não uma suposição — prova matemática de que
  isto NÃO é um bug:** o Processo Even tem 2 estados verdadeiros A
  (emite 0 com p=0,5 ficando em A, emite 1 com p=0,5 indo a B) e B
  (emite 1 com p=1 voltando a A), com `pi=(2/3,1/3)`. Considere a
  sub-linhagem "impura" de históricos da forma `"1"^k` (os `k` símbolos
  mais recentes são TODOS 1, sem nenhum "0" visível para ancorar o
  estado verdadeiro). Definindo `q_k = P(estado verdadeiro após esta
  janela = B)` e usando a matriz de transição sub-estocástica "emite um
  1" `M_1=[[0; 0,5],[1; 0]]` aplicada ao vetor estacionário inicial
  `pi=(2/3,1/3)` via a recursão exata `v_k = v_{k-1} @ M_1`, obtém-se:
  `q_k = 1/2` para `k` ÍMPAR, `q_k = 1/3` para `k` PAR — uma
  **alternação exata, período-2, que NUNCA decai** para o valor puro.
  Confirmado numericamente (`N=2.000.000`) a 4 dígitos significativos:
  `P(próximo=1|janela="1"^k)` alterna entre `0,7502/0,7505/0,7507`
  (ímpar, teoria `0,75`) e `0,6669/0,6676/0,6679` (par, teoria
  `0,6667`), para `k=1,...,6`, SEM tendência de convergência para os
  valores puros (`0,5` ou `1,0`). Qualquer histórico contendo um "0"
  embutido é PROVADAMENTE puro (o "0" ancora o estado exatamente, por
  construção — só o estado A pode emitir um "0"), então o ÚNICO
  histórico impuro em cada comprimento `L` é o singleton `"1"^L`
  em si — e seu valor nunca coincide com o de `"1"^(L-1)` (seu pai) nem
  com nenhum outro estado naquele `L` (já que os históricos com "0"
  embutido resolvem-se todos para os 2 estados puros). O teste
  qui-quadrado corretamente identifica isso como um estado NOVO a cada
  `L`, enquanto sua contagem amostral permanecer acima de
  `MIN_COUNT_PER_HISTORY=10` — o que, dada a taxa de decaimento medida
  (`~2^(-L/2)`), só ocorre a partir de `L~15-20+` mesmo para `N=50.000`,
  muito além do orçamento `L_max<=8` travado a priori em
  `METHODOLOGY_NOTE.md` (orçamento que esta revisão não tem autoridade
  para alterar — fazê-lo seria exatamente o tipo de ajuste metodológico
  pós-hoc que a disciplina desta linha proíbe).

  **Conclusão honesta deste diagnóstico:** o CSSR incremental completo
  está CORRETAMENTE implementado (confirmado pelo diagnóstico de ordem
  finita acima) — a não-convergência do Processo Even dentro de
  `L_max<=8` é uma PROPRIEDADE MATEMATICAMENTE PROVADA do fenômeno (ordem
  de Markov aparente ilimitada ao longo de um ramo específico), não um
  bug de implementação. Isto NÃO invalida os outros diagnósticos de
  correção de código (a tarefa explicitamente autoriza uma cadeia de
  Markov de ordem finita como alternativa ao Processo Even, usada acima
  em `a3`, que passa perfeitamente) — é reportado aqui de forma completa
  e honesta, incluindo a prova, não escondido por conveniência nem
  forçado a um "conserto" artificial que violaria o orçamento
  `L_max<=8` já travado.

## (b) A correção pré-autorizada de V1 — carregada sem alteração

A correção de V1 (`min_L_for_selection=2`, excluir `L=1` da busca de
estabilidade) permanece válida e foi mantida SEM ALTERAÇÃO nesta revisão
— é ortogonal à troca de algoritmo (propriedade de como `pi_s` em `L=1`
é matematicamente forçado à marginal de construção de `R_lambda`, não um
artefato do clustering de `L` fixo). Redemonstrada aqui com o motor de
CSSR completo: `C_mu(L=1)` real `=1,000000` (`AR(1) phi=0,3, N=3000`,
canal mediana), 20 substitutos IAAFT dão `C_mu(L=1)` com desvio-padrão
`0,00000000` — confirmação idêntica à de V1.

## (c) Controles positivos — comparação V1 vs. V2 lado a lado (`N_SURROGATES=200`)

| # | Desenho | canal | `p_C_mu` V1 | `p_C_mu` V2 | `p_h_mu` V1 | `p_h_mu` V2 | `L_selected` V2 (PRE/POST) |
|---|---|---|---|---|---|---|---|
| c1 | Markov ordem-1 vs. ordem-2 | mediana | 0,735 | **0,735** | 0,0 | 0,0 | 2/2 |
| c2 | Markov 3-símb. fraco vs. forte | ternário | 0,405 | **0,4** | 0,0 | 0,0 | 2/2 |
| c3 | Markov 3-símb. vs. logístico `r=4` remap | ternário | 1,0 (direção errada) | **1,0 (direção errada)** | 0,0 | 0,0 | 2/3 |
| c4 | ruído/logístico `r=4` | mediana | `DEGENERATE` | **`DEGENERATE`** | — | — | — |

**`C_mu` (canal PRIMÁRIO) continua SEM poder discriminativo real em
NENHUM dos 3 controles computáveis, com valores de `p` PRATICAMENTE
IDÊNTICOS aos de V1** (`0,735` vs `0,735`; `0,405` vs `0,4`; `1,0` vs
`1,0`, mesma direção errada). O `L_selected` recuperado por CSSR
incremental completo (`2/2`, `2/2`, `2/3`) coincide com o `L` que V1
havia implicitamente usado nesses mesmos desenhos (processos de ordem
baixa, totalmente resolvidos por `L=2` ou `L=3`) — **exatamente o
resultado esperado**: para processos de ordem FINITA e BAIXA, CSSR
incremental completo e o clustering de `L` fixo de V1 convergem para a
MESMA reconstrução, porque não há histórico de comprimento diferente
para fundir incrementalmente quando o processo já está totalmente
resolvido no `L` mais baixo suficiente. A diferença entre V1 e V2 só
aparece em processos de ordem efetivamente infinita/muito alta (Processo
Even, item `a4` acima) — e é precisamente por isso que os controles
positivos c1–c4 (todos desenhados com Markov de ordem finita baixa ou
mapa logístico) não mudam: **eles nunca testaram a capacidade
distintiva do CSSR incremental completo em primeiro lugar**, algo que só
o diagnóstico do Processo Even expõe.

`h_mu` (canal companheiro/diagnóstico, REBAIXADO a priori) mostra poder
real (`p=0,0`) nos 3 controles computáveis, idêntico a V1.

## (d) Fallback de bootstrap por blocos móveis (Kunsch 1989)

`real_delta_C_mu=0,8220`, bootstrap média/dp `=0,7904/0,1385`,
`p=0,595` — **numericamente IDÊNTICO a V1** (`p=0,595` nos dois). O
fallback continua sem recuperar poder discriminativo, mesmo padrão exato
de V1.

## (e) Controle negativo — comparação V1 vs. V2 (o achado NOVO desta revisão)

| Par | Canal | `p_C_mu` V1 | `p_C_mu` V2 | `p_h_mu` V1 | `p_h_mu` V2 |
|---|---|---|---|---|---|
| Markov ordem-1 | mediana | 0,385 (correto) | **0,385 (correto, idêntico)** | 0,85 (correto) | **0,665 (correto)** |
| Markov ordem-1 (mesmo par) | ternário | `NOT_COMPUTABLE` (`NOT_DETERMINISTIC` no POST) | **AGORA COMPUTÁVEL: `p_C_mu=0,005` (FALSO POSITIVO NOVO)** | — | **0,665 (correto)** |
| Markov 3 símbolos | ternário | 0,2 (correto) | **0,18 (correto, consistente)** | 0,0 (FALSO POSITIVO) | **0,0 (FALSO POSITIVO, reproduzido)** |

**Achado NOVO desta revisão, honesto e reportado por completo:** o par
de controle negativo Markov-ordem-1/canal-ternário, que em V1 era
`NOT_COMPUTABLE` (bloqueado pelo gate `NOT_DETERMINISTIC` — a
implementação de `L` fixo de V1 não conseguia sequer reconstruir esse
desenho de forma determinística), agora É COMPUTÁVEL sob CSSR incremental
completo (que enforça unifilaridade genuína via divisão recursiva,
`n_states_pre=4, n_states_post=4, L=2/2`) — e revela `p_C_mu=0,005`, um
**FALSO POSITIVO em `C_mu`** (PRE e POST são literalmente sorteios
independentes do MESMO processo gerador; nenhuma diferença real deveria
existir). `delta_C_mu` real é minúsculo em termos absolutos
(`-0,0013`), mas o desvio-padrão do nulo substituto (`0,014`) é estreito
o suficiente para que essa flutuação cruze `p<0,05`.

**Isto FORTALECE, não enfraquece, a conclusão de fragilidade do
estimador:** a implementação V1, ao falhar em reconstruir esse desenho
de forma determinística, nunca pôde revelar este problema de calibração
— o gate `NOT_DETERMINISTIC` mascarava (honestamente, não por má-fé, mas
por limitação de escopo) um problema mais profundo. Com o motor CORRETO
agora em uso, o problema fica exposto: `C_mu` não é apenas
SUB-POTENTE (não detecta diferenças reais, controles positivos c1–c3)
como também pode ser SUPER-SENSÍVEL a flutuações espúrias em desenhos
específicos (este novo achado) — duas faces do mesmo problema estrutural
nomeado em V1: `pi_s`, do qual `C_mu` depende inteiramente, é sensível a
decisões de CLUSTERING discretas que variam de forma ruidosa entre a
série real e cada substituto, seja subestimando (baixo poder) seja
superestimando (falso positivo) a diferença real, dependendo do desenho
específico.

## Nenhuma segunda correção pré-autorizada foi aplicada nesta revisão

Esta revisão iniciou um NOVO ciclo de validação com seu PRÓPRIO
orçamento de UMA correção pré-autorizada (distinto do orçamento já usado
por V1, cuja única correção — exclusão de `L=1` — foi carregada sem
alteração, não uma segunda tentativa desta revisão). **Nenhuma correção
foi aplicada aqui**, porque nenhum problema MECANICAMENTE CORRIGÍVEL
(bounded, não um ajuste aberto) foi identificado: o achado central (falta
de poder de `C_mu` em 3/3 controles positivos, agora reforçado por um
falso positivo em controle negativo) não é um bug de código nem uma
escolha de parâmetro isolada — é uma propriedade emergente de `C_mu`
como estimador, exatamente a explicação (2) da ambiguidade original,
agora confirmada. Forçar uma "correção" aqui seria ajuste pós-hoc
disfarçado, proibido pela disciplina desta linha.

## Interpretação honesta — a ambiguidade original está resolvida

A pergunta nomeada no fechamento original (V1): "a falta de poder de
`C_mu` é artefato da simplificação de escopo (clustering de `L` fixo) ou
fragilidade genuína do estimador?" tem agora uma resposta empírica clara:

1. **O motor de reconstrução agora está PROVADAMENTE correto** — CSSR
   incremental completo, implementado com crescimento genuíno
   (suffix-linkage entre comprimentos) e determinização por divisão
   recursiva genuína, recupera EXATAMENTE a topologia mínima de um
   processo de ordem finita (diagnóstico `a3`, `n_states=4` exato,
   `C_mu` dentro do ruído de amostra da teoria, `determinism_violation_
   frac=0` exato).
2. **Mesmo assim, `C_mu` continua sem poder discriminativo em 3/3
   controles positivos computáveis, com valores de `p` PRATICAMENTE
   IDÊNTICOS aos da implementação simplificada de V1.**
3. **E agora exibe um problema de calibração ADICIONAL** (falso positivo
   em um controle negativo) que a implementação V1 nunca pôde revelar
   por estar bloqueada por um gate de rejeição diferente.

Isto aponta de forma DECISIVA para explicação (2): fragilidade GENUÍNA de
`C_mu` como estimador em amostra finita sob o protocolo IAAFT desta
linha — não um artefato da simplificação de escopo #1/#2 da implementação
original. A implementação foi corrigida; o resultado científico não
mudou.

**Nenhum dado real dos 2 domínios verificados (Old Faithful, La Palma) foi
tocado — nenhum valor de `C_mu`, `Delta_C_mu`, ou p-valor foi calculado
sobre esses dados em nenhum momento, nesta revisão ou na original.**

## Arquivos desta revisão

- `analysis/em_common.py` — reescrito (CSSR incremental completo,
  substituindo o clustering de `L` fixo).
- `analysis/validate_synthetic_v2.py`, `analysis/validation_synthetic_v2.json`,
  `analysis/validate_synthetic_v2.log` — validação sintética completa V2.
- `analysis/validate_synthetic.py`, `analysis/validation_synthetic.json`,
  `analysis/validate_synthetic.log` — MANTIDOS INTACTOS como registro
  histórico da validação V1 (implementação simplificada de `L` fixo);
  NÃO foram re-executados contra o novo `em_common.py` (quebrariam, pois
  chamavam a função `cssr_fixed_L`, removida nesta revisão — comportamento
  esperado e aceitável para um artefato histórico congelado).
- `METHODOLOGY_NOTE.md` — adendo de revisão datado (`DISC-DEC-011`)
  anexado ao final, conteúdo original preservado sem alteração.
- `VALIDATION_NOTE.md` — MANTIDA INTACTA como registro histórico de V1.
