# Addendum de metodologia — auto-calibração completa de f_multi (Chae 2023 Eqs. 11-13 + procedimento iterativo)

**Status:** Estágio 1 — metodologia + validação sintética. **Não trava um
pré-registro sobre dado real** (nenhum dado real, discovery ou holdout, é
tocado nesta etapa) — este documento fixa a metodologia e os critérios de
aceitação ANTES de qualquer execução sobre dado real, mas a formalização
completa de pré-registro (`PREREGISTRATION.md` com `Status: LOCKED`) só é
exigida quando uma frente futura (Estágio 2) tocar a amostra de descoberta
real — mesma disciplina de `METHODOLOGY_EXTENSIONS.md`.

**Data:** 2026-08-22
**Test ID:** `SPARC-FMULTI-STAGE1`, retomada de `DISC-COSMOLOGY-MOND-SPARC-004`
**Autoridade:** `DISC-DEC-023` (05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml)
**Autor (agente/sessão):** Tamesis Discovery Lab, sessão 2026-08-22

## 0. Por que esta frente existe

`DISC-COSMOLOGY-MOND-SPARC-004` foi fechado `CLOSED_INCONCLUSIVE` em
2026-08-18 (`PREREGISTRATION.md` Seção 7, `02_TESTS/COSMOLOGY_WIDE_BINARIES_MC_DEPROJECTION/`)
porque a checagem adversarial obrigatória de multiplicidade oculta mostrou
que companheiras não resolvidas, em magnitude inteiramente plausível pela
literatura (`f_multi=0,25-0,47`), são sozinhas suficientes para explicar o
sinal residual real inteiro (`hidden_companion_check_v2.md`). Essa checagem,
no entanto, **não implementou a auto-calibração completa de `f_multi` de
Chae** — usou uma varredura de valores FIXOS da faixa observacional da
literatura como teste de plausibilidade pós-hoc, não o procedimento
iterativo do próprio Artigo A (ajustar `f_multi` como parâmetro livre até o
bin de maior aceleração convergir para Newtoniano). O fechamento documentou
isso explicitamente como a precondição para uma tentativa futura
(`PREREGISTRATION.md` linha 535: "disponível para uma tentativa futura que
implemente a auto-calibração completa de f_multi de Chae (Eqs. 11-13) antes
de qualquer ajuste de a0"). Esta frente implementa exatamente essa
precondição, em duas etapas (Estágio 1 = metodologia + validação sintética,
aqui; Estágio 2 = aplicação à amostra de descoberta real, autorização
futura separada; abertura do holdout selado = decisão de lock separada,
mais adiante ainda).

Verificação exata das equações citadas: `PROVENANCE_CHAE_EQS.md` (fetch
direto do fonte LaTeX do arXiv nesta sessão, não memória). Veredito: a
citação "Chae Eqs. 11-13" já usada pelo repositório está **correta**
(confirmada por checagem cruzada independente via a Eq. 18 citada
externamente pelo Artigo B) — nenhuma correção de número de equação é
necessária. Um achado adicional (não solicitado) foi documentado por
precisão: o pipeline já travado desta linha (`delta_obs_newt.py`) já usa a
versão CORRIGIDA (pós-erratum do Artigo B) da fórmula de projeção mock, não
a versão original com bug do Artigo A.

## 1. O que "auto-calibração de f_multi" significa operacionalmente

### 1a. Parâmetros livres do modelo de injeção de companheira (Eqs. 11-13)

Por sistema, POR realização Monte Carlo (varia a cada sorteio, não é fixo
por sistema como a excentricidade de Hwang):

1. **`has_multi` (Bernoulli(f_multi))** — se o sistema tem companheira
   oculta nesta realização. `f_multi` é o ÚNICO parâmetro livre do modelo
   inteiro — tudo abaixo é sorteado de distribuições JÁ fixadas pela
   literatura (Chae Seção 3.2), não ajustadas.
2. **Qual componente é afetado** — 40% só o componente mais brilhante, 30%
   só o mais fraco, 30% ambos (fixo, texto de Chae Seção
   "Including masses of hidden close binaries", não uma equação numerada).
3. **`ΔM_G` (diferença de magnitude host-companheira)** — Eq. 13,
   `p(ΔM_G;γ_M)=(1+γ_M)(ΔM_G/12)^γ_M` em `[0,12]`, `γ_M=-0,7` (Tokovinin
   2008, valor adotado nesta pipeline — Chae relata também `-0,6` de
   Riddle+2015/Raghavan+2010 como alternativa, não usada aqui por
   simplicidade, mesma escolha já feita por `hidden_companion_check_v2.py`).
4. **`κ` (fração de luminosidade do hospedeiro)** — Eq. 12,
   `κ=1/(1+10^(-0,4·ΔM_G))`, determinístico dado `ΔM_G`.
5. **Massa verdadeira do componente afetado** — Eq. 11 dá as magnitudes
   `M_{G,h}`/`M_{G,c}`; convertidas a massa pela MESMA relação
   massa-magnitude já travada nesta linha (Mamajek/Pecaut 2013). A massa
   TOTAL do componente observado (hospedeiro+companheira, ambos
   catalogados como um único ponto) fica inflada por um fator
   `B(κ)=κ^(1/3,5)+(1-κ)^(1/3,5)≥1` em relação à massa que a relação
   massa-magnitude atribuiria à luz combinada tratada como uma única
   estrela — dedução direta de Eq. 11 + a relação massa-luminosidade
   `L∝M^3,5` que o próprio Artigo A usa alhures (texto perto da Eq. 20,
   `eq:rphot`), não uma equação numerada isolada, mas consequência
   algébrica direta (documentada em `PROVENANCE_CHAE_EQS.md` Seção 4 e já
   usada, sem alteração, pelas checagens adversariais v1/v2 anteriores).
6. **Wobble de fotocentro** — Chae Seção 3.4 item 7 (Eq. 20, `eq:rphot`)
   adiciona a velocidade aparente do fotocentro (deslocado do baricentro)
   ao `v_p` do ramo MOCK. Esta pipeline reusa a aproximação já declarada
   e usada por `hidden_companion_check_v2.py` (órbita interna circular,
   fase uniforme, `a_in` log-uniforme em `[0,01;d_pc]` UA) em vez da forma
   completa de três casos da Eq. 20 (que distingue por período orbital
   interno e separação angular) — **simplificação declarada, mesma já
   aceita nas checagens anteriores desta linha**, não uma nova aproximação
   introduzida aqui.

### 1b. Dados necessários — o que já está disponível vs. o que precisou ser aproximado

| insumo | necessário para | disponível no dataset já preparado? |
|---|---|---|
| `M1_Msun`, `M2_Msun`, `Mtot_Msun` | massa catalogada (base da inflação) | **sim** — `quality_filtered_sample.parquet` |
| `Gmag1`, `Gmag2` | magnitude combinada `M_G` (para Eq. 11 inversa, se fosse necessário recuperar `M_G` a partir da massa catalogada em vez de assumir `M_G` diretamente) | **sim**, mas não estritamente necessário — esta pipeline aplica a inflação de massa DIRETAMENTE sobre `M1_Msun`/`M2_Msun` catalogados (equivalente a aplicar Eq. 11 em espaço de massa em vez de magnitude, já que a relação massa-magnitude é monotônica — mesma prática já usada por `hidden_companion_check_v2.py`, documentada lá e reaproveitada aqui sem modificação) |
| `RUWE1`, `RUWE2` | checagem de CONSISTÊNCIA (não mais a correção primária, ver Seção 2) | **sim** — `quality_filtered_sample.parquet` |
| erros de PM por componente (`e_pmRA1/2`, `e_pmDE1/2`) | orçamento de ruído astrométrico simétrico (Seção 5b, já travada) | **sim** |
| `e`, `e0`, `e1`, `alpha`, `dpm_sig` (Hwang) | amostragem de excentricidade (Gap a, já travado) | **sim** — `hwang_eccentricity_subset.parquet` |
| distribuição de `ΔM_G` observada MEDIDA para a amostra Gaia EDR3+El-Badry desta linha especificamente (em vez de reusar Tokovinin 2008/Riddle 2015, amostras diferentes) | recalibrar `γ_M` especificamente para este catálogo | **NÃO disponível/não rederivado** — esta pipeline usa `γ_M=-0,7` fixo (valor de Tokovinin 2008 já adotado pelas checagens anteriores), **não recalibrado contra a distribuição real de `ΔM_G` implícita nos pares resolvidos desta amostra especificamente**. Aproximação declarada, herdada sem alteração das checagens v1/v2. |
| catálogo externo dedicado de multiplicidade de alta ordem para a amostra Gaia EDR3+El-Badry específica (para validar `f_multi` autocalibrado contra um "gabarito" observacional independente, não só a faixa agregada da literatura 0,25-0,47) | validação externa do valor calibrado | **NÃO disponível** — não buscado nesta sessão (fora do escopo de Estágio 1, que é só validação sintética). Se buscado no futuro, permitiria comparar `f_multi` autocalibrado sobre dado REAL desta amostra com um número medido independentemente, não só a faixa agregada de outras pesquisas. |

**Conclusão da checagem de insumos:** todos os dados estritamente
necessários para reimplementar o modelo de injeção de massa (Eqs. 11-13) e
o procedimento iterativo de auto-calibração JÁ estão disponíveis no dataset
já baixado e preparado por SPARC-002/003/004 — nenhum novo download foi
necessário para o pipeline em si. A única aproximação herdada (não nova)
é `γ_M` fixo em vez de recalibrado para esta amostra específica, e a forma
simplificada do wobble de fotocentro — ambas já declaradas e aceitas nas
checagens adversariais anteriores desta linha, reaproveitadas sem alteração.

## 2. Como isso muda o pipeline de análise — substitui, não roda ao lado

**Fluxo ANTIGO (v1/v2, já fechado `CLOSED_INCONCLUSIVE`):**
```
1. Ajustar a0 sobre delta_obs-newt bruto (SEM correção de multiplicidade)
2. SE gatilho (g/gN real bruto > 1 em algum bin): rodar checagem
   adversarial PÓS-HOC (varredura de f_multi FIXOS da faixa observacional,
   comparar magnitude com o sinal já calculado) -- plausibilidade, não
   correção
3. Veredito: aceitar ou não o a0 ajustado no passo 1, dependendo do
   resultado do passo 2
```

**Fluxo NOVO (esta frente, a partir do Estágio 2 -- ainda não autorizado
nesta sessão, apenas especificado e validado sinteticamente aqui):**
```
1. Auto-calibrar f_multi ANTES de qualquer ajuste de a0: bisseção sobre
   f_multi injetando massa (Eqs. 11-13) identicamente nos ramos real E
   mock (mesma realização MC, mesma decisão estocástica de companheira por
   sistema, exatamente como o texto de Chae Sec.3.4 especifica -- "masses
   ... fixed for both real data and mock data"), até que
   delta_obs-newt no bin-âncora (o de MAIOR aceleração da grade fixa desta
   linha, bin 4 de 5, análogo ao x0~=-8 de Chae) seja consistente com zero
   dentro de uma fração pequena do sigma bootstrap (mesmo critério
   numérico do Artigo B, citado verbatim em PROVENANCE_CHAE_EQS.md Secao 5)
2. Aplicar o f_multi calibrado (e a massa injetada correspondente) aos 5
   bins -- delta_obs-newt CORRIGIDO por multiplicidade em TODOS os bins,
   não só o bin-âncora
3. Ajustar a0 sobre o delta_obs-newt CORRIGIDO (não mais o bruto)
4. As checagens antigas (RUWE alto vs. baixo, varredura de f_multi da
   literatura) NÃO desaparecem -- são REBAIXADAS a checagens de
   CONSISTÊNCIA secundárias: o f_multi autocalibrado deve cair dentro da
   faixa observacional 0,25-0,47 (Secao 7 do Artigo B fornece 0,48/0,36 de
   referência) e a diferença RUWE alto/baixo deve ser qualitativamente
   consistente com o f_multi calibrado -- mas não são mais o mecanismo
   PRIMÁRIO de correção do sinal.
```

Isto é uma mudança estrutural, não uma adição: o passo 1 do fluxo antigo
(ajustar `a0` sobre o sinal bruto) deixa de existir como o resultado
principal — o ajuste de `a0` só acontece DEPOIS da correção de
multiplicidade, sobre o sinal já corrigido. O gatilho pré-declarado
(`g/gN` bruto `>1`) continua existindo, mas sua função muda: em vez de
disparar uma checagem PÓS-HOC sobre um resultado já calculado, ele passa a
ser a justificativa a priori para SEMPRE rodar a auto-calibração antes de
qualquer ajuste de `a0` nesta linha especificamente (dado que o gatilho já
disparou nas duas versões v1/v2 sobre o dado real desta amostra).

## 3. Critérios de aceitação pré-declarados para a validação sintética (Estágio 1)

Fixados ANTES de rodar qualquer validação. O pipeline só é considerado
pronto para o Estágio 2 (dado real de descoberta, ainda não holdout) se
**todos** os itens abaixo passarem:

> **[Correção pós-adversarial, 2026-08-22]** A frase original acima dizia
> "este documento é escrito e commitado antes da execução dos scripts de
> validação abaixo" — uma verificação adversarial independente (ver
> `../ADVERSARIAL_VERIFICATION.md` item 1) mostrou, por timestamp do
> sistema de arquivos, que isso era literalmente falso: este documento foi
> escrito DEPOIS de `results/validation_A_results.json` e
> `results/validation_B_results.json` já existirem, e nada nesta pasta
> estava commitado no momento em questão. **O que de fato importa —
> os limiares numéricos A1-A4/B1-B3 abaixo — estava hardcoded nos scripts
> de validação (`analysis/validate_a_recover_f_multi.py`,
> `analysis/validate_b_recover_a0_with_contamination.py`) ANTES das
> execuções**, confirmado pelos próprios timestamps (scripts mais antigos
> que os resultados) — não há evidência de que os critérios tenham sido
> ajustados após ver o resultado. Mas a alegação de ordem/commit do texto
> original estava incorreta como escrita, e é corrigida aqui em vez de
> deixada de pé. Texto original da frase preservado acima, sem edição.

