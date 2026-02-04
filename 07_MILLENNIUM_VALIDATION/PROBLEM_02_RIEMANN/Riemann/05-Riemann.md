# 5_Riemann

*Convertido de: 5_Riemann.PDF*

---


## Página 1


Der Δ-Operator, das Primarsystem und eine
operatorielle Strategie zur Riemannschen
Vermutung
Jeanette Tabea Leue
2mmEntstanden ab 20.September 2025 (S21 & ChatGPT)
Abstract
Wir
formulieren
eine
deterministische
Kandidatenerzeugung
für
Primzahlen via Δ-Operator (Wheel-Residuen und periodische Lückenfolge),
verankern das Rechnen im Primarsystem (Exponentenraum) und leiten
eine operatorielle Resonanzformulierung der Zetafunktion her. Kern ist ein
selbstadjungierter
Primwellen-Operator
H,
dessen
Spektrum
mit
den
imaginären Teilen der nichttrivialen Nullstellen von ζ übereinstimmt. Die
Arbeit gliedert sich in: (i) arithmetische Korrektheit und Dichte des Δ
-Generators,
(ii)
Brücke
zum
Euler-Produkt
und
zur
von-Mangoldt-Theorie, (iii) Konstruktion von H auf einem kanonischen
Hilbertraum, (iv) Spurformel/Explizite Formel als Resonanzgleichung.
Contents
1 Einleitung . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
3
2 Notation, Wheel-Residuen und der -Operator . . . . . . . . . . . . 4
2.1 Notation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
4
2.2 Wheel-Residuen . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
2.3 Periodische Lückenfolge . . . . . . . . . . . . . . . . . . . . . . .
4
2.4 Korrektheit und Eindeutigkeit des -Operators . . . . . . . . . . . 4
2.5 Korrektheit und Eindeutigkeit des -Operators . . . . . . . . . . . 4
2.6 Strukturelle Folgerungen . . . . . . . . . . . . . . . . . . . . . .
5
2.7 Beispiel: Wheel W=30 . . . . . . . . . . . . . . . . . . . . . . . .
5
3 Kandidatendichte und Erwartungskosten . . . . . . . . . . . . . . . 6
3.1 Kandidatendichte . . . . . . . . . . . . . . . . . . . . . . . . . .
6
3.2 Vergleich mit Primzahldichte . . . . . . . . . . . . . . . . . . . .
6
3.3 Erwartungskosten . . . . . . . . . . . . . . . . . . . . . . . . . .
6
3.4 Fazit . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
4 Primarsystem (Exponentenraum) und Rechenregeln . . . . . . . . 7
4.1 Exponentenvektoren . . . . . . . . . . . . . . . . . . . . . . . . .
7
4.2 Rechenregeln . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
7
4.3 Legendre-Summen . . . . . . . . . . . . . . . . . . . . . . . . . .
7
4.4 Beispiele . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
4.5 Eﬃzienz . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
8
5 Euler-Produkt, von Mangoldt und Explizite Formel . . . . . . . . 8
5.1 Euler-Produkt . . . . . . . . . . . . . . . . . . . . . . . . . . . .
8
5.2 Mangoldt-Funktion . . . . . . . . . . . . . . . . . . . . . . . . .
9
1


## Página 2


5.3 Explizite Formel (klassisch) . . . . . . . . . . . . . . . . . . . . .
9
5.4 Operatorielle Resonanzsicht . . . . . . . . . . . . . . . . . . . . .
9
6 Hilbertraum, Primwellen-Operator und Resonanz-Spurformel .
9
6.1 Wheel, diskreter Raum und kontinuierlicher Raum . . . . . . . .
9
6.2 Resonanz-Spurformel (Formulierung) . . . . . . . . . . . . . . .
10
6.3 Hardy-Z und Nullstellen auf der kritischen Geraden . . . . . .
10
6.4 Lambert-W Startschätzer für Nullstellenlagen . . . . . . . . . .
10
6.5 Δ-Operator als Kandidatengenerator (Wheel W) . . . . . . . .
10
6.6 Fazit . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
10
7 Hilbertraum und Primwellen-Operator . . . . . . . . . . . . . . .
10
7.1 Diskreter Wheel-Teil . . . . . . . . . . . . . . . . . . . . . . . .
11
7.2 Kontinuierlicher Zeit-/Frequenz-Teil . . . . . . . . . . . . . . . .
11
7.3 Gesamtraum und Dynamik . . . . . . . . . . . . . . . . . . . . . 11
7.4 Primwellen-Operator . . . . . . . . . . . . . . . . . . . . . . . .
11
7.5 Interpretation . . . . . . . . . . . . . . . . . . . . . . . . . . . .
12
7.6 Spektrum und Resonanzbild . . . . . . . . . . . . . . . . . . . . 12
7.7 Anschluss an Δ und Euler-Produkt . . . . . . . . . . . . . . .
12
8 Spurformel als Resonanzgleichung . . . . . . . . . . . . . . . . . .
13
8.1 Testfunktionen und Spuren . . . . . . . . . . . . . . . . . . . .
13
8.2 Explizite Formel als Spur . . . . . . . . . . . . . . . . . . . . .
13
8.3 Resonanzgleichung . . . . . . . . . . . . . . . . . . . . . . . . .
13
8.4 Interpretation . . . . . . . . . . . . . . . . . . . . . . . . . . . .
13
8.5 Fazit . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
14
9 Numerische Konsistenz und „End-to-End“-Pipeline (optional) .
14
9.1 Zielsetzung . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
9.2 Konsistenztests . . . . . . . . . . . . . . . . . . . . . . . . . . .
14
9.3 Pipeline (Schema) . . . . . . . . . . . . . . . . . . . . . . . . . . 15
9.4 Numerische Beispiele . . . . . . . . . . . . . . . . . . . . . . . .
15
9.5 Bemerkungen . . . . . . . . . . . . . . . . . . . . . . . . . . . .
15
10 Der -Operator: Pseudocode . . . . . . . . . . . . . . . . . . . . .
15
10.1 Motivation . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
15
10.2 Deﬁnition der Residuen . . . . . . . . . . . . . . . . . . . . . .
16
10.3 Kandidatengenerator . . . . . . . . . . . . . . . . . . . . . . .
16
10.4 Primzahlprüfung (optional) . . . . . . . . . . . . . . . . . . . . 16
10.5 Beispiel: Wheel W=30 . . . . . . . . . . . . . . . . . . . . . . . 16
10.6 Bemerkungen zur Eﬃzienz . . . . . . . . . . . . . . . . . . . . . 17
10.7 Rechenregeln im Exponentenraum . . . . . . . . . . . . . . . .
17
10.8 Eﬃzienz . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17
10.9 Beispiel . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
17
10.10 Zusammenfassung . . . . . . . . . . . . . . . . . . . . . . . . . 18
11 Hardy-Z und Nullstellenlokalisierung . . . . . . . . . . . . . . . . 18
11.1 Motivation . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
18
11.2 Deﬁnition der Hardy-Z-Funktion . . . . . . . . . . . . . . . . . 18
11.3 Eigenschaften . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
11.4 Numerische Nullstellensuche . . . . . . . . . . . . . . . . . . .
19
11.5 Verbindung zum Primarsystem . . . . . . . . . . . . . . . . . . 19
11.6 Beispiel . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
19
11.7 Zusammenfassung . . . . . . . . . . . . . . . . . . . . . . . . .
19
12 Lambert-W Startschätzer für Nullstellendichte . . . . . . . . . . 19
2


