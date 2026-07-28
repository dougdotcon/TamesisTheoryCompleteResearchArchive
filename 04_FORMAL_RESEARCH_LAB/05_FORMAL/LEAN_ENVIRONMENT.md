# Ambiente Lean

## Inventário verificado

| Campo | Valor |
|---|---|
| extensão VS Code | `leanprover.lean4-0.0.237` |
| Elan | `4.2.3` |
| toolchain declarado | `leanprover/lean4:v4.32.2` |
| `elan show` | resolve `leanprover/lean4:v4.32.2`, mas informa instalação no primeiro uso |
| `elan toolchain list` | `leanprover/lean4:v4.32.tmp` |
| `elan which lean` | falha: destino definitivo não existe |
| `elan which lake` | falha: destino definitivo não existe |
| Lean no `.tmp` | `4.32.2`, commit `f3b06c705e6c85f5314019d5d3baab0fec5b580c` |
| Lake no `.tmp` | `5.0.0-src+f3b06c7` |
| shims no PATH | `elan`, `lean` e `lake`: `NOT_FOUND` nesta sessão |
| Mathlib | `NOT_CONFIGURED`; revisão exata não resolvida |
| manifesto | `packages: []`, sem dependência Mathlib |
| SHA-256 do manifesto | `F61F111EEE3C5856DD6187087B1574BDCB8A52B817F28EAD5254962EDC6C0D73` |
| smoke `lake build` | `PASS`, 12 jobs, por caminho `.tmp` |

## Classificação

`LEAN_ENVIRONMENT_DISCOVERY: PASS`

`LEAN_TOOLCHAIN_AVAILABILITY: PARTIAL`

`LEAN_SMOKE_BUILD: PASS`

O build demonstra que os binários temporários funcionam. Ele não demonstra
que o toolchain está instalado definitivamente ou que outra sessão resolverá
as mesmas versões pelos shims.

## Configuração canônica requerida

A retomada deve resolver, nesta ordem:

1. `05_FORMAL/lean/lean-toolchain`;
2. shim estável do Elan;
3. toolchain definitivo resolvido pelo Elan;
4. `lake-manifest.json` com dependências e revisões exatas.

Um caminho contendo `.tmp` não é configuração canônica e não deve ser
persistido em scripts, manifests ou variáveis do repositório.

## Correções pendentes

1. concluir a instalação definitiva de `leanprover/lean4:v4.32.2`;
2. garantir que os shims do Elan estejam no PATH das sessões de validação;
3. fixar uma revisão exata de Mathlib durante a preparação autorizada;
4. regenerar e registrar o hash do manifesto após fixar Mathlib.

Até essas correções, o ambiente completo do benchmark não é declarado
reprodutível.
