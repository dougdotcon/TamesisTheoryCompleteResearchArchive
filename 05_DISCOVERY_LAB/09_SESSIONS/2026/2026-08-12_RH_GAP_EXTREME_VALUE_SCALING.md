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

## Estado final

`DISC-CLAIM-004` registrado: `evidence_level: preregistered_confirmed`,
com nota explícita de que o IC discrimina GUE de Poisson decisivamente
mas NÃO tem precisão para confirmar o expoente exato -1/3 contra outros
valores próximos não motivados teoricamente — a interpretação GUE é
justificada pela fundamentação teórica independente, não pela proximidade
numérica isolada. `adversarial_review_verdict: CONFIRMED`.
`replication_status: NOT_SUBMITTED` — Gate de Replicação completo ainda
não acionado. `promoted_to_formal_lab: false` — confirmação numérica de
universalidade GUE já conhecida na literatura, não descoberta matemática
nova.

## Próxima decisão (não tomada nesta sessão)

Acionar o Gate de Replicação completo para `DISC-CLAIM-004` (exigiria
baixar `zeros5.txt`, regime #10²², ainda reservado), ou considerar este
resultado suficientemente estabelecido e seguir para `DISC-TRI-RG-001`.
