# Nota de validação — `evt-hill` (Dinâmica do Índice de Cauda via Estimador de Hill), ANTES de qualquer dado real

**Status: pipeline implementado exatamente como especificado em
`METHODOLOGY_NOTE.md` (commit `9c40c41`), sem reformulação de nenhuma
decisão lá travada. Diagnóstico de correção de código PASSA (`xi_Hill`
recupera o índice de cauda teórico de duas famílias conhecidas dentro de
margem de ruído esperada para o estimador de Hill). Controle negativo
calibra corretamente. Controle positivo mostra um achado de validação
genuíno e não-trivial sobre o próprio teste de significância do Gap (f)
— reportado in extenso abaixo, não escondido. Checagem de redundância
com SOC (Gap c) inconclusiva por poder estatístico (apenas 3 pares
comparáveis), mas o padrão qualitativo disponível pesa CONTRA
redundância simples. Nenhum dado real foi tocado em nenhum momento desta
sessão.**

Pipeline (`analysis/evt_hill_common.py`), script de validação
(`analysis/validate_synthetic.py`, resultado completo em
`analysis/validation_synthetic.json`) e checagem de redundância SOC
(`analysis/soc_redundancy_check.py`, resultado em
`analysis/soc_redundancy_check.json`) commitados.

## 1. Diagnóstico de correção de código — `xi_Hill`/`xi_MLE` vs. índice de cauda teórico conhecido

| Distribuição | `n` | `xi` teórico | `k*` | `xi_Hill` | erro relativo | `xi_MLE` | erro relativo |
|---|---|---|---|---|---|---|---|
| Pareto padrão (`alpha=3`, construção Lomax+1) | 20.000 | 0,3333 | 587 | **0,3137** | **−5,9%** | 0,2886 | −13,4% |
| Student-t (`df=4`) | 20.000 | 0,25 | 249 | **0,2778** | **+11,1%** | 0,1106 | **−55,8%** |

**`xi_Hill` (canal primário): PASSA** — recupera o índice de cauda
teórico dentro de ~6-11% em ambas as famílias, ordem de grandeza
consistente com o ruído de estimação finito já esperado do estimador de
Hill (variância de ordem `O(1/k)`, `k` na casa de algumas centenas aqui).

**`xi_MLE` (canal companheiro): discordância grande especificamente em
Student-t, investigada e explicada, NÃO um bug de implementação.**
Diagnóstico dedicado: reajustando GPD via o MESMO `scipy.stats.
genpareto.fit(exceedances, floc=0)` a dado GERADO DIRETAMENTE de uma GPD
verdadeira (`xi=0,25`, `scale=1,0`, várias contagens de excedência de
100 a 5.000), o ajuste recupera `xi` corretamente (ruído de amostra
finita normal, sem viés sistemático visível) — confirma que
`_fit_gpd_mle`/`genpareto.fit` em si está correto. Repetindo o
diagnóstico em excedências de Student-t(df=4) reais em vários `k`
(100 a 1.500, não só o `k*=249` selecionado pelo Gap (a)), `xi_MLE` fica
consistentemente entre 0,10-0,15 em TODO o intervalo — não um artefato
do `k*` particular escolhido. Isso é o viés pré-assintótico conhecido da
literatura de EVT: a cauda de Student-t só converge para GPD
ASSINTOTICAMENTE (`u->infinito`); em limiares finitos (mesmo os ~1-6% mais
extremos usados aqui), a curvatura de segunda ordem da cauda de
Student-t (convergência mais lenta que a de uma Pareto pura) faz o MLE
de GPD subestimar substancialmente o `xi` assintótico verdadeiro — um
efeito bem documentado (Hill converge mais rápido que MLE de GPD para
famílias de convergência lenta), não um bug. Isso é exatamente o tipo de
discordância entre os dois estimadores que o próprio Gap (b) de
`METHODOLOGY_NOTE.md` já antecipa como "informativo por si só" — reportado
aqui explicitamente, não escondido: **`xi_MLE` deve ser interpretado com
cautela adicional para famílias de convergência lenta, `xi_Hill`
permanece o canal de decisão primário.**

## 2. Controle negativo — mesma distribuição em PRE e POST

PRE e POST = dois sorteios INDEPENDENTES de Student-t(`df=6`), `n=6.000`
cada, `N_RANDOMIZATIONS=200`.

| Canal | `xi` PRE | `xi` POST | `Delta` real | nula aleatória (média±dp) | `p` |
|---|---|---|---|---|---|
| `xi_Hill` | 0,2475 | 0,2789 | +0,0313 | 0,0051 ± 0,0328 | **0,495** |
| `xi_MLE` | 0,1524 | 0,0265 | −0,1259 | −0,0627 ± 0,0480 | 0,085 |

