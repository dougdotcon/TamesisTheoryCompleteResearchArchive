# Auditoria linha a linha: contrato versus implementação

Hash: `d3d9b22cdb62a335a9cfe14d4a066d7f4ea314881892453e7594b3fa7a546d0e`  \nProtocol ID: `tamesis-mc-v1.0:d3d9b22cdb62a335a9cfe14d4a066d7f4ea314881892453e7594b3fa7a546d0e`

| ID | Afirmação contratual | Arquivo de implementação | Teste | Status | Evidência |
| --- | --- | --- | --- | --- | --- |
| C01 | Mc = mP(a0/aP)^(1/8) | mc_model.py:11 compute_mc_from_contract; config.py:237 load_v1_contract | test_contract_freeze.py:test_contract_reproduces_frozen_mc_and_protocol_id | implemented_and_tested | cálculo independente coincide: 5.292674126388712e-16 kg; mutation root 7/9 rejeitada |
| C02 | H0 convertido para SI | config.py:98-101 V1Contract.h0_si | validate_contract.py (comando executado); sem teste pytest específico | implemented_without_test | H0 70 km s^-1 Mpc^-1 -> 2.268545502662652e-18 s^-1 |
| C03 | tau_c congelado e validado | config.py:193-195; mc_model.py:48 | test_contract_freeze.py:test_derived_scale_and_radius + validate_contract.py | implemented_and_tested | 2.176246482178091 s; mutation tau_c rejeitada |
| C04 | Gamma_T=0 para M<=Mc | mc_model.py:72-78 | test_mc_model.py:test_sharp_threshold_is_explicit | implemented_and_tested | M=Mc dá 0; teste também verifica lado direito |
| C05 | Gamma_T=tau_c^-1(M/Mc)^2 acima | mc_model.py:78 | test_mc_model.py:test_quadratic_scaling_above_threshold | implemented_and_tested | razão 2Mc/4Mc=0.25 |
| C06 | visibility=exp(-(GammaT+Gammaenv)t) | mc_model.py:84-88 | test_mc_model.py:test_environment_is_an_explicit_nuisance | implemented_and_tested | ambiente é somado explicitamente |
| C07 | separação ausente em v1.0 | config/tamesis_mc_v1.yaml:57; compare_models.py:63 dx só em rivais | nenhum teste específico de ausência | partially_implemented | documentado; não entra em Gamma_T v1.0 |
| C08 | alpha explicitamente ausente | config/tamesis_mc_v1.yaml:47-49 | loader Pydantic; sem teste pytest específico | implemented_without_test | value=null/classification=absent_in_v1_0 |
| C09 | largura explicitamente ausente | config/tamesis_mc_v1.yaml:54-56 | loader Pydantic; sem teste pytest específico | implemented_without_test | value=null/classification=absent_in_v1_0 |
| C10 | modelo ambiental separado | environment_model.py; compare_models.py:107-123 | test_environment_model.py:4,11 | implemented_and_tested | inversão de pressão e escala linear passam |
| C11 | ranking marcado legacy_exploratory_ranking | compare_models.py:214 | regenerate_all.py + artefato comparison_report.json | implemented_and_tested | não tratado como conclusão física |
| C12 | sidecars de proveniência | provenance.py:36-98 | audit_freeze.py + verify_artifacts.py | implemented_and_tested | hash do artefato, inputs, protocol ID e config hash |
| C13 | manifesto automático | build_manifest.py:85-145 | audit_freeze.py + verify_artifacts.py | implemented_and_tested | seis estados distinguidos; adulterações rejeitadas |
| C14 | CSL/GRW/DP completos | compare_models.py:39-63 | nenhum | documented_not_implemented | scaffold comparativo, sem corpos estendidos/calibração final |
| C15 | likelihood estatística final | reports/STATISTICAL_ANALYSIS_PLAN_V1_0.md | nenhum | documented_not_implemented | plano pré-registrado, não análise discriminante final |
| C16 | massa-separação-geometria da plataforma | reports/TARGET_1E15_FEASIBILITY_AUDIT.md | nenhum | documented_not_implemented | limitação de plataforma, fora da dinâmica v1.0 |
