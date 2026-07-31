# FOUND-SEMIGROUP-002 — Resultado-alvo

## Enunciado principal

> Para toda função `f : X → X` sobre um tipo finito `X` e todo estado
> inicial `x`, a sequência `f^[n] x` é eventualmente periódica, com
> pré-período e período limitados por `Fintype.card X`, e a coincidência se
> propaga a todos os índices posteriores.

Assinatura candidata (`FSG2-PER-002`):

```lean
theorem exists_eventual_period
    {X : Type*} [Fintype X] (f : X → X) (x : X) :
    ∃ μ lam : ℕ,
      μ < Fintype.card X ∧
      0 < lam ∧
      μ + lam ≤ Fintype.card X ∧
      Function.iterate f (μ + lam) x = Function.iterate f μ x
```

## Meta escolhida

```text
C. CORE_BOUNDS_AND_PROPAGATION
```

Incluídos: existência da colisão (`CORE`), limitantes em `Fintype.card X`
(`BOUNDED`), e propagação para todo `k` (`PROPAGATION`).

**Excluída: decomposição única em cauda + ciclo.** Análise de custo em
`THEOREM_CANDIDATES.md`; adiada em `FSG2-GAP-004b`.

## Produtos esperados da execução futura

```text
Camada A   Reachable, IsInvariant, ponte com MulAction.orbit
           FSG2-REACH-001/002/003, FSG2-ORBIT-001, FSG2-INV-001/002

Camada C   FSG2-PER-001 (colisao)
           FSG2-PER-002 (alvo com limitantes)
           FSG2-PER-003 (propagacao)
           FSG2-PER-004 (ponte com Function.IsPeriodicPt)

Camada B   FSG2-ACT-001, corolario DERIVADO via smul_iterate_apply

Refutacao  CE-001..CE-005
```

## O que este resultado **não** é

```text
Nao eh uma descoberta matematica.
Nao eh uma nova teoria do tempo.
Nao eh uma nova teoria da transicao.
Nao valida TRI.
Nao valida TDTR.
Nao eh lei universal da dinamica.
Nao eh resultado fisico.
Nao resolve problema aberto.
Nao generaliza o modelo C3 a teoria universal.
```

A periodicidade eventual de uma função em conjunto finito é o princípio da
casa dos pombos. Ver `NOVELTY_BOUNDARY.md`, documento vinculante.

## Onde está o valor real

```text
formalizacao reutilizavel de um nucleo pequeno e correto;
separacao explicita entre acao completa, gerador e funcao;
ponte auditada com a API oficial da Mathlib, incluindo a armadilha
  do minimalPeriod;
contraexemplos que impedem sobregeneralizacao;
base para modelos discretos futuros, sem alegacao cientifica.
```

## Critério de sucesso da execução futura

```text
todos os teoremas da meta C compilam;
zero sorry / admit / axiom / unsafe;
#print axioms limitado a propext, Classical.choice, Quot.sound;
os cinco contraexemplos verificados;
nenhuma claim cientifica promovida;
nenhuma hipotese ociosa mantida.
```
