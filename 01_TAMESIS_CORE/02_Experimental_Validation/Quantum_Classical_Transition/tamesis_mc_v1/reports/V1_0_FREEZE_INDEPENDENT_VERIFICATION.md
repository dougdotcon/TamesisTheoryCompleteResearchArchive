# Verificação independente do freeze executável v1.0

## EXECUTABLE_FREEZE_VERIFIED_WITH_LIMITATIONS

O congelamento executável estrutural foi verificado com evidências positivas e mutation tests. A conclusão não significa prova física, validade estatística final ou status Bohr-level.

## Evidências positivas

- Contrato resolvido: `data/resolved_contract_v1_0.json`.
- Protocol ID: `tamesis-mc-v1.0:d3d9b22cdb62a335a9cfe14d4a066d7f4ea314881892453e7594b3fa7a546d0e`.
- Hash: `d3d9b22cdb62a335a9cfe14d4a066d7f4ea314881892453e7594b3fa7a546d0e`.
- `python -m pytest -q`: **12 passed**.
- `python audit_freeze.py`: 16 alterações/overrides rejeitados; YAML oficial inalterado.
- `python audit_fail_closed.py`: 6 cenários de fail-closed com exit 1.
- `python clean_reproduce.py`: 21 artefatos comparados; 19 idênticos entre reproduções, 0 unexpected; PNG/GIF normalizados idênticos.
- Manifesto final: 23 canonical_current, 0 canonical_stale, 0 invalid; verificado sem rebuild.
- AST import audit: 19 módulos, 0 edges legados.

## Inconsistências corrigidas

- `generate_figures.py:68` usava fórmula visual divergente (`(ratio-1)^2`); agora usa o expoente do contrato.
- `build_manifest.py` não incluía hash do artefato nos sidecars e incluía o próprio manifesto; ambos corrigidos.
- `verify_artifacts.py` reconstruía antes de verificar e não reprovava status invalid; agora verifica o manifesto existente e falha em invalid/stale.
- `regenerate_all.py` não executava `prioritize_targets.py`; agora executa.
- Proveniência visual genérica foi substituída pelos inputs reais de cada artefato.

## Limitações científicas

O freeze de software não estabelece validade fenomenológica, validade estatística, modelos ambientais completos, modelos rivais completos, derivação fundamental da raiz oitava, comportamento multipartícula ou qualquer reivindicação “Bohr-level”. O target de 1e-15 kg continua cenário hipotético; o ranking continua `legacy_exploratory_ranking`.

## Matriz final

| Requisito | Status | Evidência verificável | Bloqueador |
| --- | --- | --- | --- |
| Fonte única de verdade | pass | YAML + lock + config.py | — |
| Hash determinístico | pass | d3d9b22cdb62a335a9cfe14d4a066d7f4ea314881892453e7594b3fa7a546d0e | — |
| Protocol ID propagado | pass | tamesis-mc-v1.0:d3d9b22cdb62a335a9cfe14d4a066d7f4ea314881892453e7594b3fa7a546d0e | — |
| Ausência de hardcode ativo | pass com suspeitas classificadas | busca estrutural + config source | ruído histórico/scaffold |
| Overrides rejeitados | pass | audit_freeze/audit_fail_closed | — |
| Testes positivos adequados | parcial | 12 passed | não cobrem todos entry points |
| Testes negativos adequados | pass manual | 16 mutations + manifesto | converter para pytest |
| Reprodutibilidade limpa | pass | clean_reproducibility_evidence | — |
| Figuras ligadas ao contrato | pass | figure audit + sidecars | — |
| GIFs ligados ao contrato | pass | GIF audit + sidecars | — |
| Sidecars válidos | pass | artifact_sha256/input_hashes | — |
| Manifesto fail-closed | pass | verify sem rebuild | unknown_provenance não é inferência |
| Independência de model_summary | pass qualificado | 4 variantes + rejeição de cadeia predictions | predictions depende do summary |
| Ausência de imports legados | pass | AST graph, 0 edges | — |
| Contrato igual à implementação | pass qualificado | consistency line-by-line | alpha/largura/separação não são dinâmica |

## Decisão de avanço

**Aprovado para validação sintética e identificabilidade do software congelado. Não aprovado para afirmar descoberta física ou avançar ao ranking comparativo como conclusão.**
