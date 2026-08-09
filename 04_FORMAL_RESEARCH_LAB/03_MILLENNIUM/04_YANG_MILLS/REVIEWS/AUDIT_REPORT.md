# Relatório de auditoria — YM-LIMIT-001

Data: 2026-08-09. Autoridade: `PORTFOLIO-REVIEW-AFTER-SOBOLEV-CHAIN-2026-08-09`.

Postura epistêmica exigida (ver
`04_FORMAL_RESEARCH_LAB/01_PORTFOLIO/PORTFOLIO_REVIEW_AFTER_SOBOLEV_CHAIN.md`):
esta auditoria tenta reconstruir, a partir de literatura que só pode ler em
parte, um resultado que não tem acesso direto. As duas seções abaixo são
mantidas estritamente separadas — nada é movido de "Aproximado" para
"Verificado" sem uma citação recuperável nesta sessão.

## Verificado

Afirmações com citação recuperável via WebSearch nesta sessão
(2026-08-09), ou checadas por Lean/Python nesta sessão.

1. **Enunciado oficial do problema do milênio Yang–Mills.** "Prove that
   for any compact simple gauge group G, a non-trivial quantum Yang–Mills
   theory exists on ℝ⁴ and has a mass gap Δ > 0." Fonte: Clay Mathematics
   Institute, https://www.claymath.org/millennium/yang-mills-the-maths-gap/.

2. **Balaban, T. (1985), "Ultraviolet stability of three-dimensional
   lattice pure gauge field theories", Communications in Mathematical
   Physics, 102(2), pp. 255-275, doi:10.1007/BF01229380.** Confirmado
   título, ano, volume e páginas via WebSearch (Springer Nature Link,
   mindat.org reference entry). Nota: este artigo específico trata do
   caso **tridimensional**; a extensão a 4D é mencionada em fontes
   secundárias como parte de uma série de artigos 1984-1989 de Balaban,
   mas não foi verificada item a item nesta sessão (ver seção
   Aproximado).

3. **Osterwalder, K.; Schrader, R. (1975), teorema de reconstrução,
   Communications in Mathematical Physics.** Confirmado via WebSearch
   (nLab, "Osterwalder-Schrader theorem") que o resultado de 1975
   estabelece as condições sob as quais funções de Schwinger euclidianas
   satisfazendo os axiomas OS podem ser usadas para construir
   distribuições que satisfazem os axiomas de Wightman (reconstrução
   Euclidiano → Minkowski / Wick rotation).

