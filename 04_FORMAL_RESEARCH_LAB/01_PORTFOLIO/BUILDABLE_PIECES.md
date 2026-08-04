---
document_id: BUILDABLE-PIECES-2026-08-04
measured_at: 2026-08-04
method: PARALLEL_ELABORATION_PROBES
pieces_identified: 4
directive: "Se nao tiver algo, vamos ter que construir"
---

# As pecas construiveis, medidas

As cinco medicoes paralelas nao acharam so bloqueios. Acharam **quatro
pecas nomeaveis e autocontidas**, cada uma com valor upstream
independente do problema de milenio que destrava.

| peca | destrava | insumos ja no Mathlib | custo |
|---|---|---|---|
| **B** enumeracao espectral de compactos | RH | 2 lemas prontos | moderate |
| **C** Mordell-Weil f.g. sobre Q | BSD | 3 insumos, **0 consumidores** | moderate |
| **D** equivalencia racional e grupo de Chow | Hodge | 2 pecas desconectadas | PR-scale |
| **A** multiplicador L2 sem suavidade | NS | Plancherel | high |

## Peca C — o toolkit de descida existe e ninguem usa

Achado mais surpreendente da rodada.

```text
existe   Height.mulHeight, .logHeight, .mulHeight1, .logHeight1
existe   WeierstrassCurve.abs_logHeight_addSubMap_sub_two_mul_logHeight_le
existe   CommGroup.fg_of_descent'  <- ZERO consumidores em todo o Mathlib
falta    a altura ingenua em PONTOS: TODO explicito no proprio arquivo
         Mathlib/NumberTheory/Height/EllipticCurve.lean
```

Os tres insumos estao no Mathlib e **desconectados**. Fechar a cadeia
*altura ingenua -> lei do paralelogramo aproximada -> `fg_of_descent'`
aplicado a `WeierstrassCurve.Affine.Point` sobre Q* da **Mordell-Weil
finitamente gerado**, sem o qual `rank` e indefinivel.

Custo isolado: **moderate**. O lado analitico de BSD continua
`very_high` e depende de modularidade, da qual o Mathlib nao tem nada.

## Correcao de nome: `EllipticCurve` foi REMOVIDA

```text
antes   structure EllipticCurve
agora   WeierstrassCurve + WeierstrassCurve.IsElliptic
```

Refatoracao do Mathlib. Novo desde julho de 2026: `localEulerFactor`,
`LFunction : ArithmeticFunction Z`, `LSeries : C -> C`.

Mas `LFunction` e serie de Dirichlet **formal**: sem convergencia, sem
continuacao analitica, sem equacao funcional. Logo `ord_{s=1} L(E,s)`
**nao e expressavel**, e as **cinco** quantidades da formula BSD —
rank, regulador, Sha, Tamagawa, torcao — sao todas indefiniveis hoje.

## Peca D — Chow, e o atomo formalizavel de Hodge

```text
existe   AlgebraicGeometry.AlgebraicCycle  (arquivo de 79 linhas, semanas)
existe   Scheme.ord, .ordHom, .functionField, .residueField
falta    equivalencia racional  =>  falta grupo de Chow
```

Sem quociente por equivalencia racional, "classe de ciclo algebrico" nao
e objeto definido. As duas pecas existem e estao desconectadas: definir a
equivalencia e contribuicao de escala-PR bem delimitada.

**Mas nao toca a conjectura.** Os DOIS lados da bicondicional carecem de
objetos: nao ha de Rham algebrico, nao ha Betti, nao ha comparacao, nao
ha graduacao (p,q), nao ha variedade complexa nem metrica de Kahler, e
nao ha nem `QuasiCoherent` nem feixe cotangente relativo — logo
`H^q(X, Omega^p)`, o objeto que a conjectura gradua, e informulavel.

Atencao ao homonimo: `RingTheory/Kaehler` e **diferenciais** de Kahler,
algebra comutativa. Nada a ver com metrica de Kahler.

## O que este documento NAO afirma

```text
que BSD ou Hodge tenham ficado alcancaveis
que fechar uma peca aproxime de um enunciado de milenio
que escala-PR signifique trivial
```

Peca C da **Mordell-Weil**, nao BSD. Peca D da **Chow**, nao Hodge. Cada
uma tem valor por si, upstream, e e por isso que valem — nao por
proximidade a premio nenhum.
