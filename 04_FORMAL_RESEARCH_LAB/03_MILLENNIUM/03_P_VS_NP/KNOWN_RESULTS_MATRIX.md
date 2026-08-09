# Matriz de resultados conhecidos

Auditoria `PVSNP-PHYS-001`. Cada linha tem uma coluna `status_sessao`:
`VERIFICADO` (citação bibliográfica recuperada nesta sessão via WebSearch,
2026-08-09) ou `APROXIMADO` (afirmação técnica lida de resumo/fonte
secundária desta busca, ou do documento legado, sem conferência do texto
primário nesta sessão). Ver `REVIEWS/AUDIT_REPORT.md` para a versão
consolidada com todas as fontes.

| # | Item | Modelo `(E,M,R)` | Afirmação | `status_sessao` |
|---|---|---|---|---|
| 1 | Baker–Gill–Solovay 1975 | N/A (Turing clássico + oráculos) | Existem oráculos `A`,`B` com `P^A=NP^A` e `P^B≠NP^B`; técnicas de diagonalização/relativização não podem, sozinhas, decidir `P` vs `NP` | VERIFICADO (citação: *Relativizations of the P =? NP Question*, SIAM J. Computing 4(4):431–442, 1975; conteúdo do teorema consistente em múltiplas fontes secundárias) |
| 2 | Blum–Shub–Smale 1998 | BSS sobre `ℝ`/`ℂ` | Define máquina de custo unitário sobre corpo `R`; classes `P_R`, `NP_R` | VERIFICADO (citação: *Complexity and Real Computation*, Springer 1998) |
| 3 | Bürgisser–Cucker 2006 | BSS sobre `ℂ` vs. clássico (Booleano) | Relaciona `NP_ℂ`/`VP_ℂ`/`VNP_ℂ` com classes clássicas; parte dos resultados **condicional à Hipótese Generalizada de Riemann (GRH)** | citação VERIFICADA (*Counting complexity classes for numeric computations II: Algebraic and semialgebraic sets*, J. Complexity 22(2):147–191, 2006); enunciados técnicos exatos (ex. "`NP⊄BPP` implica `VP_ℂ≠VNP_ℂ` sob GRH") **APROXIMADO** — lido de resumo de busca, não do PDF primário nesta sessão |
| 4 | Maass–Orponen 1998 | computação analógica de tempo discreto com ruído | Ruído analógico arbitrariamente pequeno reduz o poder computacional do modelo ao de autômatos finitos | citação VERIFICADA (*On the Effect of Analog Noise in Discrete-Time Analog Computations*, Neural Computation 10(5):1071–1095, 1998); enunciado do resultado **APROXIMADO** — paráfrase de resumo, não conferido linha a linha contra o artigo |
| 5 | Siegelmann & Sontag 1994; Siegelmann 1999 | ARNN (rede neural recorrente analógica), pesos reais de precisão infinita | Poder computacional "super-Turing" sob tempo polinomial e pesos reais idealizados | citação e existência do resultado geral VERIFICADO (múltiplas fontes secundárias consistentes); **classe de complexidade exata citada (ex. "BPP/log*") é APROXIMADA** — não conferida contra o artigo original nesta sessão |
| 6 | Talagrand 2006 | modelo Sherrington–Kirkpatrick (vidro de spin de campo médio) | Prova rigorosa da fórmula de Parisi para a energia livre do modelo SK | VERIFICADO (citação exata: *The Parisi formula*, Ann. of Math. 163 (2006), 221–263; base em Guerra 2003 e Aizenman–Sims–Starr) |
| 7 | Aaronson 2005 | levantamento de propostas físicas (bolhas de sabão, dobramento de proteínas, computação adiabática quântica, dilatação temporal relativística, curvas fechadas tipo-tempo, etc.) | Nenhuma proposta conhecida resolve problemas NP-completos eficientemente; argumenta por uma tese de Church–Turing física/estendida | VERIFICADO (citação: *NP-complete Problems and Physical Reality*, ACM SIGACT News 36(1):30–52, 2005 / arXiv:quant-ph/0502072) |
| 8 | Deutsch 1985 | tese de Church–Turing física | "Todo sistema físico finitamente realizável pode ser perfeitamente simulado por uma máquina computadora universal operando por meios finitos" | citação VERIFICADA (*Quantum theory, the Church–Turing principle and the universal quantum computer*, Proc. R. Soc. Lond. A 400:97–117, 1985); formulação exata citada **APROXIMADA** — paráfrase de fonte secundária |
| 9 | "Physical Computation Axiom" (PCA), documento legado Tamesis | N/A | "ZFC + PCA ⊢ P≠NP" | **NÃO LOCALIZADO** nesta sessão como termo/resultado da literatura externa — ver `ASSUMPTIONS.md` §3. Não classificável como VERIFICADO nem como APROXIMADO de uma fonte externa; é interno ao legado |
| 10 | Redução k-SAT → vidro de spin com gap espectral `Δ(N) ~ exp(-αN)` "provado", citada no documento legado | N/A | Universalidade da redução | **NÃO VERIFICADO** nesta sessão — nenhuma fonte primária localizada que estabeleça esta redução como teorema geral; o item 6 acima (Talagrand 2006) prova algo diferente (fórmula de energia livre do modelo SK em si, não uma redução de complexidade computacional) |

## Leitura consolidada

Nenhum item 1–8 estabelece uma ponte de simulação universal
(`DEFINITIONS.md` §3) entre qualquer `P_phys`/`NP_phys` e as classes
clássicas `P`/`NP`. Os itens 3 e 4 são os candidatos mais próximos de
"teoremas de simulação/limite" e ambos são **condicionais**: o item 3 a uma
hipótese matemática não relacionada (GRH), o item 4 a um modelo físico
específico de ruído. Os itens 9–10 são exatamente os pontos onde o
documento legado ia além do que esta sessão conseguiu verificar — ver
`REVIEWS/AUDIT_REPORT.md`.
