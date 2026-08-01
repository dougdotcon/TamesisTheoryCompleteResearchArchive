---
document_id: ENC-ENCODING-LAWS
---

# Leis da codificação

## As duas leis

```lean
decode_encode : ∀ s : S, decode (encode s) = s
encode_decode : ∀ i : Fin n, encode (decode i) = i
```

Juntas dizem que `encode` e `decode` são inversas mútuas — isto é, uma
bijeção entre `S` e `Fin n`, fornecida, não descoberta.

## Qual lei sustenta o quê

```text
decode_encode   sustenta a comutacao de um passo
encode_decode   sustenta a sobrejetividade de encode
```

Esta separação é vinculante. Na prova de `table_step_commutes`, a lei
necessária é **`decode_encode`**:

```text
encodedStep (encode s) = encode (stepS (decode (encode s)))
                       = encode (stepS s)          por decode_encode
```

Usar `encode_decode` ali seria um erro de direção. `STOP-ENC-002` cobre
o caso de as leis serem insuficientes; este documento congela **qual**
lei é usada **onde**.

## Corolários

Resultado mínimo obrigatório:

```lean
theorem CertifiedFiniteEncoding.encode_injective :
    Function.Injective e.encode :=
  Function.LeftInverse.injective e.decode_encode
```

Demonstrado no probe. Termo de uma linha.

Corolário adicional confirmado, mesma origem:

```lean
theorem CertifiedFiniteEncoding.decode_surjective :
    Function.Surjective e.decode :=
  Function.RightInverse.surjective e.decode_encode
```

Corolários **não** congelados nesta frente, por não serem necessários aos
resultados centrais:

```text
decode injetiva
encode sobrejetiva
S equivalente a Fin n como Equiv explicito
```

Ficam disponíveis, e cada um custa uma linha. Não entram na API pública
por princípio de API mínima.

## `encode_injective` é o fecho da soundness

É o último passo do DAG de `analyzeEncodedSystem_sound`: a igualdade em
`Fin n` só vira igualdade em `S` porque `encode` é injetiva. Sem a lei
`decode_encode`, a soundness não termina em `S` — termina em índices, e
`STOP-ENC-018` dispararia.

## Nenhuma igualdade decidível

```text
DecidableEq S nao eh exigida em lugar nenhum.
```

As leis são proposicionais. A execução não compara estados de `S`; ela
compara índices de `Fin n`, cuja decidibilidade já existe.


---

## Revisão — `2066edc`

Confirmado que `decode_encode` é a lei da comutação. Acrescentado pela
revisão: `encode_surjective`, provado por
`Function.RightInverse.surjective` **sem axiomas**, é a consequência que
exprime o contrato de `encode_decode`. Permanece `DEFERRED_OPTIONAL`.
