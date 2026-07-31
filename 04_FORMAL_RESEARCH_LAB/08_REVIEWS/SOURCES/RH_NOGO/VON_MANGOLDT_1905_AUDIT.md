# VON_MANGOLDT 1905 — auditoria de fonte primária

Fonte: H. von Mangoldt, *Zur Verteilung der Nullstellen der Riemannschen
Funktion ξ(t)*, Mathematische Annalen **60** (1905), 1–19.
Cópia: `pdf/von_mangoldt_1905_mathann60.pdf`, sha256 `7dd69d35…`, GDZ.
Estado de leitura: `PARTIALLY_AUDITED` — páginas 1, 2, 18 e 19 lidas
integralmente como imagens renderizadas; páginas 3–17 (aparato numérico das
estimativas) não lidas. O PDF é digitalização por imagem, **sem camada de
texto**; nenhuma OCR foi usada.

## Respostas literais às 12 perguntas do gate

### 1. Qual função de contagem é definida?

Página 2, linha central:

> „Wenn dann *N* die Anzahl derjenigen Nullstellen der Funktion ξ(t)
> bezeichnet, deren reelle Teile zwischen 0 und *T* liegen, jede so oft
> gezählt, als ihre Ordnungszahl angibt …“

`N` = número de zeros de `ξ(t)` cujas **partes reais** estão entre `0` e `T`.

### 2. Quais zeros são contados?

Os zeros da função `ξ(t)` de Riemann — não os de `ζ(s)` diretamente.
A ponte é a equação (1) da página 2:

> (1) ξ(T−ia) = Π(1/4 + a/2 + iT/2)·(a − 1/2 + iT)·π^(−1/4−a/2−iT/2)·ζ(1/2 + a + iT)

### 3. Qual região do plano complexo é usada?

Página 2: fixa-se uma constante `a > 1/2` arbitrária; traça-se no plano da
variável complexa `t` uma paralela ao eixo real pelo ponto `−ia` e uma
paralela ao eixo imaginário pelo ponto `T` (Fig. 1). O contorno percorre os
segmentos `−ia ⋯ T−ia` e `T−ia ⋯ T`. A contagem é sobre a faixa das partes
reais em `(0, T)`.

### 4. As multiplicidades são incluídas?

**Sim, literalmente**: „jede so oft gezählt, als ihre **Ordnungszahl**
angibt“ — cada zero contado tantas vezes quanto indica sua ordem
(multiplicidade). Página 2.

### 5. Como zeros sobre os limites do intervalo são tratados?

**Excluídos por escolha de `T`**, página 2:

> „Den Wert *T* selbst denke man sich so gewählt, daß die letztere Parallele
> durch keine Nullstelle der Funktion ξ(t) hindurchgeht.“

Isto é, `T` é escolhido de modo que a reta vertical por `T` não passe por
zero algum. Não há convenção de meia-contagem.

### 6. Qual é a variável assintótica?

`T`, real positivo, com a restrição explícita `T > 28,558` no resultado
final.

### 7. Qual fórmula exata é provada?

Página 19 (última página do artigo), resultado final, para `T > 28,558`:

```
N = (T/2π)·l(T/2π) − T/2π + 7/8
      + η·(0,43200·lT + 1,91662·llT + 12,20373),      (−1 < η < 1)
```

onde `l` é o logaritmo natural (nota de rodapé ** da página 1) e `ll` o
logaritmo iterado.

Consistência verificada com a página 1, que enuncia a mesma coisa sem o
termo `7/8`, com a cota `0,43200 lT + 1,91662 llT + 13,07873`; de fato
`12,20373 + 7/8 = 13,07873`. As duas páginas concordam exatamente.

### 8. Qual é o termo de erro?

Explícito e **efetivo**: `|erro| < 0,43200·lT + 1,91662·llT + 12,20373`
para `T > 28,558`. Em notação moderna, `O(log T)`.

Página 1 registra o avanço sobre o trabalho anterior do próprio autor
(J. reine angew. Math. **114** (1895), 266), onde a cota era
`0,34·(lT)² + 1,35·lT + 2,58` — de ordem `(log T)²`. O ganho de 1905 é
justamente reduzir a ordem do erro a `log T`:

