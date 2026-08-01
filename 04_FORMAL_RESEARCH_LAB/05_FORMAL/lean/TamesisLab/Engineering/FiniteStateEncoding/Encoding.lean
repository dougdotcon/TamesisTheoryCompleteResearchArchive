import TamesisLab.Engineering.FiniteStateRuntime

set_option autoImplicit false

/-!
# ENG-FINITE-STATE-ENCODING-001 — codificação certificada

A codificação é **dado executável fornecido pelo consumidor**, nunca
derivada. A alternativa — obter a bijeção a partir de `[Fintype S]` —
passa por uma API não computável, e tornaria a tabela inavaliável.

```text
encode e decode    dados
as duas leis       proposicoes, apagadas na execucao
typeclasses        nenhuma
```

O tamanho é o parâmetro `n`. Não existe campo redundante.
-/

namespace TamesisLab.Engineering.FiniteStateEncoding

/-- Bijeção **fornecida** entre um tipo de estados e `Fin n`.

Dois campos de dado e duas leis. Nenhuma typeclass é exigida do
consumidor: nem `Fintype`, nem `DecidableEq`, nem habitação.

Os dois papéis são distintos e ambos necessários:

```text
decode_encode   dependencia de prova da comutacao e da soundness
encode_decode   contrato: TODO indice de Fin n eh um estado real
```

Sem a segunda lei, `n` seria apenas um limite superior e a tabela
poderia conter linhas sem estado correspondente. -/
structure CertifiedFiniteEncoding (S : Type*) (n : Nat) where
  /-- Índice do estado. -/
  encode : S → Fin n
  /-- Estado do índice. -/
  decode : Fin n → S
  /-- Decodificar o código de um estado devolve o próprio estado. -/
  decode_encode : ∀ s : S, decode (encode s) = s
  /-- Codificar o estado de um índice devolve o próprio índice. -/
  encode_decode : ∀ i : Fin n, encode (decode i) = i

variable {S : Type*} {n : Nat}

/-- `encode` é injetiva.

Última seta do DAG da soundness tipada: é ela que transforma uma
igualdade em `Fin n` numa igualdade em `S`. Não exige igualdade
decidível — afirmar que dois estados são iguais não requer poder
decidi-lo. -/
theorem CertifiedFiniteEncoding.encode_injective
    (encoding : CertifiedFiniteEncoding S n) :
    Function.Injective encoding.encode :=
  Function.LeftInverse.injective encoding.decode_encode

/-- A dinâmica tipada, lida sobre índices.

Descreve o **conteúdo semântico da tabela antes** do transporte para
`Fin table.next.size`: a linha de índice `i` é exatamente
`encode (stepS (decode i))`.

Total por construção — o limite vem do tipo `Fin n`, e não de uma
verificação. Não há caso de erro, não há `Option`, não há valor
padrão. -/
def CertifiedFiniteEncoding.encodedStep (encoding : CertifiedFiniteEncoding S n)
    (stepS : S → S) : Fin n → Fin n :=
  fun i => encoding.encode (stepS (encoding.decode i))

end TamesisLab.Engineering.FiniteStateEncoding
