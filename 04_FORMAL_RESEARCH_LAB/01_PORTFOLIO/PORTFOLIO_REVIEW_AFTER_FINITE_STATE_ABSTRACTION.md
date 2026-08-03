---
document_id: PORTFOLIO-REVIEW-AFTER-FINITE-STATE-ABSTRACTION
reviewed_at: 2026-08-03
previous_work_item: FOUND-FINITE-STATE-ABSTRACTION-001
selected_next_action: LAB-GOV-FRONTMATTER-SCAN-001
alternatives_compared: 6
---

# Revisão de portfólio — depois da abstração de estados finitos

## Estado de entrada

```text
FOUND-FINITE-STATE-ABSTRACTION-001   VERIFIED / APPROVED   ENCERRADA
claims no ledger                     23
duplicatas YAML relatadas             0, em 57 arquivos
lake build                            PASS, 8767 jobs
```

## As seis alternativas

| | Candidato | Custo | Risco | Veredito |
|---|---|---|---|---|
| A | Cobertura do scanner de duplicatas em front matter | baixo | baixo | **SELECIONADO** |
| B | Bissimulação, `ABS-GAP-015` | alto | médio | adiado |
| C | Invariância do witness sob recodificação, `ENC-GAP-020` | médio | alto | rejeitado de novo |
| D | Quocientes, `ABS-GAP-016` | alto | médio | adiado |
| E | Extração nativa, CLI, parser | médio | alto | rejeitado |
| F | Frente matemática nova e independente | alto | alto | adiado |

## Por que A, e por que agora

A escolha **não** foi feita por conveniência. Ela foi feita porque um
probe descartável encontrou um defeito na própria cadeia de evidência do
laboratório.

### O achado, medido

```text
arquivos Markdown no laboratorio              483
com front matter YAML                         332
arquivos enumerados pelo scanner               57
Markdown enumerados pelo scanner                0
LAB_STATE.md dentro do scan de duplicatas     NAO
```

`labctl.yaml_files_under` seleciona por **extensão**:

```python
if candidate.suffix.lower() not in (".yaml", ".yml"):
    continue
```

Consequência: `LAB_STATE.md` — o arquivo mais crítico da governança — e
outros `331` documentos com front matter **nunca foram varridos**, e
mesmo assim todo relatório de gate afirma:

```text
yaml_duplicate_key_scan: PASS
```

### Por que isso é grave, e não cosmético

A regra de governança do laboratório diz, textualmente:

```text
"Último valor vence" não é semântica de governança, e a ausência
de erro no parser não demonstra integridade.
```

Mas `read_front_matter` usa `yaml.safe_load`, que aplica exatamente
"último valor vence". Verificado em probe:

```text
entrada   status: READY  seguido de  status: VERIFIED
resultado {'document_id': 'SAMPLE', 'status': 'VERIFIED'}
```

Uma chave duplicada em `LAB_STATE.md` — por exemplo dois
`authorized_action` — seria **silenciosamente resolvida pelo parser** e
passaria por `labctl validate` sem erro.

### Por que o custo é baixo

O detector **já funciona** sobre conteúdo de front matter. O mesmo probe
mostrou:

```text
detect_duplicate_yaml_keys aplicado a um .md com chave duplicada:  1 achado
```

Ou seja: a lógica de detecção está correta; apenas a **seleção de
arquivos** está estreita. O defeito é de escopo, não de algoritmo.

## Por que não B, C, D, E, F agora

- **B, D** — bissimulação e quocientes são a continuação científica
  natural, e continuam `NOT_AUTHORIZED` por decisão da frente recém
  encerrada. Elas merecem gate próprio, e merecem ser abertas com a
  cadeia de evidência **confiável**, não antes disso.
- **C** — `ENC-GAP-020` foi rejeitado na revisão anterior por
  acoplamento com a ordem de enumeração do detector. Nada mudou.
- **E** — extração, CLI e parser distribuem garantia sem contrato
  semântico; permanecem `NOT_AUTHORIZED`.
- **F** — abrir frente matemática nova enquanto o instrumento de
  validação tem cobertura parcial seria acumular resultados sobre uma
  medição que já se sabe incompleta.

## O princípio que decidiu

```text
Quando se descobre que o instrumento de medicao tem cobertura
menor do que declara, conserta-se o instrumento antes de
produzir mais medicoes com ele.
```

Este gate encontrou o defeito **por probe**, não por suspeita. Ele não
é hipotético.

## Ação selecionada

```text
LAB-GOV-FRONTMATTER-SCAN-001
Cobertura integral do scanner de chaves YAML duplicadas
```

Não é frente de pesquisa: é correção de governança, no mesmo formato de
`LAB-GOV-YAML-DUPLICATE-KEYS-001`. Um único gate corretivo.

## Escopo negativo do gate selecionado

```text
nao alterar a logica de deteccao de duplicatas
nao alterar nenhuma frente encerrada
nao alterar nenhum arquivo Lean
nao promover claim
nao abrir frente matematica
nao mexer em bissimulacao, quocientes, extracao, CLI ou parser
```

## Se a varredura ampliada encontrar duplicatas reais

Elas devem ser corrigidas **no mesmo gate**, com cada correção
registrada individualmente. Se forem muitas ou divergentes, o gate para
e reporta, em vez de normalizar em massa.
