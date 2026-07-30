# LAB-0.10 — Auditoria HTTP do cache Mathlib

## Conclusão

O cache selecionava inicialmente `C:\Windows\System32\curl.exe` 7.55.1,
mesmo quando `Git\mingw64\bin` aparecia antes no PATH do Lake. A razão é que
`Cache.IO.getCurl` lança o nome simples `curl` e a resolução do subprocesso Lean
no Windows escolheu o binário do sistema. O mecanismo interno da Mathlib dá
precedência ao arquivo absoluto `%USERPROFILE%\.cache\mathlib\curl-7.88.1`;
uma cópia verificável do cURL Git 8.21.0 nesse caminho fez `cache.exe` usar o
binário moderno de fato.

## Implementação auditada

- cURL recomendado: >= 7.81; mínimo para modo paralelo: 7.70.
- cURL abaixo de 7.70: execução serial, sem `--parallel`.
- modo paralelo: `--request GET --parallel --silent --retry 5 --write-out
  %{json}` e `--config %USERPROFILE%\.cache\mathlib\curl.cfg`.
- não há `--connect-timeout` nem `--max-time` no download do cache.
- hosts: `lakecache.blob.core.windows.net`, containers `mathlib4-master` e
  `mathlib4` (legacy).
- variáveis: `MATHLIB_CACHE_DIR`, `MATHLIB_CACHE_GET_URL`,
  `MATHLIB_CACHE_FROM` e `MATHLIB_CACHE_REPO_SCOPE`.

## cURLs

| Caminho | Versão | TLS | SHA-256 |
|---|---|---|---|
| `C:\Windows\System32\curl.exe` | 7.55.1 | WinSSL | `0BA1C44D0EE5B34B45B449074CDA51624150DC16B3B3C38251DF6C052ADBA205` |
| `C:\Program Files\Git\mingw64\bin\curl.exe` | 8.21.0 | Schannel | `0E773709C3A44DB47B88B71351D902027682ED87C3BD3821009E454BACCA8778` |

`Git\usr\bin` contém `uname.exe` e `chmod.exe`, mas não contém cURL. Portanto,
adicioná-lo sozinho mantinha o cURL 7.55.1 selecionado.

## Rede

Não havia proxy de ambiente e WinHTTP estava em acesso direto. DNS resolveu
`lakecache.blob.core.windows.net` para `20.209.19.193`; TCP 443 passou. Os dois
cURLs completaram TLS e HTTP em uma URL real do cache. A URL master para
`263a7904304fd614.ltar` respondeu 404; a mesma hash no container legacy
respondeu 200 com 24.459 bytes.

`cache query HEAD` terminou em 7–10 s nos três ambientes e informou que o HEAD
do repositório Tamesis não possui cache de fork. Isso não bloqueia os objetos
Mathlib por hash nos containers master/legacy.

## Processo real e curl.cfg

Antes da correção, o filho de `cache.exe` era
`C:\Windows\System32\curl.exe`. Após instalar a cópia validada no caminho
interno esperado, o processo real foi
`C:\Users\CLIENTE\.cache\mathlib\curl-7.88.1`, SHA idêntico ao cURL Git 8.21.0.
Sua linha sanitizada foi:

```text
curl-7.88.1 --request GET --parallel --silent --retry 5
  --write-out %{json} --config C:\Users\CLIENTE\.cache\mathlib\curl.cfg
```

O `curl.cfg` observado continha 2.981 URLs do container legacy, uma URL e um
arquivo `.part` por objeto. Não havia retry timeout, connect timeout ou maximum
time no arquivo; `--retry 5` vinha da linha de comando.

## Download direcionado

`cache get Mathlib.Tactic --repo=leanprover-community/mathlib4` iniciou
transferências reais. Foram recebidos 398 `.ltar`; 2.583 `.part` permaneceram,
muitos contendo respostas 404. A contagem de `.olean` subiu de 920 para 1.173,
confirmando descompactação parcial. Depois de 60 s sem mudança de bytes ou
contagens, somente os processos dessa execução foram encerrados.

`Mathlib/Tactic.olean` e `Mathlib.olean` não foram produzidos. O smoke mínimo
passou; os smokes de tática e umbrella falharam por esses objetos ausentes.
Cache completo e builds Lake não foram executados.

## Decisão

O erro de criação de processo do LAB-0.9 está resolvido. O bloqueio atual é
`LAB010_CACHE_TRANSFER_STALLED`: o modo paralelo transfere e descompacta parte
do cache, mas não conclui após milhares de misses/partials e não possui limites
internos de conexão/transferência. Nenhuma versão Lean/Mathlib foi alterada.
