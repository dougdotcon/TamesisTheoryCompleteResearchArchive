# Programa: Camadas de Realidade, Consciência e os Limites da Lógica

**Status:** ABERTO — 4 linhas candidatas em Fase 0 (escopo/dado real sendo localizado)
**Origem:** dois documentos fornecidos pelo usuário em 2026-08-27 ("Linhas de
Pesquisa: Camadas de Realidade, Consciência e os Limites da Lógica" e
"Serial Experiments Lain: Ideias Verificáveis vs. Ficção Especulativa"),
ambos já pré-classificados por status epistêmico pelo próprio usuário.
**Decisão de governança:** `DISC-DEC-101` (`05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`)
**Ledger operacional:** `05_DISCOVERY_LAB/01_PORTFOLIO/TEST_QUEUE.yaml` (linhas
`DISC-SCHUMANN-RESONANCE-001`, `DISC-IIT-PHI-REPRO-001`,
`DISC-FEP-PREDICTIVE-CODING-001`) e `04_FORMAL_RESEARCH_LAB/02_FOUNDATIONS`
(linha de lógica não-clássica, ver §3 abaixo).

Este documento aplica ao conteúdo dos dois textos fornecidos exatamente a
mesma disciplina que já rege este laboratório desde `DISC-DEC-003`
(`00_GOVERNANCE/RESEARCH_PIPELINE.md`, `AGENTS.md`): toda linha nova entra
como candidata de risco alto em `05_DISCOVERY_LAB/02_TESTS/`, com
pré-registro travado ANTES de tocar em dado real, reexecução adversarial
obrigatória, e nenhuma alegação de "Tamesis confirmado" ou de progresso
sobre qualquer Problema do Millênio a partir de um único teste. Os próprios
documentos do usuário já fazem a triagem inicial testável/não-testável com
um rigor que este laboratório reconhece como o seu próprio — a tabela
abaixo herda essa triagem e a conecta à infraestrutura concreta já
existente aqui.

---

## 1. Tabela mestra

| # | Item (dos dois documentos) | Categoria | Destino no laboratório |
|---|---|---|---|
| A | Free Energy Principle / predictive coding | Testável, escopo amplo | `DISC-FEP-PREDICTIVE-CODING-001` — Fase 0 (busca de alvo falsificável estreito) |
| B | IIT / Φ (Tononi) | Testável, parcial | `DISC-IIT-PHI-REPRO-001` — Fase 0 (localizar valor Φ publicado para reproduzir) |
| C | Decoerência quântica (fenda dupla) | Ciência estabelecida, não é hipótese nova | **Não vira linha de teste** — ver §5 |
| D.1 | Teoremas de Gödel formalizados | Formalizável, mas de escopo massivo | Levantamento apenas (ver §3) — não prometido como alvo alcançável |
| D.2 | Lógicas não-clássicas (paraconsistente/fuzzy) em Lean4 | Formalizável, escopo tratável | Nova linha exploratória em `04_FORMAL_RESEARCH_LAB/02_FOUNDATIONS` (ver §3) |
| E | Auto-similaridade fractal / MUH | Parcialmente testável (fractal); MUH não-testável | Fractal/SOC **já testado e fechado** em `TRI_RG` (`CLOSED_NULL`) — ver §4. MUH literal: fora de escopo, ver §6 |
| F | Terror Management Theory | Ciência estabelecida, citação de fundo | Sem linha dedicada — contexto, não hipótese nova a testar |
| G | Umwelt (von Uexküll) | Conceito estabelecido, citação de fundo | Sem linha dedicada |
| H | Modelo de auto-representação (Metzinger) | Framework teórico estabelecido, citação de fundo | Sem linha dedicada |
| Lain-1 | Ressonância de Schumann (fenômeno físico) | Testável, dado público real | `DISC-SCHUMANN-RESONANCE-001` — Fase 0 (localizando fonte de dado real) |
| Lain-1b | Ressonância de Schumann → conexão neural/telepatia | Sem mecanismo biofísico conhecido | Fora de escopo, ver §6 |
| Lain-2 | Continuidade de identidade / cérebro dividido | Parcialmente testável; núcleo é debate conceitual | Sem linha nova — Sperry/Gazzaniga já são replicação estabelecida na literatura, nada para este laboratório testar de novo |
| Lain-3 | Memória reconstrutiva (Loftus) | Ciência estabelecida | Sem linha dedicada |
| Lain-4 | Emergência coletiva (Boids) | Demonstração de modelo estabelecido | **Não vira linha de teste** — ver §5 |
| Lain-4b | "Deus com intenção" emergindo de rede | Sem definição operacional | Fora de escopo, ver §6 |
| Lain-5 | Crença reescrevendo história retroativamente | Ficção pura, sem mecanismo | Fora de escopo, ver §6 |
| Lain-6 | Argumento da simulação (Bostrom) | Argumento formal, não-testável experimentalmente | Fora de escopo, ver §6 |

