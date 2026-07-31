# Questões de fonte não resolvidas

Registro das lacunas descobertas por esta auditoria. Nenhuma foi fechada.

---

## Q1 — Lei de Weyl **global** para a Classe W (bloqueante)

**Estado:** aberto. **Bloqueia:** etapa E de `SOURCE_BRIDGE_REQUIREMENTS.md`
e a hipótese W8 de `CLASS_W_SOURCE_MAPPING.md`.

Hörmander 1968 prova a assíntota **local** da função espectral na diagonal.
Não enuncia `N_P(Λ) ~ C_P Λ^{d/m}`. É necessária uma fonte que enuncie a
contagem global para a classe exata, ou uma dedução documentada do local
para o global (integração sobre `Ω` compacta, com uniformidade).

Candidatos **não obtidos e não lidos** (nenhum pode ser citado até ser
auditado):

- L. Hörmander, *The Analysis of Linear Partial Differential Operators*,
  vol. III/IV — o capítulo sobre assíntotas espectrais;
- M. A. Shubin, *Pseudodifferential Operators and Spectral Theory*;
- S. Agmon, trabalhos sobre autovalores de operadores elípticos;
- Yu. Safarov & D. Vassiliev, *The Asymptotic Distribution of Eigenvalues
  of Partial Differential Operators*;
- V. Ivrii, *Microlocal Analysis and Precise Spectral Asymptotics*.

Nota: a listagem de candidatos é **hipótese de trabalho bibliográfica**, não
atribuição de conteúdo. Nenhum deles foi verificado como contendo o
enunciado necessário.

## Q2 — Discretude do espectro (W7)

**Estado:** aberto. Hörmander 1968 não prova nem enuncia que o espectro é
discreto com multiplicidade finita. Em variedade compacta isto segue de
elipticidade (resolvente compacto), mas o teorema precisa de fonte.
Provavelmente resolvido pela mesma fonte de Q1.

## Q3 — Fibrados vetoriais / sistemas (W2)

**Estado:** aberto, com informação negativa explícita. Hörmander 1968,
p. 216: os métodos se aplicam a sistemas **com autovalores distintos do
símbolo principal**; para multiplicidade, „we have no information beyond“
Agmon–Kannai e Hörmander [8].

Duas saídas possíveis, ambas fora deste gate:
1. **estreitar** a Classe W para o caso escalar (ou autovalores distintos);
2. obter fonte que cubra fibrados gerais.

## Q4 — Formulação da auto-adjunção (W5)

**Estado:** divergência registrada. A Classe W exige **essencial
auto-adjunção**; Hörmander assume positividade formal e toma **uma**
extensão de Friedrichs („at least one self-adjoint extension“). Como o
espectro depende da extensão escolhida, o enunciado do no-go precisa dizer
*qual* extensão. Decisão pendente.

## Q5 — Paridade da ordem `m` (W3)

**Estado:** defeito de formulação descoberto. `OPERATOR_CLASS.md` admite
`m ≥ 1` inteiro qualquer. Elipticidade + positividade com símbolo principal
real forçam `m` **par** quando `d ≥ 2`. A classe declarada é vazia para `m`
ímpar. Corrigir a formulação (não o resultado) em gate futuro.

## Q6 — Convenção de fronteira na contagem dos zeros

**Estado:** menor, aberto. von Mangoldt escolhe `T` de modo que nenhum zero
tenha parte real igual a `T`; a definição moderna de `N_ζ(T)` usa
`0 < Im ρ ≤ T`. A reconciliação é elementar mas não está escrita.

## Q7 — Uso de resultados sobre zeros baixos em von Mangoldt

**Estado:** aberto por leitura parcial. A p. 18 invoca de la Vallée Poussin
(1899) para o fato de que os zeros em questão são reais e simples, e os
valores de Gram (1902). Pela leitura das pp. 1, 2, 18 e 19 isto é uso de
fatos **verificados para zeros baixos específicos**, não da RH — mas as
páginas 3–17 não foram lidas e a confirmação integral está pendente.
Nenhuma conclusão deste laboratório depende dessa confirmação, já que o
enunciado final da p. 19 é incondicional em sua forma.

## Q8 — Original alemão de Riemann 1859

**Estado:** não obtido. Só a tradução Wilkins (1998) está no acervo.
Nenhuma afirmação sobre a redação alemã original é feita.

## Q9 — EuDML inacessível

**Estado:** contornado. `https://eudml.org/doc/158173` retornou HTTP 403 a
acesso automatizado. O texto integral de von Mangoldt foi obtido pelo GDZ
(Göttingen), com PURL registrada no manifesto.

## Q10 — Leitura integral pendente

**Estado:** aberto por escolha de escopo.

| fonte | lido | não lido |
|---|---|---|
| VONMANGOLDT-1905 | pp. 1, 2, 18, 19 | pp. 3–17 (aparato numérico) |
| HORMANDER-1968 | Seções 1 e 5 | Seções 2–4, 6 |
| BOMBIERI-CLAY | Seção I e início da II | resto |
| RIEMANN-1859 (tradução) | integral | — |

`CONTENT_AUDITED` só se aplica a RIEMANN-1859 (tradução). Todas as demais
permanecem `PARTIALLY_AUDITED`. As perguntas obrigatórias do gate estão
respondidas pelas partes lidas; a verificação das **provas** não foi feita e
não fazia parte do mandato.
