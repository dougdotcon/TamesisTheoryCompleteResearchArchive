# RH-NOGO-001 — Mapa de rotas de escape

Rotas espectrais que o no-go estreito **não cobre**. A existência dessas
rotas não prova que alguma funcione; ela apenas limita corretamente a
conclusão.

| # | Rota | Por que escapa da Classe W | Exemplo na literatura |
|---|---|---|---|
| 1 | espaços não compactos | W1 exige compacidade; sem ela, Weyl padrão não se aplica e a contagem pode ganhar fatores logarítmicos (regularizações de `H = xp` produzem exatamente `(T/2π)log(T/2π)` na contagem média suavizada) | Berry–Keating 1999 |
| 2 | geometrias singulares | W1 exige suavidade; singularidades alteram a assintótica espectral | — |
| 3 | geometria não comutativa | não há variedade suave subjacente; o "espaço" é o espaço de classes de adeles | Connes 1999 |
| 4 | espectros de absorção | os zeros aparecem como ausências (absorção) num contínuo, não como autovalores discretos de um operador da Classe W | Connes 1999 |
| 5 | ressonâncias | polos da matriz de scattering não são autovalores `L²` | — |
| 6 | operadores não locais | W3 exige operador diferencial (local) | — |
| 7 | ordem variável | W3 exige ordem fixa `m` | — |
| 8 | pseudodiferenciais fora da classe | v1 cobre só diferenciais; ψDOs exóticos (símbolos não clássicos) podem violar W8 | — |
| 9 | regularização dependente da energia | contagem efetiva pode adquirir `log` (cutoffs de Berry–Keating dependem de `T`) | Berry–Keating 1999 |
| 10 | pares / problemas generalizados `Au = λBu` | não é o espectro de um único `P` auto-adjunto da classe | — |
| 11 | zeros como subconjunto do espectro | a exclusão exige espectro positivo **completo** = `{γ_n}`; um espectro maior contendo os zeros não é tocado | — |
| 12 | PT-simétricos sem auto-adjunção convencional | W5 exige auto-adjunção em `L²` padrão | Bender–Brody–Müller 2017 |
| 13 | auto-adjunção adaptada em domínios não padrão | noção de auto-adjunção fora do quadro `L²(M)` compacto | Hedenmalm, preprint 2026 |
| 14 | reescalonamento espectral não trivial | a exclusão compara `λ_n = γ_n` diretamente; `λ_n = f(γ_n)` (ex.: `γ log γ`) muda a contagem e escapa | — |

## Leitura correta do resultado

> Excluímos, no máximo, uma classe convencional delimitada;
> **não excluímos Hilbert–Pólya.**

Qualquer texto futuro que cite RH-NOGO-001 deve reproduzir essa limitação.
