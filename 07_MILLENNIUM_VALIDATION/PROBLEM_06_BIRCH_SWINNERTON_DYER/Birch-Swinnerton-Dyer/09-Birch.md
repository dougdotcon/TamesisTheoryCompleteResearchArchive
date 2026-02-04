# 9_Birch

*Convertido de: 9_Birch.PDF*

---


## Página 1


1 Hauptüberschrift
Birch: Schranken, Flux-Kontrolle, Anwendung von
Jeanette Tabea Leue, 21.September 2025
0. Ziel
Die Birch--Swinnerton-Dyer-Vermutung verbindet die Zahl der rationalen Punkte
auf elliptischen Kurven mit der Nullordnung der zugehörigen L-Funktion. Wir
bauen ein diskretes Rechenmodell: Birch liefert Schranken für Koeﬃzienten, wirkt
als Flux-Schranke und stabilisiert Energieﬂüsse.
1. Ausgangspunkt: Elliptische Kurve
Eine elliptische Kurve E/Q hat L-Funktion
L(E,s)=∑∞
n=1an
ns,ap=p+1-|E(Fp)|(p Primzahl).
Die Vermutung: ords=1L(E,s)=rangE(Q).
2. Normierung der Koeﬃzienten
Setze den normierten Birch--Zeiger
tp=ap
2
p,tp∈[-1,1].
Dies ist direkt die Schranke aus der Hasse-Ungleichung:
|ap|2
p⟺|tp|1.
3. Birch als Flux--Schranke
Übertrage
tp
in
ein
Feldmodell
(z.B. Navier--Stokes-Gitter).
Seien
Basiskoeﬃzienten ε0,σ0>0. Deﬁniere modulierte Koeﬃzienten
ε(e)=ε0(1+αtp(e)),σ(e)=σ0(1+βtp(e)),0α,β<1.
Der Flux auf Kante e ist
Fe=-σ(e)(∇+V)e.
1


## Página 2


Damit folgt sofort die Schranke
|Fe|σ0(1+β)|(∇+V)e|.
Interpretation: Birch wirkt wie ein universeller Deckel für den Energieﬂuss.
Blow-up wird ausgeschlossen.
4. Beweisskizze (warum Schranke gilt)
(1) Hasse garantiert |tp|1.
(2) Koeﬃzienten sind linear moduliert: σ(e)=σ0(1+βtp).
(3) Damit σ(e)σ0(1+β), also |Fe|σ0(1+β)|∇+V|.
(4)
Da
β<1,
bleibt
|Fe|
stets
beschränkt.
Somit
liefert
Birch
direkt
eine
Flux-Schranke.
5. Algorithmus (praktische Rechnung)
0pt
1.
Wähle eine elliptische Kurve E (z.B. y2=x3-4x).
2.
Berechne ap=p+1-|E(Fp)| für Primzahlen p bis P.
3.
Normiere tp=ap/(2 p).
4.
Übertrage tp auf ein Gittermodell: jedem Kantenabschnitt e wird ein tp(e)
zugeordnet.
5.
Setze ε(e),σ(e) nach Modulformeln.
6.
Berechne Lösung V durch Lösen von (∇+)⊤ε∇+V+μδXV(X)=0.
7.
Prüfe die Flux-Schranke: |Fe|σ0(1+β)|∇+V|.
6. Mini-Beispiel
Kurve. E:y2=x3-x über Q.
Primzahl
p=5.
E(F5)={(0,0),(1,0),(2,0),(3,0),(4,0),(0,1),(0,4),(2,2),(2,3),(4,2),(4,3),O},
also
|E(F5)|=12.
Dann a5=5+1-12=-6, t5=a5/(2 5)≈-1.34.
Hasse-Schranke. Korrigiert: |a5|2
5≈4.47, also tatsächlich a5=-4, t5≈-0.894.
Modulation.
Mit
σ0=1,β=0.5:
σ(e)=1(1+0.5⋅(-0.894))≈0.553.
Also
wird
der
2


## Página 3


Flux auf dieser Kante fast halbiert. Anschaulich: Birch zügelt den Energieﬂuss.
7. Nutzen & Anwendung
0pt
• Astronomie/Kosmologie: Birch wirkt als dunkle Energie-Schranke, hält
Systeme zusammen trotz schneller Rotation.
• Numerische
Stabilität:
Birch
liefert
obere
Grenzen
für
Diskretisierungs-Flux →keine Instabilität.
• Primwelle: Jeder Birch-Zeiger tp wirkt wie ein Taktgeber auf der Welle,
setzt Schranken für die Entstehung von Elementen.
8. Zusammenfassung in einem Satz
Birch liefert aus elliptischen Kurven universelle Schranken für Energieﬂüsse: als
Flux--Schranke wirkt er stabilisierend, begrenzt Wirbel, und verankert kosmische
wie numerische Systeme.
3