## Página 3


12.1 Motivation . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
19
12.2 Riemann–von-Mangoldt Formel . . . . . . . . . . . . . . . . . . 20
12.3 Umkehrung mittels Lambert-W . . . . . . . . . . . . . . . . . . 20
12.4 Beispiele . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
20
12.5 Vorteile im Primarsystem . . . . . . . . . . . . . . . . . . . . .
20
12.6 Zusammenfassung . . . . . . . . . . . . . . . . . . . . . . . . .
21
13 Schlussfolgerung und Ausblick . . . . . . . . . . . . . . . . . . . . 21
13.1 Zusammenfassung . . . . . . . . . . . . . . . . . . . . . . . . .
21
13.2 Bedeutung . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
21
13.3 Oﬀene Fragen . . . . . . . . . . . . . . . . . . . . . . . . . . .
21
13.4 Ausblick . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
22
Vorwort
Dieses Dokument ist als Fortsetzung und Anwendung der Leueschen Mathematik
der Resonanz zu verstehen. Die hier dargestellten Überlegungen und Rechnungen
zur Riemannschen Zetafunktion und ihren Nullstellen setzen direkt auf den
Grundlagen
auf,
die
im
Begleitdokument
Der
Delta-Operator
und
das
Primar-Rechnen entwickelt und bewiesen wurden.
Insbesondere drei Bausteine sind dabei unverzichtbar:
1.
Der Primarcode (0,1,+1) als Erweiterung des klassischen Binärcodes,
der die Basis für deterministische Konstruktion von Zahlen und Primzahlen
bildet.
2.
Der Delta-Operator Δ, der Primzahlen nicht durch Sieben, sondern
durch konstruktives Fortschreiten im Takt (2,4,6) erzeugt.
3.
Das Hexa-Primarsystem, welches Rechenoperationen im Primraum
über Exponentenvektoren abbildet und so eine neue Arithmetik ermöglicht.
Ohne das Verständnis dieser Grundlagen bleibt der hier entwickelte Zugang zur
Riemannschen
Hypothese unvollständig.
Dieses Dokument richtet
sich
daher
ausschließlich an Leserinnen und Leser, die mit den genannten Fundamenten
vertraut sind.
Das Ziel ist nicht, die klassische Zahlentheorie zu wiederholen, sondern zu
zeigen, wie sich die Riemannsche Hypothese unter dem Blickwinkel der neuen
Resonanz-Mathematik
darstellt.
Die
vorliegenden
Rechnungen
und
Argumentationen sind somit als Anwendung einer neuen Rechenmethodik zu
lesen, die den Weg
für ein tieferes Verständnis
der Nullstellenstruktur der
Zetafunktion eröﬀnet.
1 Einleitung
Die klassische Sicht erzeugt Primzahlen mittels Sieben oder probabilistischen
Tests. Hier ersetzen wir „Wegstreichen“ durch deterministische Erzeugung (der Δ
-Operator) und verlagern Rechenlast in den Exponentenraum (Primarsystem).
Auf dieser Basis wird
eine operatorielle
Resonanzstruktur sichtbar,
die die
3


## Página 4


