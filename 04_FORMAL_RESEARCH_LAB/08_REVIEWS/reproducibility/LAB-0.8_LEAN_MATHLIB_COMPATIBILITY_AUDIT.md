# LAB-0.8 — Auditoria de compatibilidade Lean–Mathlib

## Conclusão

`v4.32.2` é uma tag oficial remota e a revisão atual usa exatamente o
toolchain `leanprover/lean4:v4.32.2`. O par é semanticamente compatível, mas
não é operacionalmente reproduzível neste ambiente porque `cache get` termina
com uma exceção de processo do Windows antes de produzir diagnóstico HTTP, e
os artefatos `.olean` essenciais permanecem incompletos. O probe isolado de
`v4.32.1` reproduziu a mesma falha de cache e também não passou.

## Cache da revisão atual

Comando executado uma vez:

```text
elan run leanprover/lean4:v4.32.2 lake exe cache get
```

Log bruto: `LAB-0.8-cache-current-revision.log`.

Saída integral observada:

```text
elan : uncaught exception: o sistema não pode encontrar o arquivo especificado. (error code: 2)
```

O wrapper PowerShell reportou `$LASTEXITCODE=1`; a exceção interna do Elan
reporta código Windows `2`. Não houve URL, HTTP status, hash, download ou
extração reportados.

## Proveniência

O remoto é `https://github.com/leanprover-community/mathlib4`. A revisão local
`905b95818eb32af7874a58b427f50c1711a5e96c` está limpa, possui tag local
`v4.32.2` e corresponde à tag remota oficial `refs/tags/v4.32.2` no mesmo SHA.
As tags remotas `v4.32.0`, `v4.32.1` e `v4.32.2` foram verificadas. O
`lean-toolchain` do checkout, do projeto e da tag é
`leanprover/lean4:v4.32.2`.

## Diagnóstico da ferramenta

O código da Mathlib usa `IO.Process.output` para executar `curl` e o
`leantar.exe` do sysroot Lean para descompressão. `curl.exe`, `git` e
`leantar.exe` existem e executam; portanto não foi demonstrada ausência de
ferramenta auxiliar. Como a exceção ocorre antes de qualquer URL/status, a
classificação conservadora é `CACHE_TOOL_INTERNAL_ERROR`, não “objeto remoto
inexistente”.

## Smokes atuais

- `MathlibMinimalSmoke.lean`: PASS, 1+1 por `rfl`, aproximadamente 5 s.
- `MathlibTacticSmoke.lean`: FAIL por `Mathlib/Tactic.olean` ausente,
  aproximadamente 2 s.
- `MathlibSmoke.lean`: FAIL por `Mathlib.olean` ausente, aproximadamente 3 s.

Isso confirma cache/build incompleto do agregador e de módulos transitivos,
sem indicar erro lógico nos exemplos.

## Probe v4.32.1

O probe foi criado fora do repositório em
`C:\Users\CLIENTE\AppData\Local\Temp\tamesis-mathlib-v4.32.1-probe`.
A tag declara `leanprover/lean4:v4.32.1`; a revisão resolvida foi
`520045ab14e26149ee970e2e617ca04b09bde5d6`. O toolchain foi instalado sem
alterar o default global. `lake update mathlib` clonou a revisão, mas o hook de
cache terminou com a mesma exceção Windows (código interno 2). O `cache get`
explícito repetiu a falha; `import Mathlib` terminou com módulo desconhecido e
`lake build` falhou por imports inválidos. Nenhum arquivo foi baixado ou
descompactado.

## Decisão

Nenhum par reproduzível foi encontrado. A configuração canônica não foi
migrada e a revisão `905b958...` não foi alterada. O benchmark, Clay e
`RH-NOGO-001` não foram executados.
