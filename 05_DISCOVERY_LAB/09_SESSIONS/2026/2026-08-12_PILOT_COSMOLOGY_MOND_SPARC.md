# Sessão 2026-08-12 — Piloto da trilha de descoberta: EFE/SPARC

**Trilha:** `05_DISCOVERY_LAB` (paralela ao ciclo de ondas Lean em
`04_FORMAL_RESEARCH_LAB`, que não foi tocado nesta sessão)

## Contexto

Sessão anterior pesquisou um resultado real da Anthropic (bound de proporção
de zeros de zeta na linha crítica, 41.6%→67.2%, produzido por exploração LLM
em larga escala com revisão adversarial substituindo peer review formal). O
usuário perguntou se fazia sentido adotar metodologia semelhante, e em
seguida levantou uma objeção estratégica mais profunda: que o sistema de
ondas do Lean lab só fazia sentido se realmente não fosse possível atacar
"problemas fundamentais" ainda, e que peer review é um requisito
institucional da academia, não um pré-requisito lógico para descoberta — seu
objetivo é descobrir, não provar, usando computação, dados públicos e
ferramentas open-source, com disciplina de revisão interna substituindo
peer review formal.

Quatro decisões explícitas do usuário (via pergunta estruturada) resultaram
desta discussão: (1) manter o ciclo de ondas Lean rodando em paralelo, não
pausar; (2) escopo aberto/multi-domínio para a nova trilha; (3) nova trilha
como diretório de topo separado (`05_DISCOVERY_LAB`); (4) auditar e refazer
o trabalho legado de cosmologia/MOND-EFE como primeiro piloto.

## O que foi feito

### 1. Governança da trilha

Criado `00_GOVERNANCE/{AGENTS.md, DECISION_LEDGER.yaml, CLAIM_LEDGER.yaml,
PREREGISTRATION_TEMPLATE.md}` — protocolo obrigatório: hipótese + dado real
localizado (não inventado) → pré-registro escrito e commitado ANTES de
tocar no dado → busca do dado com proveniência documentada → análise
pré-registrada → reexecução adversarial obrigatória por agente separado →
registro do resultado (qualquer resultado) → relatório de sessão → stop.
`DISC-DEC-001` documenta a decisão e o contexto completo.

### 2. Auditoria do código legado

`02_TESTS/COSMOLOGY_MOND_SPARC/AUDIT_LEGACY_MOND_EFE_SPARC.md` documenta 8
achados citados por arquivo:linha em
`01_TAMESIS_CORE/02_Experimental_Validation/MOND_EFE/`. O achado central:
as 8 galáxias "reais" de Virgem por trás do badge "EFE CONFIRMED,
p<0.000001" em `efe/README.md` são curvas de rotação digitadas à mão em
`sparc_slope_analysis.py`, comentadas como "ACTUAL SPARC ROTATION CURVE
DATA" — e nenhuma das 13 galáxias de Virgem citadas em todo o código legado
existe no catálogo SPARC público real (verificado por busca exata contra o
arquivo baixado nesta sessão). Um segundo script (`sparc_real_download.py`)
tinha URL quebrada (typo estrutural), SSL desabilitado, e fallback
silencioso para um catálogo embutido; um terceiro (`sparc_loader.py`) gerava
dado sintético a partir do próprio modelo MOND que deveria estar testando
(circular).

### 3. Dado real

Baixado de `https://astroweb.case.edu/SPARC/` (domínio correto — a versão
legada usava `astroweb.cwru.edu`, desatualizado): catálogo de 175 galáxias
(`SPARC_Lelli2016c.mrt`) + 175 curvas de rotação individuais
(`Rotmod_LTG/*.dat`). Proveniência completa com checksums em
`data/PROVENANCE.md`. Nenhum fallback, nenhum SSL desabilitado.

### 4. Pré-registro

