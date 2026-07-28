# Roadmap Tamesis–Clay 2026

**Corte:** 28 de julho de 2026

**Objetivo:** converter o arquivo exploratório em um programa matemático auditável, publicável e compatível com os enunciados e regras do Clay Mathematics Institute

**Documento de base:** `RELATORIO_INTEGRAL_DO_PROGRAMA_TAMESIS_2026.md`

---

## 1. Resultado pretendido

O próximo ciclo não deve tentar “fechar os sete problemas” em paralelo. Deve produzir, nesta ordem:

1. um registro de alegações corrigido;
2. enunciados exatos e independentes da linguagem Tamesis;
3. resultados parciais verdadeiros, mesmo quando negativos;
4. provas que sobrevivam a revisão adversarial;
5. preprints especializados;
6. publicação em veículos matemáticos qualificáveis;
7. apenas se uma prova completa existir e for aceita, o processo Clay.

Poincaré não é uma frente de resolução: já foi resolvido por Perelman. Ele entra como benchmark de como uma solução real foi verificada, publicada e aceita.

---

## 2. O que “padrão Clay” significa

As regras vigentes do Clay Mathematics Institute foram revisadas em 2018. O CMI:

- não aceita submissão direta de supostas soluções;
- exige publicação em um **Qualifying Outlet**;
- só considera uma solução após pelo menos dois anos da publicação;
- exige aceitação geral pela comunidade matemática mundial.

