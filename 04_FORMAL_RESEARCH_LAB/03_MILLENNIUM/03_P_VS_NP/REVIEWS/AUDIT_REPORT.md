# Relatório de auditoria — `PVSNP-PHYS-001`

Onda: `PORTFOLIO-REVIEW-AFTER-SOBOLEV-CHAIN-2026-08-09` (auditoria paralela,
não tentativa de resolução — ver
`04_FORMAL_RESEARCH_LAB/01_PORTFOLIO/PORTFOLIO_REVIEW_AFTER_SOBOLEV_CHAIN.md`).
Data da sessão: 2026-08-09. Buscas via `WebSearch`.

Postura exigida pelo documento de revisão de portfólio: separar, de forma
legível, o que foi verificado nesta sessão do que foi aproximado (lido do
legado ou de memória de treino, sem fonte primária conferida agora). As
duas seções abaixo **não se misturam**.

---

## Verificado

Citação bibliográfica exata recuperável nesta sessão via `WebSearch`
(2026-08-09), consistente entre múltiplas fontes independentes:

1. **Baker, T.; Gill, J.; Solovay, R.** — *Relativizations of the P =? NP
   Question*. SIAM Journal on Computing 4(4):431–442, 1975. Existem
   oráculos `A`, `B` com `P^A = NP^A` e `P^B ≠ NP^B`; provas que
   relativizam não podem, sozinhas, decidir `P` vs `NP`.

2. **Blum, L.; Shub, M.; Smale, S.** — *Complexity and Real Computation*.
   Springer, 1998. Define a máquina BSS (custo unitário sobre um corpo,
   ex. `ℝ` ou `ℂ`) e as classes `P_ℝ`, `NP_ℝ`.

3. **Bürgisser, P.; Cucker, F.** — *Counting complexity classes for
   numeric computations II: Algebraic and semialgebraic sets*. Journal of
   Complexity 22(2):147–191, 2006. (Citação bibliográfica confirmada; ver
   ressalva na seção "Aproximado" sobre os enunciados técnicos exatos.)

4. **Maass, W.; Orponen, P.** — *On the Effect of Analog Noise in
   Discrete-Time Analog Computations*. Neural Computation 10(5):1071–1095,
   1998. (Citação confirmada; ver ressalva sobre o enunciado exato.)

5. **Talagrand, M.** — *The Parisi formula*. Annals of Mathematics
   163(1):221–263, 2006. Prova rigorosa da fórmula de Parisi para a energia
   livre do modelo Sherrington–Kirkpatrick de vidro de spin de campo médio,
   construindo sobre o método de interpolação de Guerra (2003) e sobre
   Aizenman–Sims–Starr.

6. **Aaronson, S.** — *NP-complete Problems and Physical Reality*. ACM
   SIGACT News 36(1):30–52, 2005 (arXiv:quant-ph/0502072). Levantamento de
   propostas físicas para resolver problemas NP-completos eficientemente
   (bolhas de sabão, dobramento de proteínas, computação adiabática
   quântica, dilatação temporal relativística, curvas fechadas tipo-tempo,
   entre outras); conclusão: nenhuma delas é conhecida como capaz de
   resolver NP-completos eficientemente.

7. **Deutsch, D.** — *Quantum theory, the Church–Turing principle and the
   universal quantum computer*. Proceedings of the Royal Society of London
   A, 400:97–117, 1985. (Citação confirmada; ver ressalva sobre a
   formulação exata do princípio na seção "Aproximado".)

8. Busca direta pelo termo **"Physical Computation Axiom"** associado a P
   vs NP não retornou o termo nas fontes localizadas acima nem em nenhuma
   outra fonte primária de teoria da complexidade computacional pesquisada
   nesta sessão — este é um resultado negativo de busca, verificável ao
   reexecutar a mesma busca, não uma prova de inexistência do termo em
   alguma fonte não indexada.