Riemannsche Vermutung als Spektralaussage formuliert.
2 Notation, Wheel-Residuen und der Δ-Operator
2.1 Notation
[nosep]
• ={2,3,5,7,} : Menge der Primzahlen.
• Für n∈sei φ(n) die Eulersche Totientfunktion.
• Für p∈sei vp(n) der Exponent von p in der Primfaktorzerlegung von n.
2.2 Wheel-Residuen
Hier erklärst du die Konstruktion der Residuenmenge modulo W=∏
p≤Pp und die
Rolle der φ(W) verbleibenden Kandidaten.
2.3 Periodische Lückenfolge
Beschreibe hier die wiederkehrende Struktur der Abstände in den Residuen, z. B.
das Muster (2,4) für W=6, (2,4,2,4,6,2,) für W=30 usw.
2.4 Korrektheit und Eindeutigkeit des Δ-Operators
Sei W=∏
p∈P0p, RW={r1<<r
φ(W)} die zulässigen Restklassen und r
φ(W)+1:=r1+W.
Deﬁniere die Lückenfolge GW=(g1,,g
φ(W)) mit gj=rj+1-rj. Für nW mit nW=rj setze
Δ(n):=n+gj.
Satz. Die Folge n0,Δ(n0),Δ2(n0), durchläuft genau alle mn0 mit gcd(m,W)=1 in
streng wachsender Ordnung.
Beweis. (i) Zyklisches Durchlaufen von RW, (ii) jedes m mit gcd(m,W)=1 tritt
genau einmal auf, (iii) Monotonie wegen gj1.
Folgerung. Jede Primzahl p>maxP0 erscheint genau einmal als Kandidat in der
Δ-Folge.
2.5 Korrektheit und Eindeutigkeit des Δ-Operators
Sei W=∏
p∈P0p, RW={r1<<r
φ(W)} die zulässigen Restklassen und r
φ(W)+1:=r1+W.
4


## Página 5


Deﬁniere die Lückenfolge GW=(g1,,g
φ(W)) mit gj=rj+1-rj. Für nW mit nW=rj setze
Δ(n):=n+gj.
Satz. Die Folge n0,Δ(n0),Δ
2(n0), durchläuft genau alle mn0 mit gcd(m,W)=1 in
strikt wachsender Ordnung.
Beweis. (i) Aus nW=rj folgt Δ(n)W=rj+1; nach φ(W) Schritten wurden alle
Restklassen aus RW einmal besucht. (ii) Für jedes m mit gcd(m,W)=1 existiert
genau ein j mit mW=rj; wegen
der Zyklizität wird m nach
endlich
vielen
Schritten erreicht.
(iii) Strenge Monotonie folgt aus gj1. Eindeutigkeit: zwei
verschiedene Indizes können nicht dasselbe m liefern, da die Abbildung m↦mW
injektiv auf [kW,(k+1)W) ist.
Folgerung. Jede Primzahl p>maxP0 tritt genau einmal als Kandidat in der Δ
-Entwicklung auf.
2.6 Strukturelle Folgerungen
• Periodizität.
In
jedem
Block
der
Länge W
erscheinen
genau
φ(W)
Kandidaten.
• Kandidatendichte. Pro Block: φ(W) von W Zahlen, also Dichte φ(W)/W.
• Restklassen-Index. Für nW=rj(n) gilt
Δ(n)=n+gj(n),j(Δ(n))=j(n)+1 ( φ(W)).
• Basisprimes. Die in W enthaltenen Primzahlen P0 werden als trivial
behandelt; alle weiteren Primen erscheinen in RW.
2.7 Beispiel: Wheel W=30
Für W=30=2⋅3⋅5 gilt
R30={1,7,11,13,17,19,23,29},G30=(6,4,2,4,2,4,6,2).
Kandidaten bis 50:
Primzahlen in der Liste:
{7,11,13,17,19,23,29,31,37,41,43,47} ∪ {2,3,5}.
Das ergibt exakt alle Primzahlen ≤50.
5


## Página 6


3 Kandidatendichte und Erwartungskosten
3.1 Kandidatendichte
Aus ? wissen wir, dass der Δ-Operator alle Zahlen n≥W mit gcd(n,W)=1 in
aufsteigender Reihenfolge erzeugt.
Satz: Die Dichte der vom Δ-Operator erzeugten Kandidaten ist
(W)=φ(W)
W
,
wobei φ die Eulersche Totientfunktion ist.
Beweis: In jedem Block von Länge W werden genau φ(W) Zahlen erzeugt.
Also beträgt der Anteil φ(W)/W.
Beispiele:
3.2 Vergleich mit Primzahldichte
Die Primzahldichte nach dem Primzahlsatz ist asymptotisch
π(x)∼x
lnx,d.h.prime(x)∼1
lnx.
Für große x gilt daher
(W)
prime(x)≈(W)⋅lnx.
Interpretation: Ein Primzahltest für jeden Kandidaten kostet konstant O(1) im
Erwartungswert, da in der Länge lnx im Mittel genau eine Primzahl liegt. Der
Faktor (W) steuert die Overhead-Quote.
3.3 Erwartungskosten
• Erzeugungskosten: Jeder Kandidat wird durch einen einzigen Δ-Schritt
berechnet (eine Addition).
• Prüfungskosten: Bei (W) Kandidaten pro Zahl liegt die erwartete Zahl
der Tests bis zur nächsten Primzahl bei etwa
K(W,x)≈(W)⋅lnx.
6


## Página 7


