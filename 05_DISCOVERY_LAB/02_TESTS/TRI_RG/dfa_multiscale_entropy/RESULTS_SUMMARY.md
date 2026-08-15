# Resultado do fechamento dos gaps — `dfa-multiscale-entropy`

**Data:** 2026-08-14. Metodologia fixada em `METHODOLOGY_NOTE.md` (commits
`50d21ac`, `e06ce3a`) — incluindo um adendo pós-validação (bootstrap por
blocos móveis, adicionado depois que a validação sintética revelou baixo
poder do teste IAAFT original para `alpha`, ANTES de qualquer dado real).
Pipeline (`analysis/dfa_common.py`) validada contra dado sintético
(`analysis/validation_synthetic.json`, commit `dd9ee5b`) e aplicada sem
modificação aos 2 domínios (fisiologia/PhysioNet Apnea-ECG `a04`,
paleoclima/GISP2), com checagem adversarial completa no domínio que
mostrou efeito forte.

## Domínio 1 — Apneia-ECG (PhysioNet `a04`, 35 min normal → 140 min apneia severa)

| Variante | canal | Δalpha | p (IAAFT, bicaudal) | p (bootstrap, PRIMÁRIO) |
|---|---|---|---|---|
| Primária | alpha | −0,134 | 0,800 | **0,000** |
| Primária | alpha1 | +0,569 | 0,045 | **0,000** |
| Primária | alpha2 | −0,366 | 0,845 | **0,000** |
| Robustez | alpha | −0,169 | 0,990 | **0,018** |
| Robustez | alpha1 | +0,334 | 0,120 | **0,024** |
| Robustez | alpha2 | −0,346 | 0,960 | **0,002** |

Todos os 6 testes de bootstrap (teste primário desta linha, per adendo da
metodologia) significativos. O IAAFT (secundário) só confirma 1 dos 6
(`alpha1` primária, `p=0,045`) — divergência já esperada pela própria
validação sintética, que mostrou que o IAAFT tem pouco poder para `alpha`.

## Reexecução adversarial — domínio 1

Reprodução cega independente (extração de RR do zero, sem ler código/
resultado do primeiro agente): segmentos primários batem essencialmente
byte a byte (diferenças ~1e-13). Variante de robustez teve uma
DIVERGÊNCIA REAL de contagem (1373/4597 vs 1303/4615 RR) — origem
identificada: ambiguidade não resolvida na `METHODOLOGY_NOTE.md` sobre se
"50% mais recentes/próximos" se refere a 50% do TEMPO ou 50% da CONTAGEM
de amostras/intervalos (a convenção de contagem foi a usada, por
consistência com domínios de amostragem irregular como GISP2) — não muda
o veredito qualitativo em nenhuma das duas leituras.

Checagens adversariais adicionais:
- **Winsorização 1%/99%** (possíveis batimentos ectópicos): efeito
  sobrevive integralmente, até fortalece em `alpha1` — não é artefato de
  outlier.
- **Truncamento severo do POST (12 min colado à fronteira):** `alpha`
  completo PERDE significância (`p_bootstrap=0,714`); `alpha1`/`alpha2`
  continuam significativos. O efeito no canal `alpha` completo depende de
  janela POST razoavelmente longa.
- **Trajetória dentro do POST** (4 sub-blocos de ~35 min): não é um degrau
  abrupto na fronteira nem uma deriva monotônica — é flutuante
  (0,944→0,872→0,762→0,810→0,911), consistente com a natureza CÍCLICA da
  apneia já declarada como limitação a priori na `METHODOLOGY_NOTE.md`.

## Descoberta adversarial de nulos — domínio 1 (decisiva)

Um agente dedicado tentou explicar o achado por mecanismo convencional:

1. **Desequilíbrio de N (rejeitado):** nulo sintético com o MESMO N real
   (fGn de H fixo) produz `Delta alpha1` com desvio-padrão ~0,02-0,04; o
   real observado (+0,569/+0,334) fica 7-23 desvios-padrão longe — não é
   artefato de tamanho de amostra.
2. **Contaminação por ectópico (rejeitado e invertido):** PRE tem MAIS
   saltos grandes de RR que POST (2,69% vs 1,06%); winsorização
   FORTALECE o efeito, o oposto do esperado se fosse artefato de outlier.
3. **Deriva/hora da noite (não totalmente descartável):** o efeito já
   aparece quase completo nos primeiros 12 min de apneia e não cresce
   monotonicamente ao longo de 140 min — mas não existe, dentro de `a04`,
   nenhum segmento `N` tardio para controlar estágio do sono, e a própria
   literatura fundadora (Penzel et al. 2003, *Computers in Cardiology*
   30:307-310) mostra que DFA discrimina ESTÁGIO DO SONO melhor que
   severidade de apneia (78,4%/85,0% vs 60,1%/74,4%) — confusão com
   estágio do sono não pode ser descartada com um único registro.
4. **Mecanismo mundano positivo encontrado — CVHR (Cyclical Variation of
   Heart Rate):** análise espectral direta dos RR do POST mostra um pico
   periódico dominante de ~41-48 batimentos (~38-44s, consistente com
   AHI=77,4/h documentado, ~46,5s/evento) responsável por 73,7% da
   potência espectral relevante ao DFA no POST (vs 18,3% no PRE) —
   mecanismo fisiológico já descrito desde Guilleminault et al. 1984,
   explica sozinho a direção `alpha1↑`/`alpha2↓` observada.
