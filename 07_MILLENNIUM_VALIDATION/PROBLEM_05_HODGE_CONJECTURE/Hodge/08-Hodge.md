# 8_Hodge

*Convertido de: 8_Hodge.PDF*

---


## Página 1


1 Hauptüberschrift
Hodge: Zerlegung, Rechnung, Beweis, Anwendung
von Jeanette Tabea Leue, 21.September 2025
0. Ziel
Gegeben ein diskretes Vektorfeld F auf einem endlichen Gitter. Hodge besagt: F
zerfällt eindeutig in gradientenartig (wirbelfrei) und solenoidal (divergenzfrei).
Wir zeigen Deﬁnition, Rechnung, Eindeutigkeit und wofur es gut ist.
1. Diskretes Setting und Operatoren
Sei Ω⊂Z
2 ein endliches Rechteckgitter mit Rand ∂Ω. Ein Vektorfeld F=(Fx,Fy) sei
auf Kanten deﬁniert. Vorwärtsdiﬀerenzen (Gitterweite =1):
(∂
+
x φ)(i,j)=φ(i+1,j)-φ(i,j),(∂
+
y φ)(i,j)=φ(i,j+1)-φ(i,j).
Gradient: ∇+φ=(∂+
x φ,∂+
y φ). Divergenz:
+F=∂-
xFx+∂-
yFy mit ∂-
x die ruckwärtige
Diﬀerenz. Rotation (Skalar in 2D): F=∂+
x Fy-∂+
y Fx. Der diskrete Laplace: Δ=+∇+
(5-Punkte-Stencil).
Inneres Produkt: ⟨F,G⟩=∑
(i,j)∈Ω(FxGx+FyGy).
2. Hodge-Zerlegungssatz (diskret)
Satz. Auf einem endlichen Gitter Ω mit Dirichlet-Rand φ|
∂Ω=0 gilt fur jedes
Vektorfeld F:
F=∇+φ+R⟂ψ,R⟂ψ:=(∂+
y ψ,-∂+
x ψ),
wobei φ (Potential) und ψ (Stromfunktion) eindeutig durch
Δφ=+F,Δψ=F,φ|
∂Ω=0, ψ|
∂Ω=0
bestimmt sind. Die Summanden sind orthogonal: ⟨∇+φ,R⟂ψ⟩=0. Ein separater
harmonischer Anteil entfällt unter Dirichlet-Rand.
3. Beweisskizze (linear-algebraisch, endlichdimensional)
(1)
Sei
G:={∇+φ:φ|
∂Ω=0}
und
S:={R⟂ψ:ψ|
∂Ω=0}.
Dann
⟨G,S⟩={0}
wegen
partieller Summation (⟨∇+φ,R⟂ψ⟩=⟨φ,+R⟂ψ⟩=0).
1


## Página 2


(2) Fur gegebenes F löst Δφ=
+F ein wohldeﬁniertes, streng diagonaldominantes
LGS (Dirichlet) ⇒eindeutige φ. Setze F':=F-∇
+φ. Dann
+F'=0.
(3) Löse Δψ=F (Dirichlet). Setze S:=R⟂ψ. Dann
+S=0 und S=F. Somit ist
F-∇+φ-S sowohl diverg.- als auch rotationsfrei; unter Dirichlet folgt =0 (kein
harmonischer Rest).
(4) Eindeutigkeit folgt aus Orthogonalität und der Positivität von Δ.
4. Wie rechnet man das praktisch? (Algorithmus)
0pt
1.
Gegeben F=(Fx,Fy) auf Ω.
2.
Potential-Schritt: rechte Seite bφ=+F; löse Δφ=bφ (Dirichlet).
3.
Strom-Schritt: rechte Seite bψ=F; löse Δψ=bψ (Dirichlet).
4.
Setze Zerlegung: F=∇+φ+R⟂ψ.
5.
(Optional) Numerikcheck: Orthogonalität und Residuum ∥F-∇+φ-R⟂ψ∥.
5. Wofur ist das gut? (Nutzen)
0pt
• Strukturtrennung:
trennt
Potentialﬂuss
(wirbelfrei)
von
Wirbelﬂuss
(divergenzfrei) exakt und eindeutig.
• Stabilität/Energie: ∥∇+φ∥2=⟨φ,Δφ⟩und ∥R⟂ψ∥2=⟨ψ,Δψ⟩geben direkte
Energie-Maße beider Anteile.
• Randwertprobleme: Potentialfelder lösen Poisson-Probleme, Wirbelfelder
lassen sich getrennt regeln (z. B. Randwirbel = 0).
6. Mini-Beispiel (1D & 2D, durchsichtig)
1D-Kette (keine Wirbel): Knoten i=0,,N, V(0)=V(N)=0; Kantenfeld Fi fur
i=0,,N-1. Dann ist F rein gradientenartig: Fi=(∇+V)i=V(i+1)-V(i). Mit Rand
ergibt sich eindeutig V(i)=∑i-1
k=0Fk und F=∇+V.
2D-Raster
(skizziert): Sei Ω={1,,4}2. Gegeben
konstantes
Fx≡1, Fy≡0 im
Inneren.
Dann
+F=0,
F=-∂+
y Fx=0.
Folge:
φ=ψ=0
(Dirichlet),
Residuum =
Randartefakt; setzt man Innenrand frei, liefert φ die lineare Potentiallösung
V(i,j)=i+const und ψ≡0. Dies illustriert: reine Gradientenfelder werden von
Hodge als solche erkannt.
7. Orthogonalität & Eindeutigkeit (Kernsatz)
2


## Página 3


Satz. Unter Dirichlet-Rand gilt
⟨∇
+φ,R
⟂ψ⟩=0,∥F∥
2=∥∇
+φ∥
2+∥R
⟂ψ∥
2.
Beweis (Skizze): Partielle Summation liefert Orthogonalität. Die Projektionen
auf G und S sind wohldeﬁniert; Dimensionen addieren sich zur Gesamtzahl der
Kantenfreiheitsgrade. Damit ist die Zerlegung eindeutig und orthogonal.
8. Zusammenfassung in einem Satz
Hodge liefert fur jedes diskrete Vektorfeld eine eindeutige, orthogonale Zerlegung
in Potential- und Wirbelanteil durch zwei Poisson-Probleme. Das ist berechenbar,
stabil und die Grundlage fur gezielte Feldsteuerung.
3
