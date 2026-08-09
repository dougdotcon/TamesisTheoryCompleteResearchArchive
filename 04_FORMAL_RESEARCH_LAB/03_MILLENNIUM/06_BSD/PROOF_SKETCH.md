# Esboço

`NO_EXECUTION` — mantido. O produto desta frente (`BSD-HYP-MATRIX-001`) é
a matriz bibliográfica em `KNOWN_RESULTS_MATRIX.md`, não uma tentativa de
prova ou de aproximação da conjectura de Birch–Swinnerton-Dyer.

## Por que não há esboço de prova aqui

Esta frente é definida, na revisão de portfólio que a autorizou
(`01_PORTFOLIO/PORTFOLIO_REVIEW_AFTER_SOBOLEV_CHAIN.md`), como uma
**auditoria**, não uma tentativa de resolução:

> "BSD-HYP-MATRIX-001 particionar a literatura de BSD por
> hipotese/curva/posto/primo, sem unir teoremas indevidamente"

Um "esboço de prova" pressuporia uma estratégia para fechar o caso geral
(`rank ≥ 2`, não-CM, sem hipótese especial de primo) — que nenhuma fonte
auditada em `KNOWN_RESULTS_MATRIX.md` resolve. Escrever um esboço aqui
seria inventar uma estratégia não suportada pela literatura auditada,
violando a proibição de `AGENTS.md` contra tratar aproximação como prova.

## Formalização em Lean nesta sessão

Um único artefato Lean foi produzido, em
`FORMAL/hypothesis_partition_guardrail.lean`: **não** é um passo em
direção a BSD. É um lema autocontido de lógica proposicional/de
predicados (sem `import Mathlib`) que formaliza o *formato* exato do erro
que o `stop_condition` desta frente proíbe — "união de casos cobertos
implica cobertura universal" — e demonstra, com um contraexemplo concreto
de dois elementos, que essa inferência é inválida sem uma hipótese adicional
de exaustividade (que nenhuma fonte listada em `KNOWN_RESULTS_MATRIX.md`
fornece). Não usa `sorry`, `admit` nem axioma local. Não foi compilado
com `lake build` nesta sessão (ver `AGENTS.md` sobre paralelismo e cache
compartilhado) — a integração/build fica para a etapa serial de
integração.

## Próximo passo, se autorizado em gate futuro

Se uma futura frente quiser ir além da auditoria, o passo natural seria
formalizar em Lean **um teorema condicional isolado** da matriz (p.ex.
Gross–Zagier–Kolyvagin restrito a rank 0/1) como um `Prop` com hipóteses
explícitas — não como aproximação de BSD geral. Isso não foi tentado
aqui: está fora do escopo de `BSD-HYP-MATRIX-001` conforme definido pela
revisão de portfólio.