Fonte: [Rules for the Millennium Prize Problems](https://www.claymath.org/millennium-problems/rules/).

Portanto, “padrão Clay” não é um estilo de PDF nem um selo interno. É uma cadeia:

```text
enunciado oficial
    → prova completa
    → auditoria especializada
    → preprint público
    → publicação qualificável
    → pelo menos dois anos
    → aceitação geral
    → eventual consideração pelo CMI
```

O enunciado de referência deve ser o volume oficial [Millennium Prize Problems](https://www.claymath.org/wp-content/uploads/2022/02/MPPc.pdf), não uma paráfrase do arquivo.

---

## 3. Regras operacionais não negociáveis

### 3.1 Vocabulário

Usar:

- `CONJECTURE`;
- `CONDITIONAL_THEOREM`;
- `PARTIAL_RESULT`;
- `COMPUTATIONAL_EVIDENCE`;
- `COUNTEREXAMPLE_SEARCH`;
- `OPEN_GAP`;
- `RETRACTED_CLAIM`;
- `EXTERNALLY_VERIFIED`.

Não usar `SOLVED`, `PROOF COMPLETE`, `100%`, `CLOSED` ou `CLAY READY` enquanto todos os gates formais não estiverem satisfeitos.

### 3.2 Uma proposição por artefato

Cada paper deve ter:

1. um enunciado principal;
2. hipóteses numeradas;
3. dependências explícitas;
4. uma prova ou refutação;
5. relação exata com o problema Clay;
6. seção “o que este resultado não prova”.

### 3.3 Intuição física não substitui matemática

Entropia, energia, irreversibilidade, universalidade e pressão podem motivar um lema. A prova precisa usar objetos e inferências do enunciado oficial.

### 3.4 Código é instrumento de falsificação

Simulações devem:

- procurar contraexemplos;
- testar constantes e sinais;
- revelar dependências ocultas;
- validar álgebra em casos finitos;
- gerar conjecturas.

Não devem ser apresentadas como prova de uma afirmação universal.

### 3.5 Sem percentuais de completude

Substituir “85% resolvido” por uma lista binária de obrigações:

```text
[ ] enunciado oficial coberto
[ ] hipóteses declaradas
[ ] todos os lemas provados
[ ] nenhum argumento circular
[ ] nenhum limite informal
[ ] casos de fronteira tratados
[ ] revisão adversarial concluída
[ ] revisão externa recebida
```

### 3.6 Bibliografia verificável

Toda citação precisa conter:

- referência primária;
- enunciado exato usado;
- hipóteses;
- página/teorema;
- direção da implicação;
- nota sobre generalidade.

Um resultado “conhecido” não pode ser ampliado por semelhança.

---

## 4. Arquitetura recomendada no repositório

Criar, no próximo ciclo de implementação, sem mover o legado:

```text
07_MILLENNIUM_VALIDATION/
├── CLAY_2026/
│   ├── 00_GOVERNANCE/
│   │   ├── CLAIM_LEDGER.yaml
│   │   ├── BIBLIOGRAPHY_LEDGER.yaml
│   │   ├── STATUS_POLICY.md
│   │   └── RETRACTIONS_AND_CORRECTIONS.md
│   ├── 01_P_VS_NP/
│   ├── 02_RIEMANN/
│   ├── 03_NAVIER_STOKES/
│   ├── 04_YANG_MILLS/
│   ├── 05_HODGE/
│   ├── 06_BSD/
│   ├── 07_POINCARE_BENCHMARK/
│   └── 99_CROSS_PROBLEM_TOOLS/
├── RELATORIO_INTEGRAL_DO_PROGRAMA_TAMESIS_2026.md
└── ROADMAP_CLAY_2026.md
```

Cada problema deve conter:

```text
OFFICIAL_STATEMENT.md
KNOWN_RESULTS_MATRIX.md
CLAIM.md
ASSUMPTIONS.md
DEPENDENCY_DAG.md
PROOF.md
GAP_REGISTER.md
COUNTEREXAMPLES/
COMPUTATION/
EXTERNAL_REVIEWS/
REPRODUCIBILITY.md
STATUS.json
```

O legado permanece somente leitura. Novas alegações vivem em `CLAY_2026`.

---

## 5. Gates universais

### G0 — Identidade do problema

- copiar o enunciado oficial com fonte;
- fixar convenções;
- escrever critérios equivalentes apenas com prova/citação;
- listar o que não conta como solução.

### G1 — Independência da linguagem Tamesis

O resultado deve ser compreensível e verificável por um especialista que nunca leu TRI, TDTR ou Tamesis. Se um conceito novo for necessário, ele deve ser definido formalmente e ligado ao objeto clássico por um teorema.

### G2 — DAG de dependências

Toda seta da prova deve apontar para:

- axioma padrão;
- teorema publicado sob hipóteses satisfeitas;
- lema provado no próprio texto.

Qualquer seta “fisicamente deve”, “numericamente vemos” ou “por universalidade” é um gap.

### G3 — Auditoria adversarial interna

Executar:

- verificação dimensional;
- troca de quantificadores;
- casos-limite;
- sinais;
- convergência uniforme versus pontual;
- compactação versus unicidade;
- dependência de regularização;
- circularidade;
- contraexemplos pequenos.

### G4 — Revisão especializada externa

Enviar apenas o resultado parcial preciso, não todo o arquivo. Pedir ao revisor:

1. primeiro passo inválido;
2. hipótese oculta;
3. teorema de literatura mal aplicado;
4. contraexemplo provável.

### G5 — Preprint reprodutível

O pacote inclui:

- LaTeX mínimo;
- código e dados, se relevantes;
- ambiente reproduzível;
- lista de mudanças;
- declaração explícita de escopo.

### G6 — Publicação

Submeter ao periódico adequado ao resultado real. Um teorema parcial deve ser publicado como teorema parcial.

### G7 — Candidatura Clay

Esse gate só existe depois da publicação, do prazo mínimo de dois anos e de aceitação geral. Não há contato direto para “validar antes”.

---

## 6. Priorização do portfólio

O arquivo não oferece base para estimar “probabilidade de resolver” nenhum problema. A priorização abaixo considera apenas a chance de gerar um **resultado parcial verificável** com os ativos já existentes.

| Prioridade | Frente | Próximo produto legítimo |
|---|---|---|
| 1 | Navier–Stokes | auditoria/refutação ou versão correta do lema de pressão–alinhamento |
| 1 | Riemann | teorema parcial/no-go espectral sem circularidade |
| 2 | P vs NP | paper separado sobre complexidade física, sem alegar resolver P vs NP |
| 2 | Yang–Mills | mapa rigoroso de quais limites da rede não preservam o gap |
| 3 | Hodge | nota crítica sobre loci de Hodge versus classes algébricas |
| 3 | BSD | matriz auditada de hipóteses e casos conhecidos |
| benchmark | Poincaré | estudo do processo de validação de Perelman |

Navier–Stokes e Riemann devem ser as frentes matemáticas primárias. Não porque estejam “perto de uma solução”, mas porque o arquivo contém nelas um gargalo formulável que pode ser provado, enfraquecido ou refutado.

---

## 7. Roadmap por problema

### 7.1 P versus NP

#### Enunciado a preservar

Determinar se toda linguagem aceita em tempo polinomial por uma máquina de Turing não determinística também é aceita em tempo polinomial por uma máquina determinística.

#### O que preservar do arquivo

- definição de custos físicos;
- Princípio de Custo de Ação como hipótese de modelo;
- experimentos de concentração;
- distinção entre verificabilidade e busca em sistemas físicos.

#### O que reclassificar

`P_phys ≠ NP_phys`, se corretamente provado, é um resultado de complexidade física. Não implica automaticamente \(P\ne NP\).

#### Pacote imediato

1. definir formalmente \(P_{\mathrm{phys}}\) e \(NP_{\mathrm{phys}}\);
2. provar fechamento, robustez de codificação e dependência do modelo;
3. construir exemplos que separem custo físico de tempo Turing;
4. procurar um contraexemplo à redução universal alegada;
5. transformar o resultado em paper autônomo.

#### Para voltar ao problema Clay

Seria necessária uma técnica de lower bounds aplicável ao modelo Turing padrão e compatível com barreiras conhecidas. Nenhuma ponte física deve ser aceita sem um teorema de simulação nos dois sentidos e controle polinomial.

#### Critério de interrupção

Se a separação desaparecer sob mudança razoável de codificação ou se a redução introduzir custo superpolinomial, encerrar a rota Clay e publicar apenas a teoria física condicional.

---

### 7.2 Hipótese de Riemann

#### Enunciado a preservar

Todos os zeros não triviais de \(\zeta(s)\) têm parte real \(1/2\).

#### O que preservar

- decomposição de fase;
- cálculo de cúspide;
- dicionário Selberg–Weil;
- análise de operadores;
- no-go de superfícies/operadores excessivamente simples;
- scripts espectrais.

#### Pacote imediato A — resultado parcial

Formular o no-go mais forte que possa ser provado sem RH:

> uma classe explicitamente definida de operadores ou superfícies hiperbólicas não pode realizar simultaneamente as propriedades espectrais X, Y e Z necessárias à rota Hilbert–Pólya proposta.

Passos:

1. definir domínio e auto-adjunticidade;
2. fixar a fórmula de traço usada;
3. remover toda entrada que dependa de GUE;
4. provar estimativas de erro com convergência declarada;
5. testar contra exemplos clássicos.

#### Pacote imediato B — termo fora da diagonal

Isolar uma única estimativa não circular. Se ela for equivalente a RH ou mais forte, registrar isso como resultado diagnóstico, não como progresso de prova.

#### Rotas proibidas

- usar GUE como premissa para provar RH;
- construir operador cujo espectro já seja definido pelos zeros;
- chamar equivalência de positividade de demonstração da positividade;
- inferir localização de todos os zeros de amostras finitas.

#### Gate Clay específico

Uma prova deve localizar todos os zeros não triviais, não apenas reproduzir contagem assintótica, estatística local ou os primeiros zeros.

---

### 7.3 Navier–Stokes

#### Enunciado a preservar

Usar exatamente uma das alternativas oficiais de existência e suavidade ou de breakdown para o sistema tridimensional, com dados e domínio especificados no texto Clay.

#### O que preservar

- identidade da enstrofia;
- análise da Hessiana de pressão;
- geometria da vorticidade;
- DNS como mecanismo de busca;
- cadeia pressão → alinhamento → estiramento → regularidade.

#### Pacote imediato A — auditoria do lema crítico

Reescrever o lema de dominância/rotação:

- quantificadores completos;
- normas e espaços;
- dependência temporal;
- condições de contorno;
- constantes;
- sinal exato.

Depois:

1. verificar a identidade por cálculo simbólico;
2. testar famílias explícitas: shear, Burgers vortex, Taylor–Green e soluções axisimétricas;
3. procurar campos divergência-zero que violem o sinal;
4. separar afirmação pontual, média e integrada;
5. verificar se o lema já implica regularidade global.

#### Pacote imediato B — teorema condicional honesto

Se a cadeia posterior estiver correta, publicar:

> sob a hipótese quantitativa H sobre a Hessiana de pressão/alinhamento, soluções suaves permanecem regulares.

Isso só é novo se H for mais verificável ou mais fraca que critérios já conhecidos.

#### Rotas proibidas

- usar K41 como estimativa determinística;
- trocar controle \(L^2\) por \(L^\infty\) sem embedding/interpolação válida;
- citar critério de Euler como se fosse automaticamente o critério necessário para Navier–Stokes;
- assumir que pressão sempre regulariza.

#### Critério de interrupção

Se um contraexemplo suave violar o lema ou se H for equivalente à própria regularidade, reclassificar a rota como diagnóstico geométrico e não como solução.

---

### 7.4 Yang–Mills e gap de massa

#### Enunciado a preservar

Para todo grupo de gauge compacto simples \(G\), construir uma teoria quântica de Yang–Mills não trivial em \(\mathbb R^4\), satisfazendo axiomas pelo menos tão fortes quanto os exigidos na formulação oficial, e provar um gap \(\Delta>0\).

#### O que preservar

- código de rede;
- expansão de acoplamento forte;
- mapas de reflexão positiva;
- documentação de reconstrução OS;
- análise do gap em volumes finitos.

#### Dividir em quatro projetos

1. **medidas em rede e volume infinito**;
2. **limite contínuo e não trivialidade**;
3. **reconstrução axiomática**;
4. **gap uniforme e sua preservação**.

Nenhum projeto pode emprestar a conclusão do seguinte.

#### Pacote imediato

Produzir um teorema de impossibilidade/insuficiência:

> tightness mais gap positivo em cada cutoff não implica, sem hipóteses adicionais explícitas, uma teoria contínua única com gap positivo.

Construir exemplos abstratos de sequências de operadores em que o gap colapse no limite. Isso transformará uma falha da tentativa em resultado matemático útil.

#### Colaboração necessária

Esta frente requer especialista em constructive QFT, teoria de gauge na rede, probabilidade e análise espectral. Código sozinho não fecha a construção.

#### Rotas proibidas

- inferir gap uniforme de positividade nos extremos;
- usar Svetitsky–Yaffe fora de suas hipóteses;
- identificar anomalia do traço com prova espectral;
- confundir subsequência com limite único;
- confundir Wilson loop numérico com axiomas de uma QFT em \(\mathbb R^4\).

---

### 7.5 Conjectura de Hodge

#### Enunciado a preservar

Para uma variedade algébrica projetiva não singular sobre \(\mathbb C\), classes de Hodge racionais devem ser combinações racionais de classes de ciclos algébricos.

#### O que preservar

- cálculo de períodos;
- variação de estruturas de Hodge;
- loci de Hodge;
- exemplos computacionais;
- taxonomia de classes candidatas.

#### Pacote imediato

Escrever uma nota rigorosa:

> o que o teorema de Cattani–Deligne–Kaplan prova e por que ele não implica a Conjectura de Hodge.

Depois escolher uma família restrita de variedades onde:

- as classes de Hodge sejam computáveis;
- o grupo de ciclos conhecido possa ser comparado;
- um resultado especial novo seja plausível.

#### Rotas proibidas

- converter algebricidade do locus em algebricidade da classe;
- usar transversalidade como sobrejetividade;
- usar conjectura de períodos como lema provado;
- extrapolar de ausência de ghosts em amostra finita.

#### Gate Clay específico

É necessária uma prova geral da afirmação racional oficial. Um algoritmo explícito é opcional; existência demonstrada é essencial.

---

### 7.6 Birch e Swinnerton-Dyer

#### Enunciado a preservar

A ordem do zero de \(L(E,s)\) em \(s=1\) deve ser igual ao posto de \(E(\mathbb Q)\), além da fórmula refinada quando se alega a conjectura completa.

#### O que preservar

- base de curvas e scripts;
- mapa de Gross–Zagier/Kolyvagin;
- teoria de Iwasawa;
- twists e base change;
- cálculos de posto e invariantes.

#### Pacote imediato A — matriz de hipóteses

Para cada teorema citado, registrar:

| Campo | Conteúdo |
|---|---|
| curva/variedade permitida | exato |
| posto permitido | exato |
| primo | condições |
| redução | ordinária/supersingular/etc. |
| conclusão | posto, \(\Sha\), leading term |
| direção | algébrica → analítica ou inversa |

Depois calcular a união real de cobertura. Não usar a palavra “todas” sem prova de exaustão.

#### Pacote imediato B — estudo de caso

Escolher uma família específica ainda interessante e provar/computar um resultado condicionado claramente. A meta inicial é um paper de casos, não BSD geral.

#### Rotas proibidas

- somar coberturas condicionais incompatíveis;
- inferir as duas parcelas de \(L(E/K)=L(E)L(E^\chi)\) conhecendo apenas o produto;
- usar \(\mu=0\) como finitude automática de \(\Sha\) em todos os primos;
- trocar main conjecture \(p\)-ádica pela fórmula complexa completa sem ponte.

#### Colaboração necessária

Especialista em curvas elípticas/Iwasawa deve auditar cada teorema e cada hipótese antes de novo manuscrito.

---

### 7.7 Poincaré como benchmark

Não desenvolver uma nova “resolução Tamesis”. Construir um estudo de caso:

- enunciado exato;
- papel do fluxo de Ricci;
- cirurgia;
- preprints de Perelman;
- verificação comunitária;
- exposições completas posteriores;
- critérios usados pelo Clay.

Produto: `POINCARE_VERIFICATION_BENCHMARK.md`, uma lista de lições para as seis frentes.

---

## 8. Plano temporal

Os prazos abaixo são para produzir artefatos auditáveis, não para resolver os problemas.

### Dias 1–14 — saneamento

- criar `CLAY_2026/00_GOVERNANCE`;
- registrar todas as alegações de “solved/closed/100%”;
- marcar cada uma como histórica, retraída, condicional ou aberta;
- copiar os sete enunciados oficiais;
- congelar os dossiês antigos como legado;
- escolher responsáveis e revisores por frente.

**Entrega:** claim ledger e política de status.

### Dias 15–30 — dependências

- construir DAG de cada tentativa;
- validar bibliografia primária;
- localizar o primeiro passo não demonstrado;
- apagar percentuais de progresso da camada nova;
- escolher Navier–Stokes e RH como frentes primárias.

**Entrega:** seis `GAP_REGISTER.md` e seis `DEPENDENCY_DAG.md`.

### Dias 31–60 — falsificação

- NS: procurar contraexemplo ao lema de pressão;
- RH: remover GUE e testar o no-go;
- P vs NP: testar invariância de codificação;
- YM: construir exemplo de colapso do gap no limite;
- Hodge: testar a inferência CDK;
- BSD: construir matriz de hipóteses.

**Entrega:** relatórios de auditoria executáveis.

### Dias 61–90 — primeiro paper honesto

Escolher um resultado que sobreviveu:

- teorema condicional de NS;
- no-go espectral de RH;
- teoria de complexidade física;
- nota de insuficiência no limite de YM;
- nota crítica de Hodge;
- matriz/caso de BSD.

Redigir um único preprint especializado com seção explícita de limitações.

**Entrega:** preprint v0.1, ainda sem alegação Clay.

### Meses 4–6 — revisão externa

- obter duas leituras especializadas independentes;
- registrar objeções integralmente;
- responder com mudanças ou retração;
- reproduzir cálculos em ambiente limpo;
- submeter seminário ou workshop da área.

**Entrega:** relatório de revisão adversarial e preprint v0.2.

### Meses 7–12 — publicação de resultado parcial

- submeter o teorema real ao periódico adequado;
- manter código e errata públicos;
- não ampliar a conclusão na comunicação;
- iniciar o próximo pacote apenas depois da decisão sobre o primeiro.

**Entrega:** submissão verificável de resultado parcial.

### Após uma possível prova completa

1. auditoria interna integral;
2. especialistas independentes;
3. preprint;
4. seminários;
5. periódico qualificável;
6. correção de objeções;
7. dois anos e aceitação geral;
8. somente então, consideração pelas regras do CMI.

---

## 9. Roadmap paralelo do ramo físico

O programa \(M_c\) não deve ser misturado às provas Clay, mas pode continuar em paralelo sem mudar o contrato congelado.

### Próximos passos autorizados

1. identificar até cinco laboratórios adequados;
2. receber inventário Q0 real;
3. documentar rejeições técnicas;
4. qualificar instrumento e amostra;
5. obter primeiro espectro bruto GeV identificado;
6. executar A0;
7. decidir se A1 é viável;
8. congelar previsões antes do reveal.

### Proibições

- não criar v0.7 sem necessidade de hardware documentada;
- não ajustar \(M_c\) após observar dados;
- não chamar A0 de teste de Tamesis;
- não avançar A2 sem gates;
- não usar o sucesso do software como evidência física.

Esse ramo é um bom modelo de governança para a matemática: hipóteses congeladas, decisões pré-definidas e estados bloqueados.

---

## 10. Papéis mínimos

Cada frente deve ter:

- **autor da prova** — constrói o argumento;
- **adversário interno** — procura o primeiro erro;
- **auditor bibliográfico** — valida teoremas citados;
- **auditor computacional** — reproduz código sem contexto privilegiado;
- **especialista externo** — avalia a matemática da área;
- **curador de status** — impede promoção epistemológica indevida.

Uma pessoa pode acumular papéis no início, mas não pode ser o único aprovador de sua própria prova.

---

## 11. Métricas de progresso

Medir:

- número de gaps removidos por prova;
- número de alegações retraídas/corrigidas;
- número de citações com hipóteses validadas;
- contraexemplos encontrados;
- ambientes reproduzidos de forma limpa;
- revisões externas recebidas;
- resultados parciais submetidos/publicados.

Não medir:

- porcentagem de “solução”;
- volume de páginas;
- quantidade de simulações;
- proximidade narrativa com o problema;
- número de vezes que um resultado conhecido foi recuperado.

---

## 12. Critério de sucesso para o próximo ciclo

O ciclo 2026–2027 será bem-sucedido se entregar:

1. arquivo de alegações corrigido;
2. seis dossiês com enunciado e gaps exatos;
3. benchmark Poincaré;
4. ao menos um resultado parcial que sobreviva a dois revisores externos;
5. ao menos uma rota encerrada por contraexemplo ou equivalência ao problema original;
6. nenhuma nova declaração prematura de solução;
7. no ramo físico, um Q0 real ou uma rejeição técnica documentada.

Resolver um Problema do Milênio não é uma meta gerenciável por calendário. Produzir matemática verdadeira, verificável e cumulativa é.

---

## 13. Decisão recomendada agora

Iniciar dois sprints de auditoria, não dois sprints de “prova”:

1. **Navier–Stokes:** tentar destruir ou corrigir o lema da Hessiana de pressão;
2. **Riemann:** extrair um no-go espectral independente de GUE.

Em paralelo:

- converter P versus NP em paper de complexidade física;
- usar Yang–Mills, Hodge e BSD como frentes de revisão bibliográfica especializada até que apareça um novo lema genuíno;
- usar Poincaré como padrão histórico de verificação;
- manter \(M_c\) congelado até a chegada de hardware e metrologia.

Essa estratégia preserva a ambição do Programa Tamesis, mas troca “fechamentos” rápidos por resultados que podem permanecer verdadeiros depois da auditoria.
