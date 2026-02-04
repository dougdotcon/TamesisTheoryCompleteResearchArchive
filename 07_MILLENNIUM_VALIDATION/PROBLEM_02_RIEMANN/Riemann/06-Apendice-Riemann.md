# 6_Appendix_Riemann

*Convertido de: 6_Appendix_Riemann.PDF*

---


## Página 1


Appendix:
Ergänzende
Formalia
zur
Resonanz-Operator-Theorie
Jeanette Leue
21. September 2025
1 Einleitung
Dieses Dokument ergänzt das Hauptmanuskript. Es enthält formale Details zu Operator-Domänen,
Selbstadjungiertheit,
Spektralidentiﬁkation,
Spurformeln
sowie
numerische
Illustration
und
Referenzen.
2 Domäne und Selbstadjungiertheit von H
Wir beginnen mit der Konstruktion des Gesamthilbertraums. Sei W=∏
p∈P0p ein Produkt der ersten
Primzahlen. Die zulässigen Restklassen sind
RW={r∈{1,,W}∣gcd(r,W)=1},|RW|=φ(W).
Damit deﬁnieren wir die diskrete und kontinuierliche Komponente
Hd=ℓ2(RW),Hc=L2(),
sowie das Tensorprodukt als Gesamtraum
=Hd⊗Hc.
Diskreter Generator. Die zyklische Verschiebung auf RW deﬁniert einen unitären Operator S auf
Hd. Nach dem Spektralsatz existiert ein selbstadjungierter Operator K mit
S=e-iK,σ(K)={2πmφ(W):m=0,1,,φ(W)-1}.
Primwellen-Operator. Auf deﬁnieren wir
P=-id
dx,D(P)=H
1(),
und
H=K⊗I+I⊗P,D(H)=Hd⊗H1().
Selbstadjungiertheit. Da K⊗I beschränkt und selbstadjungiert ist (endlichdimensional), und I⊗P
selbstadjungiert
auf
Hd⊗H1(),
und
beide
stark
kommutieren,
folgt
nach
dem
Satz
von
Nelson/Kato–Rellich, dass H auf D(H) selbstadjungiert ist.
3 Spektrum und Nullstellen
Das Spektrum des Operators H ergibt sich als Minkowski-Summe der Spektren
seiner beiden
1


## Página 2


Komponenten. Es gilt
σ(H)=σ(K)+σ(P).
Für den diskreten Teil K gilt
σ(K)={2πmφ(W):m=0,1,,φ(W)-1}.
Für den kontinuierlichen Teil P=-iddx auf L
2() gilt
σ(P)=.
Damit folgt
σ(H)={2πmφ(W):m=0,,φ(W)-1}+.
Bezug zur Riemannschen Zetafunktion. Die nichttrivialen Nullstellen der Zetafunktion
ζ(s)=0,s=12+iρ,
sind durch ihre imaginären Teile ρ bestimmt.
Die Spektralhypothese lautet:
σ(H)={ℑ(ρ):ζ(12+iρ)=0}.
Ist diese Identität korrekt, so liegen alle nichttrivialen
Nullstellen auf der kritischen Geraden
ℜ(s)=12.
4 Spurformel und Distributionen
Die Spurformel verknüpft das Spektrum des Operators H mit arithmetischen Größen, insbesondere
mit der von Mangoldt-Funktion Λ(n).
Regulierte Spur. Für eine glatte Testfunktion φ∈() deﬁnieren wir die regulierte Spur von H durch
Trφ(H)=∑
λ∈σ(H)φ(λ).
Da σ(H) kontinuierlich ist, wird diese Spur im distributionellen Sinn verstanden.
Explizite Formel. Formal ergibt sich eine Identität der Gestalt
∑
∞
n=1Λ(n)φ(logn)=̂φ(0)-∑ρ̂φ(ℑρ)+(Restterme),
wobei
die
Summe
rechts
über
die
nichttrivialen
Nullstellen
ρ
von
ζ(s)
läuft
und
̂φ
die
Fourier-Transformierte von φ bezeichnet.
Interpretation. Die Spurformel macht sichtbar, dass die Primzahlen über die Mangoldt-Funktion
Λ(n) als Resonanzen im Spektrum von H erscheinen, während die Nullstellen der Zetafunktion als
Spektralresonanzen auf der rechten Seite stehen.
Damit wird die zentrale Brücke zwischen Arithmetik und Spektraltheorie geschlagen.
5 Numerische Illustration
Um die Spektralhypothese anschaulich zu machen, betrachten wir die Hardy-Z-Funktion
Z(t)=e
iθ(t)ζ(12+it),θ(t)=ℑ(logΓ(14+it2))-t2logπ.
2


## Página 3


Sie erfüllt Z(t)∈für t∈, und ihre Nullstellen entsprechen genau den Nullstellen von ζ(s) auf der
kritischen Geraden.
Erste Nullstellen. Die ersten numerisch berechneten Nullstellen von Z(t) liegen bei
t≈14.1347,21.0220,25.0109,30.4249,32.9351,37.5862,40.9187,43.3271,48.0052,49.7738,
Interpretation. An diesen Punkten wechselt Z(t) das Vorzeichen. Jede solche Nullstelle ist eine
Resonanzfrequenz, die im Spektrum des Operators H erscheint. Dadurch bestätigt die Hardy-Z
-Funktion numerisch die Spektralhypothese.
Verbindung
zur
Primzahlverteilung.
Die
Verteilung
der
Nullstellen
erklärt
die
feinen
Schwankungen in der Primzahlzählfunktion π(x) und in der Chebyshev-Funktion
ψ(x)=∑
n≤xΛ(n).
Numerische Vergleiche zeigen, dass die Oszillationen
von
ψ(x) direkt mit den
Nullstellen
der
Zetafunktion korrespondieren.
6 Literatur
E.C. Titchmarsh, The Theory of the Riemann Zeta-Function, Oxford University Press, 2nd edition,
revised by D.R. Heath-Brown, 1986.
H.M. Edwards, Riemann's Zeta Function, Dover Publications, 2001.
A. Connes, Trace Formula in Noncommutative Geometry and the Zeros of the Riemann Zeta
Function, Selecta Mathematica (New Series) 5, 29–106 (1999).
M. Reed, B. Simon, Methods of Modern Mathematical Physics I: Functional Analysis, Academic
Press, 1980.
H.L. Montgomery, Ten Lectures on the Interface Between Analytic Number Theory and Harmonic
Analysis, CBMS Regional Conference Series in Mathematics, 1994.
H. Iwaniec, E. Kowalski, Analytic Number Theory, American Mathematical Society Colloquium
Publications, Vol. 53, 2004.
3
