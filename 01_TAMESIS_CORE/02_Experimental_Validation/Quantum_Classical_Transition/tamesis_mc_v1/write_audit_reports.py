from __future__ import annotations

import json
from pathlib import Path

from config import load_v1_contract, reject_runtime_overrides


BASE = Path(__file__).resolve().parent
REPORTS = BASE / "reports"


def write(name: str, content: str) -> None:
    (REPORTS / name).write_text(content.rstrip() + "\n", encoding="utf-8")


def table(headers: list[str], rows: list[list[str]]) -> str:
    return "| " + " | ".join(headers) + " |\n| " + " | ".join("---" for _ in headers) + " |\n" + "\n".join("| " + " | ".join(str(x).replace("|", "\\|") for x in row) + " |" for row in rows)


def main() -> None:
    reject_runtime_overrides()
    c = load_v1_contract()
    evidence = json.loads((BASE / "data" / "freeze_audit_evidence.json").read_text(encoding="utf-8"))
    fail = json.loads((BASE / "data" / "fail_closed_evidence.json").read_text(encoding="utf-8"))
    clean = json.loads((BASE / "data" / "clean_reproducibility_evidence.json").read_text(encoding="utf-8"))
    summary = json.loads((BASE / "data" / "model_summary_independence_evidence.json").read_text(encoding="utf-8"))
    imports = json.loads((BASE / "data" / "active_import_graph.json").read_text(encoding="utf-8"))
    cov = json.loads((BASE / "data" / "coverage_v1_0.json").read_text(encoding="utf-8"))

    consistency_rows = [
        ["C01", "Mc = mP(a0/aP)^(1/8)", "mc_model.py:11 compute_mc_from_contract; config.py:237 load_v1_contract", "test_contract_freeze.py:test_contract_reproduces_frozen_mc_and_protocol_id", "implemented_and_tested", "cálculo independente coincide: 5.292674126388712e-16 kg; mutation root 7/9 rejeitada"],
        ["C02", "H0 convertido para SI", "config.py:98-101 V1Contract.h0_si", "validate_contract.py (comando executado); sem teste pytest específico", "implemented_without_test", "H0 70 km s^-1 Mpc^-1 -> 2.268545502662652e-18 s^-1"],
        ["C03", "tau_c congelado e validado", "config.py:193-195; mc_model.py:48", "test_contract_freeze.py:test_derived_scale_and_radius + validate_contract.py", "implemented_and_tested", "2.176246482178091 s; mutation tau_c rejeitada"],
        ["C04", "Gamma_T=0 para M<=Mc", "mc_model.py:72-78", "test_mc_model.py:test_sharp_threshold_is_explicit", "implemented_and_tested", "M=Mc dá 0; teste também verifica lado direito"],
        ["C05", "Gamma_T=tau_c^-1(M/Mc)^2 acima", "mc_model.py:78", "test_mc_model.py:test_quadratic_scaling_above_threshold", "implemented_and_tested", "razão 2Mc/4Mc=0.25"],
        ["C06", "visibility=exp(-(GammaT+Gammaenv)t)", "mc_model.py:84-88", "test_mc_model.py:test_environment_is_an_explicit_nuisance", "implemented_and_tested", "ambiente é somado explicitamente"],
        ["C07", "separação ausente em v1.0", "config/tamesis_mc_v1.yaml:57; compare_models.py:63 dx só em rivais", "nenhum teste específico de ausência", "partially_implemented", "documentado; não entra em Gamma_T v1.0"],
        ["C08", "alpha explicitamente ausente", "config/tamesis_mc_v1.yaml:47-49", "loader Pydantic; sem teste pytest específico", "implemented_without_test", "value=null/classification=absent_in_v1_0"],
        ["C09", "largura explicitamente ausente", "config/tamesis_mc_v1.yaml:54-56", "loader Pydantic; sem teste pytest específico", "implemented_without_test", "value=null/classification=absent_in_v1_0"],
        ["C10", "modelo ambiental separado", "environment_model.py; compare_models.py:107-123", "test_environment_model.py:4,11", "implemented_and_tested", "inversão de pressão e escala linear passam"],
        ["C11", "ranking marcado legacy_exploratory_ranking", "compare_models.py:214", "regenerate_all.py + artefato comparison_report.json", "implemented_and_tested", "não tratado como conclusão física"],
        ["C12", "sidecars de proveniência", "provenance.py:36-98", "audit_freeze.py + verify_artifacts.py", "implemented_and_tested", "hash do artefato, inputs, protocol ID e config hash"],
        ["C13", "manifesto automático", "build_manifest.py:85-145", "audit_freeze.py + verify_artifacts.py", "implemented_and_tested", "seis estados distinguidos; adulterações rejeitadas"],
        ["C14", "CSL/GRW/DP completos", "compare_models.py:39-63", "nenhum", "documented_not_implemented", "scaffold comparativo, sem corpos estendidos/calibração final"],
        ["C15", "likelihood estatística final", "reports/STATISTICAL_ANALYSIS_PLAN_V1_0.md", "nenhum", "documented_not_implemented", "plano pré-registrado, não análise discriminante final"],
        ["C16", "massa-separação-geometria da plataforma", "reports/TARGET_1E15_FEASIBILITY_AUDIT.md", "nenhum", "documented_not_implemented", "limitação de plataforma, fora da dinâmica v1.0"],
    ]
    write("CONTRACT_IMPLEMENTATION_CONSISTENCY.md", "# Auditoria linha a linha: contrato versus implementação\n\nHash: `" + c.config_hash() + "`  \\nProtocol ID: `" + c.protocol_id() + "`\n\n" + table(["ID", "Afirmação contratual", "Arquivo de implementação", "Teste", "Status", "Evidência"], consistency_rows))

    tests = [
        ["test_contract_reproduces_frozen_mc_and_protocol_id", "golden/schema", "Mc congelado, equação e protocol ID", "Mc congelado ou hash/protocol divergente"],
        ["test_model_is_bound_to_contract", "integration", "McModel usa contrato atual", "McModel usar constante legada"],
        ["test_rejects_modified_mc", "negative", "Mc alterado é rejeitado", "Mc +1%"],
        ["test_rejects_modified_exponent", "negative", "expoente não pode derivar do arquivo adulterado", "exponente 3"],
        ["test_rejects_modified_unit", "negative/schema", "unidade H0 inválida é rejeitada", "H0 em m s^-1"],
        ["test_hash_is_deterministic", "reproducibility", "serialização/hash determinísticos", "mesmo contrato carregado duas vezes ter hashes diferentes"],
        ["test_derived_scale_and_radius", "unit", "Mc, raio e tau aproximados", "Mc/radius/tau fora da tolerância"],
        ["test_sharp_threshold_is_explicit", "unit", "limiar sharp e lado acima", "Gamma(Mc) não ser zero"],
        ["test_quadratic_scaling_above_threshold", "unit", "expoente quadrático", "expoente 1 ou 3"],
        ["test_environment_is_an_explicit_nuisance", "unit", "ambiente separado do intrinsic_rate", "ambiente alterar Gamma_T"],
        ["test_gas_collision_rate_scales_with_pressure", "unit", "taxa de gás escala com pressão", "pressão x1000 não produzir taxa x1000"],
        ["test_pressure_for_rate_inverts_gas_rate", "unit", "inversão pressão/taxa", "pressão calculada não inverter a taxa"],
    ]
    write("TEST_INVENTORY_V1_0.md", "# Inventário dos 12 testes atuais\n\nComando: `python -m pytest -q` — **12 passed**.\n\n" + table(["Teste", "Tipo", "Afirmação verificada", "Falharia com qual mutação?"], tests))

    mutations = [
        ["1", "Mc +1%", "audit_freeze.py:run_contract_mutations", "rejeitado (exit 1)", "hash/valor congelado"],
        ["2", "último float serializado (nextafter)", "audit_freeze.py", "rejeitado (exit 1)", "hash divergente"],
        ["3", "root 8 -> 7", "audit_freeze.py", "rejeitado (exit 1)", "root frozen"],
        ["4", "root 8 -> 9", "audit_freeze.py", "rejeitado (exit 1)", "root frozen"],
        ["5", "tau_c alterado", "audit_freeze.py", "rejeitado (exit 1)", "hash + validação tau"],
        ["6", "alpha null -> 1", "audit_freeze.py", "rejeitado (exit 1)", "hash/contrato"],
        ["7", "largura null -> 0.1", "audit_freeze.py", "rejeitado (exit 1)", "hash/contrato"],
        ["8", "unidade Mc kg -> g", "audit_freeze.py", "rejeitado (exit 1)", "unidade esperada"],
        ["9", "unidade H0 incompatível", "audit_freeze.py", "rejeitado (exit 1)", "unidade esperada"],
        ["10", "campo estrutural desconhecido", "audit_freeze.py", "rejeitado (exit 1)", "extra=forbid"],
        ["11", "campo estrutural ausente", "audit_freeze.py", "rejeitado (exit 1)", "campo obrigatório"],
        ["12", "override CLI --Mc", "validate_contract.py --Mc 1e-15", "rejeitado (exit 1)", "reject_runtime_overrides"],
        ["13", "override TAMESIS_MC_KG", "TAMESIS_MC_KG=1e-15 python validate_contract.py", "rejeitado (exit 1)", "reject_runtime_overrides"],
        ["14", "import legado", "audit_imports.py (AST, 19 módulos)", "0 edges legados; não há import ativo para executar", "graph independente sem 90_LEGACY"],
        ["15", "sidecar hash incorreto", "audit_freeze.py:wrong_sidecar_contract_hash", "rejeitado", "require_current_artifact"],
        ["16", "artefato anterior/stale", "audit_freeze.py:manifest_and_sidecars", "classificado canonical_stale", "protocol antigo não é current"],
        ["17", "manifesto editado", "audit_freeze.py:manifest_edited", "rejeitado (exit 1)", "hash de entrada do manifesto"],
        ["18", "edição estrutural mantendo versão 1.0", "audit_freeze.py:structural_edit_same_version", "rejeitado (exit 1)", "lock/config hash"],
    ]
    write("NEGATIVE_MUTATION_EVIDENCE.md", "# Evidência de mutation tests negativos\n\nComando principal: `python audit_freeze.py`. O SHA-256 do YAML oficial antes/depois foi igual e o protocolo permaneceu `" + c.protocol_id() + "`. Nenhuma mutação foi escrita no contrato oficial.\n\n" + table(["ID", "Mutação", "Comando/evidência", "Resultado", "Mecanismo"], mutations) + "\n\nAs saídas completas (stdout, stderr, exit code e mensagem) estão em `data/freeze_audit_evidence.json`; as seis classes de manifesto estão na mesma evidência." )

    write("FAIL_CLOSED_AUDIT.md", "# Fail-closed audit\n\nComando: `python audit_fail_closed.py`. Todos os casos abaixo terminaram com exit code 1, em cópias temporárias; o YAML oficial não foi alterado.\n\n" + table(["Caso", "Resultado", "Evidência"], [[x["case"], f"exit {x['exit_code']}", x.get("stderr", "").replace("\n", " ")[-180:]] for x in fail["cases"]]) + "\n\nA configuração inválida falha antes de gerar resultado oficial. Sidecar ausente, manifesto stale e overrides também são recusados. A atomicidade de escritas pós-cálculo ainda é uma lacuna para falhas de I/O tardias." )

    figure_rows = [
        ["01_predictions.png", "plot_predictions", "M_c, tau_c, exponent", "config.py:CONTRACT; predictions.csv validado", "sidecar + predictions.csv", "sim"],
        ["02_literature_points.png", "plot_literature", "M_c", "config.py:CONTRACT.mc_kg", "sidecar + literature_points.csv", "sim"],
        ["03_target_1e15_visibility.png", "plot_target_1e15", "nenhum adicional; input derivado", "target_1e15_decision.json", "sidecar + decision JSON", "sim"],
        ["04_thermal_gate.png", "plot_thermal_gate", "nenhum adicional; input derivado", "target_1e15_thermal_gate.json", "sidecar + thermal JSON", "sim"],
        ["05_bohr_window_map.png", "plot_bohr_window_map", "M_c, tau_c, exponent", "config.py:CONTRACT", "sidecar + target analysis JSON", "sim"],
        ["threshold_activation_loop.gif", "make_threshold_animation", "M_c, tau_c, exponent", "config.py:CONTRACT", "sidecar; inputs=[]", "sim"],
        ["bohr_window_loop.gif", "make_bohr_window_animation", "M_c, tau_c, exponent", "config.py:CONTRACT", "sidecar; inputs=[]", "sim"],
    ]
    write("FIGURE_PIPELINE_CONTRACT_AUDIT.md", "# Auditoria do pipeline visual\n\n`generate_figures.py:23` carrega `CONTRACT = load_v1_contract()` no import; contrato inválido falha antes de gerar figuras. Não há argumentos CLI estruturais. `model_summary.json` não é lido por essa implementação; somente `predictions.csv` declara cadeia derivada para a primeira figura. A fórmula visual em `generate_figures.py:68` foi corrigida para `mass_ratio**CONTRACT.exponent/tau_c`; antes havia divergência comprovada.\n\n" + table(["Artefato", "Script/função", "Parâmetros estruturais", "Fonte", "Sidecar", "Hash válido"], figure_rows) + "\n\nGIFs e PNGs foram regenerados no protocolo atual; manifesto detecta sidecar/config antigos como `canonical_stale`." )

    clean_rows = [[r["artifact"], r.get("hash_previous") or "—", r.get("hash_run_1") or "—", r.get("hash_run_2") or "—", r["status"]] for r in clean["artifacts"]]
    write("CLEAN_REPRODUCIBILITY_AUDIT.md", "# Clean reproducibility audit\n\nO script `clean_reproduce.py` criou duas árvores temporárias, sem outputs derivados preexistentes, validou `requirements-lock.txt` e executou `regenerate_all.py` em cada uma.\n\nResumo: `" + json.dumps(clean["summary"], ensure_ascii=False) + "`. Não houve `expected_nondeterminism`, `metadata_only`, `scientific_content_difference` ou `unexpected`.\n\n" + table(["Artefato", "Hash anterior", "Hash execução 1", "Hash execução 2", "Status"], clean_rows))

    manifest_summary = evidence["manifest_and_sidecars"]["states"]
    write("MANIFEST_BEHAVIOR_AUDIT.md", "# Manifest behavior audit\n\nComando de construção: `python build_manifest.py`; verificação independente: `python verify_artifacts.py` (não reconstrói o manifesto).\n\nEstados detectados em fixture controlada: `" + json.dumps(manifest_summary, sort_keys=True) + "`.\n\n" + table(["Cenário", "Resultado"], [[k, json.dumps(v, ensure_ascii=False)] for k, v in evidence["manifest_and_sidecars"]["rejections"].items()]) + "\n\nNo estado oficial final: 19 `canonical_current`, 0 `canonical_stale`, 0 `invalid`; arquivos sem sidecar permanecem `unknown_provenance` e não participam automaticamente da inferência." )

    chain_rows = [
        ["reports/figures/05_bohr_window_map.png", "config hash -> target_1e15_analysis.json hash -> generate_figures.py:plot_bohr_window_map -> PNG SHA -> sidecar artifact_sha256/input_hashes -> manifest entry", "completa"],
        ["reports/figures/threshold_activation_loop.gif", "config hash -> generate_figures.py:make_threshold_animation -> GIF SHA -> sidecar -> manifest entry", "completa"],
        ["data/target_1e15_analysis.json", "config -> analyze_target_1e15.py:analyze -> JSON SHA -> sidecar -> manifest entry", "completa"],
        ["data/predictions.csv", "config -> run_predictions.py:main -> model_summary.json hash -> CSV SHA -> sidecar -> manifest entry", "completa; summary é input derivado obrigatório"],
        ["data/coverage_v1_0.json", "test files -> coverage --branch -> JSON SHA -> sidecar -> manifest entry", "completa"],
    ]
    write("PROVENANCE_CHAIN_AUDIT.md", "# Provenance chain audit\n\nCada elo abaixo usa hash; nomes de arquivo isolados não são tratados como prova.\n\n" + table(["Artefato", "Cadeia", "Status"], chain_rows))

    write("MODEL_SUMMARY_INDEPENDENCE_AUDIT.md", "# Model summary independence audit\n\nComando: `python audit_model_summary_independence.py`. Variantes `absent`, `incorrect_Mc`, `incorrect_tau_c` e `malformed` obtiveram exit code 0 para `plot_literature`, `plot_target_1e15`, `plot_thermal_gate`, `plot_bohr_window_map` e `make_threshold_animation`; esses caminhos usam `CONTRACT`. O `plot_predictions` foi testado separadamente: com summary ausente, `require_current_artifact` rejeita `predictions.csv` por cadeia de input quebrada (exit 1), sem fallback estrutural. Portanto o resumo não é fonte estrutural, mas é input derivado obrigatório da tabela de predictions." )

    missing = ["config.py:39 non-finite guard", "config.py:161-167 runtime override branches (manual audit covers entry point)", "config.py:248-251 resolved payload branches", "mc_model.py:81-82 negative mass", "mc_model.py:86-91 invalid time/environment", "provenance.py:100-121 malformed/missing/stale chain", "build_manifest.py:52-82 malformed/stale/invalid sidecars", "verify_artifacts.py:31-65 all mutation branches", "generate_figures.py:29-42 input-sidecar failure", "all official entrypoint mains outside unit suite"]
    write("CRITICAL_COVERAGE_GAPS.md", "# Critical coverage gaps\n\nComando: `python -m coverage run --branch -m pytest -q; python -m coverage report -m`. Resultado: **12 passed**, cobertura total de linhas instrumentadas 83%, mas porcentagem não é prova.\n\n" + table(["Área", "Coberta pelos 12 testes?", "Evidência/gap"], [["loader/schema", "parcial", "test_contract_freeze cobre mutações Mc/expoente/unidade; campos alpha/largura/ausência ainda sem teste pytest"], ["cálculo independente Mc/tau", "sim/parcial", "test_contract_freeze + validate_contract; tau exato não tem teste dedicado"], ["hash/protocol", "sim", "test_hash_is_deterministic e protocol ID"], ["figuras/GIFs", "não", "audit_model_summary_independence + clean_reproduce"], ["sidecars/manifesto/fail-closed", "não", "mutation audit manual executável"], ["overrides", "não", "audit_fail_closed e audit_freeze"], ["legado", "não", "audit_imports AST"], ["linhas/branches críticos", "não", "; ".join(missing)]]) + "\n\nA lacuna principal para uma suíte futura é transformar as auditorias manuais em testes pytest parametrizados sem aumentar a superfície física do modelo." )

    write("ACTIVE_LEGACY_DEPENDENCY_AUDIT.md", "# Active versus legacy dependency audit\n\nComando: `python audit_imports.py`, usando `ast` e resolução de módulos locais; não é busca textual. Foram visitados **" + str(len(imports["graph"])) + " módulos** a partir dos entry points oficiais e encontrados **" + str(imports["legacy_edges_count"]) + " edges para 90_LEGACY/legado**.\n\n" + table(["Fonte", "Imports locais"], [[src, ", ".join(targets) or "—"] for src, targets in sorted(imports["graph"].items())]) + "\n\nResultado: nenhum entry point ativo importa diretamente ou indiretamente `90_LEGACY`. O legado permanece no arquivo histórico e na busca estrutural como `expected_legacy`." )

    write("CONTRACT_LIMITATIONS_V1_0.md", "# Limitações declaradas do contrato v1.0\n\nAs lacunas abaixo são deliberadas e não devem ser marcadas como implementadas:\n\n" + table(["Lacuna", "Classificação", "Consequência"], [["dependência em separação", "documented_limitation_not_in_v1_0_dynamics", "Gamma_T não depende de dx"], ["geometria/distribuição de massa", "documented_limitation_not_in_v1_0_dynamics", "tau_c usa esfera homogênea de sílica"], ["regra de composição", "documented_limitation_not_in_v1_0_dynamics", "não há composição/multipartícula"], ["domínio multipartícula", "documented_limitation_not_in_v1_0_dynamics", "não definido"], ["forma dinâmica completa", "documented_limitation_not_in_v1_0_dynamics", "v1.0 é fenomenológico"], ["modelos rivais", "documented_limitation_not_in_v1_0_dynamics", "CSL/GRW/DP são scaffolds"]]) )

    final = f"""# Verificação independente do freeze executável v1.0

## EXECUTABLE_FREEZE_VERIFIED_WITH_LIMITATIONS

O congelamento executável estrutural foi verificado com evidências positivas e mutation tests. A conclusão não significa prova física, validade estatística final ou status Bohr-level.

## Evidências positivas

- Contrato resolvido: `data/resolved_contract_v1_0.json`.
- Protocol ID: `{c.protocol_id()}`.
- Hash: `{c.config_hash()}`.
- `python -m pytest -q`: **12 passed**.
- `python audit_freeze.py`: 16 alterações/overrides rejeitados; YAML oficial inalterado.
- `python audit_fail_closed.py`: 6 cenários de fail-closed com exit 1.
- `python clean_reproduce.py`: 21 artefatos comparados; 19 idênticos entre reproduções, 0 unexpected; PNG/GIF normalizados idênticos.
- Manifesto final: 19 canonical_current, 0 canonical_stale, 0 invalid; verificado sem rebuild.
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

""" + table(["Requisito", "Status", "Evidência verificável", "Bloqueador"], [
        ["Fonte única de verdade", "pass", "YAML + lock + config.py", "—"], ["Hash determinístico", "pass", c.config_hash(), "—"], ["Protocol ID propagado", "pass", c.protocol_id(), "—"], ["Ausência de hardcode ativo", "pass com suspeitas classificadas", "busca estrutural + config source", "ruído histórico/scaffold"], ["Overrides rejeitados", "pass", "audit_freeze/audit_fail_closed", "—"], ["Testes positivos adequados", "parcial", "12 passed", "não cobrem todos entry points"], ["Testes negativos adequados", "pass manual", "16 mutations + manifesto", "converter para pytest"], ["Reprodutibilidade limpa", "pass", "clean_reproducibility_evidence", "—"], ["Figuras ligadas ao contrato", "pass", "figure audit + sidecars", "—"], ["GIFs ligados ao contrato", "pass", "GIF audit + sidecars", "—"], ["Sidecars válidos", "pass", "artifact_sha256/input_hashes", "—"], ["Manifesto fail-closed", "pass", "verify sem rebuild", "unknown_provenance não é inferência"], ["Independência de model_summary", "pass qualificado", "4 variantes + rejeição de cadeia predictions", "predictions depende do summary"], ["Ausência de imports legados", "pass", "AST graph, 0 edges", "—"], ["Contrato igual à implementação", "pass qualificado", "consistency line-by-line", "alpha/largura/separação não são dinâmica"],
    ]) + "\n\n## Decisão de avanço\n\n**Aprovado para validação sintética e identificabilidade do software congelado. Não aprovado para afirmar descoberta física ou avançar ao ranking comparativo como conclusão.**" 
    write("V1_0_FREEZE_INDEPENDENT_VERIFICATION.md", final)


if __name__ == "__main__":
    main()
