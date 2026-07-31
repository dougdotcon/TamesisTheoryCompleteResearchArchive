# RH-NOGO-001 — Auditoria bibliográfica

> **Atualização 2026-07-31 (gate RH_NOGO_PRIMARY_SOURCE_AUDIT).** As quatro
> fontes obrigatórias foram efetivamente **obtidas** e parcialmente lidas.
> Os estados de leitura abaixo foram substituídos pelos registros de
> `../../08_REVIEWS/SOURCES/RH_NOGO/SOURCE_MANIFEST.yaml`, que é agora a
> fonte canônica de proveniência. Auditorias por documento em
> `VON_MANGOLDT_1905_AUDIT.md`, `HORMANDER_1968_AUDIT.md`,
> `RIEMANN_1859_AUDIT.md` e `BOMBIERI_CLAY_AUDIT.md` (mesmo diretório).
> `CONTENT_AUDITED` aplica-se somente à tradução de Riemann.

Método: `PROTOCOLO_AUDITORIA_RIGOROSA_DE_ARTIGOS.md` (raiz do repositório,
leitura obrigatória). Nenhuma fonte abaixo sustenta mais do que o campo
`claim_supported` declara. Estados de verificação:

- `KNOWN_RECORD` — registro bibliográfico estabelecido, conhecido do
  agente; conteúdo não re-baixado nesta sessão;
- `LISTING_CONFIRMED` — existência confirmada em listagem pública nesta
  sessão (2026-07-31), conteúdo não auditado;
- `TO_FETCH` — deve ser baixada e lida antes do gate de prova.

---

