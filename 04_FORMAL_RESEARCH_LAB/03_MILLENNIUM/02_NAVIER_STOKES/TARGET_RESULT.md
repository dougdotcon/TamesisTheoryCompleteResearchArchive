# Resultado alvo

Testar a hipótese quantitativa da Hessiana de pressão; obter contraexemplo,
correção ou teorema condicional com espaços, normas, constantes e
quantificadores explícitos.

## Status após auditoria de 2026-08-09 (NS-PRESSURE-001)

Produto obtido: **correção + contraexemplo explícito** (não teorema
condicional — o Lemma 3.1 necessário para qualquer versão condicional
continua sem prova).

- A forma nua do "Alignment Gap" (`⟨α₁⟩ ≤ 1-δ₀` isolado, sem a
  componente de taxa de dominância da pressão) é **refutada**: existe
  um sistema explícito, verificado por computação nesta sessão (a
  equação de Euler restrita de Vieillefosse 1982), onde `α₁ → 0`
  (desalinhamento quase perfeito) ao longo de toda trajetória que
  explode em tempo finito. Ver `COUNTEREXAMPLES/restricted_euler_alignment_gap.md`.
- A forma fortalecida (com o Lemma 3.1 do documento legado) continua
  `NOT_PROVEN`; esta sessão acionou o `stop_condition` da frente ao
  avaliar que fechar o Lemma 3.1 exigiria pesquisa matemática original
  (estimativa não-local do Hessiano de pressão anisotrópico), não uma
  auditoria de literatura. Ver `PROOF_SKETCH.md`, seção STOP CONDITION,
  e `GAP_REGISTER.yaml`.

Nenhum teorema condicional com espaços/normas/constantes explícitos foi
produzido nesta rodada — as hipóteses necessárias (Lemma 3.1) não estão
estabelecidas, então qualquer "teorema condicional" seria vazio de
conteúdo verificável.
