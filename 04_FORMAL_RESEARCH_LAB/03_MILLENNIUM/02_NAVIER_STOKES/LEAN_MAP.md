# Mapa Lean

Navier-Stokes em si (fraca ou forte) segue `NOT_FORMALIZED` — fora do
alcance desta auditoria.

Um fragmento algébrico autocontido foi escrito e compilado nesta rodada
(auditoria `NS-PRESSURE-001`, 2026-08-09):

- `FORMAL/PressureHessianAlgebra.lean` — `tr(A·Ω) = 0` para `A` simétrica,
  `Ω` antissimétrica, e a decomposição `tr((A+Ω)²) = tr(A²) + tr(Ω²)`, a
  identidade algébrica por trás da equação de Poisson da pressão e da
  equação de Euler restrita (Vieillefosse 1982). Compilado (`lake env
  lean`, `exit 0`) na integração serial; `#print axioms` confirma
  `[propext, Classical.choice, Quot.sound]`. **Não** registrado em
  `TamesisLab.lean`. O restante da hipótese (Lemma 3.1, parte
  anisotrópica/não-local do Hessiano de pressão) permanece
  `NOT_FORMALIZED` — é uma estimativa não-local, fora do alcance de um
  lema de álgebra linear finita.