```yaml
- source_id: RIEMANN-1859
  citation: "B. Riemann, 'Ueber die Anzahl der Primzahlen unter einer gegebenen Grösse', Monatsberichte der Berliner Akademie, 1859"
  publication_type: memória acadêmica histórica
  peer_reviewed: não (formato da época)
  primary_or_secondary: primária
  claim_supported: "definição de ζ e dos zeros não triviais; enunciado (sem prova) da fórmula aproximada de contagem dos zeros"
  assumptions: []
  relevance: "origem do problema e da fórmula de contagem"
  inside_operator_class: NOT_APPLICABLE
  outside_operator_class: NOT_APPLICABLE
  limitations: "a contagem é afirmada, não provada, no manuscrito"
  verification_status: KNOWN_RECORD + TO_FETCH (edição crítica)

- source_id: VONMANGOLDT-1905
  citation: "H. von Mangoldt, 'Zur Verteilung der Nullstellen der Riemannschen Funktion ξ(t)', Mathematische Annalen 60 (1905), 1–19; trabalho preparatório em J. reine angew. Math. 114 (1895)"
  publication_type: artigo de periódico
  peer_reviewed: sim (padrão da época)
  primary_or_secondary: primária
  claim_supported: "prova da fórmula de contagem N_ζ(T) = (T/2π)log(T/2π) − T/2π + O(log T) — a hipótese A do núcleo"
  assumptions: ["análise complexa clássica; nenhuma dependência da RH"]
  relevance: ESTABLISHED — pilar A
  inside_operator_class: NOT_APPLICABLE
  outside_operator_class: NOT_APPLICABLE
  limitations: "nenhuma relevante ao uso"
  verification_status: KNOWN_RECORD + TO_FETCH

- source_id: BOMBIERI-CLAY
  citation: "E. Bombieri, 'Problems of the Millennium: The Riemann Hypothesis', Clay Mathematics Institute, descrição oficial do problema (claymath.org)"
  publication_type: descrição oficial de problema
  peer_reviewed: revisão institucional
  primary_or_secondary: secundária autorizada
  claim_supported: "enunciado oficial da RH; status em aberto do problema"
  assumptions: []
  relevance: "fonte do enunciado oficial; confirma que nenhuma prova é aceita"
  inside_operator_class: NOT_APPLICABLE
  outside_operator_class: NOT_APPLICABLE
  limitations: "não é fonte para resultados técnicos finos"
  verification_status: KNOWN_RECORD

- source_id: HORMANDER-1968
  citation: "L. Hörmander, 'The spectral function of an elliptic operator', Acta Mathematica 121 (1968), 193–218"
  publication_type: artigo de periódico
  peer_reviewed: sim
  primary_or_secondary: primária
  claim_supported: "lei de Weyl com resto O(Λ^{(d−1)/m}) para operadores elípticos (inclusive pseudodiferenciais) de ordem positiva em variedades compactas — a hipótese B (W8) do núcleo"
  assumptions: ["elipticidade, compacidade, auto-adjunção, ordem positiva"]
  relevance: ESTABLISHED — pilar B
  inside_operator_class: sim (é a fonte da classe)
  outside_operator_class: não
  limitations: "GAP-RH-002: a versão exata (escalar vs fibrado; diferencial vs ψDO; enunciado preciso do resto) deve ser transcrita do artigo antes do gate de prova"
  verification_status: KNOWN_RECORD + TO_FETCH

- source_id: BERRYKEATING-1999
  citation: "M. V. Berry, J. P. Keating, 'The Riemann zeros and eigenvalue asymptotics', SIAM Review 41 (1999), 236–266"
  publication_type: artigo de revisão
  peer_reviewed: sim
  primary_or_secondary: secundária (revisão) com propostas primárias
  claim_supported: "discussão explícita de que a contagem média dos zeros é (T/2π)log(T/2π) e de que isso aponta para H = xp em espaço NÃO compacto com regularizações — evidência direta de que a observação por trás do no-go é folclore da área (GAP-RH-007)"
  assumptions: ["heurísticas semiclássicas"]
  relevance: "auditoria de novidade; rota de escape 1 e 9"
  inside_operator_class: não
  outside_operator_class: sim
  limitations: "heurístico; não prova existência de operador"
  verification_status: KNOWN_RECORD + TO_FETCH

- source_id: CONNES-1999
  citation: "A. Connes, 'Trace formula in noncommutative geometry and the zeros of the Riemann zeta function', Selecta Mathematica 5 (1999), 29–106; arXiv:math/9811068"
  publication_type: artigo de periódico
  peer_reviewed: sim
  primary_or_secondary: primária
  claim_supported: "interpretação dos zeros como espectro de absorção no espaço de classes de adeles — rota fora da Classe W (não comutativa, não compacta, absorção)"
  assumptions: ["geometria não comutativa; fórmula de traço condicional"]
  relevance: "rota de escape 3 e 4; mostra que o no-go não pode alegar generalidade"
  inside_operator_class: não
  outside_operator_class: sim
  limitations: "a fórmula de traço equivalente à RH não está provada"
  verification_status: KNOWN_RECORD

- source_id: BBM-2017
  citation: "C. M. Bender, D. C. Brody, M. P. Müller, 'Hamiltonian for the zeros of the Riemann zeta function', Physical Review Letters 118 (2017), 130201; arXiv:1608.03679"
  publication_type: artigo de periódico
  peer_reviewed: sim
  primary_or_secondary: primária
  claim_supported: "proposta de operador não hermitiano com estrutura PT cujas autofunções formais correspondem aos zeros — rota fora da Classe W (sem auto-adjunção convencional demonstrada)"
  assumptions: ["quantização formal; questões de domínio e auto-adjunção abertas na literatura subsequente"]
  relevance: "rota de escape 12"
  inside_operator_class: não
  outside_operator_class: sim
  limitations: "criticado e refinado em trabalhos posteriores; não estabelece operador auto-adjunto"
  verification_status: KNOWN_RECORD

- source_id: HEDENMALM-2026
  citation: "H. Hedenmalm, 'Spectral interpretation of Riemann zeta zeros', preprint arXiv, junho de 2026 (math.CA / math.NT, 9 pp.)"
  publication_type: preprint
  peer_reviewed: NÃO
  primary_or_secondary: primária não validada
  claim_supported: "NENHUMA para este gate — entra somente em CLAIMS_REQUIRING_INDEPENDENT_AUDIT"
  assumptions: ["problema diferencial na semirreta com noção adaptada de auto-adjunção (descrição do mantenedor; não auditada)"]
  relevance: "rota de escape 13; prova que a classe estreita não cobre propostas atuais"
  inside_operator_class: não (semirreta = não compacto; auto-adjunção adaptada)
  outside_operator_class: sim
  limitations: "preprint recente, sem revisão por pares; conteúdo não lido nesta sessão"
  verification_status: LISTING_CONFIRMED (arXiv, 2026-07-31) + TO_FETCH
```

## CLAIMS_REQUIRING_INDEPENDENT_AUDIT

- HEDENMALM-2026 (integral);
- qualquer preprint que alegue prova da RH — **nenhum** pode entrar como
  autoridade em qualquer gate deste programa.

## Fontes rejeitadas como autoridade

- Preprints de "prova da RH" (qualquer autor): não citáveis como
  estabelecidos.
- Documentos legados do arquivo Tamesis sobre Riemann
  (`90_LEGACY_MAP/HISTORICAL_CLAIMS.yaml`): históricos, sem precedência
  científica.
- Bases de conhecimento das skills: orientam método, não são fontes.
