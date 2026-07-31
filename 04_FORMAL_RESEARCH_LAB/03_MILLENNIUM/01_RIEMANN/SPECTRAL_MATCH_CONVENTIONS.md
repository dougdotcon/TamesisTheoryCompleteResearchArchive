---
status: SPECIFIED_NOT_PROVED
---

# Convenções de identificação espectro ↔ zeros

## A implicação pretendida

```text
Se o multiconjunto dos autovalores positivos de P coincide
exatamente com o multiconjunto das ordenadas positivas dos zeros,
incluindo multiplicidades, entao E0 vale e, portanto, E2 devera valer.
```

**A implicação só vale sob as obrigações abaixo.** Nenhuma foi provada.

## Obrigações

```yaml
- id: SMC-001
  item: "desigualdade estrita versus nao estrita (< T versus <= T)"
  N_P: "CORIASCO-DOLL-2020 eq.(1) usa ESTRITA: N(lambda) = #{j : lambda_j < lambda}"
  N_zeta: "definicao moderna usa 0 < Im(rho) <= T"
  status: UNRESOLVED_CONVENTION_MISMATCH
  note: >
    As duas contagens diferem no maximo pela multiplicidade dos elementos
    exatamente em T. Como consequencia, uma coincidencia de multiconjuntos
    daria E0 apenas fora de um conjunto discreto de T. Isso ainda implica
    E2, mas o argumento precisa ser escrito.

- id: SMC-002
  item: "zeros/autovalores exatamente no limite"
  detalhe: >
    von Mangoldt 1905 p.2 evita o problema escolhendo T tal que nenhuma
    ordenada seja igual a T. A definicao moderna nao faz essa escolha.
  status: UNRESOLVED_CONVENTION_MISMATCH
  note: "reconciliacao elementar, NAO escrita; ver RVM_LIMIT_BRIDGE.md"

- id: SMC-003
  item: "multiplicidade"
  N_P: "autovalores contados com multiplicidade (finita, por GWB-001)"
  N_zeta: "zeros contados com multiplicidade (von Mangoldt p.2, literal)"
  status: COMPATIBLE
  note: "as duas convencoes coincidem; nenhuma hipotese de simplicidade dos zeros eh usada"

- id: SMC-004
  item: "valores positivos"
  N_P: "espectro de P contido em (0, +infinito) por positividade da classe"
  N_zeta: "ordenadas POSITIVAS; os zeros vem em pares conjugados"
  status: COMPATIBLE
  note: "a escolha de ordenadas positivas eh canonica e casa com espectro positivo"

- id: SMC-005
  item: "possiveis deslocamentos"
  detalhe: "lambda_j = gamma_j + a para constante a"
  status: ABSORVED_BY_E2
  note: >
    Um deslocamento constante altera a contagem por O(1) em T, que eh
    o(T log T). Portanto E2 continua valendo e o no-go continua excluindo.
    Esta eh uma das vantagens de usar E2 em vez de igualdade exata.

- id: SMC-006
  item: "possiveis autovalores extras"
  detalhe: "Spec+(P) contem propriamente {gamma_n}"
  status: OUT_OF_SCOPE
  note: >
    Se P tem autovalores alem dos gamma_n, N_P - N_zeta pode NAO ser
    o(T log T), e o enunciado nada afirma. Rota de escape 11 de
    ESCAPE_ROUTES.md permanece aberta.

- id: SMC-007
  item: "normalizacao da variavel espectral"
  detalhe: >
    O enunciado compara N_P e N_zeta na MESMA variavel T. Isso pressupoe
    que os autovalores sao comparados diretamente as ordenadas, sem
    reescala.
  status: EXPLICIT_ASSUMPTION
  note: >
    Se lambda_j = f(gamma_j) com f nao linear (por exemplo f(x) = x log x),
    a contagem muda e o enunciado nao se aplica. Rota de escape 14 de
    ESCAPE_ROUTES.md permanece aberta.
```

## Não são automaticamente equivalentes

Registro literal exigido pelo gate. As seguintes noções **não** são tratadas
como equivalentes em nenhum artefato deste laboratório:

```text
espectro completo;
subconjunto espectral;
espectro apos transformacao nao linear;
ressonancias;
espectro de absorcao;
zeros apos reescala dependente da energia.
```

Cada uma corresponde a uma rota de escape já mapeada em
`ESCAPE_ROUTES.md` (rotas 4, 5, 11, 14) e permanece **fora** do alcance do
enunciado estreito.

## Direção da implicação

```text
igualdade espectral exata  ⟹  E0  ⟹  E2      (sob SMC-001..004)
E2                         ⟹  igualdade espectral     ✗ FALSO
```

A segunda seta é **falsa** e nunca deve ser usada. Duas funções de contagem
podem satisfazer E2 com multiconjuntos espectrais bastante diferentes.
