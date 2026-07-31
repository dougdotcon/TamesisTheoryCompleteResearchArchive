---
document_id: FCD-ALGORITHM-SELECTION
primary_algorithm: BOUNDED_CERTIFICATE_SEARCH
frozen: true
---

# Seleção do algoritmo

## Decisão

```yaml
primary_algorithm: BOUNDED_CERTIFICATE_SEARCH
future_optimization: FLOYD
reference_alternative: VISITED_TABLE
deferred_algorithm: BRENT
```

**Congelado para a primeira versão.**

## Descrição

> Enumerar finitamente todos os pares candidatos `(μ, λ)` dentro das cotas
> já provadas e retornar o primeiro par que satisfaça a igualdade de
> iterações.

## Motivo da mudança

Floyd foi a recomendação **preliminar** do portfólio, e o gate de seleção
registrou explicitamente que a escolha não estava congelada e caberia à
especificação. A busca limitada por certificado foi selecionada porque:

```text
- reutiliza diretamente exists_bounded_iterate_collision;
- a terminacao eh estrutural e imediata;
- nao exige invariantes de tartaruga e lebre;
- nao repete a casa dos pombos;
- nao exige memoria ou estado mutavel complexo;
- produz um certificado explicito;
- permite uma primeira extracao executavel;
- reduz o risco formal da primeira versao.
```

O argumento decisivo é o primeiro. O contrato do certificado é
**literalmente** a conclusão de `exists_bounded_iterate_collision`: mesmas
quatro propriedades, mesma ordem, mesmas cotas. A completude deixa de ser
uma prova nova e passa a ser um transporte.

## O que **não** está sendo afirmado

```text
NAO se afirma que a busca limitada eh superior assintoticamente.
```

Ela provavelmente **não** é: avalia `Function.iterate` repetidamente para
vários pares, enquanto Floyd usa memória constante e um número de
avaliações muito menor. Ver `ALGORITHM_COMPARISON.md`.

```text
Floyd continua candidato a uma otimizacao posterior, depois do
fechamento do baseline executavel.
```

## Separação de etapas

```text
v1: detector simples, executavel e formalmente completo
v2: otimizacao de desempenho com Floyd ou Brent
```

A primeira vitória é ter um programa verificado funcionando. A otimização
vem depois, sem contaminar a prova básica.
