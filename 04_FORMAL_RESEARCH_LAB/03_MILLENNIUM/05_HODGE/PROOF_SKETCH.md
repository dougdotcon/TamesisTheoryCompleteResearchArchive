# Esboço — HODGE-CDK-001

`NO_EXECUTION` quanto à Conjectura de Hodge. O único "esboço de prova"
produzido nesta rodada é o do caso especial auditado em
`RESULTS/WORKED_CASE_NOETHER_LEFSCHETZ.md` (Noether–Lefschetz em `P^3`,
codimensão de ciclo 1), que é um resultado **conhecido e citado**, não
uma tentativa de resultado novo. Nenhuma parte deste esboço avança em
direção a uma prova (parcial ou condicional) da Conjectura de Hodge
geral.

## O que este documento faz

1. Reconstrói, com citação, exatamente o que o Teorema de
   Cattani–Deligne–Kaplan prova (`DEFINITIONS.md`,
   `KNOWN_RESULTS_MATRIX.md`).
2. Reconstrói, com citação, exatamente o que ele explicitamente não
   prova (`ASSUMPTIONS.md`).
3. Audita passo a passo um caso de baixa codimensão
   (`RESULTS/WORKED_CASE_NOETHER_LEFSCHETZ.md`) onde a conclusão que a
   inferência ilegítima produziria por acidente é verdadeira — mas por
   um teorema totalmente diferente (Lefschetz (1,1)), não por CDK.
4. Identifica o ponto exato em que continuar generalizando esse
   argumento exigiria cometer a inferência proibida pelo
   `stop_condition` desta frente, e para nesse ponto.

## Por que não há tentativa de formalização Lean da Conjectura de Hodge, de CDK, ou de Lefschetz (1,1) nesta rodada

- Mathlib não possui, até onde verificado nesta sessão (busca informal
  no próprio repositório de Mathlib não foi feita — apenas inferência a
  partir do estado conhecido da biblioteca): variações de estrutura de
  Hodge, domínios de período, o mapa de classe de ciclo, ou a sequência
  exponencial em variedades complexas com a generalidade necessária.
  Formalizar qualquer um dos três exigiria construir esses objetos do
  zero — fora do escopo de uma auditoria de literatura de uma sessão.
- O `FORMAL/` desta frente contém, em vez disso, um rascunho **pequeno
  e autocontido** que formaliza apenas a **estrutura lógica** da
  falácia auditada (algebricidade/finitude de um locus não implica
  sobrejetividade do mapa subjacente), com um contraexemplo explícito
  finito. Ver `FORMAL/hodge_locus_fallacy_sketch.lean`. Este arquivo
  **não** formaliza CDK, Lefschetz (1,1), nem nenhum enunciado de
  geometria algébrica — o cabeçalho do arquivo repete isso
  explicitamente para evitar leitura equivocada futura.
- Este rascunho não foi compilado nesta sessão (proibição de rodar
  `lake build` em paralelo, conforme instrução da onda). Deve ser
  verificado na fase de integração serial.

## Não tentado nesta rodada, e por quê

- Qualquer prova, mesmo condicional, da Conjectura de Hodge geral —
  fora de escopo por proibição de `AGENTS.md` e por não haver caminho
  identificado na literatura consultada.
- Extensão do caso Noether–Lefschetz (codimensão 1) para codimensão
  `≥ 2` — é precisamente o `stop_condition` desta frente; ver
  `RESULTS/WORKED_CASE_NOETHER_LEFSCHETZ.md`, Passo 5.
- Leitura completa do artigo original de CDK (JAMS 1995) — o PDF da AMS
  retornou HTTP 403 nesta sessão; o conteúdo do teorema foi reconstruído
  via citação em fonte secundária de qualidade (notas de aula de
  François Charles, que citam o enunciado quase literalmente como
  "Theorem 2.8"), não lido diretamente do original.
