# Nota de validação — `entropia-de-permutacao` (Entropia de Permutação Multiescala + Plano Complexidade-Entropia), ANTES de qualquer dado real

**Status: validação sintética obrigatória (`METHODOLOGY_NOTE.md` Gap (b))
concluída em UMA tentativa — PASSOU CLARAMENTE para os DOIS canais.**
Pipeline (`analysis/pe_common.py`) e script de validação
(`analysis/validate_synthetic.py`) commitados; resultado completo em
`analysis/validation_synthetic.json`. **Nenhum dado real (VitalDB,
PhysioNet European ST-T) foi tocado em nenhum momento deste passo.**

## Resumo honesto do resultado — a pergunta central desta validação

`METHODOLOGY_NOTE.md` Gap (b) formulava uma hipótese a priori explícita,
baseada na literatura mas testada aqui, não assumida: `C_JS`/`MCI`
(desenhado por Rosso et al. 2007 especificamente para separar ruído
estocástico linear de dinâmica caótica) deveria mostrar poder real contra
IAAFT (como `CI`/`beta` de MSE); `H_S`/`PCI` (risco nomeado por Zunino et
al. 2008 de ser reparametrização do expoente de Hurst, já fechado
NEGATIVO 6x nesta linha sob outros nomes — `alpha` de DFA, `h(2)`
wavelet) poderia repetir o padrão de baixo poder do DFA.

**O resultado observado NÃO confirma essa hipótese assimétrica — é outro
padrão, relatado aqui honestamente: OS DOIS CANAIS mostram poder real
contra o substituto IAAFT no controle positivo (`p=0,0` para
`Delta_PCI` E `Delta_MCI`, ambos com separação de dezenas de
desvios-padrão da nula), e os dois se comportam corretamente sob o
controle negativo (`p` não-significativo para ambos).** Isso não é uma
falha de desenho nem um resultado ambíguo — é um achado direto e
completo: para o processo caótico específico usado no controle positivo
(mapa logístico `r=4`), tanto a entropia ordinal normalizada quanto a
complexidade estatística de Jensen-Shannon capturam a determinismo que o
IAAFT (que preserva espectro+marginal mas destrói estrutura de fase não
linear) não reproduz.

## Diagnóstico de correção do código (ANTES dos controles estocásticos)

Rodado primeiro, como exigido pela tarefa: onda senoidal determinística
(período 50, N=1.000), embedding `m=4`, `tau_BP=1`, escala única `s=1`
(sem coarse-graining, para isolar exatamente o que o diagnóstico
pretende verificar). Diferente do RQA, nenhum "dither" numérico foi
necessário aqui — a contagem de padrões ordinais usa ordenação estável
(`argsort(kind='stable')`), que é bem definida mesmo sob empates exatos;
amostras de ponto flutuante de uma senoide praticamente nunca empatam de
fato em `N=1.000`/período `50`.

Expectativa verificável à mão: uma curva suave é monotônica (crescente ou
decrescente) na esmagadora maioria das janelas de 4 pontos consecutivos,
exceto perto dos 2 extremos por ciclo — então a distribuição de padrões
ordinais deveria se concentrar em ~2 dos 24 padrões possíveis (o
crescente puro e o decrescente puro), dando `H_S` baixo.

| Métrica | Resultado |
|---|---|
| `n_windows` | 997 |
| `n_patterns_observed` (de 24 possíveis) | 13 |
| Padrão mais provável (`pi=0`, crescente puro) | `p=0,4684` |
| 2º padrão mais provável (`pi=23`, decrescente puro) | `p=0,4514` |
| Soma dos 2 padrões monotônicos | `0,9198` (91,98% da massa de probabilidade) |
| `H_S` | `0,3405` |
| `C_JS` | `0,2518` |

**Confirma que o código de embedding de Bandt-Pompe + contagem de código
de Lehmer + fórmulas `H_S`/`C_JS`/`Q_0` está correto** antes de testar em
dado genuinamente ambíguo. (Verificado adicionalmente, fora do script de
validação, por comparação força-bruta: o código de Lehmer vetorizado
usado em `pe_common.py` foi conferido contra `list(itertools.permutations(range(4))).index(...)`
padrão-a-padrão para 50 janelas aleatórias — nenhuma divergência.)

## Controles sintéticos (`seed=12345`, `N_SURROGATES=200`, `N_IAAFT_ITER=50`)

### Controle positivo (`METHODOLOGY_NOTE.md` Gap (b), especificação exata)