**Corretamente calibrado, nenhuma significância espúria** — `p=0,495`
(`xi_Hill`) e `p=0,085` (`xi_MLE`, abaixo de 0,10 mas acima do limiar
convencional de 0,05) para uma comparação sem mudança genuína de
distribuição.

## 3. Controle positivo — achado central da validação (poder do teste de randomização do Gap (f))

### 3a. Student-t `df=10 -> df=3` (mudança real e grande, `xi` teórico `0,10 -> 0,333`)

PRE/POST balanceados, `n=6.000` cada (`n_total=12.000`, ponto de corte
real do dado sintético exatamente no meio, posição 6.000).

| Canal | `xi` PRE | `xi` POST | `Delta` real | nula aleatória (média±dp) | `p` |
|---|---|---|---|---|---|
| `xi_Hill` | 0,1994 | 0,3870 | **+0,1876** | **+0,1495 ± 0,0455** | **0,265 (NÃO sig.)** |
| `xi_MLE` | −0,1353 | 0,3635 | +0,4989 | +0,2754 ± 0,1908 | 0,08 (NÃO sig.) |

**A mudança real de `xi_Hill` NÃO cruza `p<0,05`, apesar de ser uma
mudança de índice de cauda genuína e grande.** Investigação da causa
(não um bug): a nula do Gap (f) para este cenário está DESLOCADA para
longe de zero, na MESMA direção do sinal real (média +0,1495, não ~0) —
`corr(ponto_de_corte, Delta_aleatorio) = -0,85` nas 200 réplicas. Motivo
identificado: com PRE e POST de comprimento IGUAL e a transição real
exatamente no meio do conjunto combinado, TODO ponto de corte aleatório
sorteado no intervalo `[0,2; 0,8]` do Gap (f) necessariamente captura uma
MISTURA de PRE e POST em pelo menos um dos dois lados (o corte cai antes
OU depois da posição 6.000, mas o intervalo permitido nunca evita a
transição real) — cada réplica "aleatória" já contém, diluído, o mesmo
salto de regime que o corte real mede, inflando a nula na mesma direção
do efeito e reduzindo o poder do teste. **Isso não é um bug de
implementação — é uma propriedade estrutural do teste de randomização do
ponto de corte especificado no Gap (f), que a validação sintética
descobriu exatamente para isso.**

**Checagem complementar (não fazia parte do desenho original de 3
partes, adicionada para isolar a causa):** repetindo o MESMO salto de
`xi` teórico (Student-t `df=10 -> df=3`) com PRE/POST DESBALANCEADOS
(`n_pre=1.500`, `n_post=6.000`, transição real na posição 1.500, perto
da borda inferior do intervalo `[0,2; 0,8]*7.500=[1.500; 6.000]`
resultante), o MESMO tamanho de efeito real (`Delta_xi_Hill=+0,183`,
quase idêntico ao caso balanceado) torna-se **`p=0,0`** — altamente
significativo — porque agora a maioria dos cortes aleatórios cai
inteiramente dentro de um único regime (comparando duas sub-janelas do
MESMO POST, por exemplo), produzindo uma nula corretamente centrada perto
de zero (média 0,058, muito menor que no caso balanceado). **Isso é
tranquilizador para o passo de dado real:** `METHODOLOGY_NOTE.md` Gap (d)
já define PRE/POST domain-agnósticos que, nos 2 domínios reais desta
rodada (onda de calor PDX, furacão Florence), são estruturalmente
ASSIMÉTRICOS por desenho (PRE = "todo o histórico disponível antes",
POST = "até o próximo evento documentado", tipicamente PRE >> POST em
extensão temporal, ou vice-versa dependendo do domínio) — o cenário de
pior caso para o poder do Gap (f) (PRE=POST exatamente no meio do pool)
é improvável de ocorrer nos dados reais, mas **fica registrado
explicitamente como uma ressalva de interpretação: se algum resultado
real vier com `p` não-significativo apesar de um `Delta_xi`
aparentemente grande, a extensão relativa de PRE/POST e a posição da
transição real dentro do intervalo `[0,2; 0,8]` do pool devem ser
verificadas antes de concluir ausência de efeito.**

### 3b. Robustez — Pareto `alpha=4 -> alpha=1,5` (`xi` teórico `0,25 -> 0,667`, família distinta)

PRE/POST balanceados, `n=6.000` cada (mesmo desenho balanceado/pior-caso
da seção 3a, deliberadamente, para ver se um efeito ainda maior sobrevive
mesmo sob o desconto de poder já documentado).

| Canal | `xi` PRE | `xi` POST | `Delta` real | nula aleatória (média±dp) | `p` |
|---|---|---|---|---|---|
| `xi_Hill` | 0,2306 | 0,6645 | +0,4338 | +0,2149 ± 0,1929 | **0,02 (sig.)** |
| `xi_MLE` | 0,1699 | 0,6899 | +0,5201 | +0,1711 ± 0,2640 | **0,025 (sig.)** |

