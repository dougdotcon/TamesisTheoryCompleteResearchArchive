# Nota de validação — `epsilon-machine-complexity` (Complexidade Estatística de ε-machines, `C_mu`)

**Metodologia travada em `METHODOLOGY_NOTE.md` ANTES desta validação**
(CSSR de `L` fixo com varredura de convergência `L_max∈{1,...,8}`, gate de
rejeição obrigatório — `DEGENERATE`/`NOT_CONVERGENT`/`NOT_DETERMINISTIC`
—, `I(X)=C_mu` primário + `h_mu` companheiro/diagnóstico REBAIXADO a
priori, checagem BSI companheira, substitutos IAAFT primários + bootstrap
por blocos móveis pré-autorizado). Pipeline: `analysis/em_common.py`.
Script de validação: `analysis/validate_synthetic.py`,
`analysis/validation_synthetic.json`, `analysis/validate_synthetic.log`.

**Veredito final, adiantado aqui:** este candidato é **FECHADO NA ETAPA DE
VALIDAÇÃO** — nenhum dado real (Old Faithful, La Palma) foi tocado. `C_mu`
(canal primário) não mostra poder discriminativo real contra substitutos
IAAFT nem contra o fallback de bootstrap em NENHUM dos 4 desenhos de
controle positivo testados, mesmo após a ÚNICA correção pré-autorizada.
`h_mu` (canal companheiro, REBAIXADO a priori) mostra poder real nos
controles positivos, mas exibe um FALSO POSITIVO espúrio em um controle
negativo — não pode ser promovido como substituto confiável.

## (a) Diagnósticos de correção de código

Todos rodados diretamente sobre `cssr_fixed_L`/`select_Lmax_and_reconstruct`
(não passando pela simbolização `R_lambda`, que é testada separadamente
nos controles positivo/negativo abaixo):

- **Sanidade do teste qui-quadrado:** distribuições idênticas classificadas
  como equivalentes, distribuições opostas classificadas como
  não-equivalentes — **OK**.
- **Processo período-2 (alternância 0,1,0,1,...):** `n_states=2`,
  `C_mu=1,000000` (esperado `1,0` exatamente), `h_mu=0,000000` (esperado
  `0,0` exatamente) — **OK**, correspondência exata.
- **Cadeia de Markov de primeira ordem, à mão computável** (`P(1|0)=0,1`,
  `P(1|1)=0,5`, `N=200.000`): `n_states=2` (esperado `2`),
  `C_mu=0,6488` (teoria `H(5/6,1/6)=0,6500`, erro absoluto `0,0012`) —
  **OK**, correspondência muito próxima em amostra grande. Esta é a
  alternativa explicitamente autorizada pela tarefa ao Processo Even
  ("...ou um processo periódico/cadeia-de-Markov simples com estados
  causais computáveis à mão").
- **Processo Even (exemplo do próprio artigo de Shalizi & Klinkner
  2004):** máquina mínima VERDADEIRA tem exatamente 2 estados causais,
  `C_mu=H(2/3,1/3)=0,9183` bits. **Achado honesto, não escondido:** esta
  implementação simplificada (decisão de escopo #1 de `em_common.py` —
  clustering de `L` fixo, não o crescimento incremental de árvore
  completo de CSSR) **NÃO recupera essa topologia mínima** — a curva de
  número de estados é `[2,3,3,3,3,3,3,3]` para `L=1..8`: converge e
  estabiliza em **3 estados**, não 2, a partir de `L=2`. Isto é uma
  LIMITAÇÃO ESTRUTURAL genuína e documentada da simplificação de escopo
  #1 (o Processo Even tem ordem de Markov infinita mas complexidade de
  estado causal finita — exatamente o tipo de processo que exige o
  crescimento/poda RECURSIVOS de CSSR completo para ser recuperado
  corretamente; o clustering de `L` fixo aqui usado, correto para
  processos de ordem finita — confirmado pelo diagnóstico anterior —,
  não é capaz de colapsar históricos de comprimentos diferentes na mesma
  classe de equivalência). Isto NÃO invalida os diagnósticos de correção
  de código acima (a tarefa explicitamente autoriza uma cadeia de Markov
  simples como alternativa ao Processo Even) mas é reportado aqui de
  forma completa e honesta, não escondido por conveniência.

## (b) A ÚNICA correção pré-autorizada, aplicada durante esta validação

**Problema descoberto:** para `R_lambda` de mediana (`K=2`) e tercil
(`K=3`), sempre que as histórias de comprimento `L=1` NÃO se fundem sob o
teste qui-quadrado, `pi_s` em `L=1` é MATEMATICAMENTE FORÇADO a igualar a
marginal de CONSTRUÇÃO do próprio `R_lambda` (exatamente `0,5/0,5` para
mediana, exatamente `1/3` cada para tercil) — independente da dinâmica
real do segmento. `C_mu` em `L=1` colapsa então a um valor TRIVIAL e
CONSTANTE (`log2(K)`) sempre que `n_states(1)==K`, carregando ZERO
informação discriminante. **Confirmado empiricamente:** processo AR(1)
real (`phi=0,3`, `N=3.000`, canal mediana) deu `C_mu(L=1)=1,000000`
exatamente (`=log2(2)`); 20 substitutos IAAFT reais do MESMO segmento
deram `C_mu(L=1)` com média `1,000000` e **desvio-padrão `0,00000000`** —
confirmação direta e concreta de que `L=1` é estruturalmente inútil como
seleção para este `R_lambda` específico, não uma suposição teórica.

