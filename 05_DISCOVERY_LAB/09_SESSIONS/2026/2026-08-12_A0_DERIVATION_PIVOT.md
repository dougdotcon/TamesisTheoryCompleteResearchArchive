# Sessão 2026-08-12 — Pivô SPARC-002: qual derivação interna de a₀ sobrevive ao dado real

## Contexto

Continuação da sessão que criou `05_DISCOVERY_LAB` e adotou a arquitetura
de três motores (`DISC-DEC-003`). Usuário pediu para priorizar, entre as
três linhas candidatas registradas, aquela com "mais riqueza de
ferramentas... e onde podemos fazer descobertas em curto/médio prazo".
Escolhida `DISC-COSMOLOGY-MOND-SPARC-002` (dado SPARC já baixado e
verificado, modelo concorrente com fórmula pública — ver detalhamento
abaixo).

## O que aconteceu

1. **Busca obrigatória pelo `next_action` original** (extrair de
   `01_TAMESIS_CORE` uma previsão Tamesis quantitativa distinta de MOND
   genérico, com fonte exata arquivo:linha) — resultado **negativo**:
   nenhuma previsão dessas existe. Todo lugar do repositório que toca
   dinâmica galáctica cita `a₀=1,2×10⁻¹⁰` de McGaugh et al. (2016)
   diretamente, e usa a função de interpolação "simple" padrão (Famaey &
   Binney 2005) — as próprias notas de auditoria internas já admitem
   isso (`02_MOND_Emergence/AUDITORIA.md:3`,
   `02_Holographic_Uniqueness/AUDITORIA.md:3`).
2. **Achado adicional, verificado por recálculo direto**: o corpo teórico
   contém duas derivações internas conflitantes de `a₀`, nunca testadas
   uma contra a outra: (A) `a₀=cH₀/(2π)` (Ponte Holográfica,
   `mond_derivation_proof.py:28`) ≈ 1,08×10⁻¹⁰; (B) `a₀=cH₀` (MOND
   Emergence, `index.html:282`) — cuja própria alegação numérica
   "≈1,2×10⁻¹⁰" é aritmeticamente incorreta por fator ~5,7 (o valor real
   de `cH₀` com H₀=70 km/s/Mpc é ~6,8×10⁻¹⁰), independente de qualquer
   comparação com dado externo.
3. **Pivô** (`DISC-DEC-004`): teste redesenhado para perguntar qual das
   duas derivações sobrevive ao contato com dado real, em vez de forçar
   um pré-registro sobre uma previsão inexistente.
4. **Pré-registro travado** (`PREREGISTRATION.md`) ANTES de qualquer
   cálculo: H_A vs. H_B, estatística de teste (ajuste não-linear de
   `g†` + IC bootstrap 95% por galáxia), critério de falsificação, split
   discovery(120)/holdout selado(55) gerado com seed determinístico e
   commitado.
5. **Fórmula do modelo concorrente verificada por fetch direto**:
   McGaugh, Lelli & Schombert (2016, PRL 117, 201101) — `Υ_disk=0,50`,
   `Υ_bul=0,7` M☉/L☉, quadratura com preservação de sinal.
6. **Análise rodada** sobre a amostra de descoberta (120 galáxias, 2327
   pontos). **Bug numérico real encontrado e corrigido durante a própria
   execução**: `scipy.optimize.curve_fit` sem reescala "convergia"
   silenciosamente para o próprio palpite inicial (underflow do
   Jacobiano numérico em escala absoluta ~10⁻¹⁰) — verificado testando
   múltiplos `p0` e vendo cada um "convergir" para perto de si mesmo.
   Corrigido reescalando para unidades de 10⁻¹⁰ antes do ajuste.
7. **Resultado**: `g†` ajustado = 1,1977×10⁻¹⁰ m/s² (0,2% do valor
   publicado — checagem de sanidade passa). IC bootstrap 95% =
   [6,76×10⁻¹¹, 2,78×10⁻¹⁰]. `a₀_A` dentro do IC (H_A sobrevive); `a₀_B`
   fora por fator ~2,5× (H_B falsificada).
8. **Reexecução adversarial independente** (agente separado, código
   próprio, escrito antes de ler o script primário): reproduziu N de
   pontos, N excluídos, e `g†` (0,004% de diferença) — e redescobriu o
   mesmo bug numérico de forma independente antes de corrigi-lo.
   Verificou robustez: ajuste em espaço log dá `g†` mais baixo mas H_B
   continua falsificada por margem grande (~7×); excluir o pior outlier
   não muda o veredito. **Veredito: CONFIRMED.**

## Resultado após reexecução adversarial de primeira linha (não é o final)

`DISC-CLAIM-002` inicialmente registrado: `preregistered_falsified` (para
H_B), `adversarial_review_verdict: CONFIRMED`. Ao contrário do piloto
anterior (`DISC-CLAIM-001`, p=0,049, zona frágil), este parecia um
resultado **decisivo e robusto** na amostra de descoberta: a falsificação
de H_B não dependia de escolhas de implementação (linear vs. log, com/sem
outlier).

## Gate de Replicação (acionado a pedido do usuário) — resultado final

