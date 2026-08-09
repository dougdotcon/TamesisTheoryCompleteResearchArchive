# Relatório de auditoria — NS-PRESSURE-001

work_item: NS-PRESSURE-001
autorização: PORTFOLIO-REVIEW-AFTER-SOBOLEV-CHAIN-2026-08-09
data: 2026-08-09
alvo: testar se a hipótese quantitativa sobre a Hessiana de pressão
(pressure-alignment) é verdadeira e suficiente para controlar blow-up em
Navier–Stokes 3D.
produto: correção (à forma nua da hipótese, com contraexemplo explícito)
+ `stop_condition` acionado (para a forma fortalecida).

Este relatório separa, como exigido pela postura epistêmica desta onda
(`01_PORTFOLIO/PORTFOLIO_REVIEW_AFTER_SOBOLEV_CHAIN.md`), o que foi
**verificado** nesta sessão (citação recuperável via WebSearch, ou
checado por computação/Lean) do que é **aproximado** (lido do documento
legado ou de memória de treino, sem fonte primária conferida agora). As
duas seções abaixo não se misturam.

---

## VERIFICADO

Afirmações com citação recuperável nesta sessão (WebSearch) ou checadas
por computação nesta sessão (Python/sympy/scipy). Ver
`KNOWN_RESULTS_MATRIX.md` para a tabela completa com URLs de origem.

1. **Caffarelli, Kohn, Nirenberg (1982)**, "Partial regularity of
   suitable weak solutions of the Navier-Stokes equations", *Comm. Pure
   Appl. Math.* 35, 771–831. Citação confirmada via WebSearch.

2. **Beale, Kato, Majda (1984)**, "Remarks on the breakdown of smooth
   solutions for the 3-D Euler equations", *Comm. Math. Phys.* 94.
   Critério confirmado: `T*` é tempo de blow-up ⟺
   `∫₀^{T*}‖ω‖_∞ dt = ∞`.

3. **Constantin, Fefferman (1993)**, "Direction of vorticity and the
   problem of global regularity for the Navier-Stokes equations",
   *Indiana Univ. Math. J.* 42, 775–789. Citação e enunciado
   confirmados: direção da vorticidade Lipschitz-contínua (uniforme no
   tempo, em regiões de vorticidade intensa) ⟹ regularidade.

4. **Nečas, Růžička, Šverák (1996)**, "On Leray's self-similar
   solutions of the Navier-Stokes equations", *Acta Math.* 176,
   283–294. Citação confirmada: soluções autossimilares de Leray têm de
   ser identicamente nulas.

5. **Ashurst, Kerstein, Kerr, Gibson (1987)**, "Alignment of vorticity
   and scalar gradient with strain rate in simulated Navier-Stokes
   turbulence", *Phys. Fluids* 30, 2343. Citação e achado confirmados:
   em DNS, a vorticidade se alinha preferencialmente com o autovetor
   **intermediário** da deformação (não o mais extensional), atribuído
   a conservação de momento angular via um modelo de Euler restrita.

6. **Cantwell (1992)**, "Exact solution of a restricted Euler equation
   for the velocity gradient tensor", *Phys. Fluids A* 4, 782–792.
   Citação e conteúdo confirmados: solução exata (funções elípticas de
   Jacobi) da dinâmica de Vieillefosse.

7. **Chevillard, Meneveau (2006)** e trabalho relacionado
   (Chevillard–Meneveau–Biferale–Toschi, *Phys. Fluids* 20, 101504,
   2008): fechamento "Recent Fluid Deformation" (RFD) para o Hessiano
   de pressão; confirmado que o próprio modelo **não reproduz bem**
   certas propriedades em regiões dominadas por rotação — citado
   explicitamente nos resumos recuperados.

8. **Evan Miller (2020)**, "A regularity criterion for the
   Navier-Stokes equation involving only the middle eigenvalue of the
   strain tensor", *Arch. Ration. Mech. Anal.* 235. Citação e achado
   confirmados: identidade de crescimento de enstrofia dependente só do
   autovalor intermediário da deformação (contorna a interação
   não-local vorticidade–deformação de outra forma), com condições
   necessárias e suficientes de blow-up críticas em escala.

9. **Achado computacional próprio desta sessão** (não uma citação):
   integração numérica da equação de Euler restrita (Vieillefosse
   1982) para 6 condições iniciais aleatórias mostra blow-up em tempo
   finito em 6/6 casos, com `cos²(ω,e₁) → 0` (desalinhamento quase
   perfeito com o autovetor mais extensional) ao longo de toda a cauda
   da trajetória que explode. Script, saída bruta e discussão em
   `COMPUTATION/restricted_euler.py`,
   `COMPUTATION/restricted_euler_output.log`,
   `COUNTEREXAMPLES/restricted_euler_alignment_gap.md`.

10. **Identidades algébricas próprias desta sessão**, verificadas
    simbolicamente com `sympy` para o caso 3×3: `tr(AΩ)=0` para `A`
    simétrica e `Ω` antissimétrica; `Ω_v² = v vᵀ - |v|²I`;
    `tr(Ω_v²) = -2|v|²`. Rascunho Lean correspondente (não compilado
    nesta sessão) em `FORMAL/PressureHessianAlgebra.lean`.

