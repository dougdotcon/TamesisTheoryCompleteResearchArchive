---
document_id: PR-CERTIFIED-STATE-ENCODING-CANDIDATE
work_item_id: ENG-FINITE-STATE-ENCODING-001
status: SCOPED
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_SOFTWARE_BRIDGE
---

# Candidato selecionado — codificação certificada de estados

## Objetivo preliminar

```text
Dado um sistema deterministico finito TIPADO,
uma codificacao e uma decodificacao inversas,
construir sua tabela de transicoes e provar que a execucao da tabela
corresponde EXATAMENTE a execucao do sistema original.
```

## Escopo congelado como proposta

Apenas isto, e apenas como proposta de portfólio:

```text
tipo de estados S;
tamanho n;
encode : S -> Fin n;
decode : Fin n -> S;
leis de inversao;
stepS : S -> S;
construcao de RawTransitionTable;
prova de validade;
comutacao de um passo;
comutacao de iteracoes;
aplicacao de analyzeTransitionTable;
interpretacao do witness no sistema tipado.
```

## Interface candidata

```lean
structure CertifiedFiniteEncoding (S : Type) (n : Nat) where
  encode : S → Fin n
  decode : Fin n → S
  decode_encode : ∀ s, decode (encode s) = s
  encode_decode : ∀ i, encode (decode i) = i
```

A codificação é **recebida**, nunca derivada. Essa é a decisão que mantém
tudo computável — ver a auditoria de `Fintype.equivFin` abaixo.

Construção candidata:

```lean
table.next = Array.ofFn (fun i => (encode (stepS (decode i)) : Nat))
```

## O que NÃO está decidido

```text
estrutura final;
nomes Lean definitivos;
uso de Equiv em vez de quatro campos;
uso de Array.ofFn;
API total;
extracao;
CLI;
parser;
estado externo real.
```

Essas decisões pertencem ao gate de especificação. Nada aqui é assinatura
congelada.

## APIs auditadas — probes descartáveis, já removidos

| Conceito | Assinatura exata | Origem | Classificação |
|---|---|---|---|
| construção do array | `Array.ofFn : {α} → {n : ℕ} → (Fin n → α) → Array α` | `Init/Data/Array/Basic.lean:331` | `API_FOUND` |
| tamanho | `Array.size_ofFn : (Array.ofFn f).size = n` | `Init/Data/Array/Lemmas.lean:4254` | `API_FOUND` |
| leitura | `Array.getElem_ofFn (h : i < (Array.ofFn f).size) : (Array.ofFn f)[i] = f ⟨i, ⋯⟩` | `Init/Data/Array/Lemmas.lean:4282` | `API_FOUND` |
| limite de índice | `Fin.isLt : ∀ (self : Fin n), ↑self < n` | núcleo | `API_FOUND` |
| bijeção | `Equiv`, `Equiv.symm_apply_apply`, `Equiv.apply_symm_apply` | `Mathlib/Logic/Equiv/Defs.lean` | `API_FOUND` |
| permutação | `Equiv.Perm : Sort u → Sort (max 1 u)` | Mathlib | `API_FOUND`, **não necessário** |
| iteração | `Nat.iterate`, notação `f^[n]` | núcleo | `API_FOUND` |
| passo de iteração | `Function.iterate_succ_apply (f) (n) (x) : f^[n.succ] x = f^[n] (f x)` | Mathlib | `API_FOUND` |
| soma de iterações | `Function.iterate_add_apply (f) (m n) (x) : f^[m+n] x = f^[m] (f^[n] x)` | Mathlib | `API_FOUND` |
| semiconjugação | `Function.Semiconj : (α → β) → (α → α) → (β → β) → Prop` | `Mathlib/Logic/Function/Conjugate.lean` | `API_FOUND` |
| **iteradas da semiconjugação** | `Function.Semiconj.iterate_right : Semiconj f ga gb → ∀ n, Semiconj f ga^[n] gb^[n]` | Mathlib | `API_FOUND` |
| semiconjugação à esquerda | `Function.Semiconj.iterate_left` | Mathlib | `API_FOUND`, forma diferente |
| composição | `Function.Semiconj.comp_eq : Semiconj f ga gb → f ∘ ga = gb ∘ f` | Mathlib | `API_FOUND` |
| equivalência com `Fin` | `Fintype.equivFin (α) [Fintype α] : α ≃ Fin (Fintype.card α)` | `Mathlib/Data/Fintype/EquivFin.lean:80` | `API_FOUND`, **`noncomputable`** |
| versão truncada | `Fintype.truncEquivFin (α) [DecidableEq α] [Fintype α] : Trunc (α ≃ Fin (card α))` | idem | `API_FOUND`, `Trunc` |
| `Function.iterate` como identificador | — | — | `NOT_FOUND` (o nome é `Nat.iterate`) |

