# RH-NOGO-001 — Matriz de claims

## ESTABLISHED (externos, com fonte)

| Item | Fonte |
|---|---|
| fórmula de contagem de Riemann–von Mangoldt (incondicional) | VONMANGOLDT-1905 |
| lei de Weyl para a classe elíptica auditada, com resto | HORMANDER-1968 (versão exata: GAP-RH-002) |
| comparações assintóticas elementares (`log = o(potência)`, divergência de `log`) | análise real padrão; Mathlib (`isLittleO_log_rpow_atTop`, `tendsto_log_atTop`) |
| RH permanece sem solução aceita | BOMBIERI-CLAY |

## CONDITIONAL (exigem hipóteses adicionais antes de uso)

| Item | Condição pendente |
|---|---|
| extensão do no-go a variedades com bordo | condições elípticas de bordo auditadas |
| extensão a pseudodiferenciais clássicos de ordem real `m > 0` | transcrição exata de HORMANDER-1968 |
| extensão a operadores apenas limitados inferiormente | redefinição de "espectro positivo" com corte |

## PROPOSED (formulação deste gate, sem prova)

| Item | Registro |
|---|---|
| RH-NOGO-001: exclusão da Classe W nos três níveis (igualdade exata, discrepância limitada, densidade assintótica) | `TARGET_RESULT.md`, `OPERATOR_CLASS.md` |
| ASYM-NOGO-001: incompatibilidade `T log T` vs `C·T^α` | `ASYMPTOTIC_CORE.md`; assinatura em `SignatureProbe.lean` |

## OUT_OF_SCOPE (não avaliados, não refutados, não usados)

- Hilbert–Pólya em geral;
- Connes (absorção, geometria não comutativa);
- Berry–Keating (`H = xp`, regularizações);
- Bender–Brody–Müller (PT, não hermitiano);
- Hedenmalm 2026 (preprint; CLAIMS_REQUIRING_INDEPENDENT_AUDIT);
- geometrias não compactas ou singulares; operadores não convencionais;
- quaisquer supostas provas recentes da RH;
- claims históricas do arquivo Tamesis sobre Riemann.

## Regra de citação

Nenhum item PROPOSED pode ser citado como resultado. Nenhum item
OUT_OF_SCOPE pode ser citado como refutado. A frase de escopo obrigatória
está em `ESCAPE_ROUTES.md`.
