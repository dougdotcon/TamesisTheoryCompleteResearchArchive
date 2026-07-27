# Evidência de mutation tests negativos

Comando principal: `python audit_freeze.py`. O SHA-256 do YAML oficial antes/depois foi igual e o protocolo permaneceu `tamesis-mc-v1.0:d3d9b22cdb62a335a9cfe14d4a066d7f4ea314881892453e7594b3fa7a546d0e`. Nenhuma mutação foi escrita no contrato oficial.

| ID | Mutação | Comando/evidência | Resultado | Mecanismo |
| --- | --- | --- | --- | --- |
| 1 | Mc +1% | audit_freeze.py:run_contract_mutations | rejeitado (exit 1) | hash/valor congelado |
| 2 | último float serializado (nextafter) | audit_freeze.py | rejeitado (exit 1) | hash divergente |
| 3 | root 8 -> 7 | audit_freeze.py | rejeitado (exit 1) | root frozen |
| 4 | root 8 -> 9 | audit_freeze.py | rejeitado (exit 1) | root frozen |
| 5 | tau_c alterado | audit_freeze.py | rejeitado (exit 1) | hash + validação tau |
| 6 | alpha null -> 1 | audit_freeze.py | rejeitado (exit 1) | hash/contrato |
| 7 | largura null -> 0.1 | audit_freeze.py | rejeitado (exit 1) | hash/contrato |
| 8 | unidade Mc kg -> g | audit_freeze.py | rejeitado (exit 1) | unidade esperada |
| 9 | unidade H0 incompatível | audit_freeze.py | rejeitado (exit 1) | unidade esperada |
| 10 | campo estrutural desconhecido | audit_freeze.py | rejeitado (exit 1) | extra=forbid |
| 11 | campo estrutural ausente | audit_freeze.py | rejeitado (exit 1) | campo obrigatório |
| 12 | override CLI --Mc | validate_contract.py --Mc 1e-15 | rejeitado (exit 1) | reject_runtime_overrides |
| 13 | override TAMESIS_MC_KG | TAMESIS_MC_KG=1e-15 python validate_contract.py | rejeitado (exit 1) | reject_runtime_overrides |
| 14 | import legado | audit_imports.py (AST, 19 módulos) | 0 edges legados; não há import ativo para executar | graph independente sem 90_LEGACY |
| 15 | sidecar hash incorreto | audit_freeze.py:wrong_sidecar_contract_hash | rejeitado | require_current_artifact |
| 16 | artefato anterior/stale | audit_freeze.py:manifest_and_sidecars | classificado canonical_stale | protocol antigo não é current |
| 17 | manifesto editado | audit_freeze.py:manifest_edited | rejeitado (exit 1) | hash de entrada do manifesto |
| 18 | edição estrutural mantendo versão 1.0 | audit_freeze.py:structural_edit_same_version | rejeitado (exit 1) | lock/config hash |

As saídas completas (stdout, stderr, exit code e mensagem) estão em `data/freeze_audit_evidence.json`; as seis classes de manifesto estão na mesma evidência.
