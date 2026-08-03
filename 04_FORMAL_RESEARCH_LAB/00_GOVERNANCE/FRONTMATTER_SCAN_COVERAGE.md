---
document_id: LAB-GOV-FRONTMATTER-SCAN-001
status: VERIFIED
scope: yaml_files_and_markdown_front_matter
---

# Cobertura da varredura de chaves YAML duplicadas

## O defeito corrigido

```text
antes    57 arquivos varridos, 0 Markdown
depois  390 arquivos varridos, 333 front matter Markdown
```

`labctl.yaml_files_under` selecionava por extensão:

```python
if candidate.suffix.lower() not in (".yaml", ".yml"):
    continue
```

`332` documentos com front matter YAML ficavam fora — inclusive
`LAB_STATE.md`, que é onde vivem `authorized_action`, `work_status` e
`canonical_commit`.

Todo relatório de gate afirmava `yaml_duplicate_key_scan: PASS`. A
afirmação era verdadeira sobre `57` arquivos, e era lida como se fosse
sobre todos.

## O defeito era de escopo, não de algoritmo

`detect_duplicate_yaml_keys` sempre funcionou sobre conteúdo de front
matter — o probe confirmou isso antes de qualquer alteração. Por isso a
correção **não tocou a lógica de detecção**: ela reutiliza o mesmo
percurso da árvore sintática, `_walk_yaml_node`.

## O que mudou

```text
extract_front_matter                  novo
detect_duplicate_front_matter_keys    novo, reutiliza _walk_yaml_node
markdown_files_under                  novo
scan_duplicate_yaml_keys              escopo ampliado, relatorio detalhado
read_front_matter                     passou a REJEITAR duplicatas
```

### Numeração de linhas

O detector conta a partir de `1` dentro do bloco YAML. A linha `1` do
arquivo é o `---` de abertura, então o deslocamento para o arquivo é
exatamente `1`. Fixado por `FM-TEST-004`.

### `read_front_matter` deixou de aceitar "último valor vence"

A regra de governança já dizia:

```text
"Último valor vence" não é semântica de governança, e a ausência
de erro no parser não demonstra integridade.
```

Mas `read_front_matter` chamava `yaml.safe_load` direto. Medido antes da
correção:

```text
entrada    status: READY  seguido de  status: VERIFIED
resultado  {'document_id': 'SAMPLE', 'status': 'VERIFIED'}
```

Num campo como `authorized_action`, isso seria uma autorização escolhida
pelo parser. Agora a leitura falha com `DUPLICATE_YAML_KEY`.

## O que a varredura ampliada encontrou

```text
duplicatas em front matter        0
front matter malformado           1
```

O corpus estava limpo quanto a duplicatas. O único achado foi
estrutural.

### O achado: `LAB_STATE.md`

```text
linha 233 antes:   ---# Estado atual
linha 233 depois:  ---
                   (linha em branco)
                   # Estado atual
```

O delimitador de fechamento dividia a linha com o primeiro título. Isso
passava apenas porque a expressão regular de `read_front_matter` é
tolerante (`\n---\s*\n?`). Qualquer ferramenta com delimitador estrito
leria o arquivo inteiro como front matter, ou nenhum.

Corrigido, e fixado como regressão por `FM-TEST-006` e `FM-TEST-009`.

## Estado após a correção

```text
files_scanned                    390
yaml_files_scanned                57
markdown_files_seen              484
markdown_front_matter_scanned    333
duplicate_count                    0
malformed_front_matter             0
status                          PASS
```

`markdown_front_matter_scanned` é `333` e não `332` porque `LAB_STATE.md`
passou a ser parseável com delimitador estrito.

## Regra incorporada

```text
Uma varredura so pode ser declarada integral depois de se medir
quantos arquivos ela realmente abriu.

O relatorio passa a publicar o escopo — yaml_files_scanned e
markdown_front_matter_scanned — para que a afirmacao seja
conferivel sem ler o codigo.
```

## Limites

```text
front matter TOML ou JSON        NAO coberto, e nao existe no repositorio
YAML embutido em blocos de codigo  NAO coberto, e nao e governanca
arquivos fora de 04_FORMAL_RESEARCH_LAB   fora de escopo
```

Estes limites são declarados aqui justamente para que a palavra
"integral" não volte a significar mais do que a medição sustenta.
