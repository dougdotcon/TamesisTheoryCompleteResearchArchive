---
document_id: ENC-ENCODED-STEP
---

# Passo codificado

```lean
def CertifiedFiniteEncoding.encodedStep
    (e : CertifiedFiniteEncoding S n) (stepS : S → S) : Fin n → Fin n :=
  fun i => e.encode (stepS (e.decode i))
```

Uma linha, e é onde o sistema tipado vira sistema sobre índices.

## Propriedades congeladas

```text
computavel                    sim
usa escolha                   nao
usa Fintype S                 nao
usa DecidableEq S             nao
usa fallback                  nao
usa modulo                    nao
altera indices                nao
total por construcao          sim, o codominio eh Fin n
```

A totalidade é gratuita: `encode` devolve `Fin n`, logo `encodedStep`
devolve `Fin n`. Não existe caso de erro, não existe `Option`, não existe
correção silenciosa — o limite vem do **tipo**, e não de uma verificação.

## Visibilidade

```yaml
declaration: CertifiedFiniteEncoding.encodedStep
category: PUBLIC_EXECUTABLE_CORE
justification: >
  aparece no enunciado de buildTransitionTable_getElem, que eh publico;
  torna-lo privado obrigaria a expor o corpo do Array.ofFn no enunciado.
```

Foi avaliado torná-lo `INTERNAL_HELPER`, como o gate pede. A conclusão é
que ele **precisa** ser público — mas apenas por isso, e o documento
registra a razão para que a revisão possa contestá-la.