`N=3.000` amostras (sem subamostragem, abaixo do teto `MAX_N_PER_SEGMENT=20.000`).
PRE = ruído branco Gaussiano iid. POST = mapa logístico caótico (`r=4`),
remapeado por posto (rank-remap) sobre os valores exatos do PRE —
marginal idêntica por construção, espectro confirmado empiricamente
quase plano em ambos (`spectral_exponent_pre=-0,058`,
`spectral_exponent_post=+0,014`). Grade de escala: `s_max=25`,
`n_scales=12` (log-espaçadas, únicas) para ambos os segmentos.

| Canal | PRE real | POST real | Δ real | média nula IAAFT | desvio nulo | σ-equivalente | `p` (bicaudal, n=200) | veredito |
|---|---|---|---|---|---|---|---|---|
| `PCI` (`H_S` somado) | 11,8597 | 11,5520 | **−0,3077** | −0,0005 | 0,0248 | **−12,37σ** | **0,0** | `IAAFT_HAS_REAL_POWER` |
| `MCI` (`C_JS` somado) | 0,1868 | 0,5430 | **+0,3563** | +0,0005 | 0,0336 | **+10,60σ** | **0,0** | `IAAFT_HAS_REAL_POWER` |

`p=0,0` aqui significa literalmente zero, entre os 200 substitutos
válidos, com `|Delta_substituto| >= |Delta_real|` — a separação é total,
não apenas abaixo do limiar de 0,05. Nenhum substituto ficou indefinido
em nenhum canal (`n_valid=200` para ambos).

### Controle negativo (dois sorteios independentes de fGn-like, H=0,7 fixo)

Sonda diretamente o risco espectral/linear nomeado no Gap (b) (Zunino et
al. 2008). `N=3.000` para PRE e POST, sementes independentes
(`555001`/`555002`), `s_max=25`, `n_scales=12`.

| Canal | PRE real | POST real | Δ real | média nula IAAFT | desvio nulo | `p` (bicaudal) | veredito |
|---|---|---|---|---|---|---|---|
| `PCI` | 9,7376 | 9,4292 | −0,3085 | −0,4076 | 0,2658 | **0,63** | corretamente não significativo |
| `MCI` | 2,1671 | 2,3566 | +0,1894 | +0,2301 | 0,1409 | **0,585** | corretamente não significativo |

Ambos os `p` ficam bem acima de 0,05 — o IAAFT está corretamente
calibrado sob a hipótese nula de "mesmo processo linear, sem mudança
estrutural genuína" para os dois canais.

## Veredito de poder IAAFT — por canal, honesto, sem forçar a hipótese a priori

- **`H_S`/`PCI` (canal primário):** `IAAFT_HAS_REAL_POWER`. `p=0,0` no
  controle positivo (σ-equivalente `-12,37`), `p=0,63` no controle
  negativo. **Isso contraria a expectativa a priori de baixo poder
  (padrão DFA-alpha)** — pelo menos contra o mapa logístico `r=4`, `H_S`
  detecta a mudança estrutural com poder total.
- **`C_JS`/`MCI` (canal companheiro):** `IAAFT_HAS_REAL_POWER`. `p=0,0`
  no controle positivo (σ-equivalente `+10,60`), `p=0,585` no controle
  negativo. **Isso CONFIRMA a expectativa a priori de poder real
  (padrão CI/beta de MSE)** para este canal especificamente.
- **Não houve achado de não-computabilidade estrutural em nenhum
  canal**, confirmando empiricamente (não apenas assumindo) a expectativa
  do próprio `METHODOLOGY_NOTE.md`: ao contrário do FNN do RQA, o
  embedding ordinal de Bandt-Pompe não precisa "resolver" dimensão
  alguma — é uma contagem combinatória direta, sempre computável para
  `N>=m`. `real_pre`/`real_post` retornaram `status="ok"` em TODOS os
  controles (positivo e negativo), com todos os 12 valores de escala
  definidos (`n_scales_undefined=0`) em cada caso.
- **O fallback de bootstrap por blocos móveis (Kunsch 1989),
  pré-autorizado em `METHODOLOGY_NOTE.md` Gap (b)/(e) e já implementado
  em `pe_common.py` (`moving_block_bootstrap_resample`,
  `run_block_bootstrap_test`) exatamente para o caso de baixo poder, NÃO
  precisou ser invocado** — nenhum canal mostrou baixo poder. A máquina
  fica disponível no módulo, não utilizada nesta validação.

## Resposta direta à pergunta central desta validação