`PREREGISTRATION.md` travado no commit `49867fa`, antes de qualquer cálculo
sobre o dado real. O desenho original (Virgem vs. campo, replicando a
estrutura do código legado) teve que ser abandonado — nenhuma galáxia de
Virgem citada existe na amostra real — e foi substituído por
aglomerado-de-Ursa-Maior-vs-campo usando um campo já nativo do catálogo
oficial (`f_D=4`, documentado no próprio `.mrt` como "Ursa Major Cluster of
Galaxies"), evitando qualquer lista de membership externa não verificável.
Hipótese fundamentada em `efe/index.html:271-309,337-344` (predição
MOND/EFE padrão, Milgrom 1983). Estatística: inclinação externa log-log da
curva de rotação (outer half, mesma definição do código legado, agora
computada sobre dado real). Critério de falsificação, correção de
comparações múltiplas (N=1, nenhuma outra), e escopo do que não está sendo
testado — todos travados antes de ver o resultado.

### 5. Execução e reexecução adversarial

Análise primária (`analysis/run_preregistered_analysis.py`) rodou sobre as
175 galáxias reais, 0 exclusões: N_aglomerado=28, N_campo=147, slope médio
+0.078 (aglomerado) vs. +0.149 (campo), teste t de Welch de uma cauda
p=0.049373 — direção bate com EFE, cruza o limiar de 0.05, mas cai
exatamente na zona frágil (0.04–0.06) que o próprio pré-registro (Seção 5)
já previa.

Um agente independente reescreveu a análise do zero, sem ler o script
primário antes, e reproduziu os números exatamente (nenhum bug encontrado).
Checagem de robustez adicional (declarada como informativa, não um novo
teste pré-registrado): 4 galáxias de campo têm ajuste de inclinação externa
baseado em apenas 2 pontos (resíduo zero, alavancagem máxima); excluí-las
faz p subir para 0.0635, invertendo o veredito binário pela mesma fórmula.
**Veredito formal do agente adversarial: INCONCLUSIVE.**

### 6. Registro

`DISC-CLAIM-001` registrado em `CLAIM_LEDGER.yaml` com
`evidence_level: preregistered_inconclusive` e
`adversarial_review_verdict: INCONCLUSIVE` — nenhuma linguagem
"CONFIRMED"/"DETECTED" usada. `TEST_QUEUE.yaml` atualizado para
`CLOSED_INCONCLUSIVE`. `DISC-DEC-002` documenta o fechamento.
`DISCOVERY_LAB_STATE.md` atualizado.

## Resultado desta sessão em uma frase

O piloto confirmou, com evidência verificável arquivo:linha, que o
resultado "EFE CONFIRMED, p<0.000001" do arquivo legado era baseado em dado
fabricado; refeito com dado real e disciplina de pré-registro + reexecução
adversarial, o teste comparável disponível deu um resultado real, correto,
independentemente reproduzido — e honestamente inconclusivo, não uma nova
manchete.

## Estado ao final

- `05_DISCOVERY_LAB/` totalmente committado e (após este relatório) pronto
  para push.
- `04_FORMAL_RESEARCH_LAB` (ciclo de ondas Lean) intocado, Wave 7 permanece
  o estado mais recente lá.
- Nenhum teste ativo na trilha de descoberta; próximo teste requer nova
  decisão de escopo (a trilha continua aberta/multi-domínio, conforme
  decisão original do usuário).

## Lições para o próximo teste desta trilha

1. Sempre verificar se a fonte de dado real realmente contém as entidades
   que a hipótese assume (o desenho "Virgem vs. campo" só foi descartado
   depois de tentar cruzar os nomes contra o catálogo real — vale a pena
   fazer essa checagem de existência ANTES de escrever o pré-registro, não
   depois).
2. Estatísticas baseadas em poucos pontos por unidade amostral (aqui, o
   ajuste de inclinação com só 2 pontos) merecem uma checagem de robustez
   sempre que o p-valor for marginal — vale considerar declarar isso como
   parte do pré-registro em testes futuros (ex. exigir N mínimo de pontos
   por curva como critério de inclusão, declarado a priori), em vez de
   descobrir a fragilidade só na reexecução adversarial.
