---
document_id: PORTFOLIO-REVIEW-DIRICHLET-OSCILLATORY-INTEGRAL-2026-08-09
reviewed_at: 2026-08-09
conclusion: FOUND-DIRICHLET-OSCILLATORY-INTEGRAL-001_AUTHORIZED
---

# Revisão de portfólio — lema de integral oscilatória tipo Dirichlet

## Base para esta frente

`RESEARCH_SCOPING_SINGULAR_INTEGRAL_INFRASTRUCTURE_2026_08_09.md`
(pesquisa dedicada, sem edição de código, citação re-verificada por
leitura direta do PDF de Grafakos) identificou que TODA rota rumo a
limitação L²/L^p do núcleo Constantin-Fefferman de coeficiente
congelado exige, como peça irredutível, um fato clássico de análise
real que o Mathlib não tem infraestrutura alguma: uma família de
limites de integrais oscilatórias tipo

```text
lim_{ε→0, N→∞} ∫_ε^N (cos(r·a) − cos(r))/r dr = log(1/|a|)   (a ≠ 0 real)
```

(Grafakos, *Classical Fourier Analysis*, 3ª ed., Springer GTM 249, 2014,
Lema 5.2.5, p. 336-337), que por sua vez se apoia no valor clássico da
integral de Dirichlet `∫₀^∞ sin(r)/r dr = π/2`. O Mathlib não tem
Fresnel, Dirichlet, nem infraestrutura de integral oscilatória imprópria
alguma (verificado por busca exaustiva na pesquisa anterior).

## Escopo autorizado

```text
1. Formalizar o valor da integral de Dirichlet ∫₀^∞ sin(r)/r dr = π/2
   (ou o limite impróprio equivalente, conforme a formulação mais
   tratável no Mathlib -- via truque de Feynman/parâmetro de
   convergência, ou qualquer rota genuína encontrada).
2. Formalizar o(s) limite(s) do Lema 5.2.5 de Grafakos (a forma exata
   -- ler a Proposição diretamente da fonte primária antes de comprometer
   o enunciado Lean, não assumir a forma acima sem confirmar).
3. Publicar como item de FUNDAMENTOS standalone (02_FOUNDATIONS/), sem
   qualquer tentativa de conectar a distribuições de valor principal,
   à Proposição 5.2.3, ao multiplicador de Fourier, ou ao núcleo D
   deste laboratório -- isso é trabalho de uma frente FUTURA e separada,
   explicitamente fora de escopo aqui.
```

Item explicitamente reutilizável além desta linha -- não é
Navier-Stokes-específico, por isso vive em `02_FOUNDATIONS/`, não em
`03_MILLENNIUM/`.

## O que isso NÃO significa

```text
NÃO prova a Proposição 5.2.3 de Grafakos (a fórmula da transformada)
NÃO prova limitação de multiplicador algum
NÃO conecta a CZKernelClass, ao núcleo D, ou a fourierMulL2
NÃO é progresso em NS-GAP-001/004
NÃO afirma que Navier-Stokes ficou alcançável
```

## Trava

`authorized_action: FORMALIZATION`. Frente nova, independente da cadeia
Constantin-Fefferman/Calderón-Zygmund já fechada -- escolhida pelo
usuário ("continue") após apresentação explícita dos dois caminhos
possíveis (investir nesta infraestrutura vs. parar na fronteira atual).