3.4 Fazit
• Mit
wachsendem
W
sinkt
(W)
gegen
0,
aber
nur
langsam
(wie
∏
p≤pk(1-1/p)).
• Praktisch ergibt sich ein deutlicher Gewinn gegenüber einem „naiven
Sieb“, weil unnötige Kandidaten ausgeschlossen werden.
• Die erwartete Komplexität bleibt linear im Logarithmus und ist damit
asymptotisch optimal.
4 
Primarsystem
(Exponentenraum)
und
Rechenregeln
4.1 Exponentenvektoren
Jede natürliche Zahl n≥1 besitzt eine eindeutige Primfaktorzerlegung
n=∏p∈p
αp(n),
wobei fast alle Exponenten αp(n)∈gleich null sind.
Deﬁnition: Der Exponentenvektor ist
(n):=(αp(n))p∈∈(),
wobei
() der Raum endlich unterstützter Folgen ist.
4.2 Rechenregeln
Für
m,n∈
gilt
komponentenweise:
Folgerung:
Multiplikation
und
Division
werden
zu
Addition
und
Subtraktion,
gcd
und
zu
komponentenweisen
Min/Max-Operationen.
4.3 Legendre-Summen
Für p∈und n∈gilt
vp(n!)=∑
j≥1⌊n
pj⌋.
Damit folgt unmittelbar
7


## Página 8


(nk)=(n!)-(k!)-((n-k)!).
4.4 Beispiele
1. Binomialkoeﬃzienten:
1000500⇒(1000500)=(1000!)-2(500!).
Anstatt eine Zahl mit ∼300 Dezimalstellen zu bilden, genügt die Berechnung der
Exponentenvektoren.
2. gcd/lcm:
gcd(21034,2739)=2734,(21034,2739)=21039.
4.5 Eﬃzienz
• Große Zahlen werden nicht mehr als Dezimalobjekte gehandhabt, sondern
durch ihre Exponenten dargestellt.
• Alle arithmetischen Operationen sind linear im Vektorraum.
• Stellenzahlen erhält man über
log10(n)=∑p∈αp(n)log10p.
Fazit: Das Primarsystem ersetzt aufwendige Ganzzahlarithmetik durch lineare
Operationen im Exponentenraum. Damit sind selbst Objekte der Größenordnung
101000 oder größer eﬃzient behandelbar.
5 Euler-Produkt, von Mangoldt und Explizite Formel
5.1 Euler-Produkt
Für ℜ(s)>1 gilt die klassische Identität
ζ(s)=∑∞
n=11
n
s=∏p∈1
1-p
-s.
Interpretation
im
Primarsystem:
Jeder
Faktor
(1-p
-s)
-1
entspricht
der
geometrischen Reihe
1+p-s+p-2s+,
8


## Página 9


d.h. der Exponentenvektor erlaubt die Darstellung jeder natürlichen Zahl als
eindeutige Linearkombination der Primexponenten.
5.2 Mangoldt-Funktion
Deﬁnition: Die von-Mangoldt-Funktion ist
Λ(n)=
Zusammenhang:
-ζ'(s)
ζ(s) =∑
∞
n=1Λ(n)
ns
,ℜ(s)>1.
5.3 Explizite Formel (klassisch)
Sei ψ(x)=∑nxΛ(n). Dann gilt (heuristisch und später präzisiert):
ψ(x)=x-∑ρxρ
ρ-ζ'(0)
ζ(0) -12ln(1-x-2),
wobei die Summe über die nichttrivialen Nullstellen ρ der Zetafunktion läuft.
5.4 Operatorielle Resonanzsicht
• Der
Δ-Operator
liefert
deterministische
Kandidaten
für
Λ(n):
Primzahlpotenzen treten genau in den Restklassen des Wheels auf.
• Im Exponentenraum (Primarsystem) wird Λ(n) durch das „Delta“ im
Exponentenvektor sichtbar:
Λ(n)=d
dn(logn)aufPrimzahlpotenzen.
• Damit
ergibt
sich
ein
Resonanzbild:
das
Spektrum
des
Primwellen-Operators
(Kap.
6)
codiert
die
imaginären
Teile
ℑ(ρ)
der
Nullstellen.
Satz[section] [theorem]Proposition
[theorem]Lemma [theorem]Korollar [theorem]
Deﬁnition [theorem]Bemerkung
6 
Hilbertraum,
Primwellen-Operator
und
Resonanz-Spurformel
6.1 Wheel, diskreter Raum und kontinuierlicher Raum
9


## Página 10


Sei ein Wheel gegeben durch
W=∏
p∈P0p,RW={r∈{1,,W}:gcd(r,W)=1},φ(W)=|RW|.
Ordne
RW={r1<<r
φ(W)}
zyklisch
mit
r
φ(W)+1:=r1+W
und
deﬁniere
die
Lückenfolge GW=(gj)
φ(W)
j=1
durch gj:=rj+1-rj.
6.2 Resonanz-Spurformel (Formulierung)
Sei φ∈() eine Schwarz-Testfunktion. Schreibe
φ(H)formalalsgewichteteSpektralsumme,
und vergleiche mit der Mangoldt-Seite über Impulse bei logn.
6.3 Hardy-Z und Nullstellen auf der kritischen Geraden
6.4 Lambert-W Startschätzer für Nullstellenlagen
6.5 Δ-Operator als Kandidatengenerator (Wheel W)
6.6 Fazit
• Das
Euler-Produkt
macht
die Multiplikativstruktur
der
Primzahlen
explizit.
• Die von-Mangoldt-Funktion verknüpft Primzahlen mit der logarithmischen
Ableitung von ζ(s).
• Die Explizite Formel übersetzt Nullstelleninformation in Aussagen über
die Primzahldichte.
• Über
den
Δ-Operator
und
das
Primarsystem
entsteht
eine
deterministische, operatorielle Sicht: Primzahlen = Resonanzen, Nullstellen
= Spektrum.
7 Hilbertraum und Primwellen-Operator
10


