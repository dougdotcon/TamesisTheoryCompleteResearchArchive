# Sessão 2026-08-12 — Segundo sub-teste da linha RH-REAL: escala de valor extremo

## Contexto

Continuação da sessão que fechou `DISC-RH-ZERO-GAP-RUNS-001` com
`REPLICATION_PASSED`. Usuário pediu para escolher entre o item 7
(constante de gaps pequenos de Inoue 2026) ou abrir `DISC-TRI-RG-001`.
Escolhido o item 7 — reaproveita infraestrutura e dado já validados nesta
linha, enquanto `TRI-RG` ainda precisa de trabalho de formulação
substancial (nomear um mapa de renormalização, achar dois domínios reais
comparáveis).

## Desenho do teste

Item 7 (Inoue 2026, arXiv:2604.05733) é uma afirmação de `liminf` —
não testável com dado finito, mesmo problema do item 9 antes de ser
reformulado. Pergunta proxy desenhada via teoria de valores extremos: o
gap mínimo entre `N` zeros reais escala como `N^(-1/3)` (GUE, repulsão de
nível) ou `N^(-1)` (Poisson, sem correlação)? Os dois são modelos
concorrentes nomeados, satisfazendo a exigência de discriminating
observable.

Método pré-registrado: blocos não-sobrepostos, grade `N ∈ {500; 1.000;
2.000; 5.000; 10.000}`, mediana dos mínimos de bloco por `N`, ajuste OLS
de `log(mediana) vs log(N)`, IC bootstrap 95% em `β` (10.000 réplicas).
`zeros5.txt` (regime #10²²) reservado, não baixado, para o Gate.

## Resultado: decisivo

`β` observado = **-0,3395**, quase exatamente a previsão GUE de
**-1/3 = -0,3333** (diferença ~0,006). IC 95% = **[-0,3872; -0,2868]** —
contém -1/3 folgadamente, exclui -1 (Poisson) com folga grande.
Mais limpo e decisivo que o teste anterior desta linha (que teve
significância só em `c=0,30`).

## Revisão adversarial: `CONFIRMED`

Reprodução independente bit a bit (medianas de bloco a 8 casas decimais,
`β` idêntico verificado por três métodos: equações normais, `np.polyfit`,
`scipy.stats.linregress`). Nenhum bug de código. Único defeito
encontrado: erro de digitação cosmético no texto do pré-registro travado
(diz "99, 99, 49, 19, 9 blocos", deveria ser "199, 99, 49, 19, 9" —
`floor(99999/500)=199`) — não corrigido por estar no documento travado, e
não se propagou para nenhum cálculo em nenhum dos dois scripts (ambos
usam divisão inteira correta).

**Checagens de robustez adicionais:**
- Verificação numérica direta de que a Wigner surmise GUE tem expoente
  próximo de zero exatamente igual a 2 (não assumido).
- Checagem bônus: expoente GOE (-1/2) também cai fora do IC — discrimina
  especificamente a classe de universalidade GUE, não só "GUE vs.
  aleatório".
- Remover qualquer extremo da grade de `N` (4 pontos em vez de 5)
  preserva o veredito qualitativo em ambos os casos.
- Ressalva legítima: com apenas 9 blocos em `N=10000`, o bootstrap da
  mediana tem discretização conhecida na literatura estatística (Bickel
  & Freedman 1981) — afeta a precisão do IC nesse ponto extremo, não a
  direção/magnitude da conclusão (confirmado pela checagem de robustez).

## Gate de Replicação completo (acionado a pedido do usuário) — resultado inconclusivo por falta de poder

Sem holdout selado declarado — cláusula de fallback aplicada, checagem
contra `zeros5.txt` (Odlyzko, regime #10²², γ≈1,37×10²¹, nunca baixado
nesta sessão antes). Terceiro agente independente baixou o arquivo,
verificou proveniência por conta própria (incluindo verificação de
conteúdo em precisão exata via `decimal.Decimal`, não `float64`, evitando
o mesmo risco de cancelamento catastrófico já visto no Gate do
teste-irmão), e escreveu implementação nova.

**Achado estrutural:** `zeros5.txt` tem apenas 10.000 zeros → 9.999
gaps — quase 10× menos que o primário (`zeros1.txt`, 99.999 gaps).
Insuficiente para a grade travada (até `N=10.000`): contagens de bloco
obtidas foram 19 (N=500), 9 (N=1.000), 4 (N=2.000), 1 (N=5.000), **0
(N=10.000 — estruturalmente impossível)**. Só `N=500` e `N=1.000`
atingem a barra de `≥8` blocos que o próprio pré-registro declara.
Restrito a esses dois pontos: IC=[-0,682; 0,116] — não-informativo
(inclui -1/3, 0, e -1/2 simultaneamente). A grade ingênua de 4 pontos
(contaminada por pontos de 1 e 4 blocos) dá IC=[-0,240; -0,097], mas o
próprio agente do Gate avaliou esse resultado como não confiável.

Adversário de nulo: artefato de precisão descartado (erro relativo
~0,016%, desprezível); nenhuma publicação prévia encontrada rodando este
teste específico nesta altura extrema; o caveat de bootstrap de amostra
pequena (já identificado no dataset primário) é estruturalmente pior
aqui, não apenas marginal.

**Veredito do Gate: `REPLICATION_FAILED` / `CLOSED_INCONCLUSIVO`** — não
por contradição com confiança, e não uma falha de processo (requisitos 1,
2 e 4 do Gate plenamente satisfeitos). O requisito 3 foi executado
honestamente, mas a fonte reservada acabou pequena demais para a grade
travada entregar uma checagem bem-poderada. Registrado com o mesmo peso
evidencial que um `REPLICATION_PASSED`.

**Lição de governança documentada em `03_REPLICATION_GATE/PROTOCOL.md`:**
ao reservar uma fonte de dado adicional para o Gate, verificar A PRIORI
que ela tem amostra suficiente para a grade já travada — não apenas que
existe em regime diferente.

## Estado final

`DISC-CLAIM-004`: `evidence_level: preregistered_confirmed` (achado
primário sobre `zeros1.txt`, 100k zeros — NÃO contradito pelo Gate).
`adversarial_review_verdict: CONFIRMED`. `replication_status:
REPLICATION_FAILED`, com nota explícita de que isso significa
inconclusivo por falta de poder, não contradição. `promoted_to_formal_lab:
false` — confirmação numérica de universalidade GUE já conhecida na
literatura, não descoberta matemática nova.

## Próxima decisão (não tomada nesta sessão)

Não há mais fonte adicional de Odlyzko disponível no regime #10²² para
resolver a falta de poder sem consumir dado já usado. Seguir para
`DISC-TRI-RG-001`, ou considerar as duas linhas RH-REAL já executadas
(gap-runs `REPLICATION_PASSED`, escala de valor extremo
`preregistered_confirmed` com Gate inconclusivo) suficientes por ora.
