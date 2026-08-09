# Hipóteses

Estado: `AUDITED_PARTIAL` (auditoria de literatura nesta sessão; não é
verificação formal). Este arquivo lista as hipóteses estruturais que
atravessam vários teoremas da matriz, para que `KNOWN_RESULTS_MATRIX.md`
não precise repeti-las em cada linha, e para deixar explícito onde esta
auditoria **não** confirmou o enunciado exato contra a fonte primária.

## Hipóteses estruturais (valem para quase toda a literatura)

1. **`E` definida sobre `Q`, curva elíptica não singular** — padrão em
   toda a matriz salvo onde indicado (Rubin cobre `E` com CM, possivelmente
   sobre corpos quadráticos imaginários).
2. **Modularidade** — incondicional para todo `E/Q` desde BCDT 2001.
   Deixa de ser hipótese restritiva pós-2001. **Verificado**.
3. **Hipótese de Heegner** (Gross–Zagier/Kolyvagin) — exige um corpo
   quadrático imaginário `K` onde todo primo dividindo o condutor `N` se
   comporta de modo compatível com a existência de pontos de Heegner
   (tipicamente: todo `p | N` é split ou ramifica em `K`, `K` ≠ `Q(i)`,
   `Q(√-3)` em casos degenerados). A existência de tal `K` é um fato
   clássico de teoria dos números elementar (reciprocidade quadrática +
   TCR) e não é, por si, uma restrição às curvas cobertas — mas a
   **escolha de `K`** entra na demonstração, não é livre de todo detalhe
   técnico. **Aproximado**: forma exata da hipótese não reconferida contra
   Gross–Zagier 1986 nesta sessão (só o resultado, não o enunciado
   completo do artigo, foi lido).
4. **Hipóteses (H1)–(H4) de Skinner–Urban** — o documento legado
   (`ANALISE_CRITICA_BSD.md`) cita quatro condições técnicas, culminando em
   "N⁻ (produto dos primos de má redução multiplicativa split) deve ser
   squarefree com número ímpar de fatores primos". **Não verificado nesta
   sessão**: não consegui recuperar o enunciado exato de (H1)-(H4) de uma
   fonte primária (o artigo Skinner–Urban, *Iwasawa Main Conjectures for
   GL2*, Inventiones 195 (2014), 1–277, foi confirmado como existente e
   como tratando de Iwasawa Main Conjecture ordinária para GL2, mas a
   busca não retornou o texto com a lista literal de hipóteses). Tratar
   como **aproximado**, herdado do documento legado, até confirmação
   primária.
5. **Boa redução ordinária em `p`, `E[p]` irredutível** — hipótese comum a
   Skinner–Urban e ao trabalho de base change (Burungale–Castella–Skinner).
   O artigo BCS (IMRN 2025, `rnaf082`) é descrito, nos resumos recuperados
   nesta sessão, como removendo justamente a hipótese de ramificação sobre
   `E[p]` presente em trabalhos anteriores — mas a correspondência exata
   com "(H4)" do documento legado **não foi confirmada linha a linha**.
6. **Redução semiestável em `p` supersingular** — hipótese de
   Burungale–Skinner–Tian–Wan (arXiv:2409.01350, 2024). **Verificado**
   (resumo do artigo recuperado via WebFetch nesta sessão): prova a
   conjectura principal de Kobayashi (2002) para curvas semiestáveis em
   primos supersingulares.
7. **Primo de Eisenstein (representação mod `p` redutível)** — regime do
   trabalho Castella–Grossi–Skinner (Math. Annalen 393(2), 2025) e
   Castella–Grossi–Lee–Skinner (Inventiones 227(2), 2022). Estruturalmente
   **excludente** com a hipótese "`E[p]` irredutível" usada por
   Skinner–Urban/BCS — não são o mesmo `p` para a mesma curva em geral;
   ver nota em `KNOWN_RESULTS_MATRIX.md` sobre não somar coberturas.

## O que NÃO é hipótese satisfeita automaticamente

- **Main Conjectures p-ádicas (Iwasawa) não são, por si só, BSD complexa
  geral.** Cada Main Conjecture prova uma igualdade de ideais/característicos
  em um anel de Iwasawa; a tradução para "a fórmula BSD vale para `E` em
  `s=1`" exige, adicionalmente, uma fórmula de Gross–Zagier p-ádica (ou
  Kato + interpolação) ligando o lado analítico ao algébrico, E QUE essa
  ligação seja feita primo a primo — nenhuma fonte auditada aqui afirma
  fechar "todos os primos simultaneamente" para uma curva arbitrária de
  posto 0/1. Isto é mantido como `NOT_AUDITED` em detalhe — ver
  `GAP_REGISTER.yaml` (`BSD-GAP-006`).
- **Nenhuma hipótese de exaustividade foi encontrada ou é reivindicada por
  qualquer fonte auditada**: nenhum artigo lido afirma "toda curva elíptica
  sobre `Q` satisfaz H_i para algum `i` da lista conhecida". Essa é
  exatamente a lacuna que o `stop_condition` desta frente proíbe fechar por
  inferência informal (soma/produto de percentuais). Ver
  `REVIEWS/AUDIT_REPORT.md`.
