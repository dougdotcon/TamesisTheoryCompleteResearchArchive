# LAB-0.9 — Auditoria do runtime Windows do cache

## Resultado

O erro Windows `2` foi reproduzido e o recurso ausente identificado:
`uname.exe`. A Mathlib detecta o `curl.exe` do Windows como versão 7.55.1,
abaixo de 7.70, e chama `IO.Process.output { cmd := "uname" }`; como `uname`
não estava no PATH, a criação do processo falhava com `o sistema não pode
encontrar o arquivo especificado (error code: 2)`. `chmod.exe` também estava
ausente no PATH, mas não foi alcançado nessa ramificação Windows.

O `elan.exe` do Scoop e os shims `lean.exe`/`lake.exe` têm o mesmo SHA-256
`175089...5AD` e são proxies do Elan. Eles não colidem com `leantar.exe`, cujo
SHA é `00B3...0F8`. Os binários reais do toolchain são distintos.

## Matriz

- Teste A (shim Lake): versões e help PASS; `cache get` falhou sem diagnóstico
  visível, código 1.
- Teste B (`elan run`): versões e help PASS; `cache get` falhou, código 1.
- Teste C (Lake real): versão e help PASS; `cache get` falhou com exceção
  Windows 2 quando os shims permaneciam no PATH.
- Precedência real (`Git/usr/bin` + toolchain antes dos shims): o erro de
  processo desapareceu; o cache iniciou múltiplos `curl.exe`, mas não concluiu
em 600 s e nenhum `.ltar` foi obtido. Uma tentativa controlada de `cache get!`
após a correção também excedeu 120 s, sem baixar ou descompactar artefatos.

O probe Lean de subprocessos confirmou: `curl`, `curl.exe`, `git` e `lean`
executam; `uname` e `chmod` lançam exatamente o erro Windows 2.

## Correção aplicada

Foi aplicada somente uma correção temporária de sessão: adicionar
`C:\Program Files\Git\usr\bin` ao PATH antes do toolchain. Nenhuma alteração
global, reinstalação ou modificação de Mathlib foi feita. A causa inicial foi
identificada, mas o cache não foi validado porque a etapa seguinte ficou presa
em downloads `curl` sem produzir arquivos ou conclusão.

Não foi usado Process Monitor: a causa exata foi identificada diretamente pela
matriz e pelo probe de subprocessos; não houve necessidade de instalar uma
ferramenta externa.

## Estado

O par Lean/Mathlib não foi alterado. Smokes completos e `lake build` não foram
executados após o cache, pois `cache get` não terminou. `LAB-BENCH-001` continua
bloqueado; Clay e `RH-NOGO-001` permanecem sem execução.
