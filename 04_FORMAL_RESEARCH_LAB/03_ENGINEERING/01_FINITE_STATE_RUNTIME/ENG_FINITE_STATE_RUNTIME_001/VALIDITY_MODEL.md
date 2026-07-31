---
document_id: RT-VALIDITY-MODEL
frozen: true
---

# Modelo de validade — congelado

```lean
def RawTransitionTable.Valid (t : RawTransitionTable) : Prop :=
  ∀ i : Fin t.next.size, t.next[i] < t.next.size
```

## Significado vinculante

```text
cada posicao do array representa um estado;
cada estado possui exatamente um sucessor;
todo sucessor pertence ao mesmo dominio Fin next.size.
```

## O que **não** significa

```text
tabela nao vazia;
todos os estados alcancaveis;
um unico componente;
um unico ciclo;
estado inicial valido;
ausencia de estados transitorios.
```

Esta lista é tão importante quanto a definição. A validade é uma
propriedade **estrutural** da tabela; ela não diz nada sobre a dinâmica.

## Propriedades confirmadas

```text
proposicional    eh um Prop, nao um Bool
finita           quantifica sobre Fin next.size
decidivel        instancia construida e sintetizada no probe
sem Classical.choose explicito
sem correcao silenciosa dos dados
```

## As três formulações auditadas

### Por `Fin` — **adotada**

```lean
∀ i : Fin t.next.size, t.next[i] < t.next.size
```

### Por `Nat`

```lean
∀ i : Nat, i < t.next.size → t.next[i] < t.next.size
```

### Por elementos

```lean
∀ destination ∈ t.next.toList, destination < t.next.size
```

### Decisão

```text
publicamente, a formulacao por Fin.
```

Motivo: ela corresponde **diretamente** ao domínio da função `step`. O
campo `closed` de `ValidatedTransitionTable` é literalmente o que `step`
consome para construir `⟨t.next[i], t.closed i⟩` — sem lema intermediário,
sem conversão de índice.

As outras duas **só** virarão lemas se a implementação as exigir de fato.
`Nat.decidableBallLT` está disponível no checkout e serviria à segunda
formulação; `Fintype.decidableForallFintype` serve à primeira, e é a que
o probe efetivamente usou.

```text
NAO criar tres predicados publicos concorrentes.
```

## Instância decidível

```lean
instance RawTransitionTable.decidableValid (t : RawTransitionTable) :
    Decidable t.Valid :=
  inferInstanceAs (Decidable (∀ i : Fin t.next.size, t.next[i] < t.next.size))
```

Verificado no probe: `#synth Decidable (RawT.Valid ⟨#[0]⟩)` resolve para
a instância declarada. A rota por `by unfold; infer_instance` é
equivalente; a forma com `inferInstanceAs` foi a testada.

Infraestrutura inferida: `Fintype (Fin n)` e a decidibilidade de `<` em
`Nat`, via `Fintype.decidableForallFintype`. **Nenhum** `Classical.decEq`,
**nenhum** `Classical.choose`, **nenhuma** marca de não-computabilidade.

Achado do probe, digno de registro:

```text
#print axioms validateT   ->   [propext, Quot.sound]
```

A camada de validação, isolada, **não** depende de `Classical.choice`. A
pegada só aparece quando o detector entra, por `Fintype.card`. E, como já
estabelecido em `FOUND-CYCLE-DETECTION-001`, pegada axiomática não é
não-computabilidade.
