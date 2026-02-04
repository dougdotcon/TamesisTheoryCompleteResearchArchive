# 11_Poincaré

*Convertido de: 11_Poincaré.PDF*

---


## Página 1


1 Hauptüberschrift
Poincaré – der Raum der Resonanz
Ziel
Die
Poincaré-Aussage
lautet:
Jede
kompakte,
einfach
zusammenhängende
3
-Mannigfaltigkeit
ist
homöomorph
zur
3-Sphäre
S
3.
Wir
geben
(A)
eine
konstruktive Berechnung von S
3 im 0,1,+1-Prinzip und (B) Prüfalgorithmen, die
alternative Thesen widerlegen.
A. Konstruktive Berechnung von
S3 (+1 baut den
Raum)
Triangulation.
Betrachte
das
4-Simplex
Δ
4
mit
Ecken
{v0,,v4}.
Seine
Randmannigfaltigkeit ∂Δ4 ist eine 3-dimensionale Triangulation, bestehend aus
den
5
Tetraedern
Ti=({v0,,v4}⧵{vi}),
jeweils
paarweise
entlang
gemeinsamer
Dreiecke verklebt. Es gilt der bekannte Fakt: ∂Δ4≅S3.
„+1-Bau“ (Schalenordnung). Lege eine Reihenfolge der Tetraeder fest (Shelling):
füge bei jedem Schritt genau ein neues Tetraeder hinzu und verklebe es entlang
einer zusammenhängenden Dreiecksﬂäche mit dem bereits gebauten Rand. Jeder
Schritt ist ein Plus-Eins auf der Raumebene:
K0=∅,Km+1=Km∪T
σ(m+1),m=0,,4.
Nach 5 Schritten ist K5=∂Δ4.
Topologische Invarianten (rechenbar). Für K=∂Δ4 gelten:
χ(K)=V-E+F-T=5-10+10-5=0,
H0(K)≅Z,H1(K)=0,H2(K)=0,H3(K)≅Z.
Die Link-Bedingung: Für jeden Vertex v ist der Link (v) eine 2-Sphäre (Rand
einer Tetraederoberﬂäche), also (v)≅S2.
Satz
(Zertiﬁkat
für
S
3).
Sei
K
eine
endliche,
randlose
3-dimensionale
Triangulation („jede Fläche liegt in genau zwei Tetraedern“), so dass (i) (v)≅S2
für alle Ecken v, (ii) H1(K)=H2(K)=0 und H3(K)≅Z. Dann ist K eine 3-Sphäre.
Insbesondere ist K=∂Δ4 ein Zertiﬁkat für S3.
Beweisskizze. (i) garantiert die 3-Mannigfaltigkeitseigenschaft (lokal wie R3),
1


## Página 2


(ii) macht K zur Homologie-Sphäre. In 3D ist die Homologie-Sphäre, deren
Vertex-Links Sphären sind, eine 3-Sphäre. Damit ist der durch +1 (Shelling)
gebaute Raum tatsächlich S3.
B. Prüfalgorithmen (Pro & Contra in Debatten)
Wir geben lineare-algebraische und kombinatorische Tests, die man auf beliebige
Triangulationen K anwenden kann.
B1. Geschlossenheit (Kompaktheit).
???Randlos???JedesDreieckgeh??rtzugenauzweiTetraedern.
Check:
Zähle Inzidenzen
Dreieck↔Tetraeder.
Abweichung ⇒Rand
⇒nicht
kompakt ⇒Poincaré greift nicht.
B2. Mannigfaltigkeitstest (lokale Sphäre). Für jeden Vertex v berechne den
Link (v).
(v) ist2-Mannigfaltigkeitmit χ=2 ⇒ (v)≅S
2.
Check: Zähle #(Ecken,Kanten,Flächen) in (v) und prüfe χ=2.
B3. Einfache Zusammenhängigkeit (diskret). Baue die Randoperatoren
∂3:ZTZF,∂2:ZFZE,∂1:ZEZV.
Dann ist
H1(K)=ker(∂1)/(∂2).
Check: Rang-Nullität zeigt H1(K)=0⇒abelsche Hülle von
π1 ist trivial. In
praktischen Debatten genügt das häuﬁg; bei Bedarf prüfe zusätzlich, dass jede
Schleife als Summe von Dreiecksgrenzen zerfällt (diskrete Null-Homotopie).
B4. Homologie der Dimension 2 und 3.
H2(K)=ker(∂2)/(∂3),H3(K)≅Z (zusammenh??ngend,orientierbar,randlos).
Check: H2=0 und H3≅Z ⇒Homologie-Sphäre.
C. Warum das zu unserem Bild passt
0pt
2