---

## 2. As três linhas empíricas abertas (`05_DISCOVERY_LAB/02_TESTS/`)

### 2.1 `DISC-SCHUMANN-RESONANCE-001`
**Hipótese candidata (a travar em pré-registro):** dado público real de
monitoramento eletromagnético/geofísico mostra um pico de densidade
espectral de potência dentro de uma janela pré-registrada em torno de
7.83 Hz (± tolerância a definir a partir da variação sazonal documentada
na literatura), consistente com a ressonância de Schumann fundamental.
**O que isto NÃO testa:** nenhuma alegação de conexão neural, telepatia,
ou transmissão de consciência — o próprio documento de origem já exclui
isso por ausência de mecanismo biofísico conhecido (Lain-1b, fora de
escopo, §6).
**Por que é um teste real e não uma demonstração:** existe tolerância
numérica pré-registrável, uma fonte de dado real verificável por fetch
direto, e um critério de falsificação explícito (pico fora da janela, ou
ausência de pico distinguível do ruído de fundo).
**Estado:** Fase 0 despachada (localizar fonte pública real — ex. estações
INTERMAGNET, GCI/HeartMath, ou equivalente — e verificar por fetch direto
antes de travar o pré-registro).

### 2.2 `DISC-IIT-PHI-REPRO-001`
**Hipótese candidata:** o pacote `PyPhi` (autoria do próprio grupo de
Tononi), aplicado a uma rede booleana pequena e canônica já publicada na
literatura de IIT (ex. um dos exemplos de Oizumi, Albantakis & Tononi
2014), reproduz o valor de Φ publicado dentro de tolerância numérica.
**O que isto NÃO testa:** a questão metafísica de fundo (se Φ>0 implica
"consciência" em qualquer sentido) — isto é uma checagem de
reprodutibilidade computacional de uma métrica definida, não um teste da
tese panpsiquista. Ver `05_DISCOVERY_LAB/00_GOVERNANCE/AGENTS.md` — o
mesmo princípio já aplicado ao caso EEG/depressão (`CLOSED_REFUTED`,
`COGNITIVE_EEG_SPECTRAL`).
**Estado:** Fase 0 despachada (localizar a citação exata — paper, rede
exemplo, valor de Φ publicado — antes de travar o pré-registro; sem
citação verificada, o teste não prossegue, por proibição explícita de
`AGENTS.md`).

### 2.3 `DISC-FEP-PREDICTIVE-CODING-001`
**Hipótese candidata:** ainda não formulável com precisão — o Princípio
da Energia Livre é, por desenho, uma estrutura teórica muito flexível
(crítica conhecida na literatura: dificuldade de falseabilidade em escopo
amplo). Este item entra como um levantamento estilo "Fase 0" (mesmo
padrão já usado para `RH-REAL` e `TRI-RG` antes de qualquer pré-registro
real): buscar na literatura uma previsão numérica ESTREITA e
genuinamente falseável de predictive coding, testável contra dado real
acessível.
**Resultado honesto esperado como possibilidade real:** pode ser que a
Fase 0 não encontre um alvo estreito o suficiente — isso fecharia a linha
como `CLOSED_NULL`/`OUT_OF_DOMAIN` na própria Fase 0, sem custo de
pré-registro desperdiçado, e é um resultado tão válido quanto qualquer
outro (mesma disciplina de `RESEARCH_PIPELINE.md`: `CLOSED_*` nunca é
derrota).
**Estado:** Fase 0 despachada.

