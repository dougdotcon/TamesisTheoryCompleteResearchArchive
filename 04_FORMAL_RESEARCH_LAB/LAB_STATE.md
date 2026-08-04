---
schema: tamesis-formal-lab-state/1
updated_at: 2026-08-04T00:46:17-03:00
canonical_commit: "7a93a03145ad561b9748d6187a44cd4dcc7b7866"
canonical_commit_policy: >
  Aponta para o último commit canônico integralmente encerrado
  antes da sessão atual. Deve existir e ser ancestral do HEAD.
  Igualdade com o HEAD é válida no começo de uma sessão; a
  ancestralidade NÃO é estrita.
repository_clean: true
active_track: "foundations"
active_work_item: "FOUND-MONOVARIANT-DESCENT-001"
work_status: "READY"
specification_status: "READY_FOR_REVIEW"
specification_review: "NOT_STARTED"
formalization_status: "NOT_STARTED"
result_review: "NOT_STARTED"
extension_status: "NOT_AUTHORIZED"
external_integration_status: "NOT_AUTHORIZED"
relational_bisimulation_status: "NOT_AUTHORIZED"
nondeterministic_systems_status: "NOT_AUTHORIZED"
bisimulation_status: "NOT_AUTHORIZED"
quotient_status: "NOT_AUTHORIZED"
extraction_status: "NOT_AUTHORIZED"
cli_status: "NOT_AUTHORIZED"
parser_status: "NOT_AUTHORIZED"
integration_status: "NOT_AUTHORIZED"
evidence_level: "F"
formalized_at_commit: "d8a68e6bfd000062949c8349800d98b317763bbb"
last_verified_artifact: "found-bisimulation-boundary-001-result-review.json"
current_blocker: null
next_single_action: >
  Revisar a especificação: conferir as sete assinaturas congeladas,
  a recuperação de 0 < period e a negação sobre boa fundação.
authorized_action: "FOUND_MONOVARIANT_DESCENT_001_SPECIFICATION_REVIEW_AUTHORIZED"
portfolio_review_status: "CONSUMED"
frontmatter_scan_coverage: "FULL"
yaml_scan_files_covered: 390
yaml_scan_markdown_front_matter_covered: 333
yaml_duplicate_key_status: "VERIFIED_CLEAN"
consumed_authorizations: ["LAB_GOV_YAML_DUPLICATE_KEYS_CORRECTION_AUTHORIZED", "LAB_GOV_FRONTMATTER_SCAN_CORRECTION_AUTHORIZED", "LAB_GOV_DECISION_LEDGER_CORRECTION_AUTHORIZED"]
decision_ledger_integrity: "VERIFIED_CLEAN"
decision_citations_unregistered: 0
closed_work_items:
  FOUND-INVARIANT-UNREACHABILITY-001:
    work_status: VERIFIED
    specification_status: APPROVED
    specification_review: APPROVED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    relational_invariants_status: NOT_AUTHORIZED
    monovariant_status: NOT_AUTHORIZED
    termination_status: NOT_AUTHORIZED
    complete_invariant_status: NOT_AUTHORIZED
    nondeterministic_systems_status: NOT_AUTHORIZED
    classical_choice_present: false
    mathematical_novelty: NONE
    algorithmic_novelty: NONE
  FOUND-BISIMULATION-BOUNDARY-001:
    work_status: VERIFIED
    specification_status: APPROVED
    specification_review: APPROVED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    relational_bisimulation_status: NOT_AUTHORIZED
    nondeterministic_systems_status: NOT_AUTHORIZED
    labelled_actions_status: NOT_AUTHORIZED
    coinduction_status: NOT_AUTHORIZED
    quotient_status: NOT_AUTHORIZED
    extraction_status: NOT_AUTHORIZED
    axiom_footprint: NONE
    mathematical_novelty: NONE
    algorithmic_novelty: NONE
  FOUND-FINITE-STATE-ABSTRACTION-001:
    work_status: VERIFIED
    specification_status: APPROVED
    specification_review: APPROVED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    bisimulation_status: NOT_AUTHORIZED
    quotient_status: NOT_AUTHORIZED
    extraction_status: NOT_AUTHORIZED
    cli_status: NOT_AUTHORIZED
    parser_status: NOT_AUTHORIZED
    external_integration_status: NOT_AUTHORIZED
    external_abstraction_correctness: PERMANENTLY_OUT_OF_SCOPE
    mathematical_novelty: NONE
    algorithmic_novelty: NONE
  FOUND-SEMIGROUP-002:
    work_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    mathematical_novelty: NONE
  FOUND-FUNCTIONAL-GRAPH-001:
    work_status: VERIFIED
    specification_status: APPROVED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    mathematical_novelty: NONE
  FOUND-CYCLE-DETECTION-001:
    work_status: VERIFIED
    specification_status: APPROVED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    totalization_status: DEFERRED
    extraction_status: NOT_AUTHORIZED
    optimization_status: NOT_AUTHORIZED
    minimality_status: NOT_AUTHORIZED
    mathematical_novelty: NONE
    algorithmic_novelty: NONE
  ENG-FINITE-STATE-RUNTIME-001:
    work_status: VERIFIED
    specification_status: APPROVED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    extraction_status: NOT_AUTHORIZED
    cli_status: NOT_AUTHORIZED
    external_format_status: NOT_AUTHORIZED
    integration_status: NOT_AUTHORIZED
    detailed_diagnostics_status: NOT_AUTHORIZED
    external_abstraction_correctness: DEFERRED
    mathematical_novelty: NONE
    algorithmic_novelty: NONE
  ENG-FINITE-STATE-ENCODING-001:
    work_status: VERIFIED
    specification_status: APPROVED
    specification_review: APPROVED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    reencoding_invariance_status: NOT_AUTHORIZED
    extraction_status: NOT_AUTHORIZED
    cli_status: NOT_AUTHORIZED
    parser_status: NOT_AUTHORIZED
    integration_status: NOT_AUTHORIZED
    external_abstraction_correctness: DEFERRED
    mathematical_novelty: NONE
    algorithmic_novelty: NONE
