# Contraexemplos abstratos — YM-LIMIT-001

Três construções. As duas primeiras estão formalizadas em Lean
(`FORMAL/InsufficiencyToyModel.lean`, sem `sorry`/`admit`/axioma oculto,
build não executado nesta rodada — ver nota de isolamento no topo do
arquivo). A terceira é dada em prosa matemática apenas.

Nenhuma delas modela a medida de Yang–Mills real. São contraexemplos à
**estrutura lógica** dos argumentos de interpolação/limite usados na
literatura secundária sobre o mass gap, não à física.

## Contraexemplo 1 — gap uniforme não implica teoria limite única

**Objeto:** \(a : \mathbb N \to \mathbb R\), \(a_n = 2\) se \(n\) par,
\(a_n=3\) se ímpar.

**Hipóteses satisfeitas:**
- Gap uniforme: \(\forall n,\ a_n \ge 2 > 0\).
- Tightness/limitação: \(\{a_n\} \subset [2,3]\), compacto.

**Conclusão que falha:** não existe \(L\) tal que \(a_n \to L\).
Demonstração: a subsequência \(a_{2k} \to 2\), a subsequência
\(a_{2k+1}\to 3\); se \(a_n \to L\) então toda subsequência convergiria
para \(L\) (unicidade de limite em espaço de Hausdorff), forçando
\(L=2\) e \(L=3\) simultaneamente — contradição, pois \(2 \ne 3\) em
\(\mathbb R\).

**Leitura para YM:** isto é a forma matemática mais simples possível do
erro descrito no `stop_condition` desta frente. Tightness da família de
medidas de rede (Prokhorov) garante que *alguma* subsequência de
espaçamentos \(a\to 0\) converge fracamente — não que a família completa
converge, nem que duas escolhas diferentes de subsequência (ou de
prescrição de regularização) convergem para a mesma teoria contínua. Sem
um argumento de unicidade independente (ex.: universalidade rigorosa —
listada como Opção C, dificuldade ALTA, no documento legado
`ANALISE_CRITICA_YM.md` §6.1), "existe um limite contínuo" e "existe *o*
limite contínuo, único" são afirmações logicamente distintas.

**Lean:** `toyGap`, `toyGap_uniform_lower_bound`, `toyGap_even_subseq`,
`toyGap_odd_subseq`, `toyGap_no_unique_continuum_limit`.

## Contraexemplo 2 — gap positivo em cada volume finito não é uniforme

**Objeto:** \(g:\mathbb N\to\mathbb R\), \(g_n = 1/(n+1)\).

**Hipóteses satisfeitas:** \(\forall n,\ g_n > 0\) — gap de volume finito
estritamente positivo em todo estágio.

**Conclusão que falha:** \(\inf_n g_n = 0\); não existe \(c>0\) com
\(g_n \ge c\) para todo \(n\). Demonstração elementar: dado
\(\varepsilon>0\), por Arquimedianidade existe \(n\) com
\(n > 1/\varepsilon\), donde \(g_n = 1/(n+1) < \varepsilon\).

**Leitura para YM:** corresponde ao "GAP 1"/"GAP 2" do documento legado —
mostrar \(m(a,L)>0\) para cada \((a,L)\) individualmente (o que Balaban dá
no regime UV e strong coupling dá no regime IR) é logicamente mais fraco
do que mostrar \(\inf_{a,L} m(a,L) > 0\) (o que exigiria fechar o regime
intermediário, não coberto por nenhum dos dois). "Positivo em cada ponto"
e "uniformemente limitado por baixo" são hipóteses diferentes, e a
literatura secundária às vezes as trata como a mesma coisa via um
argumento de "continuidade + positividade nos extremos" que este mesmo
contraexemplo mostra ser insuficiente em geral (uma função pode ser
positiva em cada ponto de um intervalo e ter ínfimo zero).

**Lean:** `toyFiniteVolumeGap`, `toyFiniteVolumeGap_pos`,
`toyFiniteVolumeGap_not_uniform`,
`finite_volume_gap_does_not_survive_without_uniform_bound`.

## Contraexemplo 3 — gap uniforme sob convergência forte não sobrevive ao limite (não formalizado em Lean nesta rodada)

**Objeto:** em \(\mathcal H = \mathbb C \oplus L^2([0,1])\), definir para
cada \(n\ge 1\)

\[
H_n = 0 \oplus M_{f_n}, \qquad f_n(x) = \max(x, 1/n),
\]

onde \(M_{f_n}\) é o operador de multiplicação por \(f_n\) em
\(L^2([0,1])\), e \(0\) atua como escalar no somando \(\mathbb C\)
(estado de vácuo, autovalor isolado 0).

**Fatos (não formalizados em Lean, prosa matemática apoiada em fato padrão
de análise espectral — ver `REVIEWS/AUDIT_REPORT.md`):**

- \(\mathrm{spec}(M_{f_n})\) = imagem essencial de \(f_n\) =
  \([1/n, 1]\), pois \(f_n\) é contínua e sobrejetora em \([1/n,1]\) com
  \(f_n(x)=1/n\) constante em \([0,1/n]\).
- Logo \(\mathrm{spec}(H_n) = \{0\}\cup[1/n,1]\): gap de vácuo
  \(=1/n>0\), positivo para todo \(n\) finito (mas **não** uniforme —
  reaproveita Contraexemplo 2 em disfarce espectral).
- \(\|f_n - \mathrm{id}\|_\infty = 1/n \to 0\), logo \(M_{f_n} \to
  M_{\mathrm{id}}\) em **norma de operador** (convergência mais forte que
  convergência forte de resolvente, que por sua vez é mais forte que
  convergência fraca de medidas espectrais).
- \(\mathrm{spec}(M_{\mathrm{id}}) = [0,1]\) (imagem essencial da
  identidade). Logo \(\mathrm{spec}(H) = \{0\}\cup[0,1] = [0,1]\) para
  \(H = 0\oplus M_{\mathrm{id}}\): **o gap fechou completamente** —
  \(0\) deixou de ser um ponto isolado do espectro.

**Leitura para YM:** mesmo sob a hipótese de convergência de operador
mais forte usualmente citada como suficiente (convergência em norma, a
fortiori convergência forte de resolvente), gap positivo em cada
aproximante não sobrevive ao limite sem uma hipótese adicional de
uniformidade (\(\inf_n \mathrm{gap}(H_n) \ge c > 0\)) — que é precisamente
`H6'` em `ASSUMPTIONS.md`. O resultado geral usado aqui — "espectro do
limite não expande sob convergência forte de resolvente, mas pode
contrair repentinamente" — está listado como **Verificado** em
`REVIEWS/AUDIT_REPORT.md` a partir de um levantamento de literatura de
análise espectral; a construção específica \(f_n = \max(x,1/n)\) acima é
autoral desta sessão (instância concreta do fenômeno geral), não uma
citação — não deve ser lida como resultado publicado.

**Por que não foi formalizado em Lean nesta rodada:** exigiria (a)
`Mathlib.Analysis.NormedSpace` + operadores de multiplicação em
`L^2`, (b) cálculo do espectro como imagem essencial (`Mathlib` tem
suporte parcial a operadores de multiplicação e seu espectro, mas
montar o exemplo completo com prova sem `sorry` está fora do orçamento de
tempo desta frente paralela). Registrado como gap de formalização, não
como afirmação sem prova — a prova em prosa acima é elementar e
verificável manualmente, mas não é `T` no sentido do laboratório
(`F ≠ T`, ver `AGENTS.md`/separação Lean-Python) até ser formalizada.