A hipótese a priori de `METHODOLOGY_NOTE.md` era ASSIMÉTRICA: `C_JS`
teria poder, `H_S` talvez não. **O que de fato aconteceu é diferente:
OS DOIS CANAIS mostraram poder real e completo (`p=0,0`) contra o
substituto IAAFT no controle positivo, e os dois se comportaram
corretamente (não significativos) no controle negativo.** A parte da
hipótese sobre `C_JS`/`MCI` foi confirmada; a parte sobre `H_S`/`PCI`
mostrando baixo poder foi refutada — pelo menos para o processo caótico
usado neste teste (mapa logístico `r=4` com marginal e espectro casados
por rank-remap sobre ruído branco).

**Nota honesta sobre o que isso significa e o que NÃO significa:** o
risco de identificabilidade nomeado por Zunino et al. 2008 (`H_S`
correlacionado quase monotonicamente com o expoente de Hurst `H` para
processos GAUSSIANOS AUTOSSIMILARES lineares — fGn/fBm) é sobre uma
classe de processo diferente da usada no controle positivo aqui (mapa
logístico determinístico, não um fGn/fBm de `H` variável). O controle
negativo (fGn `H=0,7` vs. fGn `H=0,7`, mesmo `H`) testa diretamente essa
classe e mostra `PCI` corretamente não-significativo (`p=0,63`) — o que
é consistente com Zunino et al. 2008 (mesmo `H`, `H_S` não deveria
mudar) mas NÃO testa se `H_S` discrimina processos com `H` DIFERENTE
entre si, que é a hipótese de reparametrização propriamente dita.
**Este teste não foi rodado aqui** porque não era o controle exigido por
`METHODOLOGY_NOTE.md` Gap (b) (que especifica ruído branco → mapa
logístico, não um par fGn com `H` diferente) — permanece uma pergunta em
aberto se, em dado real, uma mudança de `H_S` refletir uma mudança
genuína de dinâmica não-linear ou simplesmente uma mudança de `H`
efetivo (a mesma ambiguidade de interpretação, não de poder estatístico
contra IAAFT, que motivou o risco de identificabilidade em primeiro
lugar). Isso é uma ressalva de INTERPRETAÇÃO para a etapa de dado real
subsequente, não uma limitação do resultado de PODER relatado aqui.

## Nenhum desvio metodológico

Nenhuma decisão metodológica de `METHODOLOGY_NOTE.md` foi alterada
depois de ver o resultado. O fallback de bootstrap por blocos móveis foi
adicionado a `pe_common.py` exatamente como pré-autorizado pelo Gap
(e)/(b) — mas apenas como maquinário disponível, não invocado, porque
nenhum canal mostrou o padrão de baixo poder que autorizaria seu uso
como teste primário. `m=4`, `tau_BP=1`, `s_min=1`,
`n_min_per_scale=120`, `n_scales_cap=15`, `MAX_N_PER_SEGMENT=20.000`,
`N_SURROGATES=200`, `N_IAAFT_ITER=50`, `seed=12345`, e a fórmula de `Q_0`
permanecem exatamente como fixados em `METHODOLOGY_NOTE.md`, sem
reformulação alguma.

## Próximo passo — decisão pendente para a sessão orquestradora

Este agente NÃO decide se/como prosseguir para o dado real — essa
decisão cabe à sessão orquestradora, mesma disciplina já aplicada a
`d_B` em `grafo-de-visibilidade` e ao veredito final de `RQA`. O achado
fica registrado aqui:

- **Ambos os canais (`H_S`/`PCI` e `C_JS`/`MCI`) mostraram poder real e
  completo contra IAAFT no controle positivo**, e calibração correta no
  controle negativo — nenhuma barreira estrutural, nenhum canal precisou
  do fallback de bootstrap. Por essa métrica, a validação de PODER exigida
  por Gap (b) **passou para os dois canais**, sem exceção e sem precisar
  de um segundo desenho de controle positivo (diferente de RQA, que
  precisou de uma segunda tentativa e mesmo assim fechou negativo na
  validação).
- A ressalva de interpretação sobre `H_S`/`PCI` (risco Zunino et al. 2008
  de reparametrização de Hurst para processos autossimilares
  especificamente, não testado diretamente por este desenho de controle
  positivo) permanece um risco de identificabilidade a ter em mente ao
  interpretar um eventual `Delta_PCI` significativo em dado real — mas
  não é um problema de PODER estatístico, que é o que esta validação
  mede.
- Nenhum dado real (VitalDB, PhysioNet European ST-T) foi tocado. O
  candidato `entropia-de-permutacao` está pronto, do ponto de vista desta
  validação, para a etapa de dado real — decisão final de prosseguir cabe
  à sessão orquestradora.