11. **Conclusão de auditoria, apoiada nos itens 6+9 acima**: a forma
    nua do "Alignment Gap" (Passo 2 do esboço legado, isolado, sem a
    componente de taxa do Lemma 3.1) não é, por si só, suficiente para
    impedir blow-up — refutada por contraexemplo explícito no sistema
    mais favorável a ela (Euler restrita). Ver `PROOF_SKETCH.md` e
    `GAP_REGISTER.yaml`, `NS-GAP-003`.

---

## APROXIMADO

Lido do documento legado (`RECURSOS_PARA_PESQUISA/07_MILLENNIUM_VALIDATION/PROBLEM_03_NAVIER_STOKES/ANALISE_CRITICA_NS.md`)
ou de memória de treino, **sem fonte primária conferida nesta sessão**.
Nada aqui deve ser tratado como fato estabelecido.

1. **Leray (1934)**, existência global de solução fraca em `L²` — fato
   clássico amplamente citado na literatura e usado como pressuposto
   pelo documento legado; não foi re-verificado via WebSearch nesta
   sessão (é matemática de 1934, considerada assentada, mas a citação
   exata não foi conferida agora).

2. **"Seregin-Šverák: Type I blow-up excluído"**, como citado no
   documento legado, seção 5, como resultado clássico 100% rigoroso
   sem qualificação. A auditoria desta sessão confirmou via WebSearch
   que Seregin e Šverák publicaram trabalho relevante sobre cotas de
   pressão (2002, ARMA) e sobre Tipo I axissimétrico (2009, Comm.
   PDE), mas **não conseguiu confirmar o enunciado exato** nem se a
   exclusão vale sem hipóteses adicionais (axissimetria, cota de
   pressão) fora da subclasse autossimilar já coberta por
   Nečas–Růžička–Šverák (1996, este sim verificado). Tratar como
   `NOT_AUDITED` até confirmação futura (`GAP_REGISTER.yaml`,
   `NS-GAP-005`).

3. **Vieillefosse (1982)** propriamente (o artigo original de 1982): a
   existência do resultado (blow-up em tempo finito da Euler restrita)
   foi confirmada via literatura secundária que o cita (Cantwell 1992,
   e resumos de artigos posteriores), mas o artigo original de 1982
   não foi acessado diretamente nesta sessão. A afirmação em si foi,
   no entanto, **reproduzida de forma independente por computação**
   nesta sessão (item 9 da seção "Verificado"), o que dá confiança
   adicional além da mera citação.

4. **Todos os números do documento legado** (`⟨α₁⟩ ≈ 0.15`,
   `δ₀ ≈ 0.85`, percentuais de "80-85% framework", cronograma "6-12
   meses"): lidos do documento legado, não re-derivados nem
   re-verificados nesta sessão. O documento legado já os apresenta como
   avaliação interna não peer-reviewed (`Sistema Tamesis`, 2026-02-05),
   não como resultado publicado — esta sessão não eleva seu status.

5. **A cadeia completa de 6 passos** (Pressure Dominance → Alignment
   Gap → Stretching Reduction → Enstrophy Bound → L∞ Bound → BKM),
   como estrutura lógica: reproduzida do documento legado para fins de
   auditoria; não é uma citação externa, é o objeto sob teste.
   `Lemma 3.1` e `Theorem 3.2`, no próprio documento legado, já estão
   marcados `🔴 NÃO PROVADO` — esta sessão não inverte essa marcação em
   nenhuma direção; apenas acrescenta um contraexemplo independente
   para a subparte isolável (Passo 2) e uma avaliação de dificuldade
   estrutural para a subparte que sobra (Passo 1/Lemma 3.1).

6. **Avaliação de "dificuldade estrutural equivalente à regularidade
   global"** para o Lemma 3.1 fortalecido (seção STOP CONDITION de
   `PROOF_SKETCH.md`): é uma avaliação qualitativa desta sessão, por
   analogia com o histórico de outros critérios de regularidade
   condicional (Constantin–Fefferman 1993, Prodi–Serrin, Evan Miller
   2020) nunca verificados a priori — **não é uma prova formal de
   equivalência lógica bicondicional**, e é apresentada explicitamente
   como tal.

---

## Veredicto desta auditoria

A hipótese quantitativa sobre a Hessiana de pressão, na forma em que o
documento legado a decompõe em "Alignment Gap" (Passo 2) mais "Rotation
Dominance" (Lemma 3.1), **não é verdadeira e suficiente por si só** na
sua forma nua (Passo 2 isolado) — contraexemplo explícito produzido
nesta sessão. Na sua forma fortalecida (com o Lemma 3.1), continua
`NOT_PROVEN`, exatamente como o próprio documento legado já registrava,
e esta sessão não encontrou motivo para tratá-la como mais perto de uma
prova do que estava antes; ao contrário, encontrou razão estrutural
para tratá-la como comparável em dificuldade a outros critérios de
regularidade condicional nunca fechados. O `stop_condition` desta
frente foi acionado; nenhuma tentativa adicional de fechar o Lemma 3.1
foi feita nesta sessão, conforme protocolo.

Nenhum Problema do Milênio é declarado resolvido, aproximado ou
alcançável por este relatório.