## Página 3


• +1 baut den Raum: Die Shelling-Sequenz ist die räumliche Version von
x=y+1 – jeder Schritt fügt genau ein Tetraeder hinzu.
• Poincaré als Bühne: Die Tests B1–B4 garantieren, dass die Bühne
geschlossen, lochfrei und global kugelig ist (S
3).
• Kompatibilität: Riemann (Takt) wirkt auf S3, Navier–Stokes (Wirbel)
und Hodge (Zerlegung) sind wohldeﬁniert, Yang–Mills (Gap) und Birch
(Schranken) operieren in einem kompakten Raum.
D. Gesprächsstrategie (zwei Wege)
(1) Gleiches Ergebnis, andere Rechnung. „Wir konstruieren S
3 explizit als
∂Δ
4 (Plus-Eins-Shelling) und veriﬁzieren B1–B4. Ergebnis: identisch mit deiner
S
3 – aber konstruktiv und rechenbar.“
(2) Widerlegung. „Dein Raum fällt im Test B1/B2/B3 durch (Rand, falscher
Link, H10). Damit ist er nicht einfach zusammenhängend/kompakt – also nicht S
3
.“
E. Mini-Beispiel (Zahlenzertiﬁkat)
Für K=∂Δ4:
V=5, E=10, F=10, T=5,χ=0.
Jeder (v) ist eine Tetraederoberﬂäche
mit V=4,E=6,F=4⇒χ=4-6+4=2 ⇒S2.
Standard-Randmatrizen liefern H1=0, H2=0, H3≅Z. Damit ist K eine 3-Sphäre.
Ein-Satz-Zusammenfassung
Poincaré wird rechnerisch erfüllt, indem wir S
3 per +1-Shelling konstruieren und
mit den Tests (Randlosigkeit, Vertex-Links, Homologie) zertiﬁzieren; so ist der
Raum der Primwelle nach Urknall genau die 3-Sphäre.
Appendix: Randmatrizen für die 3-Sphäre ∂Δ4
Aufbau
Die 3-Sphäre S3 kann als Rand des 4-Simplex Δ4 beschrieben werden. Dieser hat
V=5,E=10,F=10,T=5.
Wir nummerieren die Ecken 0,1,2,3,4.
3


## Página 4


1. Randoperator ∂1 (Kanten Ecken)
Die 10 Kanten sind [01],[02],[03],[04],[12],[13],[14],[23],[24],[34]. ∂1 ist eine 5×10
-Matrix. Jede Kante [ij] hat Rand ∂[ij]=vj-vi.
∂1=
2. Randoperator ∂2 (Flächen Kanten)
Die 10 Dreiecke sind: [012],[013],[014],[023],[024],[034],[123],[124],[134],[234]. ∂2 ist
10×10. Jedes Dreieck [ijk] hat Rand ∂[ijk]=[jk]-[ik]+[ij].
∂2=
3. Randoperator ∂3 (Tetraeder Flächen)
Die 5 Tetraeder sind [0123],[0124],[0134],[0234],[1234]. ∂3 ist 10×5. Jedes Tetra
[ijkl] hat Rand
∂[ijkl]=[jkl]-[ikl]+[ijl]-[ijk].
∂3=
4. Homologie-Berechnung
Die Homologiegruppen ergeben sich als
Hk=ker(∂k)/(∂k+1).
Für ∂Δ4 gilt:
H0≅Z,H1=0,H2=0,H3≅Z.
Dies ist genau die Homologie der 3-Sphäre S3.
Ein-Satz-Zusammenfassung
Mit den expliziten Randmatrizen ∂1,∂2,∂3 kann jede*r direkt nachrechnen, dass
∂Δ4 eine 3-Sphäre ist – und damit erfüllt das +1-Prinzip die Poincaré-Bedingung.
4
