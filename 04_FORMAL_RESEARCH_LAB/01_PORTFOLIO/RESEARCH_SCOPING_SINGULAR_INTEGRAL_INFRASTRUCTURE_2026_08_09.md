---
document_id: RESEARCH-SCOPING-SINGULAR-INTEGRAL-INFRASTRUCTURE-2026-08-09
reviewed_at: 2026-08-09
conclusion: NO_SINGLE_SESSION_MILESTONE_FOUND — SMALLEST_IRREDUCIBLE_UNIT_IDENTIFIED
code_touched: false
governance_touched: false
---

# Pesquisa de escopo — infraestrutura de integral singular/Calderón-Zygmund

Pesquisa dedicada (sem edição de código nem de governança), solicitada
pelo usuário após a terceira checagem de exaustão do dia
(`PORTFOLIO_REVIEW_QUEUE_EXHAUSTED_2026_08_09_EVE.md`), para responder:
existe um primeiro marco realista e limitado (escala comparável às três
frentes fechadas hoje) rumo a limitação L²/L^p do operador
Constantin-Fefferman de coeficiente congelado, ou o investimento exige
um programa multi-sessão?

## Inventário exaustivo do Mathlib (re-verificado, não assumido)

Busca sistemática em `05_FORMAL/lean/.lake/packages/mathlib/Mathlib`
(8268 arquivos `.lean`) confirmou, de forma independente da pesquisa
anterior: decomposição de Calderón-Zygmund, integral singular (nomeada),
função maximal de Hardy-Littlewood, interpolação de Marcinkiewicz, BMO/
John-Nirenberg, lema de Cotlar-Stein, distribuições de valor principal,
harmônicos esféricos/Bochner-Hecke, "transformada de Riesz" (nomeada), e
cubos diádicos/decomposição de Whitney — **todos ausentes**, zero
resultados de grep.

Infraestrutura ADJACENTE genuína que EXISTE (nuance honesta, não
capturada pela pesquisa anterior): coordenadas polares generalizadas em
dimensão `n` (`HaarToSphere.lean`, já usada pelo laboratório), lemas de
cobertura de Vitali/Besicovitch, transformada de Fourier da gaussiana,
fórmula integral da função Gamma, fórmula layer-cake, desigualdade de
Markov/Chebyshev em `Lp`, e o teorema das três linhas de Hadamard
(`Complex/Hadamard.lean` — o motor complexo-analítico por trás de
Riesz-Thorin, embora Riesz-Thorin em si não esteja montado).

## Três rotas candidatas avaliadas, nenhuma de escala de uma sessão

```text
(a) Formalizar a Proposição 5.2.3 de Grafakos (fórmula da transformada
    de Fourier de um núcleo p.v. homogêneo de média zero) sozinha —
    lida diretamente da fonte primária (PDF buscado e OCR'd de novo
    nesta pesquisa, não confiado da pesquisa anterior). Trava
    irredutível: o Lema 5.2.5 de Grafakos exige uma família de
    integrais oscilatórias tipo Dirichlet (∫sin(r)/r dr → π/2), que o
    Mathlib NÃO tem infraestrutura alguma (zero Fresnel/Dirichlet/
    integral oscilatória imprópria). Custo: high.

(b) Computar o multiplicador em forma fechada especificamente para o
    núcleo D(ŷ,e2,e3)/‖y‖³ deste laboratório (aproveitando que
    D(θ,e2,e3) é harmônico esférico de grau 2, verificado por cálculo
    direto: seu traço é exatamente tripleProduct_self_left, já provado
    = 0). Mesma trava irredutível do Lema 5.2.5 -- economia modesta,
    não de ordem de grandeza. Custo: high. Constante fechada citável
    NÃO verificada nesta pesquisa -- reportado honestamente como questão
    aberta, não afirmado.

(c) Decomposição de Calderón-Zygmund + interpolação de Marcinkiewicz
    (rota real-variável, evita multiplicadores de Fourier). Trava
    irredutível: API de cubos diádicos inexistente no Mathlib, mais
    função maximal e interpolação de Marcinkiewicz, ambas ausentes.
    Mais infraestrutura nova que (a)/(b), não menos. Custo: very_high.
```

Rotas alternativas descartadas com justificativa (Cotlar-Stein reduz à
mesma lacuna diádica de (c); nenhum atalho tipo Schur-test existe pois
`‖K‖²` diverge perto da origem; restringir-se ao operador truncado já
formalizado (`HasLocalPV`) não avançaria a afirmação de limitação, seria
apenas reformulação).

## Recomendação

Nenhuma rota fecha em uma única sessão. A menor unidade irredutível de
trabalho identificada: **formalizar o lema de integral oscilatória tipo
Dirichlet (Lema 5.2.5 de Grafakos, ou equivalente suficiente)** como item
autônomo de fundamentos -- reutilizável para qualquer núcleo de média
zero futuro, não apenas este. Estimativa honesta: `moderate` a `high`
por si só. Só depois disso faria sentido revisitar a Proposição 5.2.3 +
Corolário 5.2.6 para o núcleo `D` como sessão separada de custo `high`.

**Nenhuma formalização foi tentada nesta pesquisa.** Nenhum arquivo
`.lean` ou de governança foi tocado.

## Fontes citadas (verificadas por leitura direta, não confiadas de
pesquisa anterior)

- Loukas Grafakos, *Classical Fourier Analysis*, 3ª ed., Springer GTM
  249, 2014, Cap. 5 "Singular Integrals of Convolution Type", §5.1.4
  (p. 325), §5.2.1-5.2.3 (pp. 333-338, Prop. 5.2.3 e Lema 5.2.5 lidos
  literalmente), §5.3.1 (Teorema 5.3.1, p. 355).
- Mathlib (árvore vendorizada, arquivos citados inline no relatório
  completo do agente de pesquisa).