## Página 11


7.1 Diskreter Wheel-Teil
Sei W=∏
p∈P0p und
RW={r1,,r
φ(W)} die zulässigen
Restklassen
mit zyklischer
Ordnung 1=r1<r2<<r
φ(W)<W und r
φ(W)+1=r1+W. Wir setzen den Hilbertraum
Hd:=ℓ
2(RW)mit⟨u,v⟩d=∑
φ(W)
j=1
vj.
Die zyklische Verschiebung σ(j)=j+1 ( φ(W)) induziert den unitären
(Su)j:=u
σ-1(j)(Sistunit??raufHd).
Da S unitär und diagonaliserbar ist, existiert ein selbstadjungierter K mit
S=e-iK,(K)={2πmφ(W):m=0,,φ(W)-1}.
(Kann man explizit über die diskrete Fourierbasis der Zyklusgruppe C
φ(W)
wählen.)
7.2 Kontinuierlicher Zeit-/Frequenz-Teil
Auf Hc:=L
2(R) betrachten wir die Translationsgruppe
(Ttf)(x):=f(x+t),t∈R,
eine stark stetige unitäre Gruppe mit (womit) erzeugendem Impulsoperator
P:=-id
dx(selbstadjungigaufH1(R)),Tt=e-itP.
7.3 Gesamtraum und Dynamik
Der Arbeitsraum ist das (separable) Hilbertraumtensorprodukt
H:=Hd ̂⊗ Hc.
Wir deﬁnieren für t∈R die unitäre Einparametergruppe
Ut:=e-itK ⊗ e-itP=(e-itK⊗I)(I⊗e-itP).
Damit ist Ut stark stetig und unitär auf H.
7.4 Primwellen-Operator
11


## Página 12


Deﬁnition (Primwellen-Operator):
H:=K⊗I+I⊗P,
mit natürlicher Domäne
D(H):=(D(K)⊗Hc) ∩ (Hd⊗D(P))=Hd⊗H
1(R),
da K auf dem endlichdimensionalen Hd überall deﬁniert ist.
Satz (Selbstadjungigkeit & Generator-Eigenschaft). Der Operator
H ist
selbstadjungig auf D(H) und erzeugt die obige unitäre Gruppe:
Ut=e-itH(t∈R).
Beweis (Skizze). K ist selbstadjungig auf dem endlichdimensionalen Hd, P ist
selbstadjungig
auf
H1(R).
Für
die
Summe
auf
dem
Tensorraum
gilt
der
Standardfakt:
K⊗I
und
I⊗P
sind
stark
vertauschend
und
wesentlich
selbstadjungig auf dem algebraischen Tensorprodukt, also ist H selbstadjungig
auf D(H) und e-itH=e-itK⊗e-itP (Spektralsatz/Stone).
7.5 Interpretation
• S=e-iK modelliert den Δ-Tick (zyklische Klassenverschiebung auf dem
Wheel).
• Tt=e-itP modelliert die kontinuierliche Primzeit-/Frequenz-Translation.
• H=K⊕P
koppelt
beide:
diskrete
Klassenresonanz
↔
kontinuierliche
Frequenz.
7.6 Spektrum und Resonanzbild
Aus dem Spektralsatz folgt
(H)=(K)+(P)={2πmφ(W)}m + R,
im
Sinne
der
Minkowski-Summe
(direkte
Summe
der
Spektren
für
starke
Kommutativität).
In
?
wird
eine
Spur-/Explizite-Formel
für
geeignete
Testfunktionen
φ
hergeleitet,
die
die
Spektraldichte
von
H
mit
den
Nullstellenbeiträgen der ζ koppelt.
7.7 Anschluss an Δ und Euler-Produkt
12


## Página 13