frozen_work_items:
  RH-NOGO-001:
    work_status: FROZEN_PARTIAL_RESULT
    authorization_state: NOT_AUTHORIZED
    execution_state: NO_EXECUTION
    concrete_layer_status: DEFERRED
governance_lock_renamed:
  from: NO_ACTION_AUTHORIZED
  to: PORTFOLIO_REVIEW_REQUIRED
  reason: "o sufixo _AUTHORIZED convidava a ler a trava como autorização"
  satisfied_by: PORTFOLIO_REVIEW
governance_rules:
  post_commit_validation: >
    Quando uma auditoria obrigatória falhar depois do primeiro commit e
    amend e commit corretivo estiverem ambos proibidos, parar com
    GATE_POST_COMMIT_VALIDATION_FAILED e aguardar gate corretivo explícito.
  truncated_output: >
    Não assumir sucesso a partir de saída truncada. Toda etapa de patch
    termina com verificação independente do efeito.
  yaml_scan_scope: >
    A varredura de chaves duplicadas cobre arquivos .yaml e .yml E o front
    matter YAML de todo documento Markdown versionado sob o laboratorio. O
    relatorio publica yaml_files_scanned e markdown_front_matter_scanned
    para que a palavra "integral" seja conferivel sem ler o codigo.
  yaml_duplicate_keys: >
    Cada chave de um mapa YAML ocorre exatamente uma vez. Duplicatas
    idênticas também são proibidas. "Último valor vence" não é semântica
    de governança, e a ausência de erro no parser não demonstra
    integridade. labctl validate rejeita qualquer duplicata em todo YAML
    versionado sob o laboratório, com o código DUPLICATE_YAML_KEY.
  aggregate_counts: >
    Contagens agregadas de declarações, gaps, arquivos, claims, testes e
    estados não são fonte primária. Toda contagem agregada deve ser
    derivada ou conferida automaticamente contra as entradas individuais
    antes do commit, e a conferência deve percorrer TODAS as entradas, não
    um subconjunto nomeado.
  mandatory_probe_exit_code: >
    Experimentos negativos, provas exploratórias destinadas a falhar e
    testes de impossibilidade não podem compartilhar arquivo com probes
    obrigatórios cujo contrato exige exit 0. Validações obrigatórias
    devem terminar com código de saída zero. Resultados negativos são
    preservados em documentação, nunca reexecutados como validação.
    Um processo Lean com exit 1 nunca é evidência de PASS.
