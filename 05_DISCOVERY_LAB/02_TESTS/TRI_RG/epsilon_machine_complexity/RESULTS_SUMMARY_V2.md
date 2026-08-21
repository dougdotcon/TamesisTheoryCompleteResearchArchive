# Resultado da revisão — `epsilon-machine-complexity` (CSSR incremental completo, `DISC-DEC-011`)

**Data:** 2026-08-21. Esta é uma REVISÃO do fechamento original
(`RESULTS_SUMMARY.md`, mantido intacto como registro histórico), autorizada
explicitamente pela sessão orquestradora como uma correção de completude
de implementação (não uma reformulação de hipótese) — ver o adendo em
`METHODOLOGY_NOTE.md` e a nota completa em `VALIDATION_NOTE_V2.md`.

**Veredito final:** `epsilon-machine-complexity` (`C_mu`) permanece
**FECHADO NA ETAPA DE VALIDAÇÃO** — nenhum dado real (Old Faithful,
GeyserTimes.org; La Palma/Cumbre Vieja 2021, catálogo EMSC/IGN) foi
tocado em nenhum momento, nem na sessão original nem nesta revisão. A
ambiguidade honesta deixada em aberto pelo fechamento original —
"a falta de poder de `C_mu` era artefato da simplificação de `L` fixo, ou
fragilidade genuína do estimador?" — está agora **resolvida de forma
decisiva**: é fragilidade genuína do estimador. O fechamento é, portanto,
MAIS decisivo agora do que era antes desta revisão, não menos.

## O que esta revisão fez