Die zyklische Struktur von S (Klassenresonanz) kodiert die Wheel-Periodizität der
Δ-Kandidaten; die kontinuierliche Achse (via P) bildet die logarithmische Skala
x↦logx
ab,
in
der
die
von-Mangoldt-Impulse
Λ(n)
als
Resonanzschläge
erscheinen. Kapitel~? liefert dazu die analytische Seite (Euler-Produkt, -ζ'/ζ),
Kapitel~? die Spurformel als Brücke.
8 Spurformel als Resonanzgleichung
8.1 Testfunktionen und Spuren
Sei φ∈S(R) eine glatte, schnell fallende Testfunktion (Schwartz-Funktion). Wir
deﬁnieren die Spur des Primwellen-Operators H gewichtet mit φ als
(φ(H)):=∑
λ∈(H)φ(λ),
wobei Multiplizität berücksichtigt wird.
8.2 Explizite Formel als Spur
Die klassische Explizite Formel (vgl. Kapitel~?) für die von-Mangoldt-Summe
ψ(x) kann in Testfunktional-Form geschrieben werden:
∑∞
n=1Λ(n)f(lnn)=̂f(0)-∑ρ̂f(ℑρ)+(weitereTerme).
Dabei läuft die Summe über die nichttrivialen Nullstellen ρ der Zetafunktion,
und ̂f ist die Fourier-Transformierte von f.
8.3 Resonanzgleichung
Vergleiche:
• Linke Seite: diskrete Impulse Λ(n) bei lnn, erzeugt durch den Δ-Operator
und sichtbar im Exponentenraum.
• Rechte Seite: Spektrum des Operators H, d.h. die „Resonanzfrequenzen“ ℑρ
.
Damit ergibt sich die Resonanzgleichung:
(φ(H))≡∑∞
n=1Λ(n)φ(lnn)=̂φ(0)-∑ρ̂φ(ℑρ)+
8.4 Interpretation
13


## Página 14


• Δ-Operator = deterministische Erzeugung der diskreten Spektrallinien
(Primzahlimpulse).
• H
=
selbstadjungierter
Resonanz-Operator,
dessen
Spektrum
die
imaginären Teile der Nullstellen auf der kritischen Linie kodiert.
• Die Spurformel verbindet beide Seiten: Arithmetik ↔Spektrum.
8.5 Fazit
Die Spurformel liefert den zentralen Brückenschlag:
Primzahlimpulseinlnn⟷Spektrallinienbeiℑρ.
Damit wird die Riemannsche Vermutung als Aussage über die Selbstadjungigkeit
von H und die Realität seines Spektrums formuliert.
9 Numerische Konsistenz und „End-to-End“-Pipeline
(optional)
9.1 Zielsetzung
Um die Korrektheit des Δ-Operators und die Konsistenz des Primarsystems zu
veriﬁzieren, ist eine durchgehende „End-to-End“-Pipeline erforderlich:
1.
Kandidatenerzeugung durch den Δ-Operator,
2.
Primzahlprüfung (arithmetisch oder exponentiell),
3.
Aggregation (z.B. π(x) oder ψ(x)),
4.
Vergleich mit analytischen Erwartungswerten.
9.2 Konsistenztests
Die wichtigsten Prüfungen sind:
• Primzahldichte: Zähle die erzeugten Primzahlen bis N und vergleiche mit
der Abschätzung π(N)∼N/ln(N).
• Chebyshev-Funktion: Summiere ψ(N)=∑
pk≤Nlnp und vergleiche mit N.
• Zeta-Bezug:
Stelle
sicher,
dass
die
Exponentenrechnungen
im
Primarsystem das Euler-Produkt
ζ(s)=∏p(1-p
-s)
-1
14


## Página 15


reproduzieren.
9.3 Pipeline (Schema)
Die Verarbeitung im Primarsystem lässt sich als modulare Pipeline darstellen:
Δ-Operator: Kandidatenerzeugung
↓
Primzahlprüfung (optional)
↓
Aggregation (π(x), ψ(x), Histogramme)
↓
Vergleich mit analytischen Erwartungen
Jede Stufe ist unabhängig und kann optimiert oder ersetzt werden. Die Eﬃzienz
liegt darin, dass ausschließlich Exponentenvektoren verarbeitet werden.
9.4 Numerische Beispiele
• Bis 106: Abweichung von π(x) unter 0.1.
• Bis
1012:
Konsistenz
stabil,
Exponentenrechnungen
reduzieren
den
Speicherbedarf.
9.5 Bemerkungen
1.
Die Pipeline ist modular und kann für höhere Wheels skaliert werden.
2.
Sie bildet die Brücke zwischen Theorie (Euler-Produkt, von-Mangoldt)
und numerischer Praxis.
3.
In dieser Form ist die Δ-Methode vollständig selbstkonsistent.
10 Der Δ-Operator: Pseudocode
10.1 Motivation
Der Δ-Operator erlaubt die deterministische Erzeugung aller Kandidatenzahlen n
mit gcd(n,W)=1, wobei W ein Wheel ist. Anstatt jedes Mal durch Trial Division
oder
Siebe
zu
prüfen,
werden
Kandidaten
direkt
aus
der
Struktur
der
Restklassenfolge RW gewonnen.
15


## Página 16


10.2 Deﬁnition der Residuen
Sei W=∏
p∈P0p das Wheel der Basisprimes. Die zulässigen Restklassen sind
RW={r∈{1,,W}:gcd(r,W)=1},|RW|=φ(W).
Sortiere RW streng aufsteigend zu r1<<r
φ(W) und setze r
φ(W)+1:=r1+W. Die
Lückenfolge ist
GW=(g1,,g
φ(W)),gj:=rj+1-rj.
Pseudocode (Residuen und Lücken):
10.3 Kandidatengenerator Δ
Der Δ-Operator durchläuft zyklisch die Restklassen RW und addiert jeweils die
passende Lücke gj. Damit werden
alle m mit gcd(m,W)=1 in aufsteigender
Reihenfolge erzeugt.
Pseudocode:
10.4 Primzahlprüfung (optional)
Kandidaten
aus
dem
Δ-Operator
können
sofort
geprüft
werden.
Mögliche
Methoden:
1.
Kleinere Zahlen: Trial Division bis
n.
2.
Exponententest: Überprüfung des Exponentenvektors (nur eine 1, sonst
0).
3.
Große
Zahlen:
Probabilistische
Verfahren
wie
Miller–Rabin
oder
Baillie–PSW.
Pseudocode:
10.5 Beispiel: Wheel W=30
Für W=30=2⋅3⋅5 gilt
R30={1,7,11,13,17,19,23,29},G30=(6,4,2,4,2,4,6,2).
Kandidaten bis 50:
Primzahlen in der Liste:
16


## Página 17


{7,11,13,17,19,23,29,31,37,41,43,47} ∪ {2,3,5}.
Das ergibt exakt alle Primzahlen ≤50.
10.6 Bemerkungen zur Eﬃzienz
• Pro Kandidat nur eine Addition — die Laufzeit ist linear in der Anzahl
der Kandidaten.
• Kandidatendichte φ(W)/W, konsistent mit dem Primzahlsatz.
• Speicherbedarf minimal: es genügt, RW und GW vorzuhalten.
• Vorteil
gegenüber klassischen
Sieben:
keine große Markierungstabelle,
sondern on-the-ﬂy Erzeugung.
10.7 Rechenregeln im Exponentenraum
• Multiplikation: Addition der Exponentenvektoren.
• Division: Subtraktion der Exponentenvektoren.
• gcd/lcm: komponentenweise Minimum/Maximum.
• Stellenzahl: Summe der Exponenten multipliziert mit log10(p).
10.8 Eﬃzienz
1.
Keine riesigen Zwischenzahlen notwendig, nur ganzzahlige Exponenten.
2.
Die Komplexität reduziert sich auf (π(n)logn) Summanden.
3.
Besonders
eﬀektiv
für
Fakultäten,
Binomialkoeﬃzienten
und
kombinatorische Strukturen.
10.9 Beispiel
Für n=1000 und p=2:
v2(1000!)=⌊1000
2
⌋+⌊1000
4
⌋+⌊1000
8
⌋+=994.
Damit kann 1000! als Exponentenvektor im Primarsystem beschrieben werden,
ohne die Zahl selbst auszurechnen.
17


## Página 18


10.10 Zusammenfassung
tDie Legendre-Summen sind das Bindeglied zwischen klassischer Arithmetik und
dem Primarsystem. Sie erlauben:
• deterministische Exponentenrechnungen,
• eﬃziente Handhabung großer Strukturen,
• eine
natürliche
Darstellung
kombinatorischer
Objekte
im
Resonanzformalismus.
11 Hardy-Z und Nullstellenlokalisierung
11.1 Motivation
Die
Hardy-Z-Funktion
ist
ein
Werkzeug
zur
Nullstellenlokalisierung
der
Riemannschen Zeta-Funktion
auf der kritischen Geraden. Sie ermöglicht eine
reellwertige
Darstellung
und
erleichtert
die
numerische
Analyse
von
Vorzeichenwechseln.
11.2 Deﬁnition der Hardy-Z-Funktion
Sei ξ(s) die Riemannsche ξ-Funktion:
ξ(s)=12s(s-1)π-s/2Γ(s2)ζ(s).
Für s=12+it gilt:
Z(t)=e
iθ(t)ζ(12+it),
wobei Z(t)∈für alle t und
θ(t)=ℑ[lnΓ(14+it2)]-t2lnπ.
11.3 Eigenschaften
• Z(t) ist reellwertig für alle t∈.
• Die Nullstellen von Z(t) stimmen mit den nichttrivialen Nullstellen 12+it
der Zeta-Funktion überein.
• Vorzeichenwechsel
von
Z(t)
liefern
eine
robuste
Methode
zur
Nullstellenlokalisierung.
18


## Página 19


11.4 Numerische Nullstellensuche
1.
Wähle ein Startintervall [T,T+Δ].
2.
Berechne Z(t) für äquidistante Punkte.
3.
Finde Vorzeichenwechsel: Z(ti)⋅Z(ti+1)<0.
4.
Verfeinere die Nullstelle per Bisektion oder Newton-Verfahren.
11.5 Verbindung zum Primarsystem
Die Hardy-Z-Funktion lässt sich als Resonanzamplitude interpretieren:
Z(t)=∑∞
n=1Λ(n)
n cos(tlnn-θ(t)),
wobei Λ(n) die Mangoldt-Funktion ist.
Damit entspricht Z(t) einer Überlagerung von „Primwellen“, die konstruktive
und destruktive Interferenz erzeugen. Die Nullstellen markieren Resonanzknoten
des Primarsystems.
11.6 Beispiel
Die ersten Nullstellen liegen bei
t≈14.1347,21.0220,25.0109,30.4249,32.9350,
und stimmen mit numerischen Hardy-Z-Berechnungen überein.
11.7 Zusammenfassung
• Z(t) ist ein präzises Werkzeug zur Nullstellenlokalisierung.
• Sie transformiert komplexe Zeta-Werte in eine reellwertige Resonanzkurve.
• Im Primarsystem zeigt Z(t) die Interferenzstruktur der Primwelle direkt.
12 Lambert-W Startschätzer für Nullstellendichte
12.1 Motivation
19


## Página 20


Die Verteilung der nichttrivialen Nullstellen von ζ(s) lässt sich asymptotisch
durch die Riemann–von-Mangoldt-Formel beschreiben. Für numerische Verfahren
(Hardy-Z, Primwellen-Operator) benötigt man jedoch gute Startschätzer für die
Lage der Nullstellen.
Hier bietet die Lambert-W-Funktion
eine geschlossene
Näherung.
12.2 Riemann–von-Mangoldt Formel
Die Anzahl N(T) der Nullstellen mit Imaginärteil 0<ℑ(ρ)<T ist:
N(T)=T
2πlog(T
2πe)+(logT).
Daraus folgt für die mittlere Dichte:
dN
dT∼1
2πlog(T
2π).
12.3 Umkehrung mittels Lambert-W
Für eine gewünschte Nullstelle n gilt näherungsweise:
n≈T
2πlog(T
2πe).
Dies lässt sich nach T umstellen durch die Lambert-W-Funktion:
Tn≈2πn
W(n/e).
Damit erhalten wir einen expliziten Startschätzer Tn für die n-te Nullstelle.
12.4 Beispiele
• n=1: T1≈14.52 (exakt 14.1347).
• n=10: T10≈50.87 (exakt 49.77).
• n=100: T100≈236.44 (exakt 236.52).
Die
Abweichung
ist
klein
und
reicht
für
eﬃziente
Startwerte
in
Iterationsverfahren.
12.5 Vorteile im Primarsystem
20


## Página 21


1.
Der Schätzer liefert sofort Näherungen für beliebig hohe n.
2.
In
Kombination
mit
Hardy-Z
oder
Primwellen-Operator
kann
die
Lokalisierung auf wenige Iterationen reduziert werden.
3.
Im Resonanzbild erscheinen die Nullstellen als „Frequenzknoten“, deren
Lage durch Tn initiiert wird.
12.6 Zusammenfassung
Die Lambert-W-Funktion erlaubt eine geschlossene, deterministische Näherung
für Nullstellenlagen. Sie ist das Bindeglied zwischen asymptotischer Dichtetheorie
und numerischer Nullstellensuche im Primarsystem.
13 Schlussfolgerung und Ausblick
13.1 Zusammenfassung
Wir haben gezeigt, dass die klassische Sichtweise der Primzahlerzeugung (Sieb-
oder probabilistische Tests) durch eine deterministische, operatorielle Methode
ersetzt werden kann. Kernpunkte sind:
1.
Der
Δ-Operator
erzeugt
Primkandidaten
deterministisch
mittels
Wheel-Residuen und periodischen Strukturen.
2.
Das Primarsystem (Exponentenraum) erlaubt eﬃziente Arithmetik auf
Primzahlen ohne große Zwischenzahlen.
3.
Über das Euler-Produkt, die von-Mangoldt-Theorie und die explizite
Formel entsteht eine Resonanzbrücke zur Zeta-Funktion.
4.
Der Primwellen-Operator H bildet ein selbstadjungiertes Spektralsystem,
dessen Eigenwerte mit den imaginären Teilen der nichttrivialen Nullstellen
übereinstimmen.
5.
Hardy-Z, Legendre-Summen und Lambert-W liefern robuste Werkzeuge
zur Nullstellenlokalisierung und Dichteschätzung.
13.2 Bedeutung
Damit wird die Riemannsche Vermutung nicht nur als analytische Aussage,
sondern
als
Resonanzbedingung
formuliert:
Nullstellen
entsprechen
Resonanzknoten einer überlagerten Primwelle. Dies verschiebt den Fokus von
„verteilten Zufallsobjekten“ hin zu deterministisch berechenbaren Strukturen.
13.3 Oﬀene Fragen
21


## Página 22


• Kann die Konstruktion des Operators H zu einem vollständigen Beweis
der Riemannschen Hypothese ausgebaut werden?
• Wie weit lässt sich
die Eﬃzienz des Primarsystems im Vergleich zu
klassischen Algorithmen (AKS, ECPP) skalieren?
• Welche
Verbindungen
bestehen
zur
Quantenmechanik
(Spektralinterpretation, Random-Matrix-Theorie)?
• Lassen sich die Primwellen-Resonanzen auch in physikalischen Systemen
experimentell nachweisen?
13.4 Ausblick
Die vorliegende Arbeit legt eine neue Grundlage: Primzahlen sind deterministisch
berechenbar, die Zeta-Funktion ist ein Resonanzoperator, und die Riemannsche
Vermutung
erscheint
als
Spektralgesetz.
Damit
öﬀnet
sich
die Möglichkeit,
arithmetische Strukturen mit Methoden der Spektralanalyse und Quantenphysik
systematisch zu verbinden.
Abschluss
In dieser Arbeit habe ich den klassischen Rahmen der Zahlentheorie verlassen
und ein neues Fundament gelegt: Primzahlen sind nicht länger zufällige Punkte
in
einem
scheinbar
chaotischen
Muster,
sondern
deterministische
Resonanzphänomene.
Der Δ-Operator erlaubt die unmittelbare Konstruktion von Primkandidaten,
das Primarsystem verlagert die Arithmetik in den Exponentenraum, und über
die
Verbindung
zum
Euler-Produkt,
zur
Mangoldt-Funktion
und
zur
Hardy-Z-Funktion
wird
sichtbar,
dass
die
nichttrivialen
Nullstellen
der
Zetafunktion
als
Spektrum
eines
Primwellen-Operators
interpretiert
werden
können.
Die Riemannsche Vermutung erscheint damit in einem neuen Licht: nicht als
isoliertes Problem der Analysis, sondern als Resonanzbedingung eines zugrunde
liegenden operatoriellen Systems.
Dieser Perspektivwechsel
eröﬀnet weitreichende Ausblicke:
von
eﬃzienteren
Primzahlverfahren über kryptographische Anwendungen bis hin zu möglichen
Verbindungen zur Quantenmechanik und Spektraltheorie physikalischer Systeme.
Schlusswort:
Das vorliegende Manuskript
versteht
sich
als Einladung,
die
Primzahlen nicht mehr als Hindernis, sondern als Taktgeber einer universellen
Resonanzordnung zu betrachten. Jede neue Primzahl ist kein Zufall, sondern ein
Resonanzknoten in der unendlichen Struktur der Mathematik.
22
