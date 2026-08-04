---
document_id: OPEN-PROBLEMS-MEASURED-2026-08-04
measured_at: 2026-08-04
method: PARALLEL_ELABORATION_PROBES
probes_exit: 0
items_measured: 5
corrects: ATTACK-READINESS-2026-08-04
---

# Os problemas em aberto, medidos em paralelo

Cinco medicoes concorrentes, todas por **elaboracao**, todas com
`exit 0`, todas somente-leitura (`git_dirty=0` conferido em cada uma).

Isto **corrige** a `ATTACK_READINESS.md`, que classificava os cinco de
baixo como tendo primeiro passo bibliografico. Dois dos cinco nao tem.

## Quadro revisto

| item | primeiro passo | custo | mudou? |
|---|---|---|---|
| `NS-PRESSURE-001` | **FORMAL** — projetor de Leray | high | **SIM** |
| `RH-NOGO-001` | **FORMAL** — enumeracao espectral | very_high | **SIM** |
| `TOE-INTERFACE-001` | bibliografico — falta o OBJETO | moderate | **SIM** |
| `YM-LIMIT-001` | bibliografico — falta a FERRAMENTA | very_high | nao |
| `PVSNP-PHYS-001` | formal, mas escala de pesquisa | very_high | **SIM** |

## `YM-LIMIT-001` — tres abismos, nao um

O Mathlib tem `LieGroup`, `LieAlgebra`, `killingForm`, `VectorBundle`,
`CovariantDerivative`, `SchwartzMap`, `IsGaussianProcess`.

E **nao tem**, com zero ocorrencias na arvore:

```text
PrincipalBundle   Connection   Curvature   GaugeGroup   YangMills
WightmanAxioms    OsterwalderSchrader      FockSpace    Minlos
ReflectionPositivity   SelfAdjointExtension   StoneTheorem
```

Os tres abismos, em ordem:

```text
1. a geometria nem chega ao YM CLASSICO
   campo de gauge e conexao em fibrado PRINCIPAL; Mathlib tem
   vetorial. A acao de Yang-Mills nao e sequer enunciavel.
2. a MEDIDA nao existe
   QFT euclidiana comeca por medida em S'(R^4). Falta
   Bochner-Minlos. Sem ele nem o campo LIVRE e construivel.
3. o ENUNCIADO do gap nao existe
   exige espectro de Hamiltoniano nao-limitado obtido por
   reconstrucao de Osterwalder-Schrader. Zero dos sistemas
   de axiomas esta enunciado.
```

Ter `LieGroup` mais `VectorBundle` mais `SchwartzMap` cria **ilusao de
proximidade**. E a relacao de ter aritmetica e achar que se tem teoria
analitica dos numeros: vocabulario partilhado, maquinaria nenhuma.

## `TOE-INTERFACE-001` — o bloqueio NAO e do toolchain

Achado que separa este item de todos os outros.

```text
CategoryTheory.Category  Functor  NatTrans  Adjunction  Iso
Equivalence  Comma  Limits.HasLimit  Limits.HasColimit
Limits.IsColimit  Monad  GrothendieckTopology  Sheaf
MonoidalCategory  Abelian
```

**15 de 15 elaboram.** O `target_statement` da fila pede objetos,
morfismos, invariantes e obstrucoes **sem equacao mestre** — ou seja,
uma especificacao categorial, nao fisica. A base esta completa.

O que falta e o **objeto**: nao existe, em lugar nenhum, definicao
candidata de "regime" ou de "interface". O toolchain esta pronto e o
enunciado nao existe.

Custo rebaixado de `very_high` para **`moderate`** no passo formal — o
`very_high` residual esta em **escrever a definicao**, que e conceitual e
nao mecanico.

### E o arquivo do laboratorio e esqueleto

```lean
-- TamesisLab/TOE.lean, 8 linhas, integral
def TargetStatus : String := "FORMAL_THEORY_OF_REGIMES_AND_INTERFACES"
theorem toe_smoke : True := by trivial
```

`TamesisLab/YangMills.lean` e identico em forma. Os diretorios `TOE/` e
`YangMills/` contem apenas `.gitkeep`. As frentes com conteudo real
somam cerca de 9.700 linhas.

**`theorem toe_smoke : True := by trivial` e o caso-limite do defeito de
vacuidade.** Um gate de forma passa nesse arquivo; ele nao afirma nada.

## `RH-NOGO-001` — a lacuna e maior do que estava escrito

`GLOBAL-WEYL-BRIDGE-SCALAR` supunha faltar so calculo pseudodiferencial.
Medido: **nenhuma** das premissas e expressavel.

```text
existe   multiplicadores de Fourier, besselPotential, MemSobolev
         = a subalgebra PsiDO de simbolo INDEPENDENTE de x
falta    classes de Hormander, simbolo dependente de x, parametrix,
         elipticidade, integral oscilatoria, fase estacionaria
falta    Weyl espectral por completo — todo "Weyl" no Mathlib e
         grupo de Weyl, nada espectral
falta    Schatten, traco, Hilbert-Schmidt, Rellich-Kondrachov,
         medida riemanniana, Laplace-Beltrami
```

Nem *"operador pseudodiferencial classico eliptico positivo autoadjunto
de ordem m > 0 em variedade compacta"* — a citacao de CORIASCO-DOLL-2020
ja auditada — e um **tipo escrevivel**. Cada palavra falta, exceto
"autoadjunto" e "compacta".

### Mas ha um primeiro passo formal com valor proprio

```text
estender LinearMap.IsSymmetric.eigenvalues
  de   [FiniteDimensional], indexado por Fin n
  para operadores compactos autoadjuntos em Hilbert separavel
  dando  Nat -> Real antitonica, tendendo a 0
  e      N(lambda) = Nat.card {i | lambda_i > lambda}
```

Apoia-se em `orthogonalComplement_iSup_eigenspaces_eq_bot` e
`finite_dimensional_eigenspace`, **que ja existem**. E contribuicao de
qualidade upstream, **independente de RH**, e converte
`GLOBAL-WEYL-BRIDGE-SCALAR` de *inexprimivel* para *enunciavel sob
hipotese explicita*.

Aviso registrado pelo proprio medidor: qualquer gate que formalize essa
peca precisa exibir operador compacto autoadjunto concreto de espectro
infinito — por exemplo o diagonal em `lp 2` com `lambda_i = 1/(i+1)` — e
verificar que `N(lambda)` e finito e nao-trivial. Sem isso passa vacuo,
**como ja ocorreu neste laboratorio**.

Um passo bibliografico agora seria desperdicio: as fontes ja estao
auditadas com SHA-256 em `08_REVIEWS/SOURCES/RH_NOGO/`. O gargalo nao e
leitura — e ausencia de vocabulario no assistente de prova.

## O que este documento NAO afirma

```text
que qualquer um dos 6 tenha ficado alcancavel
que algum deles deva ser aberto
que primeiro-passo-formal signifique primeiro-passo-barato
```

`RH-NOGO-001` continua `very_high` e congelado. `YM-LIMIT-001` continua
`very_high`. O que mudou foi a **classificacao do primeiro passo**, que
estava errada em tres dos cinco.
