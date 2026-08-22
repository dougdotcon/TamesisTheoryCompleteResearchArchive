# Verificação adversarial independente — Estágio 1 (`SPARC-FMULTI-STAGE1`)

**Data:** 2026-08-22
**Autoridade:** `DISC-DEC-023` (parte do mandato de verificação obrigatória
para frentes que produzirão infraestrutura destinada a tocar dado real no
Estágio 2)

Dois agentes independentes revisaram, cada um sem ler o relatório do outro
antes de formar sua própria opinião, os artefatos do Estágio 1
(`METHODOLOGY_ADDENDUM.md`, `PROVENANCE_CHAE_EQS.md`,
`RESULTS_SUMMARY_STAGE1.md`, os 5 scripts em `analysis/`, os dois JSONs em
`results/`).

## Frente 1 — proveniência das equações de Chae

**Veredito: SOUND.** Refetch direto (não por memória) dos e-prints LaTeX
brutos de arXiv:2305.04613 e arXiv:2309.10404, com hash sha256 conferido
contra os citados em `PROVENANCE_CHAE_EQS.md`. Confirmado
independentemente: (1) Eqs. 11-13 do Artigo A são exatamente as fórmulas de
fração de massa `kappa` / diferença de magnitude / distribuição de lei de
potência (`gamma_M`) descritas, com `gamma_M≈-0,7` (Tokovinin 2008) e
`≈-0,6` (Riddle 2015 + Raghavan 2010) citados corretamente; (2) contagem
independente de todos os ambientes de equação numerados no `.tex` bruto do
Artigo A confirma que a fórmula de projeção de velocidade mock é a Eq. 18
(label `eq:mockvpcomp`), e o `.tex` bruto do Artigo B contém literalmente
"to replace equation~(18) of \cite{chae2023}" mais um Apêndice A que declara
a Eq. 18 original "valid only for circular orbits" e dá a fórmula corrigida
— tudo batendo palavra por palavra com as citações do documento; (3) o
`delta_obs_newt.py` já travado desta linha implementa genuinamente a forma
CORRIGIDA (pós-erratum), confirmado por derivação algébrica direta mostrando
que as duas formas só coincidem em magnitude para `e=0`.

**Problemas encontrados (nenhum material):**
- `PROVENANCE_CHAE_EQS.md` §5 cita `\ref{sec:multi}` do Artigo A como
  "(Seção 3.5)" numa citação apresentada como verbatim; a numeração real
  (reconstruída da estrutura `\section`/`\subsection` do `.tex` bruto) é
  Seção 2.3, não 3.5. O resto do bloco citado é uma correspondência exata
  palavra por palavra com a fonte — é uma auto-referência interna do
  próprio Artigo A, não uma citação inserida por este repositório, e não
  afeta nenhuma equação/fórmula/valor usado no pipeline. **Registrado por
  precisão** via nota datada em `PROVENANCE_CHAE_EQS.md` (nenhuma das
  duas verificações compilou o `.tex` completo para confirmar a numeração
  real — não tratado como "corrigido", apenas documentado honestamente).
- Ano de publicação do Artigo B ("Chae 2024, ApJ") não pôde ser confirmado
  de forma independente na fonte primária (sem metadados de
  `\received`/`\accepted` no e-print) — não é uma alegação refutada, apenas
  não-verificável com o material disponível nesta sessão.
- Nota de processo (não é falha do documento revisado): uma primeira
  tentativa de verificação via renderização HTML `ar5iv` do Artigo B não
  surfaceou a citação da Eq. 18 nem o Apêndice A (provável truncamento de
  fetch) — só o download do `.tex` bruto (o mesmo método já usado pelo
  próprio documento revisado) revelou o trecho. Confirma que a escolha
  metodológica do documento original foi a correta.

## Frente 2 — auditoria adversarial de código e números

**Veredito: BUGS_FOUND** (nenhum dos 5 checks substantivos — circularidade,
números, sanidade estatística, ausência de dado real, lógica — encontrou um
erro que invalide qualquer resultado já reportado; os problemas achados são
de disciplina documental e robustez de borda, detalhados abaixo).

**Checks que PASSARAM limpos:**
1. **Circularidade:** `calibrate_f_multi()`/`run_delta_obs_newt_selfcal()`
   nunca recebem `f_multi_true`/`a0_true` como argumento, default ou
   global. A busca de bissecção usa um bracket fixo `[0,0; 0,9]` idêntico
   em todos os cenários (não estreitado perto do valor verdadeiro). A
   reutilização de semente entre tentativas de bissecção é uma técnica
   legítima de números aleatórios comuns para tornar `delta_ancora(f_multi)`
   suave/monótona; a avaliação final usa uma semente DIFERENTE
   (`seed+777`), tornando-a um teste fora-da-amostra mais forte, não um
   vazamento.
2. **Números:** todos os valores verificados nas tabelas de
   `RESULTS_SUMMARY_STAGE1.md` batem exatamente com os JSONs de origem,
   incluindo os valores derivados em dex recomputados de forma
   independente.
