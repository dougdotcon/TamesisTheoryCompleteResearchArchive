---
document_id: RH-NOGO-REACTIVATION-CRITERIA
work_item_id: RH-NOGO-001
status: BINDING
---

# RH-NOGO-001 — critérios de reativação

A frente **somente** pode ser reaberta quando ao menos uma das condições
abaixo ocorrer, e a ocorrência tiver sido verificada e registrada.

```yaml
- id: REACT-001
  condition: >
    Uma biblioteca Lean fornecer infraestrutura adequada para operadores
    auto-adjuntos NAO LIMITADOS e resolvente compacto.
  verification_required: >
    Localizar a API, compilar um exemplo minimo contra a revisao fixada e
    registrar os nomes dos teoremas. Nao basta a existencia de um anuncio.

- id: REACT-002
  condition: >
    Existir formalizacao reutilizavel da lei GLOBAL de Weyl.
  verification_required: >
    Obter o artefato, compila-lo, e verificar que o enunciado eh a lei
    GLOBAL (contagem N(lambda)), nao apenas a lei LOCAL da funcao espectral
    na diagonal. Esta distincao ja custou um gate inteiro a este
    laboratorio - ver GAP-RH-013.

- id: REACT-003
  condition: >
    Existir formalizacao reutilizavel de Riemann-von Mangoldt.
  verification_required: >
    Obter o artefato e verificar que ele define a funcao de contagem
    concreta dos zeros e prova a formula assintotica, nao apenas o
    corolario generico "formula forte implica limite" - este ultimo ja
    esta formalizado aqui (SB-GAP-010A, CLOSED_BY_FORMALIZATION) e NAO
    satisfaz esta condicao.

- id: REACT-004
  condition: >
    Um colaborador especializado em analise microlocal E em Lean assumir a
    camada concreta.
  verification_required: >
    Compromisso explicito com a camada concreta. Interesse geral pelo
    problema nao satisfaz.

- id: REACT-005
  condition: >
    A frente receber prioridade estrategica explicita e recursos proprios
    como projeto independente.
  verification_required: >
    Decisao registrada em DECISION_LEDGER.yaml, com escopo e horizonte.
```

## O que **não** conta como reativação

```text
Mais capacidade computacional.
Um modelo de IA mais forte.
Mais tempo de agente disponivel.
Um gate autonomo decidir por conta propria que "agora vale a pena".
Progresso em outra frente do laboratorio.
Uma nova versao da Mathlib sem a API especifica exigida.
```

A razão é direta: o obstáculo **não é** velocidade nem volume de trabalho.
É **ausência de infraestrutura matemática formalizada**. Nenhuma das coisas
acima cria cálculo pseudodiferencial em Lean.

## Procedimento de reativação

Se uma condição ocorrer:

1. Registrar a ocorrência em `DECISION_LEDGER.yaml` com evidência
   verificada, não com anúncio.
2. Reabrir `RH-NOGO-001` para **especificação**, não para execução:
   `authorized_action: RH_NOGO_CONCRETE_LAYER_SPECIFICATION_AUTHORIZED`.
3. Reauditar `W_ELLIPTIC_SCALAR_V3.md`: a infraestrutura nova pode
   permitir remover acréscimos de ponte (`B1`–`B6`) que hoje são hipóteses
   deste laboratório. Seis das doze condições da classe são nossas — uma
   biblioteca adequada pode devolver algumas delas à literatura.
4. Só então, e em gate separado, considerar execução.

**Nenhum passo dessa sequência é autorizado por este documento.**