5. **Viés de seleção do registro (não resolvido):** só `a04` foi levado a
   resultado final; os 3 registros de backup mapeados pelo agente de busca
   original (`a18`, `a14`, `a01`) nunca foram executados.

## Domínio 2 — Paleoclima (GISP2, Younger Dryas→Preboreal, mesmo dado de `critical-slowing-down`)

| Variante | canal | Δalpha | p (IAAFT, bicaudal) | p (bootstrap, PRIMÁRIO) |
|---|---|---|---|---|
| Primária | alpha | +0,362 | 0,000 | 0,126 |
| Primária | alpha1 | +0,082 | 0,425 | 0,466 |
| Primária | alpha2 | +0,538 | 0,000 | 0,506 |
| Robustez | alpha | +0,196 | 0,075 | 0,458 |
| Robustez | alpha1 | −0,030 | 0,915 | 0,042* |
| Robustez | alpha2 | +0,011 | 0,945 | 0,996 |

\* IC95% de `alpha1`/robustez é inteiramente positivo (`[0,005; 0,908]`)
apesar da estimativa pontual do delta real ser NEGATIVA — assimetria/viés
do estimador bootstrap, não interpretado como sinal real (o próprio agente
que rodou este domínio já sinalizou isso explicitamente, sem
sobre-interpretar).

**5 dos 6 testes de bootstrap (o teste primário desta linha) NÃO
significativos.** Nenhum sinal cross-domain replicado em GISP2.

## Veredito honesto

`dfa-multiscale-entropy`, como formulado e testado aqui (mesma pipeline
`I(X)`=DFA-alpha, sem reformulação por domínio, aplicada a uma transição
temporal genuína dentro do mesmo sistema em 2 domínios físicos distintos),
**não produz um invariante cross-domain confiável** — mesmo veredito já
obtido para `critical-slowing-down` e `wavelet-multiresolution-scaling`,
os 3 candidatos viáveis da Fase 0 desta linha agora testados com rigor
completo.

O achado ISOLADO no domínio de apneia-ECG É real e sobrevive à reexecução
adversarial (extração independente bate quase exatamente, não é artefato
de outlier nem de descontinuidade de fronteira) — mas: (a) é explicado por
completo por um mecanismo fisiológico já conhecido há 40 anos (CVHR,
Guilleminault et al. 1984), não por qualquer ingrediente novo de
renormalização/invariante cross-domain; (b) não sobrevive ao segundo
domínio já calculado por esta própria linha (GISP2); (c) tem um confundidor
de estágio do sono não resolvido com um único registro; (d) carrega risco
de viés de seleção não resolvido (só 1 de 4 registros candidatos foi
levado a resultado final). Isso não invalida DFA como ferramenta em
fisiologia do sono (é bem estabelecida) — apenas mostra que, como
candidato a invariante `DISC-TRI-RG-001`, não sobrevive.

## Estado da linha — os 3 candidatos viáveis da Fase 0 agora testados

| Candidato | Domínios testados | Resultado |
|---|---|---|
| `critical-slowing-down` | GISP2, PhysioNet SDDB, NASDAQ | NEGATIVO |
| `wavelet-multiresolution-scaling` | Sismologia/Tohoku, EEG/CHB-MIT | NEGATIVO |
| `dfa-multiscale-entropy` | Apneia-ECG/`a04`, GISP2 | NEGATIVO (achado de 1 domínio explicado por mecanismo mundano) |

Nenhum `PREREGISTRATION.md` foi escrito para nenhum dos 3.

## Recomendação (não travada)

Três rotas honestas seguintes, nenhuma decidida aqui:

1. **Nova rodada de busca** por candidatos ainda não considerados (os 2
   candidatos inviáveis da Fase 0 — box-covering, spacing-statistics — já
   têm rotas alternativas anotadas como sementes futuras em
   `phase0/PHASE0_SURVEY.md`).
2. **Revisitar os 3 candidatos já testados com domínios/dados diferentes**
   dos já usados (a própria descoberta adversarial mapeou 3 registros de
   backup do banco Apnea-ECG — `a18`, `a14`, `a01` — nunca executados; um
   segundo domínio replicando o mesmo tipo de transição cíclica poderia
   testar se o achado de apneia é robusto a mais de um paciente, embora
   isso ainda não resolveria a exigência CROSS-DOMAIN da linha).
3. **Considerar `DISC-TRI-RG-001` suficientemente explorada** por ora
   (mesma decisão já tomada uma vez, `DISC-DEC-005`) — toda a
   infraestrutura (metodologia, 3 pipelines validadas, dados preparados,
   9 domínios/variantes testados no total) fica commitada e reaproveitável
   para uma retomada futura.

Um achado colateral honesto, fora do escopo desta linha mas potencialmente
interessante para uma linha futura de fisiologia pura (não cross-domain
RG): o mecanismo CVHR encontrado pelo agente de descoberta de nulos é, ele
mesmo, um sinal fisiológico real e forte — só não serve como evidência
para `DISC-TRI-RG-001` porque é fisiologia já conhecida, não um invariante
novo.