---

## 3. A linha formal (`04_FORMAL_RESEARCH_LAB`)

### 3.1 Lógicas não-clássicas em Lean4 — nova linha exploratória
A pergunta do documento de origem ("a lógica clássica binária é a
'melhor' ferramenta, ou uma entre várias possíveis?") é diretamente
formalizável: definir axiomaticamente um sistema de valores de verdade
não-clássico (paraconsistente à la Priest — lógica LP, valores
designados {V, Ambos} — ou fuzzy à la Zadeh, `[0,1]`) em Lean4, e provar
mecanicamente QUAIS teoremas clássicos (princípio do terceiro excluído,
ex falso quodlibet/explosão, eliminação de dupla negação) sobrevivem e
quais quebram sob o novo sistema. Isto é matemática pura verificável pelo
type-checker do Lean, sem risco de overreach metafísico.

**Levantamento local já feito (2026-08-27):** `Mathlib4` (já instalado em
`04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib/`) não
contém nenhuma formalização de lógica paraconsistente, fuzzy, ou modal —
projeto genuinamente novo neste arquivo, sem conflito com trabalho prévio.

**Nota de arquitetura (decisão explícita, sinalizada para o usuário
poder corrigir):** `RESEARCH_PIPELINE.md` (`DEC-107`) determina que
`04_FORMAL_RESEARCH_LAB` não gera mais seus próprios alvos de física/
Millennium — só recebe claims já promovidos pelo Gate de Replicação. Uma
formalização de lógica não-clássica não é uma "claim empírica sobre a
realidade física" no mesmo sentido (não há dado externo a testar — é
definição + prova mecânica), então está sendo tratada como infraestrutura
matemática de propósito geral, no mesmo espírito de `02_FOUNDATIONS/`
já existente (`08_BISIMULATION`, `09_INVARIANTS`, `11_COMPUTABILITY_BRIDGE`
— peças de fundação, não alvos autogerados de Millennium). Se o usuário
discordar deste enquadramento, é reversível sem custo — nada foi
pré-registrado ou travado ainda além desta nota.

**Estado:** escopo de pesquisa despachado (levantamento de precedente na
comunidade Lean/Mathlib para o sistema formal específico a escolher).

### 3.2 Teoremas de Gödel — levantamento apenas, sem promessa de alvo
**Achado do levantamento local (2026-08-27):** `Mathlib4` já tem boa parte
da maquinaria de base que uma formalização de incompletude precisaria
(`Mathlib/Computability/{Primrec,Partrec,Halting,RE,TuringDegree,
PostTuringMachine}.lean`, `Mathlib/Logic/Godel/GodelBetaFunction.lean` —
a função beta usada em codificação de sequências, `Mathlib/ModelTheory/
Encoding.lean`) — mas **nenhuma** prova do teorema da incompletude em si.
**Avaliação honesta:** uma formalização completa dos teoremas de Gödel é
um empreendimento historicamente massivo (os dois exemplos conhecidos —
Russell O'Connor em Coq, ~2003-2005; Paulson em Isabelle/HOL, publicado
2013-2014 — cada um levou anos de trabalho dedicado). Não é prometido
aqui como alvo alcançável nesta rodada. O levantamento serve apenas para
mapear o que já existe e, possivelmente, identificar um sub-lema pequeno
e tratável (não o teorema inteiro) como um passo real e honesto, se
algum for encontrado.

---

## 4. O que já foi testado e fechado — não reaberto sem conteúdo novo

