---
document_id: PORTFOLIO-REVIEW-CZ-MEAN-ZERO-2026-08-09
reviewed_at: 2026-08-09
conclusion: FOUND-CZ-MEAN-ZERO-001_AUTHORIZED
---

# Revisão de portfólio — fechamento do campo `mean_zero` de `CZKernelClass`

## Achado de pesquisa que fundamenta esta frente

Pesquisa dedicada (agente de pesquisa, sem edição de código, fontes
citadas e verificadas por leitura direta de PDF — Loukas Grafakos,
*Classical Fourier Analysis*, 3ª ed., Springer GTM 249, 2014, §5.1.4 e
§5.2.1-5.2.2) descobriu que a condição `mean_zero` deixada em aberto em
`FOUND-CZ-KERNEL-DEFINITIONS-001` para `K(y):=D(ŷ,e2,e3)/‖y‖³` **não é**
o cálculo analítico difícil que se supunha, mas um fato elementar:

```text
D(θ,e2,e3) = (θ·e3)·det(θ,e2,e3) é uma forma quadrática em θ.
∫_{S²} θᵢθⱼ dσ(θ) = c·δᵢⱼ (isotropia do tensor de segundo momento de
  uma medida de superfície rotacionalmente invariante, c constante).
∴ ∫_{S²} D(θ,e2,e3) dσ(θ) = c · e3·(e2×e3) = c · det(e3,e2,e3) = 0
  (determinante com linha repetida).
```

Verificação própria (não apenas do agente): a álgebra acima foi
re-derivada manualmente nesta revisão e confere.

## O que isso NÃO significa

O próprio relatório de pesquisa é explícito: fechar `mean_zero` desta
forma:
- **NÃO** prova limitação L² do operador (exigiria a maquinaria completa
  de Grafakos Prop. 5.2.3/Cor. 5.2.6 — derivar um multiplicador de
  Fourier a partir do núcleo espacial p.v. — que não existe no Mathlib e
  não é alcançável a partir de `fourierMulL2` já formalizado nesta
  sessão, que toma o símbolo limitado como HIPÓTESE, não o deriva).
- **NÃO** toca o operador não-linear real das eq. 2.1/2.2 (onde
  `e3=ω̂(t,x-y)` varia com `y` — objeto fundamentalmente diferente do
  núcleo de coeficiente congelado já isolado).
- **NÃO** é progresso em NS-GAP-001/004.

## Escopo autorizado

```text
1. Estabelecer que `sphereSurfaceMeasure` (já definida em
   CalderonZygmundKernelDefinitions.lean, pushforward de
   MeasureTheory.Measure.toSphere ao longo da inclusão do subtipo
   esfera) tem tensor de segundo momento isotrópico:
   ∫_{S²} θᵢθⱼ dσ(θ) = c·δᵢⱼ para alguma constante c -- por rotação-
   invariância da medida, OU por qualquer via alternativa genuína
   encontrada em Mathlib (ex. via coordenadas polares e o momento de
   inércia isotrópico da bola unitária, se rotação-invariância direta de
   toSphere não estiver pronta).
2. Usando (1) e det(e3,e2,e3)=0 (linha repetida, já álgebra trivial),
   provar `∫_{S²} D(θ,e2,e3) dσ(θ) = 0` para e2,e3 fixos quaisquer.
3. Instanciar o campo `mean_zero` de `CZKernelClass sphereSurfaceMeasure
   (K e2 e3)` com essa prova, produzindo (junto com `K_homogeneous` e
   `contDiffAt_K`, já provados em FOUND-CZ-KERNEL-DEFINITIONS-001) um
   termo COMPLETO de `CZKernelClass` para o núcleo de coeficiente
   congelado -- o primeiro termo completo desta classe em todo o
   laboratório.
```

Se o passo (1) (isotropia do tensor de segundo momento de
`sphereSurfaceMeasure`) se revelar intratável no tempo disponível --
por exemplo se `MeasureTheory.Measure.toSphere` não tiver nenhum lema de
rotação-invariância utilizável e a rota alternativa via bola unitária
também não fechar -- **isso deve ser registrado como gap nomeado, não
forçado**. O campo `mean_zero` continuaria não instanciado, exatamente
como está hoje, apenas com o motivo preciso documentado.

## Trava

`authorized_action: FORMALIZATION`. Terceira extensão nomeada da
exceção de `DEC-076` (via `DEC-078`, `DEC-080`) -- ainda delimitada,
ainda sem tocar a integral p.v. real nem qualquer limitação L^p.