> „… eine noch tiefer liegende, *nur bis zur Größenordnung von lT
> ansteigende* Grenze …“

### 9. O resultado depende ou não da RH?

**Não depende.** O método é o princípio do argumento aplicado a um contorno
retangular com `a > 1/2` arbitrário (página 2): `2πN` é o dobro do
incremento do coeficiente de `i` em `l ξ(t)` ao longo dos dois segmentos.
Nenhuma hipótese sobre a localização dos zeros é introduzida.

**Ressalva registrada:** na página 18 o autor invoca de la Vallée Poussin
(Mémoires, Bd. 59, 1899, S. 23) para o fato de que *os zeros em questão*
são todos reais e simples, e os valores numéricos de Gram (1902) para
`α₁ = 14,134725`, `α₂ = 21,022040`, `α₃ = 25,010856`. Isto é uso de fatos
**verificados para zeros baixos específicos**, não da Hipótese de Riemann.
A distinção está registrada em `UNRESOLVED_SOURCE_QUESTIONS.md` como item a
confirmar nas páginas 3–17 não lidas.

### 10. O texto usa função equivalente à `N_ζ(T)` moderna?

Sim, **após a tradução de notação da questão 11**. Não é a mesma expressão
literal: von Mangoldt conta zeros de `ξ(t)` por parte real; a literatura
moderna conta zeros `ρ` de `ζ(s)` por ordenada `Im ρ`.

### 11. Qual tradução de notação é necessária?

| von Mangoldt 1905 (plano `t`) | moderno (plano `s`) |
|---|---|
| `s = 1/2 + it` (implícito na eq. (1)) | idem |
| zero de `ξ(t)` em `t` | zero `ρ = 1/2 + it` de `ζ` |
| **parte real** de `t` | **ordenada** `γ = Im ρ` |
| parte imaginária de `t` | `−(Re ρ − 1/2)` |
| `N` = #{zeros de ξ com Re t ∈ (0,T)} | `N_ζ(T)` = #{ρ : 0 < Im ρ < T} |
| `l` | `log` natural |

**Atenção a um choque de notação:** na Fig. 1 da página 2 o zero genérico é
denotado `β + iγ` no plano `t`, de modo que ali `β` é a **parte real** de
`t`, ou seja, a ordenada moderna. Isto é o inverso da convenção moderna
`ρ = β + iγ` no plano `s`. Nenhuma citação deste laboratório pode misturar
as duas convenções.

Verificação da tradução na própria eq. (1): `t = T − ia` dá
`s = 1/2 + i(T − ia) = 1/2 + a + iT`, exatamente o argumento de `ζ` no lado
direito. Confirma `Re t ↔ Im s`.

### 12. Qual passagem sustenta cada afirmação?

| Afirmação | Página | Localização |
|---|---|---|
| definição de `N` com multiplicidade | 2 | parágrafo após a Fig. 1 |
| escolha de `T` fora de zeros | 2 | parágrafo antes da Fig. 1 |
| contorno e `a > 1/2` | 2 | §1, abertura |
| relação ξ↔ζ | 2 | equação (1) |
| termo principal `(T/2π)l(T/2π) − T/2π` | 1 e 19 | abertura; fórmula final |
| constante `7/8` | 19 | fórmula final |
| cota de erro efetiva | 19 | fórmula final; e p. 1 na forma sem `7/8` |
| restrição `T > 28,558` | 1, 18, 19 | enunciado e escolha `k = 0,675`, `u = 3,2650/lT` |
| cota anterior `O((log T)²)` de 1895 | 1 | nota de rodapé *** |
| zeros baixos de Gram / de la Vallée Poussin | 18 | notas * e ** |

Data do artigo: „Aachen, den 6. Mai 1904.“ (página 19).

## Veredito para o pilar A

**SUSTENTADO.** A fonte primária estabelece, incondicionalmente e com termo
de erro efetivo de ordem `log T`, exatamente a fórmula de contagem
necessária. Dividindo por `T log T`:

```
N_ζ(T)/(T log T) → 1/(2π)
```

que é a hipótese A de `ASYM-NOGO-001` com `c = 1/(2π) > 0`. A dedução do
limite a partir da fórmula é corolário elementar, **não executado neste
gate** (ver `SOURCE_BRIDGE_REQUIREMENTS.md`, etapa C).
