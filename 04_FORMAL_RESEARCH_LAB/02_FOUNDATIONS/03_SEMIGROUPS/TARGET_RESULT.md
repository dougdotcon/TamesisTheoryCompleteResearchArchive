# FOUND-SEMIGROUP-001 — Resultado-alvo

## Enunciado

Construir e verificar em Lean um modelo finito explícito no qual:

1. um conjunto finito de três transições (`Shift3`) com composição
   (`Shift3.comp`) forma um monoide — associatividade e identidade bilateral
   provadas antes de qualquer instância;
2. as transições agem sobre um conjunto finito de três regimes (`Regime3`)
   por uma função total (`Shift3.apply`) compatível com a composição
   (`(comp a b).apply r = a.apply (b.apply r)`);
3. a ação é fiel e transitiva;
4. as cardinalidades são exatamente 3 e 3;
5. a camada abstrata é a interface oficial da Mathlib
   (`SemigroupAction`/`MulAction`), sem duplicata local.

## Produto

Modelo formal padrão de referência (`FOUNDATIONAL_FORMALIZATION_ONLY`), com
rastreabilidade FOUND-SG-001 a FOUND-SG-013, auditoria computacional finita
e contraexemplos conceituais que impedem generalização indevida.

## O que este resultado não é

Não é uma descoberta científica; não valida TRI, TDTR, TOE ou qualquer claim
histórica; não estabelece universalidade; não toca problemas Clay.
