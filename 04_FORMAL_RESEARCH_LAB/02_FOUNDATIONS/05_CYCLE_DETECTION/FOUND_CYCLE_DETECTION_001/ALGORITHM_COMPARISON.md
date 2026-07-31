---
document_id: FCD-ALGORITHM-COMPARISON
---

# Comparação de algoritmos

```yaml
Floyd:
  status: DEFERRED_OPTIMIZATION
  reason: >
    Requer invariantes e prova de terminacao mais complexos.
    Nao eh necessario para demonstrar a primeira extracao
    executavel e certificada.

VisitedTable:
  status: DEFERRED_REFERENCE_IMPLEMENTATION
  reason: >
    Pode melhorar eficiencia e produzir diretamente o primeiro
    indice repetido, mas exige estrutura de armazenamento e
    invariantes adicionais.

Brent:
  status: DEFERRED_OPTIMIZATION
  reason: >
    Invariantes de blocos e duplicacao de potencia tornam a
    primeira formalizacao desnecessariamente arriscada.
```

**Nenhum dos três será implementado neste ciclo.**

## Quadro

| | busca certificada | tabela visitada | Floyd | Brent |
|---|---|---|---|---|
| terminação | estrutural, sem prova | estrutural com acumulador | `fuel` ou recursão bem fundada | dobramento de blocos |
| memória | O(1) além da lista de candidatos | O(card X) | O(1) | O(1) |
| avaliações de `f` | muitas — recomputa iteradas | O(card X) | poucas | menos que Floyd em vários casos |
| invariantes de prova | nenhum além do predicado | acumulador e primeiro repetido | duas velocidades, colisão→entrada | blocos e potências |
| produz certificado | **sim, diretamente** | sim | sim, após três fases | sim |
| dá `μ` mínimo | não provado | naturalmente | naturalmente | naturalmente |
| risco formal da v1 | **mínimo** | médio | alto | alto |

A escolha da v1 otimiza **risco formal**, não desempenho. Isso está
registrado explicitamente para que ninguém leia a seleção como uma
afirmação de superioridade algorítmica.

## Por que a tabela visitada não é a v1

Ela seria a escolha natural se o objetivo fosse eficiência com prova
simples. Mas ela **produz** o primeiro índice repetido, e isso empurra
para dentro da v1 a tentação de afirmar minimalidade — que não está
autorizada. A busca certificada é honesta por construção: ela devolve *um*
certificado, e a especificação nunca sugere que seja *o* certificado.

## Caminho futuro

```text
v1  busca certificada        baseline executavel e completo
v2  Floyd ou tabela visitada otimizacao, com equivalencia provada
    contra o baseline da v1
```

A v1 se torna o **oráculo** contra o qual as versões otimizadas serão
comparadas. Esse é o segundo motivo, além do risco, para começar por ela.
