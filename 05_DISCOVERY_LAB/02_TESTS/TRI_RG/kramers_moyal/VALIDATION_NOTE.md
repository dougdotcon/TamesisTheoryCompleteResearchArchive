# Nota de validação — `kramers-moyal` (Reconstrução de Fokker-Planck via Coeficientes de Kramers-Moyal), ANTES de qualquer dado real

**Status: pipeline implementado e validado sinteticamente. `PKS` (canal
primário) mostra poder IAAFT real e limpo; `beta_D2` (canal companheiro)
mostra poder baixo sob os dois testes de significância tentados —
achado honesto, não resolvido unilateralmente, ver "Questão em aberto"
abaixo. Nenhum dado real foi tocado em nenhum momento desta sessão.**
Pipeline (`analysis/km_common.py`) e script de validação
(`analysis/validate_synthetic.py`) commitados; resultado completo em
`analysis/validation_synthetic.json`.

Metodologia implementada exatamente como especificada em
`METHODOLOGY_NOTE.md` (commit `afb6899`), sem reformulação de nenhuma
decisão lá travada — `tau_ME` via teste de Chapman-Kolmogorov,
`D1(x)`/`D2(x)`/`D3(x)`/`D4(x)` nos `N_BINS_X=10` bins do PRE,
`kappa` demovido a diagnóstico a priori (nunca usado em nenhum p-valor
abaixo), `PKS`/`beta_D2` como canais primário/companheiro, IAAFT
(`N_SURROGATES=200`, `N_IAAFT_ITER=50`, `seed=12345`) como protocolo de
significância padrão desta linha.

## Resumo honesto do resultado

Dois problemas REAIS de implementação foram encontrados e corrigidos no
teste de Chapman-Kolmogorov (Gap (a)) durante o diagnóstico de correção
de código, executado ANTES de qualquer controle estocástico — ver seção
dedicada abaixo. Depois de corrigidos, a validação sintética central
(controles negativo/positivo, Gap (b)) roda limpa:

| Canal | Controle positivo dedicado | `p` (positivo) | `p` (negativo) | Veredito |
|---|---|---|---|---|
| `PKS` | poço-duplo biestável (deriva bimodal), rank-remap | **0,005** | 0,23 | **`IAAFT_HAS_REAL_POWER`** |
| `beta_D2` (vs. `x`) | difusão dependente de estado, rank-remap | 0,405 | 0,805 | `IAAFT_LOW_POWER` |
| `beta_D2` (vs. `\|x-x*\|`) | difusão dependente de estado, rank-remap | 0,95 | 0,88 | `IAAFT_LOW_POWER` |