Dois agentes independentes, nenhum dos dois tendo participado da análise
primária nem da primeira reexecução adversarial:

1. **Abertura do holdout (55 galáxias, primeira vez na história deste
   teste).** Proveniência re-auditada do zero (checksums batem,
   correspondência 175/175 catálogo↔rotmod confirmada por conta própria).
   Código independente validado reproduzindo a amostra de descoberta a 5
   casas decimais antes de aplicar ao holdout. Resultado no holdout:
   `g†=4,1518×10⁻¹⁰` m/s² (bem diferente da descoberta), IC 95%=
   `[8,02×10⁻¹¹, 9,07×10⁻¹⁰]` — largo o suficiente para conter **tanto**
   `a₀_A` **quanto** `a₀_B`. Diagnóstico: 3 de 55 galáxias respondem por
   91,7% da soma pooled de `g_bar²` no holdout (vs. 58,9% na descoberta) —
   concentração de leverage que explica a discrepância sem indicar erro.
   **Veredito do Gate: `REPLICATION_FAILED_INCONCLUSIVE`** — não
   contradiz o achado de descoberta, mas também não o confirma de forma
   independente.

2. **Adversário de nulo dedicado** (papel definido em
   `METHODOLOGY_EXTENSIONS.md` §5 — tentar explicar o resultado sem
   Tamesis, não recheckar a matemática). Achados quantitativos:
   - O IC de 95% da descoberta é largo o suficiente que **~20-30%** de um
     prior log-uniforme razoável para `a₀` cairia dentro dele por acaso —
     `H_A` sobreviver é evidência real mas modesta (poder discriminativo
     ~3-5×), não rejeição decisiva de candidatos genéricos.
   - Sistemáticas SPARC conhecidas (quality flag, corte de inclinação,
     erro de distância até 30% coerente) deslocam `g†` por apenas 1-16% —
     muito aquém do necessário (~5,7×) para reconciliar `H_B`. A
     falsificação de `H_B` na descoberta **sobrevive** ao debunking.
   - **Achado novo**: `a₀_A=cH₀/(2π)` reproduz uma coincidência numérica
     já conhecida na literatura MOND padrão, décadas antes de Tamesis
     (Milgrom, arXiv:2001.09729) — reduz o poder discriminativo
     específico de Tamesis do resultado.
   - **Achado acionável independente do veredito estatístico**:
     `MOND_Emergence/index.html:282` provavelmente contém um erro de
     copy-paste — o número "≈1,2×10⁻¹⁰" citado ali para `a₀=cH₀` é quase
     certamente o resultado da OUTRA derivação (`cH₀/2π`), mal rotulado.
   - Verdict do adversário: **WEAKENED-BUT-STILL-VALID**.

## Estado final de DISC-CLAIM-002 (após integração completa)

`evidence_level`: `preregistered_inconclusive` (rebaixado de
`preregistered_falsified` — a totalidade do processo, incluindo o Gate,
não sustenta mais uma linguagem decisiva). `replication_status`:
`REPLICATION_FAILED` (inconclusivo, não contraditório).
`promoted_to_formal_lab`: `false` (achado empírico, sem núcleo
matemático demonstrável — nunca seria promovido a Lean independente do
Gate). Ver `CLAIM_LEDGER.yaml` para o detalhamento completo,
`known_gaps` e `counterevidence` atualizados com todos os achados acima.

## Prohibited claims explícitos para este resultado

- Não é "Tamesis vs. ΛCDM" — ambas H_A e H_B são internas a Tamesis.
- Não confirma a derivação "Ponte Holográfica" como correta — apenas que
  não foi falsificada pela amostra de descoberta (e o Gate não decidiu
  nem a favor nem contra).
- A derivação "MOND Emergence" (`a₀=cH₀`) permanecer válida — a amostra
  de descoberta a falsifica; deveria ser corrigida em `01_TAMESIS_CORE`
  (achado adicional: provavelmente já é um erro de copy-paste, não uma
  alegação deliberada).
- `REPLICATION_PASSED` ou qualquer linguagem que sugira Gate bem-sucedido
  — o resultado é `REPLICATION_FAILED_INCONCLUSIVE`.

## Lição para a arquitetura de três motores

Este é o primeiro uso real do Gate de Replicação, e ele fez exatamente o
que foi desenhado para fazer: um resultado que parecia forte e robusto na
reexecução adversarial de primeira linha (mesmo laboratório, dado
parcial) não sobreviveu ao padrão de evidência mais alto (dado nunca
visto, terceiro agente, debunking dedicado). Isso valida a arquitetura —
não é uma falha do teste, é a barreira extra funcionando.

## Estado final desta linha

`DISC-COSMOLOGY-MOND-SPARC-002` está encerrado nesta forma:
`REPLICATION_FAILED` em `TEST_QUEUE.yaml`. Nenhuma ação pendente. Reabrir
a pergunta específica (qual derivação de `a₀` é compatível com dado real)
exigiria um novo split discovery/holdout e um novo pré-registro — este
holdout já foi consumido. O achado de que
`MOND_Emergence/index.html:282` provavelmente contém um erro de
copy-paste é acionável de forma independente, fora do escopo desta
trilha, para quem mantém `01_TAMESIS_CORE`.