**Auto-similaridade fractal / criticalidade auto-organizada entre
domínios** (item E do documento de origem, minus a hipótese cosmológica):
isto é exatamente o que a linha `TRI_RG` já testou de forma extensiva —
16 candidatos, 5 rodadas, DFA/multiscale entropy, SOC/avalanches,
Kramers-Moyal, EVT/Hill, homologia persistente, grafos de visibilidade,
entropia de permutação, RQA — todos sobre dado real (geomagnético,
sismicidade, EEG, hidrologia, mercado financeiro) — resultado final
`CLOSED_NULL`, 0 sobreviventes (ver `05_DISCOVERY_LAB/02_TESTS/TRI_RG/`
e o funil completo no `README.md`). Reabrir essa pergunta exigiria um
mecanismo ou observável genuinamente novo, não coberto pelas 16 rodadas
já fechadas — nenhum candidato desse tipo foi identificado nos dois
documentos de origem.

---

## 5. Ilustrações computacionais — não são testes de hipótese

Decoerência quântica via `QuTiP` (item C) e emergência coletiva via
simulação de Boids (item Lain-4) demonstram mecânica quântica e dinâmica
de sistemas complexos já bem estabelecidas — não há hipótese nova,
falsificável, sendo testada contra dado real. Catalogá-las como "linha de
teste do Discovery Lab" infla artificialmente a identidade do laboratório
(`AGENTS.md`: "não é peer review... a linguagem de todo relatório desta
trilha deve refletir esse nível de confiança com precisão, nunca
inflar"). Se o usuário quiser esse material como ilustração pedagógica
(scripts standalone, fora do funil de pré-registro/revisão adversarial),
é um pedido separado e simples de atender — mas não entra no
`TEST_QUEUE.yaml` como se fosse uma hipótese em risco de falsificação.

---

## 6. Explicitamente fora de escopo

Os próprios documentos do usuário já nomeiam estes itens como não-
testáveis/não-formalizáveis (Seção 5 do documento 1, Seção 6 do documento
2) — este laboratório concorda e não abre linha para nenhum deles:

- "Tudo é consciente" (panpsiquismo como fato) — proposição metafísica
  sem definição operacional.
- "Deus como ponto de equilíbrio termodinâmico" — metáfora, não variável
  termodinâmica mensurável.
- "O universo economiza energia" / decide na fenda dupla — fisicamente
  incorreto como formulado; o que existe de real (decoerência) está no
  §5, não como teste de hipótese Tamesis.
- Ressonância de Schumann → conexão neural/telepatia — sem mecanismo
  biofísico conhecido.
- "Deus com intenção" emergindo de uma rede — sem definição operacional
  de "intenção" mensurável.
- Crença coletiva reescrevendo o passado retroativamente — sem mecanismo
  físico ou cognitivo documentado; ficção, não hipótese.
- Hipótese do Universo Matemático (MUH) como afirmação literal, e o
  Argumento da Simulação de Bostrom como proposição testável — ambos
  não-falsificáveis com meios atuais, por desenho dos próprios autores
  originais (Tegmark, Bostrom).

Nenhum destes itens recebe pré-registro, script de análise, ou entrada em
`TEST_QUEUE.yaml`/`CLAIM_LEDGER.yaml` como hipótese testável. Esta seção
existe para que a exclusão fique registrada e revisável, não silenciosa.

---

## 7. Próximos passos concretos

1. (Em andamento) Fase 0 despachada para as 3 linhas empíricas (§2) e o
   levantamento de precedente Lean (§3.1) — agentes de pesquisa rodando
   em paralelo via `Workflow`.
2. Ao retornar, cada linha some para uma de três direções: alvo real
   verificado → pré-registro travado e commitado; alvo não encontrado com
   confiança suficiente → `CLOSED_NULL`/`OUT_OF_DOMAIN` já na Fase 0;
   achado ambíguo → mais uma rodada de busca antes de decidir.
3. Nenhuma análise sobre dado real roda antes do pré-registro
   correspondente estar travado e commitado — mesma disciplina de sempre.