prohibited_actions:
  - "Não usar ordem geral ou WellFoundedRelation: a medida vive em Nat"
  - "Não afirmar que boa fundação basta: k - 1 falha em zero"
  - "Não afirmar que monovariante é necessário para ausência de ciclo"
  - "Não abrir terminação de programas nem ordinais"
  - "Não escrever contagem agregada sem derivá-la por script no mesmo gate"
  - "Não afirmar que um invariante separador é necessário para inalcançabilidade: é suficiente"
  - "Não usar invariante para certificar recorrência: só vale em ponto fixo"
  - "Não abrir monovariantes, boa ordem ou terminação nesta frente"
  - "Não conectar invariantes a Clay, TOE, física ou Riemann"
  - "Não atacar problema de milênio antes de a ferramenta estar encerrada"
  - "Não citar DEC-NNN como autoridade sem entrada correspondente no DECISION_LEDGER"
  - "Não reutilizar um decision_id já emitido para uma decisão diferente"
  - "Não reescrever entrada histórica do CHANGELOG para corrigir citação"
  - "Não tratar a janela limitada como hipótese mais fraca que OrbitSeparating"
  - "Não afirmar custo menor que busca concreta direta: não há modelo de custo"
  - "Não usar processo com exit diferente de zero como evidência de PASS"
  - "Não tratar igualdade abstrata como igualdade concreta sem hipótese de reflexão"
  - "Não afirmar que abstrações finitas não produzem ciclos espúrios"
  - "Não assumir bissimulação onde só há semiconjugação"
  - "Não aceitar duas definições da mesma chave YAML, ainda que os valores coincidam"
  - "Não adotar o valor efetivo do parser como fonte de verdade ao resolver divergência"
  - "Não afirmar invariância do witness concreto sob recodificação"
  - "Não estender ENG-FINITE-STATE-ENCODING-001 nem abrir 002 sem gate próprio"
  - "Não conferir contagem agregada por amostragem: a varredura deve cobrir todas as entradas"
  - "Não expor buildTransitionTable_getElem: é private e vive em Commutation.lean"
  - "Não provar table_step_commutes diretamente: é o .symm de tableIndex_semiconj"
  - "Não criar segundo tableIndex sobre Fin n: esse papel já é de encode"
  - "Não estender ENG-FINITE-STATE-ENCODING-001 nem abrir 002 sem gate próprio"
  - "Não misturar experimento negativo com probe obrigatório no mesmo arquivo"
  - "Não desviar das assinaturas congeladas nos documentos FINAL_* sem gate próprio"
  - "Não afirmar invariância do witness concreto sob recodificação: ENC-GAP-020"
  - "Não tornar buildTransitionTable_getElem público: é INTERNAL_HELPER"
  - "Não provar table_step_commutes diretamente: ele é o .symm da semiconjugação"
  - "Não abrir frente para remover propext, Classical.choice ou Quot.sound infraestruturais"
  - "Não derivar a codificação de Fintype: equivFin é noncomputable e truncEquivFin não produz dado"
  - "Não criar um terceiro ponto de transporte Fin n ↔ Fin table.next.size"
  - "Não usar encode_decode onde decode_encode é a lei semanticamente necessária"
  - "Não reprovar a comutação de iteradas por indução manual: Semiconj.iterate_right resolve"
  - "Não enunciar a soundness sobre a tabela: ela deve terminar em igualdade sobre S"
  - "Não alterar retroativamente RT-GAP-017 nem tocar a frente do runtime adapter"
  - "Não derivar encode de Fintype.equivFin: é noncomputable e não pode produzir dado"
  - "Não modificar ENG-FINITE-STATE-RUNTIME-001 ao construir a codificação certificada"
  - "Não declarar RT-GAP-017 fechado no caso geral: a frente cobre apenas o recorte tipado"
  - "Não iniciar a formalização de ENG-FINITE-STATE-ENCODING-001 sem gate próprio"
  - "Não desviar das assinaturas congeladas em FINAL_SIGNATURES.md sem gate próprio"
  - "Não criar CLI, parser, JSON, CSV, rede ou integração externa sem gate próprio"
  - "Não derivar contagens agregadas à mão: verificar cabeçalho contra as entradas por script"
  - "Não remover o ramo internalDetectorFailure — sua impossibilidade é teorema, não motivo de remoção"
  - "Não estender ENG-FINITE-STATE-RUNTIME-001 nem abrir 002 sem gate próprio"
  - "Não alterar a semântica de zero passos de run? — run? 0 state = some state"
  - "Não alterar a precedência dos erros: tabela, depois consulta, depois execução"
  - "Não renomear 03_ENGINEERING — a duplicação de prefixo é cosmética e reconhecida"
  - "Não desviar das assinaturas congeladas em SPECIFICATION_DECISION.md sem gate próprio"
  - "Não criar RawTransitionTable.stateCount — duplicaria next.size"
  - "Não trocar ValidatedTransitionTable por Subtype nem manter ambos"
  - "Não colapsar erro de tabela e erro de estado inicial num único construtor"
  - "Não remover o ramo internalDetectorFailure da função executável"
  - "Não corrigir destinos inválidos por módulo, clamp ou fallback silencioso"
  - "Não converter estado inicial inválido por módulo"
  - "Não permitir que a tabela validada aponte para fora do domínio"
  - "Não usar Classical.choose para produzir dados"
  - "Não depender de Function.periodicOrbit na execução"
  - "Não reimplementar o detector nem a casa dos pombos"
  - "Não misturar parsing JSON, CSV, arquivo ou rede com o núcleo formal"
  - "Não incluir servidor, banco de dados ou interface web na primeira versão"
  - "Não tornar Floyd, Brent ou a totalização dependências obrigatórias"
  - "Não declarar automaticamente correta a abstração de um sistema real em estados finitos"
  - "Não afirmar complexidade sem modelo de custo"
  - "Não formalizar Floyd, Brent ou tabela visitada — todos NOT_AUTHORIZED"
  - "Não estender FOUND-CYCLE-DETECTION-001 nem abrir FOUND-CYCLE-DETECTION-002 sem gate próprio"
  - "Não estender FOUND-FUNCTIONAL-GRAPH-001 nem FOUND-SEMIGROUP-002 sem gate próprio"
  - "Não reabrir RH-NOGO-001 sem que uma condição de RH_NOGO_REACTIVATION_CRITERIA.md ocorra e seja verificada"
  - "Não registrar testes que importam TamesisLab dentro de TamesisLab.lean — import circular"
  - "Não conectar a nova frente a TRI, TDTR, teoria de tudo, física, Hipótese de Riemann ou conjectura Clay"
  - "Não afirmar novo modelo de computação, novo algoritmo, nova teoria de autômatos ou descoberta"
  - "Não tratar reutilização em software como descoberta científica"
  - "Não modificar legado nem operar a partir de /mnt/d"
  - "Não afirmar que bissimulação reflete ciclos: BOOL_TO_UNIT já é uma bissimulação sobrejetiva"
  - "Não definir Reflects já resolvido: a existencial do zag é o conteúdo do colapso"
  - "Não escrever \"bissimulação é semiconjugação\" sem o qualificador determinístico total e funcional"
  - "Não afirmar que bissimulação é inútil: o resultado vale só neste recorte"
  - "Não estender o colapso zig/zag para sistemas não determinísticos ou bissimulação relacional"
  - "Não estender FOUND-FINITE-STATE-ABSTRACTION-001 nem abrir 002 sem gate próprio"
  - "Não declarar uma varredura integral sem publicar quantos arquivos ela abriu"
  - "Não fechar front matter com o delimitador --- na mesma linha do corpo"
  - "Não usar yaml.safe_load em front matter sem antes rejeitar chaves duplicadas"
  - "Não usar código de saída capturado através de fronteira de shell como evidência"
  - "Não declarar PASS quando a saída contiver linha error: ainda que o exit seja zero"
  - "Não registrar FoundFiniteStateAbstraction001UmbrellaAudit em TamesisLab.lean"
  - "Não usar lake env lean isolado antes do build: sem .olean das dependências dá exit 1 falso"
  - "Não usar FOUND-FINITE-ABSTRACTION-001 como item ativo: é nome candidato anterior"
  - "Não concluir igualdade em C a partir da soundness observacional sem OrbitSeparating"
  - "Não descrever a completeness abstrata como completeness concreta"
  - "Não esconder OrbitSeparating dentro de CertifiedFiniteAbstraction"
  - "Não armazenar encoding, witness, tabela ou estado inicial na estrutura da abstração"
