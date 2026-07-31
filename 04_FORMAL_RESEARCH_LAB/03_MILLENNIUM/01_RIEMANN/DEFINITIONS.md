# RH-NOGO-001 — Definições

Respostas às questões obrigatórias da especificação (seção 4 do gate).

1. **"Espectro positivo completo"** — o multiconjunto dos autovalores
   estritamente positivos de `P̄`, cada um com sua multiplicidade
   geométrica (= algébrica, por auto-adjunção). "Completo" significa que a
   coincidência exigida é de multiconjuntos inteiros, não de subconjuntos:
   um operador cujo espectro *contém* os `γ_n` mais outra coisa está fora
   do alvo (ver `ESCAPE_ROUTES.md`, rota 11).
2. **Zeros com multiplicidade** — sim. `N_ζ(T)` conta zeros
   `ρ = β + iγ` com `0 < β < 1`, `0 < γ ≤ T`, **com multiplicidade**.
   A simplicidade dos zeros é conjectural e não é usada.
3. **Apenas ordenadas positivas** — sim. Pela simetria funcional os zeros
   vêm em pares conjugados; a escolha `γ > 0` é canônica e casa com um
   espectro positivo.
4. **Dependência da RH** — **nenhuma**. A fórmula de Riemann–von Mangoldt
   conta zeros no strip crítico `0 < β < 1` e vale incondicionalmente.
   As ordenadas `γ_n` são definidas sem assumir `β = 1/2`. (Se a RH for
   falsa, ordenadas de zeros fora da linha entram na mesma contagem — a
   assintótica não muda.)
5. **Positivo vs limitado inferiormente** — a v1 exige positivo (W6).
   Limitado inferiormente basta para a assintótica (um deslocamento
   espectral finito não altera `N_P(T)/T^α`), mas exigiria emparelhar
   "espectro positivo" com um corte; registrado como extensão CONDITIONAL
   em `ASSUMPTIONS.md`.
6. **Bordo** — não na v1 (W1: fechada). Condições elípticas de bordo
   (Dirichlet/Neumann) preservam a lei de Weyl, mas adicionam hipóteses de
   regularidade; extensão CONDITIONAL, fora do alvo v1.
7. **Fibrados vetoriais** — sim, permitidos (W2); o posto entra em `C_P`.
8. **Classe exata com lei de Weyl** — Classe W (`OPERATOR_CLASS.md`), com
   W8 postulada e fonte primária da versão exata auditada em GAP-RH-002.
   Hörmander 1968 cobre inclusive pseudodiferenciais elípticos de ordem
   positiva com resto `O(Λ^{(d−1)/m})`; a v1 restringe-se a operadores
   diferenciais por prudência de escopo.
9. **Termo assintótico suficiente** — somente os termos dominantes:
   `N_ζ(T)/(T log T) → 1/(2π)` e `N_P(T)/T^α → C_P > 0`. O resto
   `O(log T)`, o termo `7/8` e `S(T)` são irrelevantes para a contradição.
10. **Igualdade excluída** — os três níveis de `OPERATOR_CLASS.md`:
    igualdade exata de multiconjuntos, discrepância limitada e equivalência
    assintótica de densidade. A prova alvo ataca o nível mais forte (iii),
    que implica os demais.
11. **Fora do escopo geométrico** — não compactos, singulares, não
    comutativos: ver `EXCLUSIONS.md`.
12. **Fora do escopo operatorial** — pseudodiferenciais gerais, ordem
    variável, não locais: ver `EXCLUSIONS.md`.
13. **Fora do escopo espectral** — espectros de absorção, ressonâncias,
    espectros embutidos/contínuos: ver `EXCLUSIONS.md`.
14. **Exclui Hilbert–Pólya em geral?** — **Não.** A resposta esperada e
    obtida é não: a conjectura de Hilbert–Pólya não especifica classe de
    operador, e todas as rotas incluídas na amostra bibliográfica
    catalogada nesta sessão ficam fora da Classe W
    (`ESCAPE_ROUTES.md`).

## Objetos técnicos

| Símbolo | Definição |
|---|---|
| `ζ` | função zeta de Riemann, continuação meromorfa da série de Dirichlet |
| `γ_n` | ordenadas positivas dos zeros não triviais, em ordem crescente, com multiplicidade |
| `N_ζ(T)` | `#{n : γ_n ≤ T}` (com multiplicidade) |
| `L²(M, E)` | espaço de Hilbert das seções quadrado-integráveis |
| `P̄` | extensão auto-adjunta (única, por W5) de `P` |
| `N_P(Λ)` | `#{j : λ_j ≤ Λ}`, autovalores de `P̄` com multiplicidade |
| `α` | `d/m > 0` |

Nenhum objeto Tamesis, Omega ou Braid aparece nesta especificação.
