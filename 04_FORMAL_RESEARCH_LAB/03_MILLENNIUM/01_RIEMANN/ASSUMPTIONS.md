# RH-NOGO-001 — Hipóteses

## Hipóteses do enunciado candidato

1. **W1–W8** da Classe W (`OPERATOR_CLASS.md`), com W8 (lei de Weyl com
   expoente `d/m` e constante positiva) **postulada como hipótese** — a
   prova alvo não reprova Weyl, usa-o.
2. **Riemann–von Mangoldt**: `N_ζ(T) = (T/2π)log(T/2π) − T/2π + O(log T)`,
   incondicional (ESTABLISHED; fontes em `BIBLIOGRAPHY_AUDIT.md`).
3. Nada mais. Em particular:

## O que NÃO é assumido

- **RH não é assumida** nem negada; a contagem vale no strip inteiro.
- **GUE / Montgomery–Odlyzko não entram** — nenhuma estatística de
  correlação de zeros é usada, eliminando o risco de circularidade
  registrado em RH-GAP-002 (herdado): não há cancelamento fora da diagonal
  a auditar porque não há fórmula de traço nesta rota.
- **Nenhum dado definido pelos próprios zeros** é usado para construir
  operador algum — este gate não constrói operadores.
- Nenhuma claim histórica do arquivo (Tamesis, TRI, TDTR, Omega, Braid).

## Variantes registradas (CONDITIONAL, fora da v1)

| Variante | Custo |
|---|---|
| `P` apenas limitado inferiormente | redefinir "espectro positivo" com corte; assintótica inalterada |
| `M` com bordo + condições elípticas | hipóteses adicionais de regularidade; Weyl preservado |
| `P` pseudodiferencial clássico elíptico de ordem `m > 0` real | Hörmander 1968 cobre; ampliaria a classe; adiado |

## Fronteira de honestidade

A exclusão só vale para a Classe W. A especificação declara explicitamente
que rotas espectrais fora da classe permanecem intocadas
(`ESCAPE_ROUTES.md`) e que o enunciado tem novidade baixa (GAP-RH-007).
