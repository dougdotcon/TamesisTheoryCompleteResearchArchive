---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-VERIFICATION-METHOD-CORRECTION
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
severity: METHODOLOGICAL
outcome: ALL_CLAIMS_RECONFIRMED
---

# Correção do método de captura de código de saída

## O defeito

A sessão executou os comandos do repositório canônico a partir de um
shell hospedeiro, atravessando uma camada de conversão. Nessa
travessia, `$?` e `$VAR` eram expandidos **pelo shell hospedeiro antes
de chegarem ao shell do repositório**.

Consequência: comandos da forma

```bash
lake env lean arquivo.lean; echo $? > /tmp/probe.exit
```

gravavam o código de saída **do hospedeiro**, não o do `lean`.

## Como o defeito foi detectado

Dois sintomas, ambos registrados:

```text
1. um probe reportou "exit 0" com `lake` AUSENTE do PATH
   (mensagem: "lake: command not found")

2. a auditoria umbrella reportou "exit 0" enquanto a saida
   continha "error: failed to synthesize"
```

O segundo caso é o decisivo: houve um erro real de elaboração
acompanhado de um código de saída falso.

## A correção

Todo comando cujo código de saída é evidência passou a viver em um
**arquivo de script**, executado dentro do repositório canônico. Assim
`$?` nunca atravessa a fronteira:

```bash
lake env lean "$target" > /tmp/lean_run.out 2>&1
rc=$?
echo "REAL_EXIT_CODE=$rc"
exit "$rc"
```

O script também reporta a contagem de linhas de erro, de modo que
código de saída e conteúdo se confirmem mutuamente.

## Reverificação

Todas as afirmações de `exit 0` feitas nos gates anteriores foram
**reexecutadas** com o método corrigido:

```text
/tmp/FiniteStateAbstractionProbe.lean         errors=0  REAL_EXIT_CODE=0
/tmp/FiniteStateAbstractionReviewProbe.lean   errors=0  REAL_EXIT_CODE=0
umbrella audit (apos correcao)                errors=0  REAL_EXIT_CODE=0
lake build                                    errors=0  REAL_BUILD_EXIT=0
```

**Nenhuma afirmação anterior era falsa.** Os dois probes de fato
compilavam; o método de medição é que não era confiável. O único erro
real que o método ocultava — o `Decidable` da auditoria umbrella — foi
encontrado e corrigido neste gate.

## Regra incorporada

```text
Um codigo de saida so e evidencia quando a sua captura nao
atravessa fronteira de shell.

Codigo de saida e conteudo da saida devem confirmar um ao outro:
"exit 0" com linha "error:" e defeito de medicao, nao PASS.
```

Isto reforça, e não substitui, a regra já existente do laboratório:
*um processo com exit diferente de zero nunca é evidência de PASS*.
