# LAB-0.11 — Cache availability audit

## Resultado

**LAB011_NO_CACHE_BACKED_PAIR_FOUND**. O HEAD atual não possui marcador de cache; os objetos críticos estão publicados apenas no container oficial `mathlib4` (legacy). O cache local permanece parcial. O release v4.32.1 existe, mas a instalação isolada do toolchain excedeu o timeout e nenhum smoke foi promovido.

## Evidência

- HEAD: `2ee0c2d76e657f9663d911c2060f23a513af4489`; `lake exe cache query HEAD`: marcador ausente.
- Lean/Mathlib atuais: Lean 4.32.2, Mathlib `v4.32.2` / `905b95818eb32af7874a58b427f50c1711a5e96c`.
- `Mathlib.Tactic` (`263a7904304fd614.ltar`): master 404; legacy HTTP 200, 24.459 bytes.
- `Mathlib` (`02750ba6c2227d9a.ltar`): master 404; legacy HTTP 200, 470.725 bytes.
- Cache local: 398 `.ltar`, 2.583 `.part`; nenhum dos dois objetos críticos está materializado como `.ltar` completo.
- cURL moderno Git 8.21.0/Schannel foi usado nos probes seriais; cURL legado 7.55.1 foi rejeitado pelo launcher.

## Decisão de segurança

Não executar benchmark/RH, não alterar Lean/Mathlib canônicos e não renomear `.part` manualmente. O próximo gate deve concluir o toolchain v4.32.1 em diretório isolado, fixar a fonte `legacy` e provar ambos os imports antes de qualquer migração.
