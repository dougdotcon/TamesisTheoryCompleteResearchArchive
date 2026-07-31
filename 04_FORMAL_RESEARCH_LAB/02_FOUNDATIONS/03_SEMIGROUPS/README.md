# Semigrupos — FOUND-SEMIGROUP-001

Modelo finito de referência: três regimes (`Regime3`) e três transições
(`Shift3`) formando um monoide cíclico que age fiel e transitivamente sobre
os regimes. Formalizado em
`05_FORMAL/lean/TamesisLab/Foundations/Semigroups/` sob a interface oficial
da Mathlib (`SemigroupAction`/`MulAction`), sem duplicata local.

`FORMALIZED` — FOUND-SG-001 a FOUND-SG-013 verificados; ver
`THEOREM_MAP.md`, `DEFINITIONS.md` e `KNOWN_RESULTS_MATRIX.md`.

Valor científico: `FOUNDATIONAL_FORMALIZATION_ONLY`. O modelo não valida
TRI, TDTR ou qualquer claim histórica; não declara universalidade.

## Contraexemplos conceituais

Para impedir generalização indevida, a auditoria computacional
(`06_COMPUTATION/python/experiments/found_semigroup_001_audit.py`, resultado
em `06_COMPUTATION/results/FOUND-SEMIGROUP-001-computational-audit.json`)
inclui fixtures negativas verificadas exaustivamente:

1. **Operação finita não associativa** — subtração truncada em `{0,1,2}`:
   `(2−1)−1 = 0 ≠ 2 = 2−(1−1)`. Associatividade não é automática em
   operações finitas.
2. **Ação incompatível com a composição** — `forward2` forçada a agir como
   identidade sob a mesma tabela de composição viola
   `apply (comp a b) = apply a ∘ apply b`. A lei da ação é uma restrição
   real, não uma consequência da tipagem.
3. **Sistema não transitivo** — o subsistema `{identity}` não alcança
   regimes distintos. Transitividade é propriedade do modelo C3, não de
   sistemas de transição em geral.
4. **Representação não fiel** — mapear `identity` e `forward2` para a mesma
   função identifica transições distintas. Fidelidade é uma propriedade a
   provar, não um dado.

As fixtures negativas são verificação computacional
(`COMPUTATIONAL_FINITE_CROSS_CHECK_ONLY`); não foram formalizadas em Lean
neste gate por não serem exigidas para a auditoria formal.
