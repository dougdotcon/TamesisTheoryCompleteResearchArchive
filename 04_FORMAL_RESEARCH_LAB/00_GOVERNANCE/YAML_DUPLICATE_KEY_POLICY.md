---
document_id: LAB-YAML-DUPLICATE-KEY-POLICY
status: ACTIVE
enforced_by: labctl validate
error_code: DUPLICATE_YAML_KEY
---

# Política de chaves YAML duplicadas

## A regra

```text
Cada chave de um mapa YAML deve ocorrer exatamente uma vez dentro
daquele mapa.

Duplicatas identicas tambem sao proibidas.

A interpretacao "ultimo valor vence" nao eh aceita como semantica de
governanca.

A ausencia de erro no parser padrao nao demonstra integridade.

Todas as estruturas YAML versionadas devem ser examinadas antes do
commit.

Contagens e estados agregados devem ser derivados ou conferidos contra
suas entradas individuais.
```

E, com o mesmo peso:

```text
Auditorias declaradas como integrais devem percorrer o conjunto
completo definido no escopo.

Uma auditoria parcial nao pode ser descrita como completa.
```

## Por que duplicatas idênticas também são proibidas

Porque a proibição não é sobre o valor: é sobre a **ambiguidade da
fonte**. Um mapa com duas definições da mesma chave descreve duas
intenções, e o parser escolhe uma delas sem avisar. Que hoje elas
coincidam não impede que a próxima edição toque só uma das duas — foi
exatamente assim que `META-ENC-003` nasceu.

## O que o parser padrão faz

```python
yaml.safe_load("a: 1\na: 2\n")   ->   {"a": 2}
```

Sem erro, sem aviso. A primeira definição desaparece. Por isso a
detecção **não** pode usar o objeto carregado: ela percorre a árvore
sintática, por `yaml.compose_all`, onde as duas ocorrências ainda
existem.

## Onde a regra é aplicada

```text
labctl validate, antes de qualquer carregamento normal
escopo: TODOS os .yaml e .yml versionados sob 04_FORMAL_RESEARCH_LAB
excluidos: .lake, __pycache__, .venv, node_modules, .git
```

A política é de integridade do **repositório**, não do caminho que o
`labctl` por acaso executa. `LAB_STATE`, `RESEARCH_QUEUE`,
`CLAIM_LEDGER`, cada `GAP_REGISTER`, cada `STATUS`, schemas e qualquer
outro YAML versionado entram na varredura.

## Severidade

```text
qualquer duplicata  ->  status: FAIL
```

Não existe modo de aviso. Não existe exceção para valores idênticos.

## Formato do erro

```text
DUPLICATE_YAML_KEY: <arquivo>:<linha_duplicada>
path=<caminho do mapa> key=<chave>
first_defined_at=<linha da primeira definicao>
classification=IDENTICAL_DUPLICATE | DIVERGENT_DUPLICATE
```

O caminho usa `.` para chaves e `[i]` para índices de sequência, de modo
que `queue[13].tests_planned` localiza o item exato de uma lista.

## Como resolver uma duplicata

```text
1. classificar: identica ou divergente;
2. se identica, manter a primeira ocorrencia e remover a outra;
3. se divergente, determinar a FONTE DE VERDADE documental;
4. registrar o valor efetivo anterior do parser;
5. registrar o valor final e qualquer mudanca semantica;
6. nunca escolher pelo que "parece correto".
```

Adotar o valor que o parser vinha usando **não** é resolver: é
ratificar o acidente.

## Testes de regressão

`06_COMPUTATION/python/tests/test_yaml_duplicate_keys.py` cobre mapa
raiz, mapa aninhado, mapa dentro de sequência, múltiplos documentos,
linhas reportadas, chaves iguais em mapas distintos, valores repetidos
em lista, diretórios excluídos e a varredura integral do laboratório.
