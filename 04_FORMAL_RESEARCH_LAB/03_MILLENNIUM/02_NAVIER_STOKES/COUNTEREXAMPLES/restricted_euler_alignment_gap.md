# Contraexemplo: "gap de alinhamento" isolado não impede blow-up

work_item: NS-PRESSURE-001
status: verificado nesta sessão (computação própria, Python/scipy + sympy)
escopo: refuta a forma NUA/isolada da hipótese; NÃO refuta (nem pode
refutar) as equações de Navier–Stokes completas — ver seção "O que isto
não mostra".

## Afirmação testada

A hipótese sob auditoria, isolando o Passo 2 ("Alignment Gap") do
esboço legado (`RECURSOS_PARA_PESQUISA/07_MILLENNIUM_VALIDATION/PROBLEM_03_NAVIER_STOKES/ANALISE_CRITICA_NS.md`):

> Se a média temporal do alinhamento `α₁ = cos²(ω, e₁)` entre a
> vorticidade `ω` e o autovetor `e₁` de maior autovalor da taxa de
> deformação `A` fica limitada, `⟨α₁⟩ ≤ 1-δ₀` com `δ₀ > 0` fixo, isso já
> é (via Passo 3, "Stretching Reduction") uma barreira contra o
> crescimento descontrolado da vorticidade.

## Construção do teste

Equação de Euler restrita (restricted Euler equation, Vieillefosse
1982), um sistema autônomo de dimensão finita (8 graus de liberdade:
`A` simétrica sem traço 3×3 + `ω` ∈ ℝ³) obtido zerando a parte
anisotrópica e não-local do Hessiano de pressão no gradiente de
velocidade completo — ver `COMPUTATION/restricted_euler.py` para a
dedução e as identidades algébricas verificadas simbolicamente
(`sympy`) nesta sessão.

Este sistema é escolhido precisamente porque é o modelo canônico, já
na literatura desde 1982, em que **não há** contribuição regularizadora
do Hessiano de pressão anisotrópico — é o "pior caso" possível para
qualquer hipótese que dependa desse termo.

## Resultado observado (6/6 condições iniciais aleatórias, seed fixa)

```
caso        blow-up?    t*        cos²(ω,e1) na cauda    cos(ω,e_mid) na cauda
random-0    sim         2.41      ≈ 0.00 (média 0.0024)  ≈ 1.0000
random-1    sim         4.84      ≈ 0.00 (média 0.0152)  ≈ 0.9995
random-2    sim         6.12      ≈ 0.00 (média 0.0203)  ≈ 0.9992
random-3    sim         4.22      ≈ 0.00 (média 0.0038)  ≈ 0.9999
random-4    sim         3.84      ≈ 0.00 (média 0.0045)  ≈ 0.9993
random-5    sim         4.21      ≈ 0.00 (média 0.0008)  ≈ 1.0000
```

(saída bruta completa em `../COMPUTATION/restricted_euler_output.log`)

Em todos os casos: o sistema explode em tempo finito, E a vorticidade
fica extremamente desalinhada de `e₁` (`α₁ → 0`, muito mais forte que
qualquer `δ₀ < 1` proposto — inclusive o `δ₀ ≈ 0.85` citado no
documento legado a partir de DNS). A vorticidade se alinha, em vez
disso, com o autovetor intermediário — reproduzindo qualitativamente o
achado clássico de Ashurst, Kerstein, Kerr & Gibson (*Phys. Fluids* 30,
2343, 1987; ver `REVIEWS/AUDIT_REPORT.md` para a citação verificada).

## Conclusão da auditoria sobre este ponto

`⟨α₁⟩` pequeno (desalinhamento com `e₁`) NÃO é, por si só, incompatível
com blow-up em tempo finito — dentro do sistema onde esse
desalinhamento é mais extremo que em qualquer simulação de Navier–Stokes
real, o blow-up acontece de qualquer forma. Isso significa que o Passo 2
("Alignment Gap") do esboço legado, tomado isoladamente, **não carrega
nenhum conteúdo regularizador**; todo o trabalho anti-blow-up teria de
vir do Passo 3 ("Stretching Reduction") — que por sua vez, no documento
legado, depende do Lemma 3.1 ("Rotation Dominance"), explicitamente
marcado lá como `🔴 NÃO PROVADO`.

Isto é uma **correção** ao esboço legado, não uma refutação de
Navier–Stokes: mostra que a arquitetura do argumento (Passo 2 ⟹ ... ⟹
regularidade) está mal-ordenada — o alinhamento por si só não é a
barreira; a barreira, se existir, tem de estar inteiramente na
desigualdade quantitativa de taxa do Lemma 3.1, que compara a
velocidade com que o desalinhamento ocorre com a velocidade do próprio
"stretching". Essa desigualdade de taxa é exatamente o termo
anisotrópico e não-local do Hessiano de pressão que a Euler restrita, e
este contraexemplo, descartam por construção.

## O que isto NÃO mostra

- **Não é** um contraexemplo às equações de Navier–Stokes completas.
  O modelo restricted Euler descarta por construção exatamente o termo
  (Hessiano de pressão anisotrópico, não-local, tipo Biot–Savart) ao
  qual a hipótese Tamesis atribui o papel regularizador. Um crítico
  poderia responder, corretamente, que "é claro que sem esse termo há
  blow-up — o ponto da hipótese é que o termo existe e o impede".
- **Não decide** se a versão quantitativa e completa da hipótese
  (Lemma 3.1 + Passos 3-6) é verdadeira para soluções reais de
  Navier–Stokes. Isso continua em aberto — ver `REVIEWS/AUDIT_REPORT.md`,
  seção "Aproximado", e `GAP_REGISTER.yaml`.
- **Não é** uma simulação de Navier–Stokes 3D; é um sistema de EDOs de
  dimensão finita (8 graus de liberdade), clássico na literatura desde
  1982. Nenhuma afirmação universal sobre Navier–Stokes é promovida a
  teorema a partir deste cálculo (`AGENTS.md`: "Python nunca promove uma
  afirmação universal a T").

## Reprodutibilidade

Script: `../COMPUTATION/restricted_euler.py`.
Saída bruta: `../COMPUTATION/restricted_euler_output.log`.
Rodado nesta sessão em 2026-08-09, `numpy`/`scipy`/`sympy` instalados
via `pip` no container.
