# Hipóteses

Auditoria `PVSNP-PHYS-001`. Substitui o placeholder `NOT_AUDITED`.

## 1. Hipóteses estruturais usadas em `DEFINITIONS.md`

```text
H1  a nocao de "polinomial" em cost_{M,R} e herdada da nocao classica de
    polinomio em uma variavel de tamanho -- nao redefinida fisicamente
H2  o esquema de codificacao E e fixado ANTES de perguntar se (E,M,R)
    admite ponte de simulacao (Secao 3 de DEFINITIONS.md) -- comparar
    triplas com E diferentes nao e uma comparacao valida
H3  "certificado fisico" em NP_phys(E,M,R) e um dado de mesma natureza que
    o certificado classico (verificavel em tempo polinomial), transportado
    para o modelo M -- nenhuma nova nocao de "certificado" e introduzida
```

Nenhuma destas é um axioma matemático novo: são convenções de notação
necessárias para que a Seção 2 de `DEFINITIONS.md` faça sentido, análogas às
convenções usadas para definir `P`/`NP` clássicos (ex.: escolha de alfabeto
binário).

## 2. A tensão real da literatura: precisão idealizada vs. física realista

Os modelos citados em `DEFINITIONS.md` §4 se dividem em dois grupos por uma
única hipótese de modelagem física, não por um axioma lógico:

```text
grupo A  precisao real/infinita idealizada
         (BSS sobre R/C; ARNN de Siegelmann-Sontag com pesos reais exatos)
         -> poder "super-Turing" ou fora de P/NP classico

grupo B  precisao finita, ruido termico/analogico presente
         (modelo de ruido analogico de Maass-Orponen 1998)
         -> poder colapsa a automatos finitos / classes classicas
```

Qual hipótese descreve melhor um computador físico real (matéria
condensada, termodinâmica em temperatura finita) é uma questão empírica de
física, não uma questão que este laboratório decide. Isto é o núcleo do que
a literatura chama informalmente de tese de Church-Turing física / estendida
(Deutsch 1985; ver `KNOWN_RESULTS_MATRIX.md`) — e é precisamente por isso
que nenhuma tripla `(E,M,R)` do grupo A ou B, por si só, decide `P` vs `NP`
clássico: a divergência de poder entre os grupos A e B é sobre *física*
(quanto ruído um sistema físico real tem), não sobre a estrutura combinatória
que `P` vs `NP` questiona.

## 3. Sobre o "Physical Computation Axiom" (PCA) do documento legado

`RECURSOS_PARA_PESQUISA/07_MILLENNIUM_VALIDATION/PROBLEM_01_P_VS_NP/01_STATUS/ANALISE_CRITICA_PNP.md`
(legado, somente leitura) descreve um "Physical Computation Axiom (PCA)" —
constituído de "toda computação física tem precisão finita", "ruído
termodinâmico é inevitável", "limites de energia implicam limites de
tempo" — como base de uma alegação anterior de que "ZFC + PCA ⊢ P≠NP".

**Busca feita nesta sessão** (WebSearch, 2026-08-09) pelo termo exato
"Physical Computation Axiom" associado a P vs NP não encontrou o termo em
nenhuma das fontes primárias localizadas (Aaronson 2005; Blum–Shub–Smale
1998; Maass–Orponen 1998; Bürgisser–Cucker 2006; Deutsch 1985). O termo não
é reconhecido como estabelecido na literatura de teoria da complexidade
computacional pesquisada nesta sessão.

Isto **não prova que o PCA seja falso ou sem sentido** — apenas que esta
sessão não conseguiu localizar uma fonte primária externa para ele. Por
`AGENTS.md` ("não inventar referências"), qualquer alegação anterior que
dependa do PCA como se fosse um resultado citável da literatura deve ser
tratada como **não verificada nesta sessão**, não como fato. O próprio
documento legado já sinaliza isto como gap crítico (ver seção "Gap 2" do
`ANALISE_CRITICA_PNP.md`): o PCA é, na melhor leitura, uma hipótese de
modelagem física proposta internamente ao projeto Tamesis anterior a esta
auditoria, equivalente em espírito (mas não identicamente citável) às
hipóteses de "grupo B" acima — precisão finita, ruído inevitável — que
*são* objeto de resultados formais reais (Maass–Orponen 1998), mas que não
constituem, por si só, um axioma de ZFC nem uma prova matemática de
`P ≠ NP`.

## 4. O que permanece `NOT_AUDITED`

```text
qualquer hipotese especifica de um paper fisico nao citado nesta sessao
qualquer alegacao de reducao k-SAT -> vidro de spin especifica
  (o documento legado cita "Talagrand/Parisi" para isto; Talagrand 2006
  prova a formula de Parisi para o MODELO SK em si, nao uma reducao de
  k-SAT -- ver ressalva em KNOWN_RESULTS_MATRIX.md e REVIEWS/AUDIT_REPORT.md)
```
