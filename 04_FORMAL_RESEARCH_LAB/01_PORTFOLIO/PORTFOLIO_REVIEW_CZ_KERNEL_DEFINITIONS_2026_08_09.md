---
document_id: PORTFOLIO-REVIEW-CZ-KERNEL-DEFINITIONS-2026-08-09
reviewed_at: 2026-08-09
conclusion: FOUND-CZ-KERNEL-DEFINITIONS-001_AUTHORIZED
---

# Revisão de portfólio — camada definicional de Calderón-Zygmund

## Achado empírico que delimita esta frente

Busca exaustiva no Mathlib (`05_FORMAL/lean/.lake/packages/mathlib`):
**zero** arquivos para Calderón-Zygmund, integral singular, BMO, função
maximal de Hardy-Littlewood, tipo-fraco, interpolação de Marcinkiewicz,
ou integral de valor principal. Nenhuma dessas ferramentas existe em
nenhum nível.

## Escolha de escopo (decidida pelo usuário)

Diante disso, três escopos possíveis foram apresentados: camada
definicional apenas, fundação completa (função maximal em diante), ou
buscar biblioteca externa. **O usuário escolheu a camada definicional
apenas** — a única compatível com uma única sessão sem comprometer a
pesquisa a um programa de meses/anos sem avaliação explícita a cada
passo.

## O que esta frente formaliza

```text
1. Integral de valor principal LOCAL: p.v. ∫_{B_R(x₀)} f :=
   lim_{ε→0+} ∫_{ε<=|y-x₀|<R} f(y) dy, quando o limite existe.
   (Formulação local, não global -- o comportamento no infinito depende
   de decaimento de ω, fora de escopo aqui.)

2. A classe estrutural de núcleo Calderón-Zygmund em R^3: homogêneo de
   grau -3, suave fora da origem, média zero sobre a esfera unitária
   (condição de cancelamento).

3. Verificação de que a peça de coeficiente congelado do núcleo de
   Constantin-Fefferman -- K(y) := D(ŷ, e2, e3)/|y|³ para e2,e3 fixos,
   usando o D já formalizado em ConstantinFeffermanDepletionKernel.lean
   -- satisfaz homogeneidade de grau -3. A condição de média zero sobre
   a esfera será tentada; se intratável no tempo disponível, ficará
   registrada como gap nomeado, não forçada.
```

## O que esta frente NÃO tenta

```text
NENHUMA limitação L^p do operador
NENHUM teorema de Calderón-Zygmund (decomposição, tipo-fraco, interpolação)
NENHUMA estimativa sobre a integral p.v. real das eq. 2.1/2.2 aplicada
  a um campo de vorticidade genuíno
NENHUM progresso em NS-GAP-001/004
```

## Por que isso ainda vale a pena

Mesmo sem a limitação L^p, ter a integral de valor principal e a classe
de núcleo CZ definidas em Lean é infraestrutura genuína e reutilizável
-- o "vocabulário" sem o qual nenhum enunciado da teoria completa pode
sequer ser escrito. Isso é consistente com o padrão desta sessão
(Sobolev, semigrupo, Duhamel): construir o vocabulário antes da
estimativa, sem fingir que o vocabulário é a estimativa.

## Trava

`authorized_action: FORMALIZATION`. Extensão nomeada da exceção de
`DEC-076` -- ainda delimitada, ainda sem tocar a estimativa real.