**Correção aplicada** (documentada em `em_common.py`,
`select_Lmax_and_reconstruct`): `L=1` é EXCLUÍDO da busca de estabilidade
que seleciona `L_max` (mas continua sendo computado e reportado na curva
de varredura, para transparência) — a busca de estabilidade agora começa
em `L=2`. Esta é uma correção de bug de implementação genuína, descoberta
durante a validação, não uma redefinição de `I(X)`/`R_lambda`/hipótese —
exatamente o tipo de correção que `METHODOLOGY_NOTE.md` pré-autoriza.
Esta é a ÚNICA correção usada nesta validação — nenhuma segunda tentativa
de redesenho foi ou será feita.

## (c) Controles positivos — 4 desenhos independentes, orçamento completo (`N_SURROGATES=200`)

Todos rodados através do pipeline de PRODUÇÃO completo
(`run_variant_analysis`/`run_em_analysis`, incluindo a simbolização
`R_lambda` real), não uma versão simplificada.

| # | PRE | POST | Canal | `Delta_C_mu` real | nulo IAAFT (média±dp) | `p_C_mu` | `Delta_h_mu` real | `p_h_mu` |
|---|---|---|---|---|---|---|---|---|
| c1 | Markov ordem-1 simétrico fraco | Markov ordem-2 (4 estados distintos) | mediana | +0,822 | +0,791±0,211 | **0,735** | −0,283 | **0,0** |
| c2 | Markov 3 símbolos, persistência fraca | Markov 3 símbolos, persistência forte | ternário | +0,211 | +0,141±0,168 | **0,405** | −0,430 | **0,0** |
| c3 | Markov 3 símbolos, fraco | mapa logístico `r=4`, remapeado por posto | ternário | −0,664 | −1,562±0,071 | **1,0** | −0,793 | **0,0** |
| c4 | ruído branco (implícito) | mapa logístico `r=4`, mediana | mediana | — | — | **`DEGENERATE`** | — | — |

**`C_mu` (canal PRIMÁRIO) não mostra poder discriminativo real em
NENHUM dos 3 controles onde é computável** (`p=0,735`; `p=0,405`;
`p=1,0` — este último na direção ERRADA, com o nulo substituto mostrando
uma diferença ainda MAIOR que o dado real). No 4º controle (mapa
logístico `r=4`, canal mediana), tanto PRE quanto POST disparam o gate
`DEGENERATE` — achado ESTRUTURAL honesto, não um bug: o limiar de
mediana coincide quase exatamente com a partição geradora do mapa
logístico `r=4`, que é conjugada por medida a um processo EXATAMENTE sem
memória (Bernoulli(1/2) iid) — o mesmo mecanismo, e a mesma conclusão
qualitativa (`LZC_median` sem poder no mesmo cenário PRE=ruído
branco/POST=logístico-remapeado), já documentado na validação de
`lempel_ziv_complexity`, que usa o MESMO `R_lambda`.

