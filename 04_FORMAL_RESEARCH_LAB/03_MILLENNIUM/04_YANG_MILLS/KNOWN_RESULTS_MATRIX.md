# Matriz de resultados conhecidos — YM-LIMIT-001

Cada linha classifica o item como **Verificado** (citação recuperável via
WebSearch nesta sessão, 2026-08-09) ou **Aproximado** (lido do documento
legado `ANALISE_CRITICA_YM.md` ou de memória de treino, sem fonte primária
conferida nesta sessão). Detalhes e URLs completos em
`REVIEWS/AUDIT_REPORT.md`.

| Item | Estado interno | Classificação | Fonte |
|---|---|---|---|
| Enunciado oficial Clay (Jaffe–Witten) | referência | **Verificado** | claymath.org/millennium/yang-mills-the-maths-gap/ |
| Wilson lattice gauge action (1974) | rede/acoplamento forte | **Aproximado** | citado no legado; não reconfirmado nesta sessão |
| Balaban, UV stability, rede 3D pura de gauge, CMP 102 (1985) | UV/rede | **Verificado** (este artigo específico, 3D) | Comm. Math. Phys. 102(2):255-275, doi:10.1007/BF01229380 |
| Extensão dos bounds de Balaban a 4D / séries 1984-1989 completas | UV/rede | **Aproximado** | mencionado no legado como "programa nunca completado em forma publicada unificada"; não reconfirmado item a item nesta sessão |
| Extensão SU(2) → SU(N) dos bounds de Balaban | UV/rede | **Aproximado** — sinalizado como gap não fechado, não como resultado disponível | legado, seção 3.1 e 6.2 |
| Strong coupling / area law / string tension > 0 ⇒ gap (regime IR) | IR | **Aproximado** | resultado padrão da literatura de rede citado no legado; não reconfirmado com referência primária nesta sessão |
| Svetitsky–Yaffe, universalidade de deconfinamento (1982) | interpolação | **Verificado** (existência e conteúdo do resultado, como *conjectura/análise de universalidade* de transição térmica) | arxiv.org/pdf/hep-lat/9701014 e outros citando "Svetitsky-Yaffe conjecture" |
| Svetitsky–Yaffe implica ausência de transição a T=0 | interpolação | **Não sustentado** — o resultado verificado é sobre transição térmica finita, não sobre o limite euclidiano a T=0 | ver `ASSUMPTIONS.md` |
| Osterwalder–Schrader, reconstrução (1975) | axiomas | **Verificado** (existência, ano, conteúdo geral: equivalência Schwinger↔Wightman sob os axiomas OS) | ncatlab.org/nlab/show/Osterwalder-Schrader+theorem; Comm. Math. Phys. (1975) |
| Osterwalder–Schrader, artigo I (1973) | axiomas | **Aproximado** — não reconfirmado nesta sessão (busca não retornou o artigo de 1973 especificamente) | — |
| Prokhorov: tightness ⇒ subsequência fracamente convergente | teoria de medida | **Verificado** | en.wikipedia.org/wiki/Prokhorov's_theorem; tratamento padrão em Billingsley, *Convergence of Probability Measures* |
| Prokhorov ⇒ limite único (sequência completa converge) | teoria de medida | **Refutado nesta auditoria como implicação geral** | ver contraexemplo abstrato, `COUNTEREXAMPLES/` e `FORMAL/InsufficiencyToyModel.lean` |
| Convergência forte de resolvente: espectro do limite não expande, mas pode contrair | análise espectral | **Verificado** | levantamento de literatura de análise espectral (survey arXiv sobre resolvent convergence, 2025); consistente com fatos padrão de Kato, *Perturbation Theory for Linear Operators* (não reconfirmado edição/ano exatos nesta sessão) |
| Gap uniforme em aproximantes ⇒ gap no limite, sem hipótese extra | análise espectral | **Refutado nesta auditoria como implicação geral** (ver contraexemplo do gap que fecha, `COUNTEREXAMPLES/`) | — |

## Nota sobre o próprio documento legado

`ANALISE_CRITICA_YM.md` já identificava os mesmos três gaps centrais
(GAP 1: bound uniforme em todo β; GAP 2: unicidade do limite; GAP 3:
preservação do gap no limite) usando linguagem informal e sem
formalização. Esta auditoria trata GAP 2 e GAP 3 como o núcleo do
`target_statement` de `YM-LIMIT-001`, fornecendo contraexemplos abstratos
formalizados (Lean, ver `FORMAL/`) para a estrutura lógica desses dois
gaps — não para os objetos físicos completos do lattice YM, que
permanecem fora do alcance desta rodada.