`PKS` (curtose em excesso da densidade estacionária reconstruída) tem
poder real e limpo — sigma-equivalente do controle positivo:
**≈ −2,04σ** (`PKS` pré=0,247, pós=−0,825, `Δ=−1,071`, nula IAAFT
média≈−0,29, desvio≈0,32), e o controle negativo fica corretamente
não-significativo (`p=0,23`). `beta_D2`, em AMBAS as variantes
(`vs. x` e `vs. |x-x*|`, ambas explicitamente autorizadas por
`METHODOLOGY_NOTE.md` Gap (b): "testado e reportado com o que for mais
estável"), não separa o controle positivo do nulo IAAFT nem do nulo
bootstrap de blocos — ver "Questão em aberto" abaixo para a
investigação completa e a decisão que fica para a sessão orquestradora.

## Diagnóstico de correção do teste CK — DOIS problemas reais encontrados e corrigidos, ANTES de qualquer controle estocástico

Executado primeiro, como exigido pela tarefa: um processo OU (Euler-
Maruyama, inovações Gaussianas iid a cada passo — Markov em QUALQUER
lag por construção) deveria passar o teste CK em todo lag da grade; um
processo genuinamente não-Markoviano deveria falhar em lags curtos.

**Problema 1 — bootstrap ingênuo tinha poder zero.** A leitura mais
literal de "reamostragem de índices temporais com reposição" —
reamostrar TRIOS `(x1,x2,x3)` inteiros com reposição, usando todos os
`n-2L` trios sobrepostos (stride-1) — mostrou-se estruturalmente
quebrada: reamostragem com reposição infla o ruído de estimação de
`P1`/`P2_direto` muito além do nível de ruído da estimativa única (não
reamostrada) da amostra completa. Resultado: a nula bootstrap ficava
SISTEMATICAMENTE MAIOR que o `chi2` observado mesmo para o processo OU
genuinamente Markoviano (`chi2_observado≈58` vs. `chi2_bootstrap
médio≈139` no lag mais curto) — `p_ck_test≈1,0` para TODO processo
testado, incluindo dois geradores deliberadamente não-Markovianos
(fGn H=0,9; OU com contaminação de ruído colorido lento aditivo), ou
seja, o teste nunca conseguia rejeitar, um problema de implementação
genuíno, não de poder de IAAFT (nada aqui toca substitutos).

**Problema 2 — corrigido com bootstrap condicional, mas com viés no
sentido oposto em lags grandes.** Corrigido com um bootstrap
"Markoviano" condicional (`_markov_bootstrap_triples`): cada réplica
reamostra ÍNDICES TEMPORAIS com reposição do conjunto de transições de
1 passo observadas, CONDICIONADO no bin atual em cada um dos dois
passos simulados — os trios resultantes são, por construção, uma
realização exata de uma cadeia Markoviana com o núcleo empírico `P1`.
Isso sozinho AINDA ficou mal calibrado em lags GRANDES: a estatística
"observada", construída com todos os `n-2L` trios sobrepostos
(stride-1), tem trios adjacentes compartilhando `L-1` das `L` amostras
do seu espaço — redundância massiva que colapsa o tamanho amostral
EFETIVO muito abaixo do nominal `n-2L`. O bootstrap condicional, ao
contrário, sorteia trios EFETIVAMENTE INDEPENDENTES a cada réplica —
tamanho amostral efetivo muito maior, logo ruído de amostragem menor,
que o dos dados reais sobrepostos. Isso apareceu empiricamente como
`chi2_observado` crescendo sistematicamente com o lag enquanto
`chi2_bootstrap_médio` ficava praticamente constante, produzindo
REJEIÇÕES FALSAS em lags grandes mesmo para o processo OU genuinamente
Markoviano (ex. `p_ck_test=0,0` em `lag=130` amostras).

**Correção final:** usar blocos NÃO SOBREPOSTOS (stride-`L`,
`t=0,L,2L,3L,...`) tanto para a estatística observada quanto para o
bootstrap, em vez de todo `t=0,1,2,...`. Isso remove a redundância
induzida por sobreposição da estimativa observada, casando sua
estrutura de independência/tamanho amostral efetivo com a que o
bootstrap condicional já produzia. Custo inevitável: menos "linhas"
disponíveis em `L` grande (`n/L` blocos em vez de `n-2L`), então o piso
de amostra insuficiente é acionado mais cedo em lags grandes — uma
consequência honesta de usar dado menos redundante, não uma
substituição silenciosa. Documentado in extenso no docstring de
`ck_test_at_lag` em `km_common.py`.

**Resultado do diagnóstico, versão final corrigida:**

- **Processo OU (Markoviano), `theta=1,0`, `sigma=1,0`, `dt=0,05`,
  `N=3000`, seed=101:** todos os 5 lags computáveis (`1,2,3,5,8`
  amostras — os 7 lags maiores da grade de 12 pontos ficam
  corretamente `insufficient_samples`, não uma falha) passam, `p`
  entre 0,80 e 1,0. **`markov_all_pass=True`.**
- **OU + contaminação de ruído colorido lento aditivo (não-Markoviano
  PRIMÁRIO), `theta_rápido=1,0`/`sigma_rápido=1,0`,
  `theta_lento=0,01`/`sigma_lento=3,0`, seed=7:** rejeita no lag MAIS
  CURTO disponível, `p=0,025` (`chi2_observado=74,1` vs. nula
  bootstrap média≈38,1). **`contam_rejects_shortest=True`.**
- **fGn(H=0,9) (não-Markoviano SUPLEMENTAR, per a própria redação de
  `METHODOLOGY_NOTE.md`):** **INCONCLUSIVO** nesta `N` — não rejeita em
  nenhum dos 5 lags computáveis (`p=1,0` em todos), e a grade não
  alcança lags mais longos o bastante (piso de blocos não-sobrepostos
  de `N=3000`) para a decaída lenta em lei de potência da
  autocorrelação de fGn divergir visivelmente de uma decaída
  exponencial/consistente-com-Markov nesse intervalo curto. Reportado
  honestamente como achado suplementar, NÃO o controle de correção
  primário (esse papel é do controle de contaminação acima, que rejeita
  limpo).

**Veredito do diagnóstico: `CK_TEST_CORRECT`.**

## Controles sintéticos (`N=3000`, `seed=12345`, `N_SURROGATES=200`)

### Controle negativo (dois sorteios independentes do MESMO processo OU)

PRE e POST = duas realizações INDEPENDENTES do mesmo processo OU
(`theta=1,0`, `sigma=1,0`), seeds 555001/555002. `tau_ME=1` amostra em
ambos. `Δ_PKS=-0,411` (`p=0,23`), `Δ_beta_D2=-0,028` (`p=0,805`),
`Δ_beta_D2(|x-x*|)=-0,025` (`p=0,88`) — **nenhum canal, nenhuma
variante, mostra significância espúria.** Corretamente calibrado.

### Controle positivo — `PKS` (poço-duplo biestável, rank-remap)

PRE = OU (unimodal, difusão constante). POST = SDE biestável clássico
`dX=(X-X^3)dt+sigma*dW` (`sigma=0,75`), rank-remapeado sobre a
distribuição empírica EXATA do PRE (mesma técnica já usada nesta linha
em RQA/PE/VG). Trajetória bruta confirmada genuinamente bimodal antes
do remap (fração perto do poço `+1`: 45,6%; perto do poço `-1`: 42,2%;
perto da barreira: 12,2% — bem distribuída, não presa em um poço só).
`tau_ME=1` amostra. `PKS` pré=0,247, pós=**−0,825** (platicúrtica,
consistente com bimodalidade), `Δ_PKS=−1,071`, **`p_PKS=0,005`**
(sigma-equivalente ≈ −2,04σ). **`PKS` detecta a bimodalidade de forma
limpa e forte**, exatamente como previsto pela justificativa teórica de
`METHODOLOGY_NOTE.md` (Livina & Lenton 2007/2010).

### Controle positivo dedicado — `beta_D2` (difusão dependente de estado)

O controle do poço-duplo acima tem difusão CONSTANTE (só a deriva é
bimodal) — não é o teste certo para `beta_D2`, que mede dependência de
estado do RUÍDO, não da deriva. Controle dedicado: PRE = mesmo OU.
POST = `dX=-theta*X*dt+sigma*(1+|X|)*dW` (`theta=1,0`, `sigma=0,6`) —
difusão genuinamente multiplicativa/dependente de estado, deriva linear
simples (sem bimodalidade), rank-remapeado sobre o PRE. `tau_ME=1`
amostra.

- **`beta_D2` vs. `x`:** pré=0,007, pós=−0,067, `Δ=−0,074`,
  **`p=0,405`** — não significativo.
- **`beta_D2` vs. `|x-x*|`** (variante alternativa explicitamente
  autorizada por `METHODOLOGY_NOTE.md` Gap (b), `x*` fixado UMA VEZ a
  partir do zero de `D1` do PRE real, reaplicado a POST/substitutos):
  pré=0,015, pós=0,006, `Δ=−0,009`, **`p=0,95`** — também não
  significativo, e com magnitude ainda menor que a variante linear.
- **Bootstrap de blocos móveis (Kunsch 1989, fallback pré-autorizado)**
  tentado no mesmo controle: `Δ_beta_D2=-0,074`, nula bootstrap
  média≈−0,065, desvio≈0,249, **`p=0,77`** — TAMBÉM não significativo.

## Veredito de poder IAAFT — por canal, honesto, sem forçar a hipótese a priori

| Canal | `p` positivo | `p` negativo | Veredito |
|---|---|---|---|
| `PKS` | 0,005 | 0,23 | **`IAAFT_HAS_REAL_POWER`** |
| `beta_D2` (vs. `x`) | 0,405 | 0,805 | `IAAFT_LOW_POWER` |
| `beta_D2` (vs. `\|x-x*\|`) | 0,95 | 0,88 | `IAAFT_LOW_POWER` |

## Questão em aberto para a sessão orquestradora — `beta_D2` não separa nem sob IAAFT nem sob bootstrap de blocos

Esta validação encontra DOIS modos de falha possíveis, per a tarefa, e
tentou distingui-los explicitamente, não confundi-los:

**(a) Poder baixo de IAAFT especificamente** — a correção pré-
autorizada é trocar para o bootstrap de blocos móveis (Kunsch 1989) e
revalidar. **Feito** (seção acima): o bootstrap de blocos TAMBÉM não
encontra significância (`p=0,77`), com a mesma ordem de grandeza de
`Δ` real e nulo. Isso descarta uma miscalibração específica do IAAFT
como explicação completa — o problema não desaparece ao trocar o teste
de significância.

**(b) Problema na implementação do teste CK** — não se aplica aqui:
o diagnóstico de correção de código (seção acima) confirma
`CK_TEST_CORRECT`, e `tau_ME` é encontrado corretamente (`=1` amostra)
em todos os controles, incluindo este.

**Explicação alternativa, investigada e reportada honestamente:** a
técnica de rank-remap em si — usada com sucesso nesta linha para
controles positivos de RQA/PE/VG (estatísticas mais robustas a
reparametrização) — pode não ser adequada para validar `beta_D2`
especificamente. Rank-remap é uma transformação estritamente monótona
mas, em geral, NÃO LINEAR (já que a distribuição bruta do gerador de
difusão dependente de estado e a distribuição OU do PRE têm formatos
diferentes). Verificação direta: o próprio `D2(x)` bruto do gerador de
difusão dependente de estado, medido em SUAS PRÓPRIAS coordenadas
nativas (sem nenhum remap), já é em forma de U (assimétrico em torno de
zero por construção — `D2(x)~(1+|x|)^2`, uma função par/simétrica), e
a variante `|x-x*|` (desenhada especificamente para capturar uma
relação par-simétrica) AINDA mostrou poder baixo depois do remap — ou
seja, a distorção do remap parece severa o bastante para embaralhar até
o sinal já linearizado por desenho. Isso é consistente com (mas não
prova definitivamente) uma distorção Jacobiana do remap: pelo lema de
Itô, aplicar uma transformação monótona não linear `f` a um processo
com difusão CONSTANTE introduz uma difusão efetiva DEPENDENTE DE ESTADO
na coordenada transformada, `D2_Y(y) ~ f'(f^{-1}(y))^2 * D2_X`, só pela
Jacobiana local do remap — o que também significa que um sinal de
`beta_D2` em qualquer controle baseado em remap não pode ser atribuído
sem ambiguidade a dinâmica multiplicativa genuína vs. artefato de
Jacobiana, nos dois sentidos (poderia mascarar um sinal genuíno OU criar
um espúrio).

**Esta sessão NÃO decide unilateralmente como resolver isso** — seria
uma decisão de DESENHO de validação (ex. construir um controle positivo
para `beta_D2` que não dependa de rank-remap, talvez gerando POST
diretamente com a MESMA marginal teórica do PRE por construção do
processo em vez de remap pós-hoc), fora do escopo dos dois modos de
falha explicitamente autorizados por esta tarefa (poder baixo de IAAFT
→ bootstrap de blocos; bug de implementação do CK → debugar). Ambos
foram tentados e nenhum resolve o achado. Fica registrado aqui para a
sessão orquestradora decidir: (i) aceitar `beta_D2` como um canal de
poder desconhecido/não estabelecido nesta rodada de validação sintética
(a informação que ele carregar em dado real precisaria ser interpretada
com essa ressalva, ou tratado como diagnóstico adicional em vez de
canal primário de decisão, análogo ao que já foi feito com `d_B` em
`grafo-de-visibilidade`); (ii) autorizar uma nova rodada de validação
com um desenho de controle positivo diferente para `beta_D2`
especificamente; ou (iii) prosseguir para dado real usando `PKS` como
canal de decisão primário (que tem poder real, limpo e bem calibrado) e
reportar `beta_D2` (ambas as variantes) como companheiro exploratório,
com esta ressalva declarada explicitamente em qualquer resultado real.

## `kappa` (diagnóstico, nunca usado em nenhum p-valor acima)

Reportado por completude em todos os controles (`delta_kappa` no
controle negativo e no positivo), nunca alimentado em nenhuma lógica de
significância/decisão em `km_common.py` — demoção a priori já decidida
em `METHODOLOGY_NOTE.md` com base na identidade algébrica de Ritchie &
Sieber (2016) com AC1/variância, não uma descoberta pós-hoc desta
validação.

## Nenhum desvio metodológico não declarado

Toda decisão de implementação que se afastou de uma leitura
absolutamente literal do texto de `METHODOLOGY_NOTE.md` está
documentada explicitamente, tanto no código (`km_common.py`) quanto
nesta nota: a correção do bootstrap do teste CK (dois problemas, ambos
descobertos e corrigidos ANTES de qualquer controle estocástico, exigido
pela tarefa) e a exploração da variante `beta_D2 vs. |x-x*|`
(explicitamente pré-autorizada pelo próprio texto do Gap (b), "testado
e reportado com o que for mais estável", não uma invenção desta
sessão). Nenhuma decisão sobre PRE/POST, bins, `tau_ME`, `MAX_N_PER_
SEGMENT`, IAAFT, ou a demoção de `kappa` foi alterada.

## Próximo passo

Aguardar decisão da sessão orquestradora sobre a questão em aberto de
`beta_D2` (seção acima) antes do passo de dado real (EUR/CHF
tick-a-tick, choque SNB; PhysioNet `vfdb` registro 418) — que é, de
qualquer forma, um passo SEPARADO desta tarefa, não iniciado aqui. Este
laboratório permanece pronto para chamar `run_km_analysis` sem
modificação assim que o dado real for buscado e a proveniência
documentada, seguindo `05_DISCOVERY_LAB/00_GOVERNANCE/AGENTS.md`.
