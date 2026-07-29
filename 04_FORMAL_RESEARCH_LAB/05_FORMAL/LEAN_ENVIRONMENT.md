# Ambiente Lean

## Inventário verificado

| Campo | Valor |
|---|---|
| extensão VS Code | leanprover.lean4-0.0.237 |
| Elan | 4.2.3 |
| toolchain declarado | leanprover/lean4:v4.32.2 |
| elan show | resolve leanprover/lean4:v4.32.2 pelo lean-toolchain do projeto |
| elan toolchain list | leanprover/lean4:v4.32.2 |
| elan which lean | caminho definitivo, sem .tmp |
| elan which lake | caminho definitivo, sem .tmp |
| Lean | 4.32.2, commit f3b06c705e6c85f5314019d5d3baab0fec5b580c |
| Lake | 5.0.0-src+f3b06c7 |
| Mathlib | commit 905b95818eb32af7874a58b427f50c1711a5e96c, tag v4.32.2 |
| manifesto | 9 dependências transitivas com commits exatos |
| SHA-256 do manifesto | 4BB811C39DA9FBFF3CE2D6BD9B947AF0A4266D865608EA83A66A5A9B97C453B9 |
| cache Mathlib | indisponível |
| smoke import Mathlib | timeout após 600s; sem PASS reivindicado |

## Classificação

LEAN_ENVIRONMENT_DISCOVERY: PASS

LEAN_TOOLCHAIN_AVAILABILITY: PASS

LEAN_SMOKE_BUILD: PASS para o smoke core anterior.

O toolchain definitivo está disponível e o Elan resolve o identificador
declarado sem depender de .tmp. A preparação ainda está parcial porque o
smoke import Mathlib não concluiu.

## Configuração canônica

A configuração canônica é composta por:

1. 05_FORMAL/lean/lean-toolchain;
2. shim estável do Elan;
3. toolchain definitivo resolvido pelo Elan;
4. lake-manifest.json com dependências e revisões exatas.

Mathlib está fixada no commit 905b95818eb32af7874a58b427f50c1711a5e96c.
O manifesto fixa também as dependências transitivas. O cache remoto falhou,
portanto a compilação local foi tentada.

## Estado do smoke

O módulo TamesisLab/Tests/MathlibSmoke.lean importa Mathlib e verifica fatos
triviais. A compilação local excedeu 600 segundos depois de gerar milhares de
artefatos; o resultado é LAB_MATHLIB_SMOKE_BUILD_FAILED.

Nenhum teorema do benchmark foi criado ou executado.
