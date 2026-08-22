# Resultados — frente C `u12-generalization-u-alpha` (onda 3, DISC-DEC-015)

**Data:** 2026-08-22. Pré-registro em `METHODOLOGY_NOTE.md` (02:07Z);
derivações em `DERIVATIONS.md` e alvos em `predictions.json` gravados
ANTES da execução única de `ualpha_sim.py` (02:13Z; ordem verificável
por timestamps). Pós-hoc declarado em `posthoc_finiten.py/.json`.

## VEREDITO

> **A pergunta "por que o expoente é exatamente 1/2" tem resposta
> DERIVADA (rota PGFL, mesma da onda 2, generalizada):** para a classe
> de redirecionamento pontual (eventos a taxa c; evento no instante s
> mata com prob. q(s), senão cria um novo início de arco),
>
> **φ_q(c) = ∫₀¹ e^{−c·H_q(t)} dt, H_q(t) = t − (1−t)∫₀ᵗ (1−q(s))/(1−s) ds,**
>
> com H_q(t) = t²/2 + a·t^{β+1}/(β+1) + … quando q(s) ~ a·s^β, logo
>
> **α = 1/(1 + min(β, 1)) e α ∈ [1/2, 1] para TODA a classe.**
>
> O 1/2 é **duplamente protegido**: (i) mecanismos cegos à estrutura
> (destino intercambiável) têm forçosamente q(s) = s (β = 1, o passado
> é massa genérica) ⇒ hazard ~ ct²; (ii) mesmo um mecanismo que nunca
> mata paga o custo de "crowding" t²/2 (cada sobrevivente cria um
> alvo de fechamento concorrente). **α < 1/2 é impossível na classe**
> (piso derivado); sair para α = 1 exige um ÁTOMO de probabilidade de
> morte em idade 0⁺ (retro-destino: auto-laço, antecessor, mistura) —
> e mecanismos naturais desse tipo existem. A heurística sugerida no
> briefing (kill ~ t^β ⇒ e^{−ct^{β+1}/(β+1)}) foi confirmada para
> β ≤ 1 e **corrigida para β > 1**: ela preveria α < 1/2, mas o
> crowding trava o expoente em 1/2.
>
> **Resposta às perguntas centrais: U_{1/2} é uma classe GRANDE
> (robusto): todo destino intercambiável, reroteamento em blocos
> (∀ b fixo, validado), e provavelmente até o mecanismo fortemente
> estrutura-dependente intra-ciclo (conjecturado). U_1 também é
> natural e povoada (auto-laço, antecessor, misturas com átomo).
> α ∈ (1/2, 1) existe na classe abstrata (q ~ a·s^β, β ∈ (0,1)) mas
> NÃO encontramos mecanismo intrínseco natural que a realize.**

## TABELA DE CLASSES (mecanismo → φ_∞ → cauda → classe U_α → status)

| Mecanismo | φ_∞(c) | cauda (c→∞) | α | classe | status |
|---|---|---|---|---|---|
| M-U (original) | ∫₀¹e^{−ct²}dt | (√π/2)c^{−1/2} | 1/2 | U_{1/2} | DERIVADO; verificado (ondas 1–2; controle B1: χ²₅=1.97, p=0.85; α̂=0.5021±0.0048) |
| qualquer destino i.i.d. intercambiável | ≡ M-U (lema §3.1) | idem | 1/2 | U_{1/2} | DERIVADO (elementar) |
| M-CLUST(b) — blocos ao longo de π | = φ_U(c), ∀ b fixo (sombreamento: b−1 pontos por bloco são π-inalcançáveis) | (√π/2)c^{−1/2} | 1/2 | U_{1/2} | DERIVADO (rascunho); VALIDADO b=8 (χ²₅=7.07, p=0.22; α̂=0.4992±0.0048) — apesar de massa perturbada 8× maior |
| M-INTRA — destino no próprio ciclo | sem forma derivada; K=1 exato φ₁=3/4, a₁=1/4 | ~const·c^{−1/2} (coef. heur. √π) | 1/2 | U_{1/2} (CONJ.) | K=1 DERIVADO e validado (z=−1.22); cauda HEURÍSTICA, **não validada no critério pré-registrado** (α̂=0.4226±0.0034; ver honestidade) |
| M-MIX(p) — self c/ prob. p | ∫₀¹e^{−c(pt+(1−p)t²)}dt | 1/(pc), ∀p>0 | 1 | U_1 | DERIVADO; K=1 (7/12) validado; curva: pré-registro FALHOU em c=160, reconciliada pós-hoc c/ termo finito-n +pc/n (χ²₅=4.33, p=0.50) |
| M-SELF — auto-laço (p=1) | (1−e^{−c})/c | 1/c | 1 | U_1 | DERIVADO (2 rotas); verificação = T4 da onda 2 (massa livre) |
| M-PREV — destino π^{−1}(i) | (1−e^{−c})/c (geometria distinta: 2-ciclos) | 1/c | 1 | U_1 | DERIVADO (2 rotas); K=1 (1/2) validado; curva: pré-registro FALHOU em c≥40, reconciliada pós-hoc c/ termo +2(c/n)(1−c/n) (χ²₅=5.08, p=0.41) |
| classe abstrata q ~ a·s^β, β∈(0,1) | ∫₀¹e^{−cH_q}dt | Γ(1+1/(β+1))((β+1)/(ac))^{1/(β+1)} | 1/(β+1) | U_{1/(β+1)} | DERIVADO ao nível M-q; **sem realização intrínseca natural encontrada** (aberto) |
| toda a classe M-q (0≤q≤1) | eq. (1.2) | entre √(π/2c) e 1/c | ∈[1/2,1] | piso/teto | DERIVADO (§2 de DERIVATIONS.md) |

