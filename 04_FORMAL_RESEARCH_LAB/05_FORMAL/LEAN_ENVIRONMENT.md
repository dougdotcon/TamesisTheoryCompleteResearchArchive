# Ambiente Lean

## Runtime canônico

| Campo | Valor |
|---|---|
| runtime canônico | Ubuntu 24.04 no WSL2 |
| usuário | `linuxdev` |
| hostname | `linux-dev` |
| diretório canônico | `/home/linuxdev/projects/TamesisTheoryCompleteResearchArchive` |
| raiz Lean | `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean` |
| kernel | `5.10.16.3-microsoft-standard-WSL2` |
| rota Windows nativa | `FROZEN / HISTORICAL / NOT_OPERATIONAL` |

O laboratório opera exclusivamente no filesystem ext4 do WSL. Nenhum caminho
sob `/mnt/` é caminho operacional. A origem congelada em
`/mnt/d/TamesisTheoryCompleteResearchArchive` permanece somente como fonte
histórica do clone e não recebe execução.

## Inventário verificado

| Campo | Valor |
|---|---|
| Elan | 4.2.3 (b6cec7e10 2026-06-08) |
| toolchain declarado | `leanprover/lean4:v4.33.0-rc1` |
| elan show | resolve `leanprover/lean4:v4.33.0-rc1` pelo `lean-toolchain` do projeto |
| toolchain instalado | `~/.elan/toolchains/leanprover--lean4---v4.33.0-rc1` (estável, sem `.tmp`) |
| which lean | `/home/linuxdev/.elan/bin/lean` |
| which lake | `/home/linuxdev/.elan/bin/lake` |
| Lean | 4.33.0-rc1, commit `62eed1db4d67327ec8120be05f1a1b0847d74561` |
| Lake | 5.0.0-src+62eed1d |
| Mathlib | tag `v4.33.0-rc1` |
| Mathlib revision | `79d0395a1825a6264ad5d269e35e60537518955e` |
| cache Mathlib | `lake exe cache get` exit 0; 8.643 arquivos descomprimidos; nenhum download pendente |
| smoke `import Mathlib.Data.Nat.Basic` | PASS |
| smoke `import Mathlib.Tactic` | PASS |
| smoke `import Mathlib` | PASS |
| `lake build` | PASS, 8.670 jobs |

## Classificação

LEAN_ENVIRONMENT_DISCOVERY: PASS

LEAN_TOOLCHAIN_AVAILABILITY: PASS

LEAN_SMOKE_BUILD: PASS

O toolchain é definitivo, resolvido pelo Elan a partir do `lean-toolchain` do
projeto, sem dependência de diretório temporário. Os três smokes de Mathlib
concluíram com exit code 0 e o build completo do alvo `TamesisLab` concluiu
com sucesso.

## Configuração canônica

A configuração canônica é composta por:

1. `05_FORMAL/lean/lean-toolchain`;
2. shim estável do Elan em `/home/linuxdev/.elan/bin`;
3. toolchain definitivo resolvido pelo Elan;
4. `05_FORMAL/lean/lakefile.toml` declarando Mathlib pela tag `v4.33.0-rc1`;
5. `05_FORMAL/lean/lake-manifest.json` com dependências e revisões exatas.

Mathlib está fixada na revisão `79d0395a1825a6264ad5d269e35e60537518955e`,
correspondente à tag `v4.33.0-rc1`. O manifesto fixa também as dependências
transitivas.

## Estado do smoke

Os três módulos de smoke compilam:

| Arquivo | Import exercitado | Resultado | Duração |
|---|---|---|---|
| `TamesisLab/Tests/MathlibMinimalSmoke.lean` | `Mathlib.Data.Nat.Basic` | PASS | 4,0 s |
| `TamesisLab/Tests/MathlibTacticSmoke.lean` | `Mathlib.Tactic` | PASS | 25,8 s |
| `TamesisLab/Tests/MathlibSmoke.lean` | `Mathlib` | PASS | 17,0 s |

`lake build` compila o alvo padrão `TamesisLab`, que importa
`TamesisLab.Tests.MathlibSmoke` e portanto exercita Mathlib integralmente.

Nenhum teorema do benchmark foi criado ou executado.

## Histórico da rota Windows nativa

A rota nativa Windows foi congelada como histórica na tag
`lab-native-windows-paused` (commit `634de1c3aa915fcb0ccc5f27d6fe6194368535a4`)
e não deve mais ser usada operacionalmente. Ela permanece registrada apenas
para auditoria dos gates LAB-0.6 a LAB-0.11, cujo bloqueio foi a
indisponibilidade do cache Mathlib sob o runtime Windows. O par
Lean/Mathlib `v4.32.2` associado a essa rota não é ressuscitado.