Mesmo efeito de deslocamento de nula descrito acima (média da nula
também deslocada para +0,21, não zero), mas o tamanho do efeito real
(`Delta=0,434`) é grande o bastante para cruzar `p<0,05` de qualquer
forma — confirma que o teste TEM poder real quando o efeito é grande o
suficiente para superar o deslocamento estrutural da nula, em uma
segunda família distribucional (não apenas Student-t).

## Veredito do diagnóstico de poder — honesto, sem forçar a hipótese a priori

| Cenário | `p_xi_Hill` | `p_xi_MLE` | Veredito |
|---|---|---|---|
| Negativo (mesma dist.) | 0,495 | 0,085 | Corretamente calibrado, sem falso positivo |
| Positivo, Student-t, PRE/POST balanceado | 0,265 | 0,08 | **NÃO detecta** — nula deslocada pela própria estrutura do corte real no meio do pool |
| Positivo, Student-t, PRE/POST desbalanceado (checagem complementar) | 0,0 | — | Detecta limpo quando a transição não fica no meio do pool |
| Positivo, Pareto, PRE/POST balanceado (robustez) | 0,02 | 0,025 | Detecta apesar do deslocamento de nula (efeito grande o bastante) |

**O teste de randomização do Gap (f) TEM poder real** (3b, e a checagem
complementar de 3a) mas é **estruturalmente conservador quando PRE e
POST têm comprimento igual e a transição real cai exatamente no meio do
pool combinado** (3a) — uma propriedade genuína do desenho específico do
Gap (f) (aleatorizar o PONTO DE CORTE dentro da série combinada, não
embaralhar rótulos nem usar um deslocamento circular), descoberta
exatamente pelo processo de validação que esta etapa exigia, não uma
falha de implementação. Como a tarefa desta sessão autoriza validar e
reportar, mas NÃO reformular a metodologia já travada em
`METHODOLOGY_NOTE.md`, esta ressalva fica registrada para a sessão
orquestradora decidir como pesar um eventual resultado real que venha
com `p` alto e `Delta` aparentemente grande, condicional à extensão
relativa de PRE/POST observada naquele domínio específico (ver seção 3a
acima para o diagnóstico completo a ser reaplicado se isso ocorrer).

## 4. Checagem de redundância com SOC (Gap c) — dado JÁ commitado, nenhum dado novo tocado

**Replicação exata dos segmentos:** antes de calcular qualquer `xi_Hill`,
`analysis/soc_redundancy_check.py` reconstrói os MESMOS segmentos
PRE/POST (primário e robustez) que `soc_avalanches` já travou e reportou
em `soc_avalanches/analysis/result_ridgecrest.json`/
`result_goes_flares.json` — checagem automática de contagem de eventos
confirma **`EXACT MATCH`** em todas as 8 contagens (2 domínios × 2
variantes × PRE/POST) antes de prosseguir.

**Quantidade contínua bruta usada** (declarado, `METHODOLOGY_NOTE.md`
diz "magnitude/energia" sem escolher uma): Ridgecrest -> ENERGIA sísmica
via relação de Gutenberg-Richter (`log10(E_joules)=1,5*mag+4,8`), não
magnitude diretamente — a cauda superior da MAGNITUDE é aproximadamente
EXPONENCIAL (Gutenberg-Richter é linear em magnitude/log-contagem), sem
índice de cauda de Hill bem definido; a energia é a transformação
monotônica que É de lei de potência por construção. Flares GOES -> FLUXO
de pico de raios-X (W/m², coluna `[72:79]` do arquivo bruto, NÃO usada
pelo pipeline original de `soc_avalanches`, que só usou o horário de
início) — já naturalmente de cauda pesada (Lu & Hamilton 1991), sem
transformação necessária.

**Resultado — 3 pares comparáveis** (Ridgecrest primário excluído: o
próprio `tau_pre` de `soc_avalanches` é indefinido lá, só 9 avalanches):

| Variante | Domínio | `Delta_xi_Hill` | `Delta_tau` (SOC) | Mesma direção de "cauda mais pesada"? |
|---|---|---|---|---|
| Primária | GOES flares | +0,153 | −0,455 | **Sim** (xi sobe = cauda mais pesada; tau desce = cauda mais pesada) |
| Robustez | Ridgecrest | −0,499 | −1,733 | **Não** (xi desce = cauda mais leve; tau desce = cauda mais pesada) |
| Robustez | GOES flares | +0,302 | +0,343 | **Não** (xi sobe = cauda mais pesada; tau sobe = cauda mais leve) |

