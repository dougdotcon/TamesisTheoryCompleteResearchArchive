---
document_id: FCD-TARGET-RESULT
---

# Resultado alvo

## Dados centrais

```text
X  : tipo finito
f  : X -> X
x0 : X
```

## Certificado

```text
mu : indice-base de uma colisao certificada
lam : periodo positivo testemunhado
```

## Contrato

```text
mu < card X
0 < lam
mu + lam <= card X
f^[mu + lam] x0 = f^[mu] x0
```

Estas são **exatamente** as quatro conclusões de
`FiniteDynamics.exists_bounded_iterate_collision`, já `VERIFIED`. A
especificação foi desenhada para que o contrato do certificado e a
conclusão do teorema anterior **coincidam termo a termo** — é isso que
torna a completude uma reutilização e não uma nova prova.

## O que a primeira versão deve provar

```text
1. o algoritmo termina;
2. se retorna um certificado, o certificado eh correto;
3. para todo tipo finito e estado inicial, algum certificado eh retornado;
4. o certificado produz um ponto periodico;
5. a repeticao se propaga para toda a cauda posterior.
```

## O que a primeira versão **não** deve provar

```text
mu minimo;
lam minimo;
complexidade assintotica otima;
memoria constante;
equivalencia operacional com Floyd;
enumeracao de toda a bacia;
enumeracao de todos os componentes;
lista ordenada do ciclo;
representante canonico do ciclo.
```

## Relação com o resultado anterior

`FOUND-FUNCTIONAL-GRAPH-001` provou que o ciclo **existe**. Esta frente
entrega um **programa** que o encontra e devolve um certificado
verificável. A diferença não é matemática — é de natureza: uma prova de
existência não é um valor calculado.