resume_read_order:
  - "LAB_STATE.md"
  - "AGENTS.md"
  - "01_PORTFOLIO/NEXT_WORK_ITEM_FINITE_STATE_RUNTIME.md"
  - "03_ENGINEERING/01_FINITE_STATE_RUNTIME/ENG_FINITE_STATE_RUNTIME_001/README.md"
  - "03_ENGINEERING/01_FINITE_STATE_RUNTIME/ENG_FINITE_STATE_RUNTIME_001/SPECIFICATION_DECISION.md"
  - "02_FOUNDATIONS/05_CYCLE_DETECTION/FOUND_CYCLE_DETECTION_001/PUBLIC_API.md"
  - "02_FOUNDATIONS/05_CYCLE_DETECTION/FOUND_CYCLE_DETECTION_001/RESULT_BOUNDARY.md"
  - "02_FOUNDATIONS/07_FINITE_ABSTRACTION/FOUND_FINITE_STATE_ABSTRACTION_001/README.md"
  - "02_FOUNDATIONS/07_FINITE_ABSTRACTION/FOUND_FINITE_STATE_ABSTRACTION_001/SPECIFICATION_DECISION.md"
  - "02_FOUNDATIONS/08_BISIMULATION/FOUND_BISIMULATION_BOUNDARY_001/README.md"
  - "02_FOUNDATIONS/08_BISIMULATION/FOUND_BISIMULATION_BOUNDARY_001/SCOPE_BOUNDARY.md"
  - "01_PORTFOLIO/RESEARCH_QUEUE.yaml"
  - "último relatório em 09_SESSIONS/"