`n_comparable_pairs=3`. Correlação de Pearson bruta entre `Delta_xi_Hill`
e `Delta_tau` = **0,977**; ajustada para a convenção de sinal oposta
entre os dois estimadores (`xi` cresce, `tau` decresce, com cauda mais
pesada) = **−0,977**. **Nenhuma das duas é estatisticamente informativa
com apenas 3 pontos (1 grau de liberdade)** — reportado por completude,
não como veredito de hipótese. O padrão QUALITATIVO disponível (mais
informativo com `n` tão pequeno que uma correlação numérica) é: **apenas
1 dos 3 pares muda na mesma direção fisicamente esperada de uma
redundância genuína; os outros 2 mudam em direções opostas.**

## Veredito honesto da checagem de redundância

Com apenas 3 pares comparáveis, esta checagem **NÃO tem poder
estatístico para confirmar OU descartar redundância com confiança**. O
padrão disponível (2 de 3 pares em direção QUALITATIVAMENTE oposta ao
que uma redundância simples "mesma cauda pesada, dois nomes diferentes"
previria) pesa CONTRA redundância trivial, mas fracamente — é
inteiramente possível que `xi_Hill` (medindo a cauda dos VALORES de
magnitude/energia/fluxo individuais) e `tau` (medindo a cauda do TAMANHO
de avalanches, clusters de eventos definidos por proximidade temporal,
uma estatística estrutural de agrupamento, não de valor) meçam
propriedades genuinamente distintas destes 2 sistemas, consistente com o
argumento teórico a priori já em `METHODOLOGY_NOTE.md` (Gap c) sobre por
que o "princípio do grande salto único" mitiga mas não elimina
completamente o risco — mas 3 pontos não bastam para reivindicar isso
com confiança. **Reportado honestamente como inconclusivo por poder, não
como "desacoplado confirmado".** Nota adicional relevante para a decisão
da linha: `soc_avalanches` em si terminou com veredito NEGATIVO em ambos
os domínios (Ridgecrest refutado por nulo ETAS; GOES sem sinal em
nenhuma variante) — mesmo que `evt-hill` fosse totalmente redundante com
`tau`, isso não implicaria automaticamente um resultado negativo em
`evt-hill`, já que os domínios reais deste candidato (clima/hidrologia)
são fisicamente distintos dos de `soc_avalanches` (sismologia/flares) —
esta checagem testa redundância de MECANISMO ESTATÍSTICO, não repete o
mesmo par de domínios.

## Nenhum desvio metodológico não declarado

Toda decisão de implementação que se afastou de uma leitura
absolutamente literal do texto de `METHODOLOGY_NOTE.md` está documentada
explicitamente, tanto no código (`evt_hill_common.py`,
`soc_redundancy_check.py`) quanto nesta nota:
- guarda de positividade no denominador/numerador do estimador de Hill
  (necessária para que a fórmula do Gap (a) passo 2 seja bem definida;
  não muda nenhum dos 6 passos numerados, só define o comportamento
  quando o limiar de um `k` específico não é positivo);
- escolha de `scipy.stats.genpareto.fit` (não um solver Newton-Raphson
  manual) para o Gap (b), documentada como decisão explícita autorizada
  pelo próprio texto ("sua escolha, o que for mais robusto");
- escolha de ENERGIA (não magnitude) para Ridgecrest e FLUXO de pico
  para GOES no Gap (c), documentada como decisão explícita necessária
  porque `METHODOLOGY_NOTE.md` diz "magnitude/energia" sem escolher uma
  das duas.

Nenhuma decisão sobre a grade de `k`, `B=200`, `N_RANDOMIZATIONS=200`,
`MIN_SEG_FRACTION`/`MAX_SEG_FRACTION`, `MIN_N_PER_SEGMENT`,
`MAX_N_PER_SEGMENT`, ou a substituição de IAAFT pelo teste de
randomização do ponto de corte foi alterada. O achado de deslocamento de
nula na seção 3 é um RESULTADO da validação, não uma mudança de
metodologia — nenhum parâmetro do Gap (f) foi modificado para "corrigir"
isso.

## Próximo passo

Este agente NÃO prossegue para dado real (fora do escopo desta tarefa,
por instrução explícita). Pipeline pronto para `run_evt_hill_analysis`
ser chamado sem modificação assim que o dado real (NOAA GHCN-Daily PDX
2021, USGS Cape Fear 02105769) for baixado e a proveniência documentada,
seguindo `05_DISCOVERY_LAB/00_GOVERNANCE/AGENTS.md`. Recomenda-se que a
sessão que rodar o passo de dado real leia a seção 3 desta nota ANTES de
interpretar qualquer `p` do Gap (f) que vier próximo do limiar — em
particular, verificar a posição relativa da transição real dentro do
pool PRE+POST combinado daquele domínio específico antes de concluir
ausência de efeito a partir de um `p` alto isolado.