**Validação A — recuperação de `f_multi` verdadeiro em população
puramente Newtoniana:**
- A1. Com um `f_multi` verdadeiro conhecido injetado (`f_multi_true`) numa
  população sintética 100% Newtoniana (zero física MOND), o `f_multi`
  autocalibrado pela bisseção deve recuperar `f_multi_true` dentro de uma
  tolerância absoluta de `0,05` (a mesma ordem de grandeza da incerteza
  observacional entre os estudos da literatura, 0,25-0,47).
- A2. Após a correção com o `f_multi` calibrado, `delta_obs-newt` deve ficar
  consistente com zero (IC 95% bootstrap contendo 0) em **todos** os 5
  bins, não só no bin-âncora usado para a calibração — esta é a checagem
  de generalização que distingue auto-calibração genuína de um ajuste
  trivial de 1 ponto.
- A3. Sem nenhuma correção (`f_multi=0` fixo), `delta_obs-newt` deve
  mostrar um viés positivo estatisticamente significativo em pelo menos
  os bins de menor aceleração (confirmando que o `f_multi_true` injetado
  realmente produz um confundidor detectável — controle de que o
  desenho experimental tem poder, não é um teste vazio).
- A4. A checagem de RUWE (sistemas com `f_multi`-atribuído "tem
  companheira" vs. não) deve mostrar RUWE sistematicamente mais alto no
  primeiro grupo (verifica que a covariável RUWE sintética construída para
  a validação carrega, de fato, sinal correlacionado com a companheira
  oculta simulada — pré-condição para a checagem de consistência do
  Estágio 2 fazer sentido).

**Validação B — recuperação de `a0` verdadeiro sob contaminação de
multiplicidade conhecida:**
- B1. Com um `a0` MOND verdadeiro conhecido injetado (`a0_true`, ex.
  `1,2e-10`) E uma contaminação de multiplicidade conhecida
  (`f_multi_true`) SIMULTANEAMENTE, o pipeline SEM correção (`f_multi=0`)
  deve produzir um `a0` ajustado enviesado (measuravelmente diferente de
  `a0_true`, replicando o mesmo modo de falha que já reprovou v1/v2 sobre
  dado real) — controle negativo confirmando que a contaminação
  realmente engana a pipeline não-corrigida.
- B2. O pipeline COM a auto-calibração de `f_multi` aplicada (calibrada no
  bin-âncora, que deve permanecer dominado pelo termo Newtoniano+massa
  porque `nu(gN_ancora/a0_true)~=1` para o `a0_true` de teste — checado
  explicitamente antes de aceitar o resultado) deve recuperar `a0_true`
  dentro do IC de 95% do ajuste — OU, se o desenho não tiver poder
  discriminativo suficiente para separar `a0_true` de `f_multi_true` de
  forma limpa (degenerescência conhecida a priori, ver Seção 4), reportar
  esse resultado como INCONCLUSIVO de forma honesta, não forçar uma
  recuperação que os dados sintéticos não sustentam.
- B3. O `f_multi` calibrado em B2 deve continuar próximo de
  `f_multi_true` (mesma tolerância de A1, `0,05`) mesmo com o `a0` real
  presente — confirma que a presença de um sinal MOND genuíno não
  desestabiliza a calibração de `f_multi` no bin-âncora (pré-condição
  para usar o bin-âncora como calibrador limpo: ele precisa ser
  insensível ao `a0` verdadeiro, não só ao `a0` nulo).

**Critério de bloqueio:** se qualquer item acima falhar, o pipeline NÃO
está pronto para o Estágio 2 — a falha específica deve ser documentada
honestamente em `RESULTS_SUMMARY_STAGE1.md`, com um diagnóstico do porquê,
antes de qualquer nova tentativa de correção (mesma disciplina de
"correção delimitada e pré-declarada, depois fechar" já usada 6+ vezes na
linha `DISC-TRI-RG-001`).

## 4. Limitação estrutural conhecida a priori — degenerescência a0/f_multi

Uma limitação teórica precisa ser declarada ANTES de rodar B2: como o
mecanismo de inflação de massa (Item 1a-5) é aproximadamente CONSTANTE
através dos bins (não depende de `g_N`, achado já documentado em
`hidden_companion_check_v2.md` Item 1), enquanto o mecanismo de wobble de
fotocentro produz alguma dependência residual de `g_N` (mesmo problema de
FORMA já identificado nas checagens v1/v2 — o wobble simplificado não
decai o suficiente em alta `g_N`), existe uma degenerescência estrutural
parcial entre "`f_multi` alto com forma de wobble imperfeita" e "`a0`
verdadeiro pequeno": ambos podem produzir um resíduo residual pequeno e
aproximadamente constante nos bins intermediários. A auto-calibração
ANCORADA no bin de maior aceleração (onde `nu(gN/a0)->1` para qualquer
`a0` fisicamente razoável, deep-MOND longe da relevância) quebra parte
dessa degenerescência (calibra `f_multi` onde o `a0` verdadeiro NÃO pode
contaminar a calibração, por construção), mas não garante poder total nos
bins de menor `g_N`, onde MOND e multiplicidade residual competem pelo
mesmo espaço de assinatura. Validação B é desenhada precisamente para
medir se essa degenerescência é ou não fatal para esta amostra/desenho
específico — reportado honestamente, item B2 permite explicitamente o
veredito "INCONCLUSIVO por desenho" em vez de forçar uma recuperação
espúria.

## 5. Escopo explícito desta etapa (Estágio 1)

- **NÃO toca o holdout selado** (12.944 sistemas, `El-Badry, Rix & Heintz
  2021`) em nenhum momento — nenhum script desta pasta lê
  `discovery_holdout_split.json` para extrair a lista de holdout, nem lê
  qualquer coluna do holdout.
- **NÃO necessariamente toca a amostra de descoberta real** (30.203
  sistemas) — as validações A e B desta etapa usam populações
  **inteiramente sintéticas**, construídas a partir de distribuições
  paramétricas documentadas em `analysis/build_synthetic_population.py`
  (massa, separação, distância, excentricidade, erro de PM — todas
  parametrizadas para refletir a ORDEM DE GRANDEZA e a ESTRUTURA da
  amostra real já caracterizada pelas sessões anteriores desta linha, mas
  SEM ler nenhum arquivo `.parquet` do catálogo real). O `v_p`/velocidade
  observado usado em toda validação desta etapa é 100% sintético, sempre.
  Nenhum arquivo desta pasta importa `quality_filtered_sample.parquet` nem
  `hwang_eccentricity_subset.parquet`.
- **Abrir o holdout exige uma decisão de lock formal própria**, decisão
  futura separada, mesmo precedente já estabelecido para outras linhas
  desta trilha (ex. FHK/variância-do-número) — reafirmado explicitamente
  aqui, herdado de `DISC-DEC-023`.
- O que ESTA etapa entrega: a especificação metodológica completa (Seções
  1-4 acima), o código do pipeline de auto-calibração
  (`analysis/companion_injection.py`, `analysis/selfcal_pipeline.py`), e
  os resultados honestos das validações A/B contra os critérios
  pré-declarados da Seção 3 — ver `RESULTS_SUMMARY_STAGE1.md`.
