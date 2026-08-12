# Instruções para agentes da trilha de descoberta computacional

Esta trilha substitui revisão por pares acadêmica por disciplina
adversarial interna. As regras abaixo existem porque uma tentativa
anterior de fazer exatamente este tipo de trabalho, neste mesmo arquivo
(`01_TAMESIS_CORE/02_Experimental_Validation/{Cosmology,MOND_EFE}`),
produziu dado fabricado disfarçado de real e alegação estatística
inflada — ver `02_TESTS/COSMOLOGY_MOND_SPARC/AUDIT_LEGACY_MOND_EFE_SPARC.md`
para o caso concreto. Estas regras não são burocracia abstrata; são a
resposta direta a um erro que já aconteceu aqui.

## Ordem obrigatória para um novo teste

1. Ler `DISCOVERY_LAB_STATE.md`.
2. Formular a hipótese e localizar (não inventar) a fonte de dado real
   que a testa. Se a fonte não for verificável por fetch direto
   (`WebFetch`/`curl`/API), o teste não pode prosseguir até que uma
   fonte real e verificável seja encontrada.
3. Escrever o pré-registro em `02_TESTS/<nome>/PREREGISTRATION.md`
   usando `00_GOVERNANCE/PREREGISTRATION_TEMPLATE.md`, **antes** de
   tocar no dado real. O pré-registro trava: hipótese exata, estatística
   de teste, modelo nulo, critério de falsificação numérico, e (quando
   aplicável) correção para comparações múltiplas.
4. Commitar o pré-registro (hash do commit vira parte do registro —
   qualquer mudança de critério depois de ver o dado é uma violação e
   deve ser reportada como tal, não escondida).
5. Buscar o dado real, documentar proveniência completa em
   `02_TESTS/<nome>/data/PROVENANCE.md` (URL exata, data de acesso,
   checksum se possível, contagem de registros).
6. Rodar a análise pré-registrada. Reportar o resultado exatamente como
   saiu — sem reformular a hipótese depois de ver o resultado
   (isso é uma nova hipótese, precisa de novo pré-registro).
7. Um segundo agente reexecuta a análise de forma independente (código
   próprio, mesma proveniência de dado) e produz um veredito adversarial.
8. Registrar o resultado em `01_PORTFOLIO/TEST_QUEUE.yaml` e, se aplicável,
   `00_GOVERNANCE/CLAIM_LEDGER.yaml` — **qualquer resultado**, inclusive
   nulo/negativo/inconclusivo.
9. Criar relatório de sessão em `09_SESSIONS/YYYY/`.
10. Atualizar `DISCOVERY_LAB_STATE.md`.
11. Parar.

## Proibições

Um agente não pode:

- usar dado embutido/fabricado no lugar de um download real que falhou —
  falha de download é reportada como falha, nunca mascarada por um
  fallback silencioso;
- desabilitar verificação TLS/SSL para "resolver" um problema de rede;
- formular ou reformular a hipótese, a estatística de teste, o modelo
  nulo, ou o critério de falsificação depois de olhar o dado real;
- reportar um p-valor sem declarar quantas comparações foram feitas e
  se houve correção;
- alegar "Tamesis confirmado", "detectado", ou "favorecido sobre ΛCDM/MOND"
  a partir de um único teste sem replicação independente — a linguagem
  correta é sempre relativa ao teste específico e ao seu poder estatístico;
- inventar uma referência, URL, ou citação — toda fonte precisa ser
  verificada por fetch direto, nunca assumida de memória;
- pular a reexecução adversarial (item 7) antes de catalogar um resultado
  como fechado;
- esconder ou deletar um resultado negativo/nulo;
- alegar que qualquer Problema do Millennium foi resolvido, aproximado,
  ou tornado alcançável, mesmo que um teste desta trilha o toque
  indiretamente.

## Separação de papéis (implementador vs. revisor)

O mesmo agente que roda a análise original não pode ser o único a validar
o resultado. A reexecução adversarial (passo 7) precisa ser um agente
separado, instruído a tentar refutar o achado, não confirmá-lo — mesmo
padrão já usado com sucesso em `04_FORMAL_RESEARCH_LAB` para revisão de
provas Lean, adaptado para artefato empírico/computacional em vez de
prova formal.

## O que esta trilha NÃO é

Não é peer review. Não é publicação. Um teste "fechado" aqui é um achado
computacional reproduzível com proveniência documentada e reexecução
adversarial interna — um padrão de evidência real, mas mais fraco que
revisão por pares formal em um periódico. A linguagem de todo relatório
desta trilha deve refletir esse nível de confiança com precisão, nunca
inflar.

## Legado

`01_TAMESIS_CORE/02_Experimental_Validation/{Cosmology,MOND_EFE}` e
`RECURSOS_PARA_PESQUISA/07_MILLENNIUM_VALIDATION` são leitura permitida
como contexto/precedente, mas seus resultados numéricos e alegações
estatísticas NÃO são citáveis como evidência válida por esta trilha até
serem auditados individualmente (mesmo tratamento dado ao caso SPARC/EFE
documentado em `02_TESTS/COSMOLOGY_MOND_SPARC/AUDIT_LEGACY_MOND_EFE_SPARC.md`).