4. **Svetitsky, B.; Yaffe, L. G. (1982) — conjectura/argumento de
   universalidade de deconfinamento.** Confirmado via WebSearch (múltiplas
   fontes secundárias, incluindo arXiv:hep-lat/9701014 "The Svetitsky-Yaffe
   conjecture for the plaquette operator") que o resultado trata da
   universalidade da **transição de deconfinamento a temperatura finita**
   de uma teoria de gauge \(D\)-dimensional, mapeada para a classe de
   universalidade do modelo de spin \((D{-}1)\)-dimensional com a simetria
   de centro de \(G\). É referido nas fontes recuperadas como
   *conjectura*/argumento de universalidade, não como teorema totalmente
   rigoroso em toda generalidade.

5. **Prokhorov (teorema).** Confirmado via WebSearch (Wikipedia,
   "Prokhorov's theorem"; tratamento padrão remetido a Billingsley,
   *Convergence of Probability Measures*) o enunciado em duas partes:
   (a) tightness de uma família de medidas de probabilidade implica que
   toda sequência na família tem subsequência fracamente convergente;
   (b) em espaço métrico completo separável, a família é tight se e
   somente se toda subsequência tem uma sub-subsequência fracamente
   convergente para uma medida de probabilidade. Nenhuma das duas partes
   afirma convergência da sequência completa nem unicidade do limite —
   ponto central desta auditoria.

6. **Semicontinuidade espectral sob convergência forte de resolvente.**
   Confirmado via WebSearch (levantamento de literatura de análise
   espectral, incluindo survey arXiv de 2025 sobre convergência de
   resolvente) o fato padrão: sob convergência forte de resolvente de
   operadores autoadjuntos, o espectro do limite não pode *expandir*
   (semicontinuidade superior), mas pode *contrair repentinamente* — ou
   seja, um gap espectral nos aproximantes não é garantido no limite sem
   hipótese adicional de uniformidade.

7. **Os dois lemas de insuficiência abstratos** (`toyGap_no_unique_
   continuum_limit`, `finite_volume_gap_does_not_survive_without_
   uniform_bound`) foram checados nesta rodada paralela apenas por
   leitura manual e grep — deliberadamente sem `lake build` (regra de
   isolamento do cache compartilhado). **Atualização (integração
   serial, mesma sessão):** a sessão orquestradora rodou `lake env lean`
   sobre `FORMAL/InsufficiencyToyModel.lean` fora desta etapa paralela;
   três correções foram necessárias (duas reduções de lambda sob
   `StrictMono`, uma `def` de divisão real marcada `noncomputable`) e o
   arquivo agora compila com `exit 0`; `#print axioms` nos dois lemas
   confirma `[propext, Classical.choice, Quot.sound]` — ver
   `LAB_STATE.md`, seção "Integração". A verificação por compilação real
   está, portanto, feita; o status da frente continua `PARTIAL_RESULT`
   porque nenhuma revisão de conteúdo substitui compilação, mas por
   outro motivo: o teorema é sobre a estrutura lógica abstrata, não
   sobre a medida real de Yang-Mills.

## Aproximado

Lido do documento legado `RECURSOS_PARA_PESQUISA/07_MILLENNIUM_VALIDATION/
PROBLEM_04_YANG_MILLS/ANALISE_CRITICA_YM.md` (somente leitura) ou de
memória de treino, sem fonte primária conferida nesta sessão.

1. **Wilson (1974), formulação de rede da teoria de gauge.** Citado no
   legado como base rigorosa; não reconfirmado com WebSearch nesta sessão.

2. **Extensão completa dos bounds UV de Balaban para todo o programa
   1984-1989 e para dimensão 4.** O legado afirma "programa nunca foi
   completado em forma publicada unificada"; esta sessão confirmou apenas
   um artigo específico (item 2 da seção Verificado, caso 3D) e não
   reconstituiu a série completa nem confirmou cobertura em 4D.

3. **Extensão SU(2) → SU(N) dos resultados de Balaban "por
   universalidade".** Tratado no legado como gap explícito, não como
   resultado disponível — esta sessão não encontrou nem buscou uma prova
   publicada dessa extensão; permanece como gap (`YM-GAP-005`).

4. **Strong coupling / area law ⇒ string tension > 0 ⇒ gap, regime IR.**
   Citado no legado como "resultado standard"; não reconfirmado com
   referência primária nesta sessão.

5. **Osterwalder–Schrader, artigo I (1973).** A busca desta sessão não
   retornou confirmação específica do artigo de 1973 (usualmente citado
   junto com o de 1975 como o par fundacional); apenas o artigo de 1975
   foi confirmado com detalhe (ver Verificado, item 3).

6. **Detalhes técnicos de Kato, *Perturbation Theory for Linear
   Operators*, como referência padrão para semicontinuidade espectral.**
   Citado de memória de treino como a referência clássica para o fato do
   item 6 da seção Verificado; edição e capítulo exatos não foram
   confirmados nesta sessão — o *fato* está confirmado via literatura
   secundária de 2025 (item 6, Verificado), a *atribuição* a Kato
   especificamente não está.

7. **A construção específica do Contraexemplo 3**
   (`COUNTEREXAMPLES/ABSTRACT_COUNTEREXAMPLES.md#contraexemplo-3`,
   operador \(H_n = 0 \oplus M_{f_n}\), \(f_n=\max(x,1/n)\)) é autoral
   desta sessão — uma instância concreta do fato geral verificado no item
   6, não uma citação de nenhuma fonte. Não formalizada em Lean.

## Resumo da separação

Nenhuma afirmação da seção "Aproximado" foi usada como premissa de um
lema Lean nesta rodada. Os dois lemas Lean (`toyGap_no_unique_continuum_
limit`, `finite_volume_gap_does_not_survive_without_uniform_bound`)
dependem apenas de análise real elementar (Bolzano–Weierstrass,
Arquimedianidade), não de nenhum resultado citado nesta seção — são
autocontidos e não usam nenhuma referência externa como hipótese.
