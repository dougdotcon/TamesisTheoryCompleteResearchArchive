---
document_id: ENC-ITERATION-COMMUTATION
probe_status: PROBE_PROVED
---

# Comutação de iterações

## Enunciado

```lean
theorem table_iterate_commutes (e) (stepS) (k : Nat) (s : S) :
    ((buildTransitionTable e stepS).step)^[k] (e.tableIndex stepS s)
      = e.tableIndex stepS (stepS^[k] s) :=
  ((tableIndex_semiconj e stepS).iterate_right k s).symm
```

**Um termo. Uma linha.** Compilou no probe.

## Rota

```text
tableIndex_semiconj
    -> Function.Semiconj.iterate_right k
        -> aplicacao em s
            -> .symm
```

Nenhuma indução manual. Nenhum `show`. Nenhuma escolha entre
`Function.iterate_succ_apply` e sua variante com apóstrofo.

## Contraste com a frente anterior

`ValidatedTransitionTable.run?_eq_iterate_step` custou:

```text
inducao em k;
quantificador no enunciado, e nao por generalizing;
dois show obrigatorios;
Function.iterate_succ_apply, com a orientacao inversa proibida.
```

Aqui, a mesma classe de resultado custa uma linha, porque a API de
semiconjugação de Mathlib já encapsula a indução. **É proibido reprovar
a identidade de iteração por indução manual** quando a API local
fornece o resultado — o gate é explícito, e o probe confirmou que ela
fornece.

## Orientação de `iterate_right`, auditada

```lean
Function.Semiconj.iterate_right :
  Semiconj f ga gb → ∀ n, Semiconj f ga^[n] gb^[n]
```

`ga` é o sistema tipado, `gb` é o passo da tabela, `f` é `tableIndex`. A
iteração aplica-se aos **dois** lados com o mesmo `n`, que é exatamente
o formato necessário. A alternativa `Function.Semiconj.iterate_left` tem
forma diferente — famílias indexadas `g : ℕ → α → α` — e **não** serve.
