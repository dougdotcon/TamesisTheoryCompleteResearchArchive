# Trilha de Descoberta Computacional (Discovery Lab)

## O que isto é

Uma segunda trilha de pesquisa do Laboratório Tamesis, paralela ao
[`04_FORMAL_RESEARCH_LAB`](../04_FORMAL_RESEARCH_LAB/) (verificação formal
em Lean4/Mathlib). Enquanto a trilha formal produz fatos pequenos,
verificados por máquina, sobre objetos deliberadamente restritos (um
operador de brinquedo, um núcleo abstrato de não-go), esta trilha produz
**achados computacionais/empíricos reproduzíveis** — testados contra dados
públicos reais, simulação, ou algoritmo — sobre hipóteses derivadas do
programa Tamesis mais amplo (`01_TAMESIS_CORE`).

## Por que existe

Criada em 2026-08-12, a pedido explícito do usuário, após uma sessão que
(a) pesquisou e verificou um resultado real da Anthropic sobre um limite
relacionado à Hipótese de Riemann (produzido por exploração LLM em larga
escala, sem revisão por pares, mas com disciplina adversarial substituindo
a revisão por pares) e (b) descobriu que uma tentativa anterior, dentro
deste mesmo arquivo, de fazer exatamente este tipo de descoberta
computacional (`01_TAMESIS_CORE/02_Experimental_Validation/{Cosmology,MOND_EFE}`)
continha dados fabricados/embutidos disfarçados de download real, SSL
desabilitado, e alegações estatísticas infladas — corrigidas depois, mas
não impedidas antes.

A decisão explícita do usuário: revisão por pares acadêmica não é
necessária para *descobrir* (é um requisito de credibilização
institucional, não um pré-requisito lógico de exploração honesta) — mas
alguma disciplina precisa ocupar o lugar que a revisão por pares ocuparia,
porque sem ela o modo "descoberta" é extremamente propenso a se enganar
sozinho (comparações múltiplas, overfitting, alucinação de padrão por
LLM, dado fabricado disfarçado de real). Esta trilha existe para fazer
essa substituição de forma explícita e auditável.

## A regra que substitui a revisão por pares

Ver [`00_GOVERNANCE/AGENTS.md`](00_GOVERNANCE/AGENTS.md) para o texto
completo. Resumo:

1. **Pré-registro travado antes de tocar em dado real.** Hipótese,
   estatística de teste, modelo nulo, e critério de falsificação
   escritos e commitados *antes* de rodar qualquer análise sobre os
   dados-alvo.
2. **Proveniência de dado verificável, nunca embutida/fabricada.**
   Toda fonte de dado precisa de URL real, verificada por fetch direto
   (não assumida), com data de acesso e, quando possível, checksum.
   Fallback silencioso para dado inventado quando o download falha é
   proibido — falha de download é reportada como falha, não mascarada.
3. **Reexecução adversarial obrigatória.** Um segundo agente
   independente reproduz a análise do zero (código próprio, mesmos
   dados) antes de qualquer resultado ser catalogado, especificamente
   checando por: dado fabricado/embutido, download quebrado, TLS
   desabilitado, p-hacking/comparações múltiplas não corrigidas,
   alegação de significância inflada.
4. **Catalogar todo resultado, inclusive negativo.** Um teste que não
   distingue Tamesis de um modelo concorrente, ou que falsifica a
   hipótese, é um resultado completo e válido — não é descartado nem
   escondido.
5. **Nenhuma alegação de "nova física confirmada"** sem replicação
   independente por terceiros. O padrão de evidência aqui é mais fraco
   que peer review formal; a linguagem usada para descrever qualquer
   achado precisa refletir isso com precisão.

## Estrutura

| Pasta | Função |
|---|---|
| `00_GOVERNANCE/` | `AGENTS.md` (disciplina), `DECISION_LEDGER.yaml`, `CLAIM_LEDGER.yaml`, `PREREGISTRATION_TEMPLATE.md` |
| `01_PORTFOLIO/` | `TEST_QUEUE.yaml` — fila de testes falsificáveis, um por hipótese |
| `02_TESTS/` | Um subdiretório por teste, cada um com pré-registro, dados com proveniência documentada, código de análise, e resultado |
| `09_SESSIONS/` | Relatórios de sessão, mesmo padrão do `04_FORMAL_RESEARCH_LAB` |

## Estado atual

Ver [`DISCOVERY_LAB_STATE.md`](DISCOVERY_LAB_STATE.md).
