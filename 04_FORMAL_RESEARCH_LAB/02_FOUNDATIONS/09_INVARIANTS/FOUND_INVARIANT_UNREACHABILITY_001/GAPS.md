---
document_id: FOUND-INVARIANT-UNREACHABILITY-001-GAPS
work_item_id: FOUND-INVARIANT-UNREACHABILITY-001
gaps_opened: 10
gaps_closed_at_specification: 0
---

# Lacunas, declaradas antes de começar

| id | conteúdo | estado |
|---|---|---|
| `INV-GAP-001` | completude: existe invariante separador sempre que há inalcançabilidade? | **ABERTA** |
| `INV-GAP-002` | invariantes relacionais, não funcionais | ABERTA |
| `INV-GAP-003` | monovariantes e argumentos de terminação | ABERTA |
| `INV-GAP-004` | estrutura algébrica do conjunto de invariantes | ABERTA |
| `INV-GAP-005` | invariante mais fino e sua relação com o quociente | ABERTA |
| `INV-GAP-006` | sistemas não determinísticos | ABERTA |
| `INV-GAP-007` | decidibilidade de `Reachable` em recortes finitos | ABERTA |
| `INV-GAP-008` | invariantes sob composição de sistemas | ABERTA |
| `INV-GAP-009` | bibliografia de argumentos de invariante em combinatória | **DELIBERADAMENTE ABERTA** |
| `INV-GAP-010` | ponte com `ABS-GAP-021`, a finitude da órbita concreta | ABERTA |

## `INV-GAP-001`, que é a lacuna honesta

A recíproca da ferramenta é **vacuamente verdadeira**: tome como
invariante a própria classe de alcançabilidade mútua, e ele separa
sempre que há inalcançabilidade. Isso não é um teorema útil, é uma
tautologia disfarçada.

A pergunta com conteúdo é outra e fica aberta:

```text
existe invariante separador CALCULAVEL, ou de tipo pequeno,
ou de forma restrita, quando ha inalcancabilidade?
```

Essa é a pergunta que o assunto de fato tem, e ela **não** é atacada
aqui. Fechá-la por delimitação seria mais frágil do que deixá-la aberta.

## `INV-GAP-009`, deixada aberta de propósito

Argumentos de invariante têm literatura própria e enorme, de tabuleiro
mutilado a quebra-cabeça de quinze a soldados de Conway. A frente não
reivindica lugar nessa literatura e não a audita. Declarar escopo não
substituiria leitura.

## O que estas lacunas impedem de afirmar

```text
que a ferramenta seja completa
que a ferramenta decida qualquer coisa
que a ferramenta seja nova
que a ferramenta resolva algum problema nomeado
```
