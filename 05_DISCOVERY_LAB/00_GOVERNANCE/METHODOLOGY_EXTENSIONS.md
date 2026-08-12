# Extensões de metodologia

Seis ferramentas técnicas adicionadas à trilha de descoberta em 2026-08-12
(`DISC-DEC-003`), a pedido de revisão estratégica externa do usuário. Não
são conceitos filosóficos novos — o arquivo já tem demais disso. São
regras operacionais concretas, cada uma com uma formalização mínima e uma
consequência prática direta em `00_GOVERNANCE/AGENTS.md`.

## 1. Identificabilidade

**Pergunta:** mesmo que Tamesis explique o dado, existe alguma observação
que *somente* Tamesis explique?

$$P(D\mid\text{Tamesis}) \gg 0$$

não basta. O padrão exigido é:

$$P(D\mid\text{Tamesis}) \gg P(D\mid M_1),\, P(D\mid M_2),\, \dots$$

para pelo menos um domínio observável $D$, contra pelo menos um modelo
concorrente real e nomeado (não um espantalho).

**Regra operacional:** nenhum item pode avançar de `CANDIDATE_FORMULATING`
para `CANDIDATE_LOCKED` sem declarar, no próprio `PREREGISTRATION.md`, seu
**discriminating observable** — a observação específica e o modelo
concorrente específico que ela deveria conseguir separar. Um teste que só
pergunta "os dados são consistentes com Tamesis?" sem nomear o que os
tornaria mais consistentes com Tamesis do que com ΛCDM/MOND-padrão/GR
não-modificada/etc. não é um teste de descoberta — é uma checagem de
consistência, e deve ser rotulado como tal, não como candidato a claim.

*Nota retrospectiva:* o piloto `DISC-COSMOLOGY-MOND-SPARC-001` não
declarou um discriminating observable explícito — testou apenas se o sinal
EFE aparece, não se aparece de um jeito que ΛCDM não consegue replicar por
nenhum mecanismo convencional (seleção, tides, etc.). Isso é consistente
com o veredito INCONCLUSIVE ter sido o teto de informação que aquele
desenho conseguia entregar, independente do valor do p.

## 2. Renormalização / Effective Field Theory (para TRI/TDTR)

A Theory of Regime Interfaces já fala de regimes, transições, escalas,
universalidade, graus de liberdade, emergência — exatamente o território de
coarse-graining, pontos fixos e fluxos de renormalização.

$$\mathcal{R}_\lambda : X_{\text{micro}} \to X_{\text{macro}}$$
$$\mathcal{R}_\lambda(S) \to S^*$$

**Perguntas obrigatórias antes de qualquer execução TOE_INTERFACE:**
quais propriedades sobrevivem ao coarse-graining? Quais não sobrevivem?
Qual informação é eliminada? Qual operador é relevante, marginal ou
irrelevante sob $\mathcal{R}_\lambda$?

**Regra operacional:** qualquer novo item de linha TRI/TDTR precisa, no
pré-registro, nomear explicitamente o mapa $\mathcal{R}_\lambda$ candidato
(mesmo que informal/numérico nesta fase) e classificar pelo menos um
operador/observável como relevante, marginal ou irrelevante sob ele. Sem
isso, TRI continua sendo linguagem interessante sem conexão matemática
testável com física conhecida — o problema que o próprio relatório de
visão do laboratório já identificava (necessidade de monotones, classes
formais, validação fora da amostra).

## 3. Minimum Description Length / complexidade algorítmica

O programa Tamesis já pergunta, em prosa, se sistemas de recursos finitos
criam novas camadas quando o custo delas é compensado por redução de erro,
dissipação, instabilidade, ou busca futura. Isso vira função objetivo:

$$J = L(M) + L(D\mid M) + \lambda E + \mu T$$

onde $L(M)$ é a complexidade descritiva do modelo, $L(D\mid M)$ é a
informação necessária para explicar os dados dado o modelo, $E$ é custo
energético, $T$ é custo temporal/computacional, e $\lambda,\mu$ são pesos
declarados a priori (não ajustados depois de ver o resultado).

Uma transição de camada é interessante quando:

$$\Delta J = J_{\text{nova camada}} - J_{\text{camada antiga}} < 0$$