### Pegada axiomática medida

```text
Array.ofFn                        [propext]
Array.size_ofFn                   [propext]
Array.getElem_ofFn                [propext, Classical.choice, Quot.sound]
Function.Semiconj.iterate_right   [propext]
Fintype.equivFin                  [propext, Classical.choice, Quot.sound]
```

E, o que mais importa:

```text
#eval (Array.ofFn (n := 3) (fun i => (i : Nat) + 1))   ->   #[1, 2, 3]
```

`Array.ofFn` é **computável**, sai com `[propext]` apenas, e produz dado
sob `#eval`. A construção da tabela não introduz peso axiomático novo.

### O achado que mais muda o plano

```lean
Function.Semiconj.iterate_right :
  Semiconj f ga gb → ∀ n, Semiconj f ga^[n] gb^[n]
```

`Semiconj encode stepS tableStep` é **exatamente** a comutação de um
passo. Se ela for provada, a comutação de iteradas é `.iterate_right n` —
um corolário de uma linha, com axiomas `[propext]`. A condição 8 da regra
de decisão não só passa: ela passa por um caminho mais curto do que o
previsto na proposta.

### O achado que mais restringe o plano

```text
Fintype.equivFin eh noncomputable.
```

Portanto a codificação **não** pode ser derivada de `[Fintype S]`. Ela
tem de ser um campo fornecido. Isso vira `STOP-ENC-006` e é a razão de a
estrutura candidata ter quatro campos em vez de um `Fintype`.

## Riscos identificados

### Computabilidade

```text
derivar encode de Fintype torna a tabela nao computavel;
Trunc nao permite extrair dado fora de eliminacao para Subsingleton;
a construcao precisa de Array.ofFn, que eh computavel.
```

### Escolha clássica

```text
proibido: Classical.choose produzindo encode, decode ou a tabela;
permitido: pegada infraestrutural herdada em provas, como ja ocorre no
detector por Fintype.card.
```

### Casts

O risco real, e o mais provável de custar tempo:

```text
Array.ofFn f tem size provado igual a n por size_ofFn,
mas table.next.size NAO eh sintaticamente n.
```

`Fin table.next.size` e `Fin n` são iguais **por teorema**, não por
definição. `Array.getElem_ofFn` ajuda — está enunciado sobre
`(ofFn f).size`, e não sobre `n` — mas a interface do adaptador fala de
`t.next.size`. Este é `ENC-GAP-004`, e `STOP-ENC-005` para se a
correspondência exigir `cast` não controlado.

Há precedente favorável: a frente anterior evitou transporte dependente
inteiro escolhendo a tabela concreta cujo campo era **sintaticamente**
igual. A mesma técnica deve ser tentada aqui, e é decisão do gate de
especificação.

### Ciclos espúrios

```text
com bijecao, NAO existem ciclos espurios.
```

`decode_encode` e `encode_decode` tornam a correspondência exata nas duas
direções. É precisamente por isso que esta frente vem **antes** da
alternativa `E`: lá, ciclo abstrato não implica ciclo concreto, e o
enunciado forte é falso sem hipóteses adicionais.

