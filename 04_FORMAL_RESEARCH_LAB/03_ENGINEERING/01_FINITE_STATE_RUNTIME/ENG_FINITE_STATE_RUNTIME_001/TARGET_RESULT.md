---
document_id: RT-TARGET-RESULT
---

# Resultado alvo

## O bloqueio

`FOUND-CYCLE-DETECTION-001` é um programa verificado que **não consegue
receber uma entrada**. Ele opera sobre

```text
X : Type*    [Fintype X]    [DecidableEq X]    f : X -> X    x : X
```

todos fixados em **compilação**.

## O alvo

```text
RawTransitionTable        Array Nat, potencialmente invalido
        |
validateTransitionTable   rejeita, nunca corrige
        |
ValidatedTransitionTable  fechamento provado
        |
validateStart             valida a consulta, separadamente
        |
Fin next.size             dominio finito tipado, construido internamente
        |
step                      funcao TOTAL sobre Fin n
        |
detectCycle?              detector ja verificado, sem copia
        |
CycleWitness
        |
detectCycle?_raw_repeat   o certificado, reinterpretado na tabela bruta
```

## O que a frente deve provar

```text
1. validacao correta e completa;
2. validacao do estado inicial correta e completa;
3. step corresponde ao lookup da tabela;
4. iteradas de step correspondem a execucao da tabela;
5. o detector adaptado herda soundness e completeness;
6. o certificado se traduz em repeticao de indices na tabela ORIGINAL;
7. a API dinamica eh correta e completa para entradas validas.
```

## O que a frente **não** deve provar

```text
minimalidade de baseIndex ou de period;
complexidade;
correcao da abstracao de um sistema real em tabela;
enumeracao global de componentes;
totalizacao do detector anterior.
```

## O ganho central

```text
o consumidor dinamico fornece apenas Array Nat e Nat.
```

Nenhuma `Fintype`, nenhuma `DecidableEq`, nenhum `Fin`, nenhuma prova e
nenhuma função Lean são exigidas de quem chama. As estruturas finitas são
construídas **internamente**, a partir do dado.

## O ponto de falha mais perigoso

```text
corrigir um destino invalido silenciosamente.
```

Um `% n` transformaria uma tabela errada em um **sistema diferente**, e o
certificado devolvido seria correto sobre um sistema que o usuário nunca
descreveu. Toda a arquitetura desta frente existe para tornar isso
impossível por construção.