9. Verificação estrutural em Lean (não `lake build` — ver `PROOF_SKETCH.md`
   §4 para o motivo): as definições `AffineBounded`, `SimEquivalent` e os
   lemas `simEquivalent_refl`, `simEquivalent_symm`, `affineBounded_zero`
   em `FORMAL/PvsNPPhys.lean` foram revisados manualmente termo a termo;
   cada prova usa apenas a tática `omega` sobre desigualdades lineares com
   coeficiente literal `1`, sem lema nomeado externo — risco de erro de
   compilação considerado baixo, mas **não confirmado por build real**
   nesta sessão.

## Aproximado

Lido de resumo de busca (fonte secundária) ou do documento legado, **sem**
conferência do texto primário nesta sessão:

1. O enunciado técnico exato de Bürgisser–Cucker 2006 (item 3 acima) —
   incluindo a formulação "`NP ⊄ BPP` implica `VP_ℂ ≠ VNP_ℂ` sob GRH" e a
   afirmação sobre colapso da hierarquia polinomial clássica ao quarto
   nível — foi obtido de um resumo de busca, não do PDF do artigo.

2. O enunciado técnico exato de Maass–Orponen 1998 (item 4 acima) —
   "ruído analógico arbitrariamente pequeno reduz o poder do modelo ao de
   autômatos finitos" — é uma paráfrase de resumo consistente com o que se
   encontra descrito sobre o artigo em múltiplas fontes, mas não foi
   conferida contra o texto do artigo.

3. A identificação exata da classe de complexidade atingida por redes
   neurais recorrentes analógicas (ARNN) de Siegelmann & Sontag sob peso
   real de precisão infinita (citada em buscas como possivelmente
   `BPP/log*`) é uma paráfrase de fonte secundária — não conferida contra
   Siegelmann & Sontag 1994 nem contra Siegelmann 1999 (*Neural Networks
   and Analog Computation: Beyond the Turing Limit*) nesta sessão.

4. A formulação exata do princípio de Church–Turing físico de Deutsch 1985
   ("todo sistema físico finitamente realizável pode ser perfeitamente
   simulado por uma máquina computadora universal operando por meios
   finitos") é uma citação entre aspas encontrada em resultado de busca,
   não conferida contra o PDF original nesta sessão.

5. **A relação entre a arquitetura BSS/análogos físicos e o modelo
   termodinâmico/de vidro de spin usado no documento legado
   (`ANALISE_CRITICA_PNP.md`) como base de uma alegação anterior de
   "P≠NP sob PCA"**: essa alegação não pôde ser reconstruída a partir de
   nenhuma fonte primária localizada nesta sessão. O que **é** verificado
   (item 5 da lista "Verificado") é que Talagrand 2006 prova a fórmula de
   Parisi para a energia livre do modelo SK — um resultado de física
   estatística rigorosa, **não** uma redução de complexidade computacional
   de k-SAT a vidros de spin, e **não** uma prova (condicional ou não) de
   `P ≠ NP`. O salto do primeiro para o segundo, presente no documento
   legado, não tem fonte recuperável nesta sessão — ver `GAP_REGISTER.yaml`
   `PNP-GAP-004`.

6. Todo o conteúdo qualitativo de `ANALISE_CRITICA_PNP.md` sobre o estado
   interno do projeto Tamesis anterior (percentuais como "~75-80%",
   classificações "95% física / 50-60% Clay") é tratado nesta auditoria
   como leitura de um documento de auto-avaliação interna, não como
   resultado matemático ou citação externa — não re-verificado nem
   endossado aqui.

---

## O que esta auditoria não afirma

```text
que P_phys = NP_phys ou P_phys != NP_phys para qualquer modelo concreto
que qualquer resultado acima decide, aproxima ou torna alcancavel
   P versus NP classico
que o "Physical Computation Axiom" seja valido OU invalido -- apenas que
   nao foi localizado como termo/resultado da literatura externa nesta sessao
que a formalizacao Lean (FORMAL/PvsNPPhys.lean) tenha sido compilada
   (lake build) nesta sessao
```

## Condição de parada

Atingida — ver `PROOF_SKETCH.md` seção 3. Reportado, não forçado.
