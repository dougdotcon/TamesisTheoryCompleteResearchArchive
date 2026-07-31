---
statement_id: NARROW-SPECTRAL-NOGO-SCALAR
status: CANDIDATE_NOT_PROVED
---

# NARROW-SPECTRAL-NOGO-SCALAR — enunciado candidato

**Não provado.** Enunciado registrado para especificar o alvo.

## Hipóteses futuras

```text
A. P eh um operador realizado que satisfaz individualmente todas as
   hipoteses de W-ELLIPTIC-SCALAR.

B. GLOBAL-WEYL-BRIDGE-SCALAR fornece:
   N_P(T) / T^(d/m) -> C_P > 0.

C. RVM-LIMIT fornece:
   N_zeta(T) / (T log T) -> 1/(2*pi).

D. A relacao entre as contagens satisfaz E2:
   N_P(T) - N_zeta(T) = o(T log T).

E. COUNTING-LAW-BRIDGE fornece:
   N_P(T) / (T log T) -> 1/(2*pi).

F. ASYM-NOGO-001 produz contradicao,
   com N := N_P, alpha := d/m, c := 1/(2*pi), C := C_P.
```

## Conclusão candidata

```text
Nenhum operador realizado P pertencente a W-ELLIPTIC-SCALAR
pode possuir uma funcao de contagem espectral cuja diferenca
para N_zeta seja o(T log T).
```

Equivalentemente, na forma quantificada correta:

> Para todo operador realizado `P` que satisfaça individualmente as
> hipóteses de `W-ELLIPTIC-SCALAR`, a diferença `N_P(T) − N_ζ(T)` **não** é
> `o(T log T)`.

## Forma de quantificação — verificação

| Correto | Proibido |
|---|---|
| „para todo operador **realizado** `P` que satisfaça individualmente as hipóteses" | „para todas as realizações auto-adjuntas de uma expressão formal" |

O objeto quantificado é a **realização** `P`, não uma expressão diferencial
abstrata com todas as suas extensões possíveis. Ver
`W_ELLIPTIC_SCALAR_V2.md`, seção "Forma de quantificação".

## O que a conclusão NÃO diz

```text
NAO diz que Hilbert-Polya foi excluido.
NAO diz nada sobre operadores fora de W-ELLIPTIC-SCALAR.
NAO cobre sistemas, fibrados nem problemas de bordo.
NAO cobre espacos nao compactos, geometrias singulares ou nao comutativas.
NAO cobre espectros de absorcao, ressonancias ou espectro continuo.
NAO cobre espectros nos quais os zeros formam apenas um subconjunto.
NAO cobre reescalas nao lineares da variavel espectral.
NAO diz nada sobre a verdade ou falsidade da Hipotese de Riemann.
```

A expressão **"nenhum operador de Hilbert–Pólya"** é proibida em qualquer
redação deste resultado. As 14 rotas de escape de `ESCAPE_ROUTES.md`
continuam intocadas, e o estreitamento desta v2 (sem bordo, escalar)
**acrescenta** duas exclusões àquela lista.

## Força do resultado, honestamente medida

O que este enunciado ganha em relação à igualdade espectral exata: ele
exclui **qualquer** `P` da classe cuja contagem difira da dos zeros por
termo subdominante — inclusive modelos aproximados, deslocados por `O(1)`,
ou assintoticamente equivalentes em razão. É um alvo estreito **e** mais
robusto.

O que ele continua não sendo: um resultado sobre a Hipótese de Riemann, ou
sobre a existência de operadores espectrais em geral.

## Estado

```text
NAO PROVADO.
NAO FORMALIZADO.
ASYM-NOGO-001 NAO APLICADO.
```
