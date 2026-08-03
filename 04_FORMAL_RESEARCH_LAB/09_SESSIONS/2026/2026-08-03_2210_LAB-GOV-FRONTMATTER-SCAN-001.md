---
session_id: 2026-08-03_2210_LAB-GOV-FRONTMATTER-SCAN-001
started_at: 2026-08-03T22:10:00-03:00
ended_at: 2026-08-03T22:10:00-03:00
agent: claude-opus-5
git_commit_before: bc717e6ffb3e38155ec8401ca53476bcbd62462e
git_commit_after: PENDING
active_work_item: FOUND-FINITE-STATE-ABSTRACTION-001
authorized_action: LAB_GOV_FRONTMATTER_SCAN_CORRECTION_AUTHORIZED
result_status: GOVERNANCE_CORRECTION_VERIFIED
claims_changed: []
gaps_opened: 0
gaps_closed: 0
---

## Objetivo autorizado

Ampliar a varredura de chaves YAML duplicadas para cobrir o front matter
dos documentos Markdown, corrigir o que a varredura ampliada encontrar e
registrar a cobertura real do instrumento.

## Estado inicial

```text
HEAD                        bc717e6ffb3e38155ec8401ca53476bcbd62462e
frontmatter_scan_coverage   PARTIAL_KNOWN_DEFECT
arquivos varridos            57, nenhum Markdown
pytest                       21 passed
```

## Trabalho executado

```text
extract_front_matter                novo
detect_duplicate_front_matter_keys  novo, reutiliza _walk_yaml_node
markdown_files_under                novo
scan_duplicate_yaml_keys            escopo ampliado
read_front_matter                   passou a rejeitar duplicatas
LAB_STATE.md                        delimitador de fechamento corrigido
13 testes novos                     FM-TEST-001 a FM-TEST-013
```

## Evidências

```text
cobertura antes    57 arquivos,   0 front matter
cobertura depois  390 arquivos, 333 front matter
LAB_STATE.md na varredura          agora SIM

duplicatas em front matter           0
front matter malformado encontrado   1  (LAB_STATE.md)
front matter malformado restante     0

pytest    34 passed
labctl validate  PASS
```

## Falhas

Nenhuma falha de execução. Um achado real:

`LAB_STATE.md` fechava o front matter com `---# Estado atual`, o
delimitador dividindo a linha com o primeiro título. Passava apenas
porque a expressão regular de `read_front_matter` é tolerante quanto ao
que segue o `---`. Corrigido, e fixado como regressão.

O interesse do achado não é o arquivo: é que ele estava **no arquivo
mais crítico da governança**, e nenhuma validação anterior podia vê-lo.

## Decisões

- A lógica de detecção **não** foi tocada. O defeito era de escopo.
- `read_front_matter` passou a rejeitar duplicatas em vez de deixar
  `yaml.safe_load` aplicar "último valor vence" — que a própria regra de
  governança já proibia por escrito.
- O relatório passou a publicar `yaml_files_scanned` e
  `markdown_front_matter_scanned`, para que "integral" seja conferível
  sem ler o código.
- Os limites remanescentes foram **declarados**, não silenciados: front
  matter TOML/JSON e YAML dentro de blocos de código continuam fora.

## O que não foi feito

```text
alteracao da logica de deteccao  NAO
arquivos Lean                    NENHUM
lake build                       NAO executado, nada de Lean mudou
promocao de claim                NAO
frente matematica nova           NAO
```

## Próxima ação única

Revisão de portfólio.

## Handoff

Instrumento de validação com cobertura conferida e publicada.
`PORTFOLIO_REVIEW_REQUIRED`.