### Tipo vazio

`n = 0` força `S` vazio, a tabela é `#[]`, estruturalmente válida, e
nenhuma consulta é aceita — comportamento já provado em `valid_empty`.
Registrado como `ENC-GAP-002` e `ENC-GAP-012`.

## PoC de trinta dias

```text
1 estrutura;
cerca de 3 definicoes;
cerca de 8 teoremas;
0 fontes primarias;
0 dependencias externas;
reutilizacao integral do adaptador.
```

`thirty_day_poc: YES`.

## Duplicata

```text
14 itens na fila; nenhum menciona codificacao certificada.
```

As três ocorrências de `ENCODING` em `01_PORTFOLIO/` são o rótulo
`REQUIRES_STATE_ENCODING` na matriz de reutilização da frente anterior —
isto é, o registro de que **falta** exatamente esta frente.

## O que NÃO está autorizado

```text
ENG_FINITE_STATE_ENCODING_001_FORMALIZATION_AUTHORIZED
ENG_FINITE_STATE_ENCODING_001_EXTRACTION_AUTHORIZED
ENG_FINITE_STATE_ENCODING_001_CLI_AUTHORIZED
ENG_FINITE_STATE_ENCODING_001_INTEGRATION_AUTHORIZED
ENG_FINITE_STATE_RUNTIME_001_EXTRACTION_AUTHORIZED
ENG_FINITE_STATE_RUNTIME_001_CLI_AUTHORIZED
FOUND_CYCLE_DETECTION_001_FLOYD_AUTHORIZED
RH_PROOF_AUTHORIZED
RIEMANN_PROOF_AUTHORIZED
```

Todos os `extension_status: NOT_AUTHORIZED` existentes permanecem.

## Gaps iniciais — dezesseis, nenhum fechado

```text
ENC-GAP-001  representacao encode/decode
ENC-GAP-002  necessidade de n > 0
ENC-GAP-003  construcao computavel do Array
ENC-GAP-004  prova de tamanho do Array
ENC-GAP-005  validade automatica da tabela
ENC-GAP-006  comutacao de um passo
ENC-GAP-007  comutacao de iteradas
ENC-GAP-008  interpretacao do CycleWitness
ENC-GAP-009  dependencia de DecidableEq
ENC-GAP-010  uso ou rejeicao de Equiv
ENC-GAP-011  pegada de Classical.choice
ENC-GAP-012  tabela vazia e tipo vazio
ENC-GAP-013  extracao futura
ENC-GAP-014  parser externo
ENC-GAP-015  correcao da aplicacao concreta
ENC-GAP-016  bibliografia e atribuicao historica
```

## Stop conditions — quatorze

```text
STOP-ENC-001  codificacao usa fallback silencioso
STOP-ENC-002  encode/decode sem leis inversas suficientes
STOP-ENC-003  Array construido sem tamanho provavel
STOP-ENC-004  step da tabela nao comuta com stepS
STOP-ENC-005  correspondencia exige cast nao controlado
STOP-ENC-006  Classical.choose produz dado executavel
STOP-ENC-007  detector anterior eh copiado
STOP-ENC-008  runtime adapter eh modificado sem autorizacao
STOP-ENC-009  parser ou CLI entra no nucleo
STOP-ENC-010  equivalencia eh assumida, nao fornecida
STOP-ENC-011  sistema externo real eh declarado correto
STOP-ENC-012  novidade eh inflada
STOP-ENC-013  frente duplica item existente
STOP-ENC-014  PoC nao cabe em 30 dias
```

## Limites científicos

```yaml
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_SOFTWARE_BRIDGE
```

Proibido afirmar: integração real concluída; modelo universal de
sistemas; correção de qualquer workflow; correção de qualquer agente;
prova de segurança de software externo; descoberta matemática; novo
algoritmo. Nada aqui toca a Hipótese de Riemann, TRI, TDTR, física ou
qualquer conjectura Clay.