## O que é DERIVADO (dado o processo contínuo herdado da onda 2)

1. Fórmula-mestre (1.1)–(1.2) e lei do expoente α = 1/(1+min(β,1)),
   com o termo de crowding t²/2 independente de mecanismo; piso 1/2 e
   teto 1 sobre toda a classe M-q.
2. Lema de intercambiabilidade (destinos i.i.d. de lei fixa invariante
   por rótulos ⇒ idêntico em lei a M-U).
3. M-CLUST(b) = M-U no limite, ∀ b fixo (rigor de rascunho;
   sombreamento + correção finita-n c_eff = c(1−c/n)^b declarada).
4. M-MIX(p), M-SELF, M-PREV: formas fechadas, cada uma por 2 rotas
   independentes onde indicado; caudas 1/(pc) e 1/c.
5. Bateria K=1 exata (size-biasing, independente da fórmula-mestre):
   φ₁ = 2/3 (M-U), 7/12 (M-MIX(1/2)), 1/2 (M-PREV/M-SELF), 3/4
   (M-INTRA); e a₁(M-INTRA) = 1/4 ≠ 1/3 = a₁(M-U).

## Validação numérica (execução única; n = 32768; sementes pré-fixadas)

**B2 (K=1, 4 alvos racionais exatos): TODOS PASSARAM** —
0.667909±0.001667 (2/3, z=+0.75); 0.585369±0.001953 (7/12, z=+1.04);
0.500473±0.002034 (1/2, z=+0.23); 0.748078±0.001569 (3/4, z=−1.22).

**B1/C1 (curvas médias):** M-U PASS (p=0.85); M-CLUST8 PASS (p=0.22)
— a predição não-trivial "b-independente" confirmada; M-MIX50 e
M-PREV **FALHARAM o critério pré-registrado** (z=+12.6 em c=160;
z=+5.7/+85.7 em c=40/160). **C3 (declives 10→160):** M-U 0.5021±0.0048
PASS; M-CLUST8 0.4992±0.0048 PASS; M-MIX50 0.8439 e M-PREV 0.6777
FAIL vs alvos-limite; M-INTRA 0.4226±0.0034 FAIL vs janela |α̂−0.5|<0.06.

**Diagnóstico pós-hoc (declarado como pós-hoc; mesmos dados MC, zero
parâmetros livres):** as falhas de M-MIX50/M-PREV são o termo aditivo
finito-n dos pontos redirecionados que são eles próprios cíclicos —
+p·c/n (auto-laços) e +2(c/n)(1−c/n) (2-ciclos) — termo que
`DERIVATIONS.md` §3.2/§3.4 JÁ identificara antes das simulações
("cyclic mass = … + |R|/n" / "+ 2|R|/n"), mas que `predictions.py`
não transportou para os alvos numéricos: **deficiência de desenho do
pré-registro, registrada como tal** (o veredito FAIL pré-registrado
fica de pé). Com os alvos emendados: M-PREV χ²₅=5.08 (p=0.41), declive
a 1.8σ do alvo emendado 0.6644; M-MIX50 χ²₅=4.33 (p=0.50), declive a
1.7σ de 0.8569. Insight quantitativo: para mecanismos U_1 a cauda
limite ~1/c é mascarada em n finito pelo termo ~c/n a partir de
c ~ √n (≈181 em n=32768) — exatamente onde as células c=160 explodiram;
a classificação U_α refere-se à função-limite, e o desenho de teste em
c ≳ √n para mecanismos U_1 foi um erro de planejamento desta frente.

## O que permanece HEURÍSTICO/CONJECTURADO (com igual peso de reporte)

