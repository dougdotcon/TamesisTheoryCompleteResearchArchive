# Atlas de Transições v0.1

Registro formal, computável e versionado de regimes físicos, relações entre regimes, hipóteses de transição, protocolos e evidências.

O Atlas é um multigrafo direcionado, tipado e atributado:

\[
\mathcal A=(\mathcal R,\mathcal T,\mathcal E,\mathcal P)
\]

Ele não é um catálogo de descobertas e não substitui uma teoria fundamental. Cada entrada carrega domínio de validade, status epistemológico, falsificação, incerteza e proveniência.

## Arquitetura

- `config/`: versão e regras do Atlas.
- `schemas/`: schemas JSON derivados dos modelos Pydantic.
- `registry/regimes/`: regimes físicos.
- `registry/transitions/`: relações e hipóteses de transição.
- `registry/evidence/`: evidências e fontes.
- `registry/protocols/`: protocolos e hashes.
- `src/transition_atlas/`: engine, validação, grafo, relatórios e integração Tamesis.
- `tests/`: testes estruturais e epistemológicos.
- `reports/`: auditorias e especificação formal.
- `outputs/`: grafos e fichas derivados.

## Comandos

Execute a partir desta pasta, com `PYTHONPATH=src`:

```text
python -m transition_atlas.validate
python -m transition_atlas.list_regimes
python -m transition_atlas.list_transitions
python -m transition_atlas.show_transition tamesis_quantum_classical_v1
python -m transition_atlas.build_graph
python -m transition_atlas.audit_evidence
python -m transition_atlas.generate_reports
python -m pytest -q
```

## Regra epistemológica

Uma anomalia observacional não é automaticamente uma transição física. Uma queda de coerência no subsistema não demonstra irreversibilidade fundamental. Promoções exigem evidência compatível, protocolo e proveniência.

O contrato executável `Tamesis M_c v1.0` permanece em `02_Experimental_Validation/Quantum_Classical_Transition/tamesis_mc_v1` e é importado somente para leitura.