**`h_mu` (canal companheiro/diagnóstico, REBAIXADO a priori por ser
"esperado redundante com a família taxa-de-entropia já testada 7+
vezes") mostra poder real e consistente (`p=0,0`) nos 3 controles
computáveis** — mas ver (e) abaixo antes de considerar isso uma
justificativa para promovê-lo.

## (d) Fallback de bootstrap por blocos móveis (Kunsch 1989)

Aplicado ao canal com o achado de baixo poder mais claro (`C_mu`,
mediana, desenho do controle c1), `200` reamostras, mesmo `L` fixo já
selecionado pelo dado real (`L=2`): `Delta_C_mu` real `=0,8220`,
reamostras bootstrap média/dp `=0,7904/0,1385`, **`p=0,595`** — o
fallback NÃO recupera poder discriminativo (na verdade fica ligeiramente
PIOR que o IAAFT, `0,595` vs `0,735` — mas ambos igualmente longe de
`0,05`). Mesmo padrão exato já documentado na validação de
`lempel_ziv_complexity` para `LZC_median` ("o fallback... TAMBÉM não
recupera poder para esse canal... PIOR que o IAAFT, não melhor").

## (e) Controle negativo — 2 pares de sorteios independentes, mesmos parâmetros

| Par | Canal | `Delta_C_mu` real | `p_C_mu` | `Delta_h_mu` real | `p_h_mu` |
|---|---|---|---|---|---|
| Markov ordem-1 (mediana) | mediana | ~0 (`1e-7`) | 0,385 (correto) | +0,0019 | 0,85 (correto) |
| Markov ordem-1 (mesmo par) | ternário | — | `NOT_COMPUTABLE` (`NOT_DETERMINISTIC` no POST) | — | — |
| Markov 3 símbolos | ternário | ~0 (`-1e-7`) | 0,2 (correto) | **+0,0135** | **0,0 (FALSO POSITIVO)** |

`C_mu` comporta-se corretamente em ambos os pares computáveis (`p` não
significativo, como esperado quando PRE e POST são sorteios
independentes do MESMO processo). **`h_mu`, porém, dispara significância
espúria (`p=0,0`) no par de Markov de 3 símbolos**, apesar de PRE e POST
serem literalmente o MESMO processo gerador — `Delta_h_mu` real
`=0,0135` é minúsculo em termos absolutos, mas o desvio-padrão do nulo
substituto (`0,0018`) é tão apertado que até essa flutuação de amostra
finita cruza `p<0,05` por larga margem (`~5,8sigma` equivalente). Isto
revela que `h_mu`, apesar de mostrar poder real nos controles positivos,
**NÃO está bem calibrado** neste desenho/canal — o teste IAAFT aplicado
a ele produz uma distribuição nula artificialmente estreita demais para
esta combinação de `R_lambda`/reconstrução, tornando-o não-confiável
como testemunha de significância mesmo quando "funciona" (mostra poder)
nos controles positivos.

## Interpretação honesta — por que fechar aqui, não continuar

Este candidato tem DOIS canais de `I(X)`, ambos agora caracterizados
empiricamente de forma completa:

1. **`C_mu` (primário, a quantidade central que define toda esta
   candidatura):** estruturalmente SEM PODER contra IAAFT e contra o
   fallback de bootstrap, em 3 desenhos de controle positivo
   independentes cobrindo os 2 canais de simbolização e 2 noções
   qualitativamente diferentes de "complexidade causal genuinamente
   maior" (ordem/persistência de Markov; determinismo caótico genuíno
   vs. estrutura Markov linear) — mesmo após a única correção
   pré-autorizada (exclusão de `L=1` da seleção). Isto não é "baixo poder
   estatístico contornável"; é consistente com uma explicação estrutural
   nomeada honestamente: `pi_s`, do qual `C_mu` depende inteiramente, é
   sensível a decisões de CLUSTERING discretas (quantos estados o teste
   qui-quadrado guloso encontra), que variam de forma ruidosa entre a
   série real e cada substituto — inflando a variância nula de `C_mu`
   muito além do que `h_mu` (uma média ponderada de entropias
   condicionais, quantidade mais "local"/suave) exibe. Isto é parcialmente
   uma propriedade da simplificação de escopo #1 desta implementação
   (clustering guloso de `L` fixo, não o CSSR incremental completo com
   refinamento recursivo), mas também é plausivelmente uma fragilidade
   mais geral de `C_mu` como estimador em amostra finita — este achado
   não permite distinguir as duas explicações com o orçamento desta
   tarefa, e isso é dito aqui honestamente, não escondido atrás de uma
   conclusão mais forte do que os dados sustentam.
2. **`h_mu` (companheiro/diagnóstico, REBAIXADO a priori por ser
   esperado redundante com a família taxa-de-entropia já testada 7+
   vezes nesta linha):** mostra poder real nos controles positivos, MAS
   exibe um falso positivo espúrio claro em um controle negativo — não é
   confiável como substituto do canal primário, e mesmo que fosse, seu
   status a priori já era de "não evidência nova" para a hipótese
   distintiva desta candidatura (que `C_mu`, especificamente, é objeto
   matematicamente distinto das medidas de entropia/taxa-de-entropia já
   testadas nesta linha).

Com o canal PRIMÁRIO sem poder demonstrável em 3/3 controles positivos
computáveis (mesmo após a única correção autorizada e o fallback de
bootstrap) e o canal companheiro mostrando calibração pouco confiável,
**a identificabilidade empírica de `C_mu` sob a disciplina de IAAFT desta
linha não pôde ser estabelecida** — o critério de fechamento pré-fixado
em `METHODOLOGY_NOTE.md` ("Se a validação NÃO mostrar poder
discriminativo genuíno... mesmo após a correção: FECHE, não toque dado
real") aplica-se aqui de forma direta e sem ambiguidade.

**Nenhum dado real dos 2 domínios verificados (Old Faithful, La Palma) foi
tocado — nenhum valor de `C_mu`, `Delta_C_mu`, ou p-valor foi calculado
sobre esses dados em nenhum momento.**

## Arquivos desta etapa

- `analysis/em_common.py` — pipeline canônica (CSSR de `L` fixo, gate de
  rejeição, BSI companheira, IAAFT, bootstrap).
- `analysis/validate_synthetic.py`, `analysis/validation_synthetic.json`,
  `analysis/validate_synthetic.log` — validação sintética completa.
- **Nenhum arquivo de dado real, proveniência, ou resultado por domínio
  foi criado** — a linha fechou antes de qualquer necessidade de
  download/preparação de pipeline (os 2 domínios foram apenas
  VERIFICADOS como acessíveis por download real, ver `METHODOLOGY_NOTE.md`,
  mas o pipeline de `C_mu` nunca rodou sobre eles).