Substituiu (não remendou) o motor de reconstrução de estados causais em
`analysis/em_common.py`: de "clustering de estados causais em `L` fixo"
(decisões de escopo #1/#2 da implementação original) para CSSR
incremental completo (Shalizi & Klinkner 2004, *UAI*) — crescimento
genuíno de históricos com ligação por sufixo entre comprimentos
consecutivos, mais determinização por divisão recursiva genuína até
unifilaridade. `I(X)=C_mu` primário/`h_mu` companheiro, o protocolo de
significância (IAAFT + bootstrap pré-autorizado) e o esquema de
simbolização (mediana/ternário) permaneceram EXATAMENTE inalterados — ver
o adendo de `METHODOLOGY_NOTE.md` para a confirmação item a item.

## Validação — recapitulação decisiva (ver `VALIDATION_NOTE_V2.md` para o detalhe completo)

**Confirmação de que a nova implementação está CORRETA:** um diagnóstico
NOVO nesta revisão — uma cadeia de Markov de SEGUNDA ordem genuína (ordem
finita, `N=300.000`, solução teórica exata via autovetor dominante) — é
recuperada **EXATAMENTE** pelo CSSR incremental completo: `n_states=4`
a partir de `L=2` (teoria: 4 estados), `C_mu=1,8102` (teoria `1,8113`,
erro de amostra), `determinism_violation_frac=0,000000` exato. Isto
confirma que o motor GROW+DETERMINIZE está implementado corretamente.

**O Processo Even (teste decisivo, exemplo do próprio artigo de Shalizi
& Klinkner) continua NÃO recuperando a topologia mínima verdadeira (2
estados) dentro do orçamento `L_max<=8` travado a priori** — mas desta
vez com uma explicação MATEMATICAMENTE PROVADA, não uma limitação vaga:
o ramo "corrida constante de 1s" do processo tem uma alternação exata,
período-2, NUNCA decadente, na distribuição condicional do próximo
símbolo dado uma janela `"1"^k` (derivada via a matriz de transição
sub-estocástica "emite um 1" e confirmada numericamente a 4 dígitos
significativos, `N` até 2 milhões) — resolvível apenas via exclusão por
contagem insuficiente em `L~15-20+`, muito além do orçamento `L_max<=8`
que esta revisão não tem autoridade para alterar. **Isto foi investigado
a fundo, conforme instruído** (não é um julgamento de conveniência): a
implementação está correta (confirmado pelo diagnóstico de ordem finita
acima); a não-convergência do Processo Even é uma propriedade do
fenômeno em relação a este orçamento específico, não um bug.

**Os 4 controles positivos, rodados a orçamento completo
(`N_SURROGATES=200`), dão valores de `p_C_mu` PRATICAMENTE IDÊNTICOS aos
de V1:**

| Controle | `p_C_mu` V1 | `p_C_mu` V2 |
|---|---|---|
| Markov ordem-1 vs. ordem-2 (mediana) | 0,735 | 0,735 |
| Markov 3-símb. fraco vs. forte (ternário) | 0,405 | 0,4 |
| Markov 3-símb. vs. logístico `r=4` remap (ternário) | 1,0 (direção errada) | 1,0 (direção errada) |
| Ruído/logístico `r=4` (mediana) | `DEGENERATE` | `DEGENERATE` |

O fallback de bootstrap por blocos móveis (Kunsch 1989) dá `p=0,595`,
numericamente IDÊNTICO a V1.

**Achado NOVO desta revisão:** um controle negativo (Markov ordem-1,
canal ternário) que em V1 era `NOT_COMPUTABLE` (bloqueado pelo gate
`NOT_DETERMINISTIC` da implementação simplificada) agora É computável sob
CSSR incremental completo — e revela `p_C_mu=0,005`, um **falso positivo
NOVO** em `C_mu` (PRE e POST são sorteios independentes do MESMO
processo; nenhuma diferença real deveria existir). Isto REFORÇA a
conclusão de fragilidade do estimador: a implementação anterior, ao
falhar em reconstruir esse desenho, mascarava (por limitação de escopo,
não má-fé) um problema de calibração que agora fica exposto.

## Veredito honesto — a ambiguidade está resolvida

O fechamento original nomeou explicitamente duas explicações possíveis,
não-distinguíveis com o orçamento daquela sessão, para a falta de poder
discriminativo de `C_mu`:

> "(1) uma fragilidade específica da simplificação de escopo desta
> implementação (clustering guloso de `L` fixo em vez do CSSR incremental
> completo de Shalizi & Klinkner...); ou (2) uma fragilidade mais geral de
> `C_mu` como estimador estatístico em amostra finita, mesmo sob uma
> implementação completa..."

**Esta revisão resolve a ambiguidade a favor de (2).** A implementação
agora está demonstravelmente correta (recupera exatamente um processo de
ordem finita com solução teórica exata) e, mesmo assim:

- `C_mu` continua sem poder discriminativo real em 3/3 controles
  positivos computáveis, com valores de `p` praticamente idênticos aos
  da implementação simplificada.
- `C_mu` agora exibe TAMBÉM um falso positivo em um controle negativo que
  a implementação simplificada nunca conseguiu sequer testar.
- O fallback de bootstrap continua sem recuperar poder (`p=0,595`,
  idêntico a V1).
- `h_mu` (canal companheiro, REBAIXADO a priori) continua mostrando poder
  real nos controles positivos mas com o MESMO problema de calibração já
  documentado em V1 (falso positivo em um controle negativo).

Isto é consistente com a nota interpretativa que a literatura de mecânica
computacional já registra: estimativas de `C_mu` em amostra finita têm
variância consideravelmente maior que as de `h_mu`, precisamente porque
`C_mu` depende da IDENTIDADE e do NÚMERO de estados causais inferidos —
uma decisão combinatória discreta e ruidosa entre a série real e cada
substituto — e não de médias suaves de probabilidades condicionais. A
correção de implementação feita nesta revisão elimina a decisão de
clustering AD HOC de `L` fixo da equação (substituída por crescimento
incremental com ligação por sufixo, matematicamente correto e verificado)
e a fragilidade permanece — isolando-a como uma propriedade do próprio
`C_mu`, não da implementação.

**Achado da linha inteira, retomado (nomeado a priori em
`METHODOLOGY_NOTE.md` original e confirmado agora com mais força):**
`C_mu` e `C_JS` (entropia de permutação, candidato #8, já fechado
negativo 8/8) pertencem à mesma família estratégica de medidas de
complexidade em forma de U-invertido/pico. Com `epsilon-machine-
complexity` agora tendo recebido uma correção de implementação completa
e AINDA ASSIM não produzindo evidência robusta — desta vez por uma razão
identificada com precisão (fragilidade do estimador, não bug de
código) — **a estratégia inteira de "complexidade-em-pico" como classe de
candidatos para esta linha acumula 2/2 tentativas sem produzir um
invariante cross-domain sobrevivente, agora com a segunda tentativa tendo
recebido o benefício adicional de uma implementação corrigida e ainda
assim confirmando o padrão.**

## Domínios reais — permanecem intocados, permanecem verificados para uso futuro

Old Faithful (GeyserTimes.org, PRE N=327/POST N=483, limpo) e La Palma
2021 (catálogo EMSC/IGN, PRE N=1.048/POST N=6.746, sem duplicatas,
magnitudes plausíveis) permanecem verificados como genuinamente acessíveis
e de boa qualidade (ver `METHODOLOGY_NOTE.md`), mas **nenhum dos dois foi
processado pelo pipeline de `C_mu` nesta revisão nem na sessão original**
— o candidato fechou na etapa de validação novamente, desta vez de forma
mais decisiva. Ambos os domínios ficam documentados para reaproveitamento
futuro caso a linha algum dia revisite este candidato com uma medida de
`I(X)` fundamentalmente diferente (não apenas uma implementação corrigida
de `C_mu`).

## Arquivos desta revisão

- `METHODOLOGY_NOTE.md` — adendo de revisão anexado ao final (datado,
  rotulado `DISC-DEC-011`), conteúdo original preservado.
- `analysis/em_common.py` — reescrito (CSSR incremental completo).
- `analysis/validate_synthetic_v2.py`, `analysis/validation_synthetic_v2.json`,
  `analysis/validate_synthetic_v2.log` — validação sintética completa V2.
- `VALIDATION_NOTE_V2.md` — nota de validação V2 completa, com comparação
  V1 vs. V2 lado a lado.
- `RESULTS_SUMMARY_V2.md` — este arquivo.
- **Mantidos intactos, sem modificação, como registro histórico:**
  `VALIDATION_NOTE.md`, `RESULTS_SUMMARY.md`, `analysis/validate_synthetic.py`,
  `analysis/validation_synthetic.json`, `analysis/validate_synthetic.log`.
- **Nenhum arquivo de dado real, proveniência, ou resultado por domínio foi
  criado nesta revisão** — o candidato fechou antes de qualquer
  necessidade de download/preparação de pipeline, exatamente como na
  sessão original.

## Estado da linha e próximo passo (para a sessão orquestradora)

`TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md`, `DECISION_LEDGER.yaml` e
`02_TESTS/TRI_RG/CLOSURE_SUMMARY.md` NÃO foram modificados por este
agente (fora do escopo desta tarefa) — ficam a cargo da sessão
orquestradora, que já tem o padrão estabelecido de como registrar um
fechamento na etapa de validação nesta linha.

O escopo desta revisão foi estritamente limitado a este único candidato
(`epsilon-machine-complexity`), por autorização explícita da sessão
orquestradora (`DISC-DEC-011`) — os outros 15 candidatos desta linha
permanecem fechados exatamente como documentado em
`02_TESTS/TRI_RG/CLOSURE_SUMMARY.md`; nenhum deles foi tocado por esta
revisão.

Com a ambiguidade da implementação agora resolvida a favor de fragilidade
genuína do estimador — não artefato de escopo — não há mais uma correção
de implementação pendente que justificasse revisitar este candidato uma
terceira vez sob a mesma definição de `I(X)=C_mu`. Uma futura revisita
legítima exigiria uma medida de complexidade estatística FUNDAMENTALMENTE
diferente (não uma correção de implementação de `C_mu`), o que
constituiria uma NOVA candidatura, não uma revisão desta. A decisão sobre
o próximo passo para `DISC-TRI-RG-001` como um todo (nova rodada de
busca, revisitar outro candidato já fechado, pausar, ou encerrar a linha)
permanece inteiramente a cargo do usuário e/ou da sessão orquestradora,
exatamente como deixado em aberto pelo fechamento original.