- **Cauda de M-INTRA:** a análise de círculo (anelada) prevê α = 1/2
  com coeficiente ~√π, AMBOS heurísticos. O critério pré-registrado
  FALHOU (α̂ = 0.4226 ± 0.0034 no alcance c ∈ [10,160], fora da janela
  0.06). Suporte qualitativo remanescente: o declive local MEDIDO sobe
  (0.406 em 10→40; 0.439 em 40→160) e a razão MC/heurística sobe
  monotonicamente para 1 (0.815 → 0.859 → 0.900 em c = 10/40/160) —
  padrão de convergência lenta para c^{−1/2}, e incompatível com as
  curvas U_1 no mesmo alcance (declives ≥ 0.66). **Status final:
  M-INTRA ∈ U_{1/2} é CONJECTURA não validada no alcance testado**;
  o que está estabelecido de M-INTRA é só o K=1 exato (3/4, validado).
- Realização intrínseca de α ∈ (1/2, 1): não encontrada; candidato
  examinado no papel (saltos π-retrógrados de cauda pesada) parece dar
  α = 1 — deixado ABERTO, sem alegação.
- Herdada das ondas 1–2: a passagem n finito → contínuo do processo de
  exploração segue controlada empiricamente, não formalizada.

## Escopo, disciplina e honestidade

- Execução única das baterias com as sementes pré-declaradas
  (20260822 / 84206); antes dela, apenas um smoke test de componentes
  com semente descartável 999 (c=0 ⇒ φ=1; π^T em 5-ciclo; inversa de
  π; cronometragem), declarado aqui e sem uso em validação.
- Nenhum ajuste de parâmetros em momento algum; a emenda pós-hoc é
  analítica, derivada e sem parâmetros livres, e está rotulada
  pós-hoc em todos os artefatos.
- Nenhuma alegação de novidade (mandato da frente A, DISC-DEC-015);
  classificação interna ao arquivo.
- **FLAG ADVERSARIAL (VC): SIM — obrigatória por DISC-DEC-015.**
  Sugestões ao adversário: re-derivar (1.1)–(1.2) e o piso α ≥ 1/2;
  atacar o argumento de sombreamento de M-CLUST (é a predição mais
  frágil das DERIVADAS); testar M-INTRA em c maiores/n maiores para o
  expoente; verificar as emendas finito-n por enumeração exata em n
  pequeno; c e sementes próprios.

## Arquivos (todos nesta pasta)

- `METHODOLOGY_NOTE.md` — pré-registro (família, programa, critérios).
- `DERIVATIONS.md` — fórmula-mestre, lei de expoentes, piso/teto,
  mecanismos, bateria K=1, tabela predita (rótulos por linha).
- `predictions.py` / `predictions.json` — alvos pré-simulação.
- `ualpha_sim.py` / `ualpha_results.json` / `ualpha_sim.log` — B1–B2 +
  critérios C1–C3 (execução única) + pós-hoc anexado ao log.
- `posthoc_finiten.py` / `posthoc_finiten.json` — reconciliação
  finito-n pós-hoc (declarada).

## ADENDO (2026-08-22, onda 4, DISC-DEC-018) — correção da correção finito-n de M-CLUST(b)

A verificação adversarial (`adversarial/ADVERSARIAL_VERDICT.md` §3)
encontrou que a correção finito-n declarada acima para M-CLUST(b)
(c_eff = c(1−c/n)^b, §3.5 de `DERIVATIONS.md`) é insuficiente para b
grande (desvio até −27,1% em b=50,c=400). A subpasta
`mclust_rigor/` (nova, onda 4) re-derivou o mecanismo do zero e
identificou dois erros reais na fórmula original — a taxa c_eff mede a
densidade NÃO-condicional de "run starts", não a taxa correta
condicional-ao-passeio (que é simplesmente c, sem depressão); e o
termo de "chain-kill" que a redação original supôs parcialmente
cancelado na verdade amplifica monotonicamente a morte, sem
cancelamento — propôs uma fórmula corrigida (φ_NEW,
`mclust_rigor/DERIVATION_MCLUST_FIXED.md` §4) e validou-a com
simulador e sementes próprios em b∈{8,50,100,200}. Resultado:
**PARCIALMENTE CORRIGIDO** — a nova fórmula fecha consistentemente
70–86% do gap identificado (ex.: b=100,c=400: −45,9% → −12,6%), mas
deixa um resíduo sistemático não totalmente explicado, crescente com
b·c/n. A classificação M-CLUST(b) ∈ U_{1/2} no limite n→∞ (∀ b fixo)
**não é afetada** por este achado. Ver `mclust_rigor/` para a
derivação completa, os dados de validação e a discussão honesta do
resíduo remanescente.