**Regra operacional:** qualquer teste que envolva comparar "modelo com uma
camada/grau de liberdade a mais" vs. "modelo sem essa camada" deve
declarar $L(M)$, $L(D|M)$, $E$, $T$ (ou o subconjunto aplicável) e os pesos
$\lambda,\mu$ no pré-registro, e reportar $\Delta J$ explicitamente. **MDL
não prova Tamesis** — é uma ferramenta para transformar uma intuição verbal
("a camada nova vale o custo") em número mensurável, comparável entre
testes.

## 4. Descoberta automática de invariantes

O fluxo atual (ler → raciocinar → propor lema → formalizar) deixa a LLM
escrever a hipótese primeiro e testar depois — risco alto de história
convincente sem sinal real por trás.

**Regra operacional, quando o teste envolver busca de padrão numérico em
múltiplas trajetórias/regimes/domínios:** a busca por
$f(x_1,\dots,x_n) \approx C$ ao longo de regimes deve ser feita por método
de descoberta direta ANTES de qualquer interpretação por LLM — regressão
simbólica, sparse equation discovery, restrições dimensionais, busca de
leis de conservação, busca de simetria, invariantes de grafo/espectrais.
A LLM entra depois, só para interpretar candidatos que já sobreviveram à
busca cega — nunca para propor a forma funcional primeiro. A pergunta
correta é "encontre expressões simples que permaneçam invariantes sob
estas N trajetórias e depois tente destruí-las", não "que equação você acha
que existe?".

*Nota de escopo:* este laboratório ainda não tem infraestrutura de
regressão simbólica instalada. Nenhum item pode alegar ter seguido esta
regra até essa infraestrutura existir e estar documentada (ver
`03_REPLICATION_GATE` para o padrão de auditoria que se aplicaria).

## 5. Descoberta adversarial de nulos

A reexecução adversarial de `00_GOVERNANCE/AGENTS.md` passo 7 já existe e
tenta refutar o resultado. Isso não é a mesma coisa que tentar **explicar**
o resultado sem Tamesis.

**Regra operacional:** para qualquer candidato que sobreviva à reexecução
adversarial padrão e entre no Gate de Replicação, um agente separado deve
ser instruído especificamente como debunker convencional — não "isso está
certo?", mas "destrua esta anomalia usando qualquer mecanismo conhecido":
selection bias, erro de calibração, parâmetros de nuisance, overfitting,
vazamento de dado, precisão numérica, artefato de coordenadas, erro de
unidade, relação dimensional trivial, contaminação de dataset,
look-elsewhere effect. Um segundo agente, se o candidato ainda sobreviver,
tenta construir um modelo convencional (ΛCDM/GR-padrão/o que for aplicável
ao domínio) que reproduza o mesmo resultado sem qualquer ingrediente
Tamesis. Este papel é tão obrigatório no Gate quanto o agente que reproduz
a análise.

## 6. Predição cega / holdout selado

**Regra operacional, obrigatória para qualquer teste sobre um dataset com
múltiplas unidades amostrais (galáxias, séries temporais, sistemas,
etc.):** o pré-registro deve declarar um split de três partes ANTES de
qualquer análise —

```text
discovery   (a maior parte -- pode ser torturada livremente: milhares de
             equações, buscas exaustivas, o que for preciso)
development (ajuste/calibração de parâmetros livres, se houver)
holdout     (selado -- ninguém, nem humano nem agente, olha antes do lock)
```

Quando uma hipótese é congelada (commit + sha256 + parâmetros do modelo
fixados), só então o holdout é aberto — dentro do Gate de Replicação
(`03_REPLICATION_GATE/PROTOCOL.md`), nunca antes. Isso não elimina o
problema de geração massiva de hipóteses por LLM (que pode achar milhões de
padrões acidentais no conjunto conhecido) — mas uma hipótese congelada
antes de ver o holdout não pode ser retroativamente ajustada para "prever
corretamente" dado que já não visto anteriormente.

*Nota de escopo:* o piloto SPARC não usou holdout (usou o catálogo inteiro
para uma única comparação de grupo, sem parâmetro livre ajustado). Esta
regra vale a partir de agora para testes com espaço de busca maior — em
particular, qualquer teste de regressão simbólica (item 4) ou de MDL/ajuste
de modelo (item 3) exige holdout selado antes de rodar.
