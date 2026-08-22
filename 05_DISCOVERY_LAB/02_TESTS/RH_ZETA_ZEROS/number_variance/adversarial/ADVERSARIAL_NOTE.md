# Nota adversarial — plano ANTES de rodar qualquer coisa

**Papel:** agente de reprodução adversarial, independente do agente primário de
`DISC-RH-NUMBER-VARIANCE-001`. Escopo travado pelo orquestrador: atacar
especificamente a exclusão GUE (Modelo A) nos dois pontos decisivos primários
(`zeros1`, `L=2155.04`, `B=11`; `zeros3`, `L=210.50`, `B=11`) e verificar se o
veredito ternário formal (`INCONCLUSIVE`/`PARTIAL_DISAGREEMENT`) se reproduz.

**Disciplina seguida até este ponto:** só li `PREREGISTRATION.md` e
`DESIGN.json` do teste primário (a especificação travada), mais os formatos
brutos de `data/zeros1.txt`, `data/zeros3.txt`, `data/zeros4.txt` (só cabeçalho,
para entender formato — não toquei em `zeros4.txt` além do cabeçalho de texto)
e `data/PROVENANCE.md` (proveniência dos dados, não resultado nenhum). **Não
li** `estimator.py`, `run_primary.py`, `primary_result.json`, nem nenhum
`validate_*.py`/`.log`/`.json` do primário — só farei isso na Etapa 6, depois
de travar meus próprios números.

Além disso, busquei a fonte primária do Modelo A/B de forma independente:
fiz fetch direto de `arxiv.org/pdf/2211.14918` (Lugar, Milinovich,
Quesada-Herrera) e li as páginas 8–9 (Conjectura 1.4.1, notação, definições de
`N(E)`, `x_m`, `n(L;x)`, `V(L;x)`). **A fórmula do Modelo A e do Modelo B
transcritas no `PREREGISTRATION.md` batem exatamente com o paper original**
(inclusive as definições de `Si`/`Ci` — `Si(x)=∫₀ˣ sin(u)/u du`,
`Ci(x)=-∫ₓ^∞ cos(u)/u du`). Isto substitui a necessidade de "não confiar" na
transcrição do primário — verifiquei contra a fonte, não contra a
transcrição.

## Plano

1. **Estimador `V(L;x)` do zero.** Implementar a definição exata da Seção 1.1
   do pré-registro (idêntica à eq. antes da Conjectura 1.4.1 do paper): função
   em escada `n(L;y)`, saltos em `y=x_m-L/2` (+1) e `y=x_m+L/2` (−1), integral
   exata de `[n(L;y)-L]²` por trechos entre pontos de quebra consecutivos.
   Esquema de blocos: `B` blocos de largura uniforme via
   `np.linspace(x_min,x_max,B+1)`; janela `y` restrita ao interior
   `[a+L/2,b-L/2]` de cada bloco; blocos com largura `<3L` descartados;
   `V̂=média dos blocos`, `SE=desvio padrão entre blocos (ddof=1)/√B`.
   Implementação própria, sem olhar `estimator.py`.

2. **Validação sintética ANTES de tocar dado real:**
   - (a) Rede regular (espaçamento determinístico 1): `V̂` deve ficar próximo
     de 0.
   - (b) Processo de Poisson (taxa 1): `V̂(L)` deve recuperar `L` dentro do
     erro padrão, na mesma grade de `L` usada na análise real.
   - (c) Checagem por força bruta: comparar a integral exata por quebra de
     pontos contra integração numérica em grade fina independente, em caso
     pequeno.
   - (d) Checagem analítica do Modelo A: verificar em código simbólico/
     numérico que o termo `π²L` se cancela exatamente contra
     `-2πL·Si(2πL)` no limite `L→∞` (`Si(∞)=π/2`), produzindo o crescimento
     log-lento `(1/π²)[log(2πL)+γ₀+1]` citado no pré-registro — checagem
     interna contra erro de transcrição de sinal/termo.
   - (e) Opcional se sobrar tempo: construção de matriz GUE com convenção de
     Mehta (`P(H)∝exp(-Tr H²/2)`: diagonal `~N(0,1)`, partes real/imaginária
     fora da diagonal `~N(0,1/2)` cada) — verificar borda espectral empírica
     `≈2√N` diretamente (sem simetrizar amostra independente, exatamente o
     modo de evitar o Bug 1 do primário).
   - Logs de validação salvos mesmo se algum passo falhar na primeira
     tentativa (preservar falha, corrigir, não apagar).

3. **Modelo A** — fórmula fechada de Berry 1.4.1(a), verificada contra o PDF
   original nesta sessão (ver acima). **Modelo B** — fórmula 1.4.1(b), soma
   sobre potências de primos `Λ(n)²/(n log²n)`, com a mesma identidade
   algébrica `Λ(p^k)²/(p^k log²(p^k)) = 1/(k²p^k)` citada no pré-registro
   (vou re-derivar essa identidade eu mesmo, não vou só confiar). `zeros1`:
   soma exata (crivo até `T≈74920.8`). `zeros3`: cota bilateral via Mertens
   com `P_cutoff=2×10⁸` (do `DESIGN.json`), mesmo método declarado na Seção 5
   do pré-registro.

4. **Dados reais.** `zeros1.txt`: γ absoluto por linha, `x=N(γ)`. `zeros3.txt`:
   offsets de `base=267653395647` (confirmado no cabeçalho do arquivo),
   `x=offset·N'(base)`, `N'(E)=(1/2π)log(E/2π)` — linearização local. Vou
   computar `V̂(L)` na grade COMPLETA de `DESIGN.json` (não só nos 2 pontos
   primários) para poder comparar a curva descritiva inteira e o padrão
   "23/23 pontos mais perto do Modelo B" citado no resultado do primário — mas
   o veredito adversarial formal foca nos 2 pontos decisivos primários
   (Seção 4 do pré-registro). `zeros4.txt` **não será tocado** em nenhuma
   linha de dado numérico.

5. **Comparação.** Só depois de travar meus `V̂`, `z_A`, `z_B` nos pontos
   primários (e na grade completa) é que vou ler `estimator.py`,
   `run_primary.py`, `primary_result.json`, `validate_*.{py,json,log}` e
   comparar célula a célula. Qualquer discrepância além de ruído numérico
   (~0.1%) será investigada até explicada.

6. **Entregáveis** nesta pasta: este arquivo, `estimator_adv.py`,
   `validate_lattice.py`, `validate_poisson.py`, `validate_bruteforce.py`,
   `validate_model_a_asymptotic.py`, `model_b_adv.py`, `run_adv_primary.py`,
   resultados/logs em JSON, e `ADVERSARIAL_VERDICT.md` (em português) com
   tabela comparativa final.

**Orçamento:** computação em primeiro plano, sem processos de fundo, meta de
runtime total ~2h. Nenhuma alegação sobre RH em nenhuma hipótese. Holdout
`zeros4` permanece selado.