3. **Ausência de dado real:** confirmado por grep de toda instrução de
   import/open/read em `analysis/*.py` — nenhuma ocorrência dos nomes dos
   arquivos reais desta linha (`quality_filtered_sample.parquet`,
   `hwang_eccentricity_subset.parquet`, `discovery_holdout_split.json`,
   `catalog.parquet`).
4. **Lógica:** binagem, atribuição do bin-âncora, fórmulas de vis-viva/
   desprojeção e o compartilhamento de `Mtot_true` entre os ramos real e
   mock batem com `METHODOLOGY_ADDENDUM.md` e com as convenções já
   travadas de `delta_obs_newt.py`.

**Problemas encontrados e disposição:**

1. **[Moderado, disciplina documental — CORRIGIDO]**
   `METHODOLOGY_ADDENDUM.md` §3 afirmava que o documento foi "escrito e
   commitado antes da execução dos scripts de validação". Os timestamps do
   sistema de arquivos contradizem isso: o documento foi escrito DEPOIS dos
   `results/*.json` terem sido gerados, e nada nesta pasta estava
   commitado no momento da checagem. **Fator atenuante confirmado:** os
   limiares numéricos realmente aplicados (`TOL_F_MULTI=0,05`,
   `A0_TOL_LOG10=0,30` dex, `ANCHOR_BIN=4`, bracket de bissecção
   `[0,0;0,9]`) estavam hardcoded nos próprios scripts de validação ANTES
   das execuções — sem evidência de ajuste posterior dos critérios para
   caber no resultado. A alegação de ordem temporal do texto do adendo,
   porém, era literalmente falsa como escrita. **Corrigido** via adendo
   datado em `METHODOLOGY_ADDENDUM.md` (texto original preservado) —
   ver abaixo.
2. **[Menor, robustez de borda — CORRIGIDO NO CÓDIGO]** `fit_a0()` não
   filtrava um ajuste convergindo para `a0<=0`, ao contrário de
   `bootstrap_a0_refit()`, que já tinha esse guarda. Isso não afetou nenhum
   número já reportado (os dois cenários da Validação B convergiram para
   `a0>0` em todas as réplicas), mas era uma lacuna latente: um futuro
   `a0<=0` produziria `log10(nan)` silencioso em vez de sinalizar falha de
   convergência. **Corrigido** em `analysis/selfcal_pipeline.py::fit_a0`
   (guarda `a0_fit>0` adicionada, espelhando `bootstrap_a0_refit`).
   Re-executada `validate_b_recover_a0_with_contamination.py` após a
   correção: resultados **idênticos** aos já reportados (`a0_fit_corr`,
   IC95%, vereditos B1/B2/B3 — todos batem à precisão já publicada),
   confirmando que a correção é um no-op para os números já catalogados,
   apenas fecha a lacuna para o Estágio 2. Ver `results/validation_B_run.log`
   (timestamp de reexecução 2026-08-22T14:10Z) e
   `results/validation_B_results.json` (timestamp 2026-08-22T14:08Z).
3. **[Menor, ressalva estatística — NÃO corrigido, documentado como
   limitação para o Estágio 2]** `N_bootstrap=400`/`N_bootstrap_a0_refit=300`
   são baixos para um IC95% percentil preciso (~7-10 réplicas definem cada
   cauda). Isso não invalida o método (percentil + alpha=0,05 corretos),
   mas significa que a margem "por pouco" do cenário 1 da Validação B
   (limite inferior do IC `1,47×10⁻¹⁰` vs. `a0_true=1,20×10⁻¹⁰`) não deve
   ser lida como precisamente calibrada. Recomendação para o Estágio 2:
   `N_bootstrap>=1000-2000`.
4. **[Menor, risco de manutenção — NÃO corrigido, documentado]** a lógica
   de atribuição de bin é reimplementada inline em 2 lugares em vez de
   chamar o helper já travado `delta_obs_newt.assign_bins_by_projected_gN`
   — atualmente byte-a-byte idênticas, mas um risco latente de divergência
   silenciosa numa edição futura. Recomendação para o Estágio 2: consolidar
   num único helper compartilhado antes de estender o pipeline.
5. **[Cosmético, sem ação]** `gN_bin_median` calculado via
   `np.exp(np.log(10)*x)` em vez de `10.0**x` — equivalente, apenas
   inconsistência de estilo.

## Veredito de integração

Nenhum dos achados desta verificação adversarial altera qualquer número
substantivo já publicado em `RESULTS_SUMMARY_STAGE1.md` — os dois
problemas com efeito real (documentação da ordem temporal; lacuna de
robustez em `fit_a0`) foram corrigidos, com o código re-executado
confirmando resultados idênticos. O veredito de prontidão do Estágio 1
("pronto para o Estágio 2, com a ressalva de viés residual em `a0` já
documentada") permanece válido, agora com duas ressalvas adicionais
honestas (tamanho de bootstrap; duplicação de lógica de binagem) a levar
para o desenho do Estágio 2.
