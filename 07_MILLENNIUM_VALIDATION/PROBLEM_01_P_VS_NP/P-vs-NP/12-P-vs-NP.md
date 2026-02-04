# 12_P_vs._NP

*Convertido de: 12_P_vs._NP.PDF*

---


## Página 1


Das
Millennium-Problem
P
vs. NP
im
Primarsystem
Jeanette Leue
19.9.2025
Einleitung
Das klassische Problem lautet:
P?=NP.
In der üblichen Informatik bedeutet P die Menge der Probleme, die sich schnell
berechnen lassen, und NP die Menge der Probleme, deren Lösungen sich schnell
überprüfen lassen. Oﬀen ist, ob beide Klassen gleich sind.
Resonanzformel
Im Primarsystem gilt die einfache Vorwärtsregel:
x=y+1.
Jeder Zustand y entwickelt sich deterministisch in den nächsten Zustand x. Es
gibt kein Minus, also keine Rückentwicklung. Die Zeit ist die Folge solcher
Vorwärtsschritte (Ticks).
Übertragung auf P und NP
Ein NP-Problem liefert eine Veriﬁkation y. Nach der Resonanzformel folgt daraus
automatisch der nächste gültige Zustand x=y+1. Damit ist jede Veriﬁkation
zugleich ein deterministischer Berechnungsschritt.
NP⊆P.
Da jedes P-Problem sowieso berechenbar ist, folgt sofort auch die Umkehrung.
Somit gilt im Primarsystem:
P=NP.
Beispiel
1


## Página 2


Primzahlen:
Eine Primzahlprüfung
ist
klassisch
in
NP.
Im
Primarsystem
nehmen wir den Index y=n und gehen einen Schritt weiter:
x=y+1⇒pn+1.
Die nächste Primzahl ist konstruiert. Damit fällt die Trennung zwischen „prüfen“
und „ﬁnden“.
Schluss
Das Millennium-Problem P vs. NP löst sich im Primarsystem unmittelbar. Da
jedes NP-Problem deterministisch durch die Resonanzformel berechenbar ist, gilt:
P=NP
2
