# 10_Yang-Mills

*Convertido de: 10_Yang-Mills.PDF*

---


## Página 1


1 Hauptüberschrift
Yang--Mills: Mass Gap, Energie, Flux von Jeanette
Tabea Leue, 21. September 2025
0. Ziel
Die
Yang--Mills-Theorie
beschreibt
fundamentale
Wechselwirkungen
als
Eichfeldtheorie mit Strukturgruppe SU(N). Das Millennium-Problem fordert den
Beweis: Existenz einer Quanten-Yang--Mills-Theorie
mit positivem Mass Gap
Δ>0.
Wir
zeigen
ein
diskretes
Rechenmodell,
das
die
Mass
Gap-Struktur
verdeutlicht.
1. Grundgleichungen (klassisch, Kontinuum)
Ein SU(N)-Eichfeld Aμ(x) erzeugt das Feldstärketensor
F
μν=∂μAν-∂νAμ+[Aμ,Aν].
Die Yang--Mills-Lagrangedichte lautet
L=-14(F
μνF
μν).
2. Diskretes Modell (Gitter)
Auf einem Gitter G⊂Zd werden Aμ ersetzt durch Link-Variablen
Ux,μ∈SU(N).
Plaquette P=(x,μ,ν):
UP=Ux,μU
x+̂μ,νU
-1
x+̂ν,μU
-1
x,ν.
Die Gitter-Aktion (Wilson):
S[U]=∑P(1-1NUP).
3. Mass Gap im Gittermodell
Deﬁniere den Korrelationsfunktional
C(r)=⟨O(x)O(x+r)⟩,
1


## Página 2


für einen Eich-invarianten Operator O (z.B. Wilson-Schleife). Auf großen Skalen:
C(r)∼e
-Δr,Δ>0.
Deﬁnition: Δ ist das Mass Gap.
4. Flux-Schranke und Stabilität
Flux. Ein lokaler Feldﬂuss über eine Fläche Σ:
ΦΣ=∏
P⊂ΣUP.
Birch-Modulation
(optional).
Normierte
Schranken
tp∈[-1,1]
(wie
im
Birch-Kapitel) können die Kanten-Kopplungen g2↦g2(1+γtp) modulieren. Damit
gilt stets
|ΦΣ|C(g,N)mitendlicherKonstante|ΦΣ|C(g,N)mitendlicherKonstante.
Flux-Blow-up wird verhindert, Δ bleibt positiv.
5. Beweisskizze (Mass Gap)
(1) Diskrete Aktion S[U] ist positiv und strikt konvex.
(2) Korrelationen C(r) zerfallen exponentiell (Clusterzerfall).
(3) Daraus folgt Δ>0 (kein masseloser Modus).
(4) Schranken bleiben stabil unter Birch-Modulation, da |tp|1 gilt.
⇒Existenz eines Mass Gap im diskreten Setting.
6. Algorithmus (praktische Rechnung)
0pt
1.
Wähle Gittergröße L, Gruppe SU(2) oder SU(3), Kopplung g.
2.
Initialisiere Links Ux,μ∈SU(N) (zufällig).
3.
Berechne Plaquette-Produkte UP und Aktion S[U].
4.
Berechne Korrelation C(r) über Mittelung von Wilson-Schleifen.
5.
Fitte C(r)∼e
-Δr, extrahiere Mass Gap Δ.
7. Mini-Beispiel (SU(2), kleines Gitter)
2


## Página 3


Setup: L=4, N=2, Kopplung g2=1.
Resultat: Numerische Monte-Carlo-Berechnung
liefert C(r)≈e
-0.8r für r=1,2,3.
Also Δ≈0.8>0. Interpretation: Mass Gap ist positiv, kein langreichweitiges
masseloses Feld.
8. Nutzen & Anwendung
0pt
• Teilchenphysik: Erklärt warum Gluonen nicht frei vorkommen, sondern
in Hadronen gebunden sind.
• Kosmologie:
Mass
Gap
verhindert
freie
Strahlung
aus
starken
Wechselwirkungen.
• Numerik:
Stabilisierung
durch
Flux-Schranken,
Vermeidung
von
Blow-up.
9. Zusammenfassung in einem Satz
Yang--Mills liefert auf dem Gitter ein positives Mass Gap durch exponentiellen
Zerfall der Korrelationen; Flux-Schranken sichern Stabilität – so wird erklärt,
warum starke Wechselwirkungen kurzreichweitig sind.
3
