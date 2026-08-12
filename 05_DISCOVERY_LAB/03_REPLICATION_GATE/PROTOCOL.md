# Protocolo do Gate de Replicação

Ver `../00_GOVERNANCE/RESEARCH_PIPELINE.md` para onde este portão se encaixa
no fluxo de três motores. Este documento define o que "passar pelo Gate"
significa em termos operacionais.

## Quando um item entra aqui

Um item de `01_PORTFOLIO/TEST_QUEUE.yaml` entra no Gate de Replicação
quando: (a) tem pré-registro travado (`PREREGISTRATION.md`, status
`LOCKED` ou posterior); (b) foi analisado; (c) já passou pela reexecução
adversarial de primeira linha exigida por `00_GOVERNANCE/AGENTS.md` passo 7
(o "tentar refutar" padrão, já em uso desde o piloto
`DISC-COSMOLOGY-MOND-SPARC-001`); (d) o resultado dessa primeira reexecução
não foi `REFUTED`/`METHODOLOGY_FLAW_FOUND`.

Isto é uma SEGUNDA barreira, mais cara e mais rígida que a reexecução
adversarial padrão — reservada para candidatos que a equipe (usuário +
agente) considera fortes o suficiente para custear o esforço de replicação
completa, não um passo automático para todo item `ANALYZED`.

## Os quatro requisitos do Gate

Um candidato só é marcado `REPLICATION_PASSED` se **todos** os quatro forem
satisfeitos por um agente que não participou da análise original nem da
primeira reexecução adversarial:

1. **Agente independente.** Não pode ser o mesmo agente (nem a mesma sessão)
   que produziu a análise original ou a primeira reexecução adversarial.
2. **Implementação nova.** Código escrito do zero a partir apenas do
   pré-registro e da proveniência de dado — nunca lendo o código anterior
   antes de produzir sua própria versão (mesmo padrão já usado no piloto:
   o agente adversarial da Seção 7 escreveu `adversarial_reproduction.py`
   sem ler `run_preregistered_analysis.py` primeiro).
3. **Dado held-out, quando existir.** Se o pré-registro declarou um split
   de holdout selado (ver `METHODOLOGY_EXTENSIONS.md` §6), o Gate é onde
   esse holdout é finalmente aberto e testado — nunca antes. Para testes
   sem holdout declarado (como o piloto SPARC), o Gate exige em vez disso
   uma checagem de robustez formal contra pelo menos uma fonte de dado
   adicional ou reamostragem independente, documentada explicitamente como
   tal.

   **Esclarecimento (adicionado em 2026-08-12, antes do primeiro uso real
   deste Gate, para fechar uma ambiguidade que o pré-registro original de
   nenhum teste até agora precisou resolver):** quando um split
   discovery/holdout foi declarado, "testar" o holdout significa reexecutar
   EXATAMENTE a mesma estatística de teste da Seção 4 do pré-registro
   (mesma fórmula, mesmo procedimento de ajuste, mesmo IC bootstrap),
   agora usando SOMENTE os dados do holdout como amostra — nunca combinando
   holdout com discovery, nunca ajustando um novo critério de decisão
   específico para o holdout. Isso responde à pergunta "qual estatística
   rodar no holdout?" com a resposta mais literal e menos manipulável
   possível: a mesma que já estava travada. Qualquer teste diferente
   (ex. usar o holdout para checar erro de predição em vez de re-ajustar)
   é uma escolha adicional que precisa ser declarada explicitamente pelo
   agente do Gate, com justificativa, antes de rodar — não escolhida
   silenciosamente pela conveniência do resultado.
4. **Auditoria de proveniência.** Reconfirmar, por conta própria (novo
   fetch/checksum quando aplicável), que a fonte de dado é a mesma
   declarada em `data/PROVENANCE.md` e que nenhum dado embutido/fabricado
   entrou em nenhuma etapa.

## Resultado do Gate

- `REPLICATION_PASSED`: os quatro requisitos satisfeitos, resultado
  reproduzido dentro de tolerância declarada. Item pode ser promovido a
  `PROMOTED_TO_FORMAL_LAB` — vira candidato a formalização em
  `04_FORMAL_RESEARCH_LAB`, sujeito à disciplina de verificação Lean padrão
  de lá (que é independente e não é substituída por este Gate).
- `REPLICATION_FAILED`: qualquer um dos quatro requisitos falha, ou o
  resultado não reproduz. Item fecha como `CLOSED_REFUTED` (se a
  replicação ativamente contradiz o resultado original) ou
  `CLOSED_INCONCLUSIVE` (se a replicação não consegue nem confirmar nem
  refutar de forma decisiva). Registrado em `CLAIM_LEDGER.yaml` com o mesmo
  peso que um `REPLICATION_PASSED` — este é um resultado de valor, não uma
  falha do processo.

## O que o Gate não é

Não é uma segunda rodada de "tentar confirmar" — o agente do Gate recebe as
mesmas instruções adversariais de tentar refutar que a primeira reexecução
recebeu (ver `00_GOVERNANCE/AGENTS.md` §"Separação de papéis"). A diferença
do Gate para a reexecução adversarial padrão não é a atitude (as duas são
adversariais), é o padrão de evidência exigido: implementação
completamente nova, dado held-out quando existir, e auditoria de
proveniência formal — coisas que o piloto SPARC fez de forma ad hoc e que
aqui viram requisito obrigatório e documentado para qualquer item que
pretenda chegar ao laboratório formal.