---

# Estado atual

```text
LAB-ARCH-001                        VERIFIED                ENCERRADO
LAB-BENCH-001                       VERIFIED                ENCERRADO
FOUND-SEMIGROUP-001                 VERIFIED                ENCERRADO
FOUND-SEMIGROUP-002                 VERIFIED / APPROVED     ENCERRADO
FOUND-FUNCTIONAL-GRAPH-001          VERIFIED / APPROVED     ENCERRADO
FOUND-CYCLE-DETECTION-001           VERIFIED / APPROVED     ENCERRADO
ENG-FINITE-STATE-RUNTIME-001        VERIFIED / APPROVED     ENCERRADO
ENG-FINITE-STATE-ENCODING-001       VERIFIED / APPROVED     ENCERRADO
FOUND-FINITE-STATE-ABSTRACTION-001  VERIFIED / APPROVED     ENCERRADO
FOUND-BISIMULATION-BOUNDARY-001     VERIFIED / APPROVED     ENCERRADO

RH-NOGO-001                         FROZEN_PARTIAL_RESULT   congelado

NS-PRESSURE-001                     SCOPED                  nunca executado
PVSNP-PHYS-001                      SCOPED                  nunca executado
YM-LIMIT-001                        SCOPED                  nunca executado
HODGE-CDK-001                       SCOPED                  nunca executado
BSD-HYP-MATRIX-001                  SCOPED                  nunca executado
TOE-INTERFACE-001                   SCOPED                  nunca executado

LAB-GOV-DECISION-LEDGER-001         VERIFIED                ENCERRADO

authorized_action: PORTFOLIO_REVIEW_REQUIRED   (trava, nao execucao)
```

**Nenhuma frente ativa.** A escolha do próximo trabalho exige um gate
explícito de revisão de portfólio.

## Por que este bloco existe

Ele esteve **desatualizado por seis gates**, descrevendo
`FOUND-FUNCTIONAL-GRAPH-001` como estado corrente enquanto o front matter
já registrava dez frentes encerradas. O YAML é a fonte de verdade e
sempre esteve correto; a prosa não. Como `resume_read_order` manda ler
este arquivo primeiro, a prosa obsoleta enganava exatamente na retomada.

## O que a cadeia de dez frentes estabeleceu

```text
semiconjugacao             NAO reflete recorrencia
bissimulacao funcional     NAO reflete   (e a mesma coisa, no caso total)
bissimulacao sobrejetiva   NAO reflete
OrbitSeparating            REFLETE
injetividade global        REFLETE  (forte demais)
```

Abstração entrega **observação**, não reflexão. Reforçar a relação de
simulação não atravessa essa fronteira; o que atravessa é **separação de
estados**.

## Limite computacional que permanece

`periodicOrbit` é **noncomputável**. `OrbitSeparating` é obrigação do
consumidor, por órbita, e **não** foi tornada decidível — a tentativa foi
formalizada em probe, compilou, e foi rejeitada por não comprar nada que
a equação única já não comprasse.

## Novidade

```yaml
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_FOUNDATION
```

## Próxima ação

Aguardar gate de revisão de portfólio. Nada mais está autorizado.
