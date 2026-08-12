# Sessão 2026-08-12 — Início da linha RH-REAL: Fase 0 + primeiro teste pré-registrado

## Contexto

Após o encerramento do Gate de Replicação de `DISC-COSMOLOGY-MOND-SPARC-002`
(sessão anterior, mesmo dia), usuário pediu para iniciar a linha
`DISC-RH-REAL-001` — pesquisa real sobre `riemannZeta`, motivada pelo caso
Anthropic, distinta do operador de brinquedo `Tp`.

## Fase 0 (exploratória, `evidence_level: exploratory_only`)

1. **Dado real localizado**: tabelas de Odlyzko
   (`www-users.cse.umn.edu/~odlyzko/zeta_tables/`, URL antiga `dtc.umn.edu`
   redireciona para cá). Baixados `zeros1.txt` (100.000 primeiros zeros
   reais), `zeros2.txt` (100 zeros de alta precisão), `zeros3.txt` (10.000
   zeros perto do zero #10¹², regime de altura completamente diferente).
   Primeiro valor de `zeros1.txt` confere com o zero didático conhecido
   (14,134725142). LMFDB verificada como fonte real mas bloqueada por
   captcha para acesso programático — documentada como referência, não
   fonte de download.
2. **Levantamento de literatura**: 12 conjecturas/resultados concretos e
   numericamente testáveis sobre zeros de zeta (não a RH em si), cada um
   com citação verificada — correlação de pares (Montgomery), estatística
   GUE, N(T) (Riemann–von Mangoldt), momentos de zeta, constantes de gaps
   pequenos/grandes, e uma questão explicitamente em aberto (dez/2024,
   arXiv:2412.15481) sobre runs de gaps moderados consecutivos.
3. **Triagem numérica** de 6 dos 12 itens sobre os 100k zeros reais —
   pipeline validado contra estatísticas GUE/N(T) já conhecidas (média de
   espaçamento normalizado = 1,0000, repulsão de nível de ~10× perto de
   u=0). Nenhum resultado de Fase 0 é descoberta — são checagens de
   consistência. Ver `PHASE0_TRIAGE_SUMMARY.md`.

## Primeiro teste pré-registrado: `DISC-RH-ZERO-GAP-RUNS-001`

Usuário pediu para escolher um candidato da Fase 0 e desenhar um
pré-registro real. Escolhido o item 9 (runs de gaps moderados
consecutivos) em vez do item 7 (constante de gaps pequenos de Inoue
2026) porque o item 7 é fundamentalmente um `liminf` — não admite uma
pergunta falsificável limpa com dado finito. O item 9 também tem sabor de
"infinitos", mas permite uma **pergunta proxy genuína**: a sequência real
mostra correlação sequencial detectável (via teste de permutação) além
do que a distribuição marginal sozinha explicaria?

### Desenho

- Grade pré-declarada: `c ∈ {0,10; 0,20; 0,30}` × `r ∈ {2; 3}` (6 células).
- Estatística: contagem de posições com `r` gaps consecutivos todos `≥ c`.
- Nulo: 10.000 permutações aleatórias do mesmo multiconjunto de gaps
  (seed 20260812).
- Correção de Bonferroni (limiar 0,05/6 ≈ 0,00833).
- Hipótese direcional: motivada por correlação de Pearson negativa
  (−0,357) entre gaps consecutivos, já observada na Fase 0 — previa MAIS
  runs no dado real que no nulo (repulsão de nível evitaria clusters de
  gaps pequenos).
- Dataset secundário (`zeros3.txt`, regime ~10¹²) reservado para checagem
  de generalização informativa, explicitamente rotulado como fora do
  critério de decisão primário.

### Resultado: `INVERSE_SIGNAL`

A direção prevista estava **errada**. Em `c=0,30` (r=2 e r=3), a contagem
real de runs ficou significativamente **abaixo** da distribuição nula
(p≈0,0001 — essencialmente nenhuma das 10.000 permutações teve contagem
tão baixa quanto o dado real ordenado). Mesmo padrão replicado no dataset
secundário, completamente disjunto, em regime de altura ~10¹² (p≈0,001 e
p≈0,0001). Em `c=0,10` e `c=0,20` nenhum efeito significativo após
correção.

**Interpretação correta** (formulada depois de ver o resultado, mas
apenas como interpretação de um resultado já travado e computado, não
como reformulação do critério): correlação negativa entre gaps vizinhos
promove **alternância**, não persistência — por isso *suprime* runs de
gaps grandes consecutivos em vez de aumentá-los. O raciocínio direcional
original estava errado; o teste capturou corretamente um efeito real na
direção oposta — exatamente o cenário `INVERSE_SIGNAL` que o próprio
pré-registro exigia reportar de forma proeminente, não escondido.

### Revisão adversarial: `CONFIRMED`

Agente independente, código escrito do zero antes de ler o script
primário, seed distinta: reproduziu as 12 contagens de runs relatadas
**bit a bit**. Nenhum bug encontrado. Checagem específica do artefato
mais preocupante — uma tendência lenta de tamanho de gap ao longo da
faixa de altura, que produziria o mesmo padrão estatístico por um
mecanismo totalmente diferente (não correlação sequencial real):
correlação posição-vs-gap ≈ 5×10⁻⁵ em ambos os datasets — indistinguível
de zero, artefato descartado. Padrão de crescimento do efeito com `c`
avaliado como assinatura coerente de poder estatístico (fração de gaps
"pequenos" cresce de 0,1% para 2,1% entre c=0,10 e c=0,30), não
cherry-picking — a grade completa foi travada antes de qualquer cálculo.

## Gate de Replicação completo (acionado a pedido do usuário)

Sem holdout selado declarado neste pré-registro — cláusula de fallback de
`03_REPLICATION_GATE/PROTOCOL.md` Seção 3 aplicada: checagem de robustez
contra uma terceira fonte de dado genuinamente nova. Terceiro agente
independente (nunca tocou código/resultados anteriores):

1. **Proveniência**: baixou `zeros4.txt` (Odlyzko, zeros #10²¹+1..+10⁴,
   γ≈1,44×10²⁰ — ~9 ordens de magnitude acima do secundário e ~15 acima
   do primário) por conta própria, fetch direto, checksum, verificação
   cruzada do primeiro valor contra o próprio cabeçalho do arquivo.
2. **Implementação nova**: pegou e corrigiu por conta própria um risco
   real de cancelamento catastrófico de ponto flutuante ao formar
   `gamma=base+offset` com uma base de 21 dígitos (não representável
   exatamente em float64) — gaps computados diretamente dos offsets
   brutos.
3. **Mesma grade travada rodada sobre `zeros4.txt`**: mesmo padrão
   replicado — `c=0,30` significativo em ambas r=2 (p=0,00100) e r=3
   (p=0,00120), `c≤0,20` não significativo. Artefato de deriva descartado
   também aqui (correlação posição-vs-gap ≈ −2,5×10⁻⁴).
4. **Adversário de nulo dedicado**: descartou artefato de
   precisão/truncamento (matematicamente incapaz de afetar a comparação
   real-vs-permutado, já que afeta os dois lados igualmente); não achou
   publicação prévia com esta estatística exata de runs via permutação;
   **achado importante**: uma simulação sintética AR(1)/cópula Gaussiana
   com a mesma correlação de lag-1 (−0,349) mas **sem nenhum conteúdo de
   zeta** reproduziu o mesmo padrão — confirma que o efeito é consequência
   **genérica** de correlação serial negativa, não um artefato numérico
   nem circular nem exclusivo de zeta. Isso não enfraquece o achado: a
   alegação substantiva sempre foi "gaps de zeta têm correlação serial
   negativa" (já bem estabelecido na literatura GUE), e este teste de
   runs é uma segunda assinatura estatística independente disso.

**Veredito do Gate: `REPLICATION_PASSED`.** Os quatro requisitos
satisfeitos, padrão confirmado a ~15 ordens de magnitude de distância do
dataset primário.

## Estado final

`DISC-CLAIM-003`: `evidence_level: preregistered_falsified` (direção
prevista por H falsificada — não significa "sem efeito": um efeito real,
forte e replicado em TRÊS datasets/regimes de altura disjuntos foi
encontrado na direção oposta). `adversarial_review_verdict: CONFIRMED`.
`replication_status: REPLICATION_PASSED`. `promoted_to_formal_lab: false`
— mantido `false` apesar do Gate ter passado, porque o próprio adversário
de nulo do Gate confirmou que é confirmação numérica de estrutura GUE já
conhecida (e genérica a qualquer sequência com a mesma correlação serial),
não descoberta matemática nova — não há teorema a extrair.

## Próxima decisão (não tomada nesta sessão)

Escolher outro candidato da Fase 0 de RH-REAL (item 7, constante de gaps
pequenos de Inoue 2026 — ainda sem desenho falsificável adequado) ou
seguir para `DISC-TRI-RG-001` (ainda não iniciado).
