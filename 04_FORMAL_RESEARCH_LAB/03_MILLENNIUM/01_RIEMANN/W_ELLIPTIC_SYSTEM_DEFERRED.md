---
class_id: W-ELLIPTIC-SYSTEM
status: DEFERRED_NOT_ACTIVE
active: false
---

# W-ELLIPTIC-SYSTEM — classe adiada (não ativa)

Classe reservada para operadores agindo em seções de fibrados vetoriais ou
sistemas. **Não está ativa** e não participa de nenhuma obrigação ou
enunciado deste laboratório.

## Registro das razões

```text
A formula de Ivrii para a constante principal utiliza a contagem
dos autovalores do simbolo principal e incorpora multiplicidades.

A identidade de traco matricial/fibrada necessaria para a etapa
local-global ainda nao foi auditada suficientemente.

Portanto, sistemas e fibrados nao pertencem a
W-ELLIPTIC-SCALAR v2.
```

## Evidência

**Constante.** Ivrii 2016, eq. (3.1.3):

```text
κ₀ = (2π)^{−d} ∬ n(x,ξ) dx dξ
```

com `n(x,ξ)` = número de autovalores de `A⁰(x,ξ)` em `(0,1)`. No caso
escalar `n` é a indicadora de `{p < 1}` e a fórmula colapsa no volume; no
caso de posto `r > 1` ela conta autovalores **com multiplicidade** e **não**
é um volume.

Regra: **não usar a fórmula escalar para sistemas**.

**Identidade de traço.** A etapa GWB-004 usa Ivrii (3.1.11)
`N⁻(λ) = ∫ e(x,x,λ) dx`, que é **escalar**. A versão fibrada exigiria
`N(λ) = ∫_M tr_E e(x,x,λ) dx` com o traço fibra a fibra, e essa forma
**não foi lida em nenhuma fonte obtida**.

**Cobertura de Hörmander.** Hörmander 1968, p. 216: os métodos cobrem
sistemas *"for which the eigenvalues of `p(x,ξ)` are **distinct**"*; para
multiplicidade, *"we have **no information** beyond"* Agmon–Kannai e
Hörmander [8]. Portanto nem a fonte original cobre fibrados gerais.

## Estado dos gaps

`GAP-RH-009` permanece **OPEN**. Este gate **não o fecha**.

## Condições para ativação futura

1. Fonte auditada que enuncie a identidade `N(λ) = ∫_M tr_E e(x,x,λ) dx`
   para fibrados hermitianos sobre variedade compacta.
2. Fonte auditada para a lei global com a constante de Ivrii no caso
   fibrado, sobre variedade compacta **sem bordo**.
3. Decisão sobre a hipótese de autovalores distintos do símbolo principal:
   manter (estreitando) ou obter fonte que a dispense.

Até lá, qualquer enunciado deste laboratório que mencione operadores é
**escalar**.
