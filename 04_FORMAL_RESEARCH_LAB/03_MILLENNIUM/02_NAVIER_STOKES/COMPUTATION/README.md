# COMPUTATION — NS-PRESSURE-001

## `restricted_euler.py`

Integra numericamente a equação de Euler restrita (restricted Euler
equation), o truncamento clássico do tensor gradiente de velocidade que
zera a parte anisotrópica e não-local do Hessiano de pressão e mantém só
a parte isotrópica (Vieillefosse 1982; forma fechada em Cantwell 1992,
*Phys. Fluids A* 4, 782–793 — ver `REVIEWS/AUDIT_REPORT.md` para a
citação verificada nesta sessão).

Sistema (dedução própria desta sessão, verificada simbolicamente com
`sympy` — ver bloco abaixo):

```
dA/dt     = -A² + (1/3)tr(A²) I  -  (ω ωᵀ - (1/3)|ω|² I)
dω/dt     =  A ω
```

com `A` = parte simétrica sem traço do gradiente de velocidade (taxa de
deformação), `ω` = vetor de vorticidade associado à parte antissimétrica
via `Ω_v x = v × x`.

Identidades usadas na dedução (verificadas simbolicamente nesta sessão
com `sympy`, 3×3 genérico):

```
tr(A Ω) = 0                         para A simétrica, Ω antissimétrica
Ω_v²    = v vᵀ - |v|² I
tr(Ω_v²) = -2|v|²
```

### O que o experimento testa

A hipótese sob auditoria (Passo 2 do esboço legado, "Alignment Gap":
`⟨α₁⟩ ≤ 1-δ₀` onde `α₁ = cos²(ω, e₁)` e `e₁` é o autovetor de maior
autovalor de `A`) é tratada aqui como uma afirmação **testável mesmo
isolada** do resto da cadeia: se o desalinhamento com `e₁`, por si só,
já bastasse para impedir blow-up, um sistema autônomo onde esse
desalinhamento é extremo não deveria explodir em tempo finito.

### Resultado (6/6 casos aleatórios, ver `restricted_euler_output.log`)

Em todos os 6 casos com condição inicial genérica (gerador de números
aleatórios com seed fixa, `numpy.random.default_rng(12345)`):

- o sistema explode em tempo finito (`|A| → 1000` em `t* ≈ 2.4`–`6.1`),
  reproduzindo o resultado clássico de Vieillefosse ("Vieillefosse
  tail");
- ao longo de toda a cauda da trajetória (últimos 20% dos passos antes
  do blow-up), `cos²(ω, e₁) → 0` — a vorticidade fica *quase
  perfeitamente desalinhada* de `e₁`, não alinhada;
- em vez disso, a vorticidade se alinha quase perfeitamente
  (`|cos(ω,e_mid)| ≈ 1`) com o autovetor **intermediário** — reproduzindo
  qualitativamente o achado empírico de Ashurst–Kerstein–Kerr–Gibson
  (1987, *Phys. Fluids* 30, 2343) em DNS de turbulência homogênea.

### Leitura para a auditoria

Isto é um contraexemplo concreto e verificado por computação (não uma
citação de terceiros) à afirmação de que "`⟨α₁⟩` limitado afastado de 1"
é, por si só, um mecanismo suficiente para impedir blow-up: aqui `α₁`
está *extremamente* afastado de 1 (perto de 0) exatamente na trajetória
que explode. Ver `COUNTEREXAMPLES/restricted_euler_alignment_gap.md`
para a discussão completa, incluindo o que este resultado NÃO mostra
(não é um contraexemplo às equações de Navier–Stokes completas, porque
o termo anisotrópico e não-local do Hessiano de pressão — exatamente o
termo que a hipótese Tamesis atribui o papel regularizador — foi
descartado por construção nesta truncagem).

### Reprodutibilidade

```
python3 -m pip install numpy scipy sympy
python3 restricted_euler.py
```

Ambiente usado nesta sessão: `numpy`/`scipy` instalados via pip no
momento da execução (09/08/2026); sem GPU, sem dependências externas
além de `numpy`, `scipy`. Saída bruta salva em
`restricted_euler_output.log`.
