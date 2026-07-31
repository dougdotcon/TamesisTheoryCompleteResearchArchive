---
document_id: FSG2-REUSE-MATRIX
work_item_id: FOUND-SEMIGROUP-002
status: ASSESSMENT_ONLY
integrations_created: 0
---

# FOUND-SEMIGROUP-002 — Matriz de reutilização

Avaliação apenas. **Nenhuma integração concreta foi criada neste gate.**

Classificações: `DIRECT_REUSE`, `REQUIRES_ADAPTER`, `CONCEPTUAL_ONLY`,
`OUT_OF_SCOPE`.

```yaml
- domain: maquinas de estados finitos (FSM)
  classification: REQUIRES_ADAPTER
  applicable_api: [exists_eventual_period, Reachable, reachable_iff_mem_orbit]
  adapter_needed: >
    Uma FSM tem alfabeto de entrada; a transicao eh
    delta : S -> A -> S, nao S -> S. Fixar uma letra da uma funcao S -> S
    (Camada C); o monoide livre sobre A agindo por delta* da a Camada A.
    Nenhuma das duas construcoes existe nesta frente.

- domain: automatos deterministicos (DFA)
  classification: REQUIRES_ADAPTER
  applicable_api: [exists_eventual_period, monoid_element_eventually_periodic]
  adapter_needed: >
    Mesmo adaptador da FSM. Para uma palavra periodica w repetida, a
    iteracao de delta_w eh exatamente monoid_element_eventually_periodic.
    Mathlib ja tem DFA (Mathlib/Computability/DFA.lean) e usa o mesmo
    pigeonhole; uma ponte seria trabalho proprio.

- domain: fluxos finitos
  classification: CONCEPTUAL_ONLY
  note: >
    "Fluxo" costuma pressupor tempo continuo. Mathlib/Dynamics/Flow.lean
    trata acao de monoide topologico. Sem topologia, so resta a analogia.

- domain: maquinas de estado de software
  classification: REQUIRES_ADAPTER
  applicable_api: [exists_eventual_period, Reachable]
  adapter_needed: >
    Exige modelar o espaco de estados como Fintype, o que raramente eh
    verdade em software real (estados costumam carregar dados nao
    limitados). Aplicavel apenas ao esqueleto de controle.

- domain: transicoes de parsers
  classification: REQUIRES_ADAPTER
  applicable_api: [exists_eventual_period]
  adapter_needed: >
    O estado do parser inclui pilha ou lookahead; so o componente de
    controle finito se encaixa. Sem esse recorte, Fintype falha.

- domain: pipelines com estados finitos
  classification: REQUIRES_ADAPTER
  applicable_api: [Reachable, IsInvariant, IsInvariant.of_reachable]
  adapter_needed: >
    Util sobretudo pelo lado dos INVARIANTES: IsInvariant.of_reachable eh
    exatamente o argumento "invariante refuta alcancabilidade". Exige
    modelar o pipeline como acao de monoide.

- domain: jogos finitos
  classification: CONCEPTUAL_ONLY
  note: >
    Jogos envolvem escolha entre jogadores; a dinamica nao eh a iteracao
    de uma unica funcao. A Camada A (alcancabilidade por ALGUM elemento)
    eh o fragmento que mais se aproxima, mas sem estrutura de turno.

- domain: modelos de agentes discretos
  classification: CONCEPTUAL_ONLY
  note: >
    Agentes tipicamente envolvem nao determinismo ou probabilidade, ambos
    fora do escopo (a acao aqui eh funcao total deterministica).

- domain: testes de alcancabilidade
  classification: DIRECT_REUSE
  applicable_api:
    - Reachable
    - reachable_refl
    - reachable_trans
    - reachable_iff_mem_orbit
    - IsInvariant
    - IsInvariant.of_reachable
  note: >
    Reutilizacao direta: a API nao exige finitude alguma. O padrao
    "exibir um invariante para refutar alcancabilidade" eh imediatamente
    utilizavel. CE-005 documenta o limite: o invariante NUNCA demonstra
    alcancabilidade.

- domain: deteccao de ciclos
  classification: REQUIRES_ADAPTER
  applicable_api: [exists_bounded_iterate_collision, exists_eventual_period]
  adapter_needed: >
    Os limitantes mu < card X e mu + lam <= card X dao a CORRECAO de um
    algoritmo de deteccao, nao o algoritmo. Extrair um procedimento
    executavel (Floyd, Brent) exigiria construcao computacional que esta
    frente nao tem.
```

## Resumo

| Classificação | Domínios |
|---|---|
| `DIRECT_REUSE` | 1 — testes de alcançabilidade |
| `REQUIRES_ADAPTER` | 6 |
| `CONCEPTUAL_ONLY` | 3 |
| `OUT_OF_SCOPE` | 0 |

O único caso de reutilização direta é o mais abstrato — alcançabilidade e
invariantes — precisamente porque essa parte da API **não exige finitude**.
Tudo que depende de `Fintype X` precisa de um adaptador que estabeleça a
finitude do espaço de estados, e essa é a hipótese que costuma falhar em
aplicações reais.

## Aviso vinculante

```text
A reutilizacao em software NAO transforma o resultado matematico padrao
em descoberta cientifica.
```

`mathematical_novelty: NONE` permanece, independentemente de quantos
domínios venham a usar a API.
