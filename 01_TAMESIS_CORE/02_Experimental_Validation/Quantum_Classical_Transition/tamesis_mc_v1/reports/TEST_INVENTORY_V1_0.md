# Inventário dos 12 testes atuais

Comando: `python -m pytest -q` — **12 passed**.

| Teste | Tipo | Afirmação verificada | Falharia com qual mutação? |
| --- | --- | --- | --- |
| test_contract_reproduces_frozen_mc_and_protocol_id | golden/schema | Mc congelado, equação e protocol ID | Mc congelado ou hash/protocol divergente |
| test_model_is_bound_to_contract | integration | McModel usa contrato atual | McModel usar constante legada |
| test_rejects_modified_mc | negative | Mc alterado é rejeitado | Mc +1% |
| test_rejects_modified_exponent | negative | expoente não pode derivar do arquivo adulterado | exponente 3 |
| test_rejects_modified_unit | negative/schema | unidade H0 inválida é rejeitada | H0 em m s^-1 |
| test_hash_is_deterministic | reproducibility | serialização/hash determinísticos | mesmo contrato carregado duas vezes ter hashes diferentes |
| test_derived_scale_and_radius | unit | Mc, raio e tau aproximados | Mc/radius/tau fora da tolerância |
| test_sharp_threshold_is_explicit | unit | limiar sharp e lado acima | Gamma(Mc) não ser zero |
| test_quadratic_scaling_above_threshold | unit | expoente quadrático | expoente 1 ou 3 |
| test_environment_is_an_explicit_nuisance | unit | ambiente separado do intrinsic_rate | ambiente alterar Gamma_T |
| test_gas_collision_rate_scales_with_pressure | unit | taxa de gás escala com pressão | pressão x1000 não produzir taxa x1000 |
| test_pressure_for_rate_inverts_gas_rate | unit | inversão pressão/taxa | pressão calculada não inverter a taxa |
