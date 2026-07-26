# Tamesis M_c v1.0: uma hipótese auditável de transição quântico–clássica

**Status:** especificação fenomenológica; não é prova nem confirmação experimental.

## Resumo

O programa Tamesis propõe uma escala de massa crítica associada a uma limitação
holográfica da coerência quântica. Esta versão reduz o programa a uma única
hipótese: uma taxa intrínseca de perda de visibilidade que é nula abaixo de
\(M_c\) e cresce quadraticamente acima dele. O valor de \(M_c\) é obtido de uma
relação de escala entre a massa e a aceleração de Planck e \(a_0=cH_0\). O
expoente \(1/8\), o limiar duro e a independência ambiental permanecem hipóteses
a serem testadas. O documento fornece números, comparadores e critérios de
falsificação sem afirmar que a teoria já foi validada.

## 1. Escopo

O Tardis/Tamesis original identificou \(M_c\) como uma previsão mesoscópica
mais limpa que as alegações cosmológicas amplas. Esta versão não tenta resolver
gravidade quântica, Riemann, \(P\) versus \(NP\) ou a origem do Modelo Padrão.
Esses problemas não entram como premissas ocultas.

## 2. Definição do modelo

Usamos as constantes \(G\), \(\hbar\), \(c\) e uma entrada cosmológica \(H_0\):

\[
 m_P=\sqrt{\frac{\hbar c}{G}},\quad
 a_P=\frac{c^2}{\ell_P},\quad
 \ell_P=\sqrt{\frac{\hbar G}{c^3}},\quad a_0=cH_0.
\]

A hipótese de escala é

\[
 M_c=m_P\left(\frac{a_0}{a_P}\right)^{1/8}.
\]

Para uma esfera de sílica de densidade \(\rho_s\), definimos apenas uma escala
geométrica auxiliar:

\[
 R_c=\left(\frac{3M_c}{4\pi\rho_s}\right)^{1/3}.
\]

A escala temporal adotada, explicitamente convencional, é a inversa da energia
de auto-gravidade \(E_g=GM_c^2/R_c\):

\[
 \tau_c=\frac{\hbar R_c}{GM_c^2}.
\]

O modelo de taxa é

\[
 \Gamma_T(M)=
 \begin{cases}
 0,& M\le M_c,\\
 \tau_c^{-1}(M/M_c)^\alpha,&M>M_c,
 \end{cases}
 \qquad \alpha=2.
\]

Para um experimento com taxa ambiental independente \(\Gamma_e\),

\[
 V(t|M)=V_0\exp[-(\Gamma_T(M)+\Gamma_e)t].
\]

Não se deve atribuir a \(\Gamma_T\) qualquer perda de contraste antes de
estimar \(\Gamma_e\) com controles de massa, pressão, temperatura, potência
óptica e separação espacial.

## 3. Números de referência

Com \(H_0=70\) km s⁻¹ Mpc⁻¹ e \(\rho_s=2200\) kg m⁻³:

\[
M_c=5.292674\times10^{-16}\;\mathrm{kg},\quad
R_c=3.85823\times10^{-7}\;\mathrm{m},\quad
\tau_c=2.17625\;\mathrm{s}.
\]

O ponto importante é a descontinuidade de uma face:
\[
\Gamma_T(M_c^-)=0,\qquad
\Gamma_T(M_c^+)=0.4595\;\mathrm{s}^{-1}.
\]

## 4. Comparação com hipóteses concorrentes

Decoerência ambiental, CSL e Diósi–Penrose podem produzir diminuição suave
de visibilidade e dependência em separação, temperatura, pressão ou tamanho.
Tamesis v1.0 faz três afirmações mais restritivas: (i) limiar em massa, (ii)
lei quadrática acima dele e (iii) componente residual que não escala com
isolamento ambiental. O teste deve comparar modelos por likelihood, incluindo
todos os parâmetros de nuisance, e não por inspeção de gráficos.

## 5. Protocolo experimental mínimo

O experimento deve medir uma série de massas próximas a \(0.5,0.9,1.0,1.01,
2,5,10\,M_c\), mantendo geometria, separação e preparação constantes. Para
cada massa devem existir controles ambientais e repetição cega. O resultado
primário é a taxa total ajustada; o resultado secundário é sua dependência em
isolamento. A análise deve ser registrada antes de abrir os dados finais.

## 6. Falsificação

Rejeitamos o modelo se não houver salto de taxa, se o expoente posterior não for
compatível com \(2\) dentro do intervalo pré-registrado, se o termo residual
diminuir com isolamento, ou se houver interferência persistente com
\(V>0.5\) por mais de um segundo em \(M\ge10^{-14}\) kg.

Esses critérios são fortes; um resultado nulo é um resultado útil. Ajustar
\(M_c\), \(\alpha\) ou \(\tau_c\) depois de observar os dados não conta como
teste da versão 1.0.

## 7. O que ainda não foi demonstrado

- a origem matemática do expoente \(1/8\);
- uma dinâmica microscópica que viole unitariedade;
- a universalidade do limiar para materiais e preparações diferentes;
- separação experimental de colapso intrínseco e decoerência convencional;
- qualquer confirmação observacional.

Portanto, este documento é um protocolo de pesquisa e não uma reivindicação de
descoberta.
