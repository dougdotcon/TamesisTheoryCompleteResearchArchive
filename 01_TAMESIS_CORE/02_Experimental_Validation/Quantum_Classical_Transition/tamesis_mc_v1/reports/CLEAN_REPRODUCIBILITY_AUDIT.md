# Clean reproducibility audit

O script `clean_reproduce.py` criou duas árvores temporárias, sem outputs derivados preexistentes, validou `requirements-lock.txt` e executou `regenerate_all.py` em cada uma.

Resumo: `{"byte_identical_between_clean_runs": 19, "compared": 21, "metadata_only": 0, "unexpected": 0}`. Não houve `expected_nondeterminism`, `metadata_only`, `scientific_content_difference` ou `unexpected`.

| Artefato | Hash anterior | Hash execução 1 | Hash execução 2 | Status |
| --- | --- | --- | --- | --- |
| data/comparison_report.json | 5316ed209991ad233b3b03cf60ac897ca4343bff228f97421be8eb3690984c14 | 5316ed209991ad233b3b03cf60ac897ca4343bff228f97421be8eb3690984c14 | 5316ed209991ad233b3b03cf60ac897ca4343bff228f97421be8eb3690984c14 | none |
| data/coverage_v1_0.json | 1b3623c8d878cad4401636315936528a45c7f108dc40d8fcdb1dd00d4f1852a0 | — | — | none |
| data/freeze_audit_evidence.json | 30ff576b93e35d4ad9dfd1a80d52f73877cf7ad24cc3f692b6955020b850257d | — | — | none |
| data/literature_points.csv | c54423255e2ed4cc2872289ddb6515b109983417edc80651eeb2c5b7885d3ab6 | c54423255e2ed4cc2872289ddb6515b109983417edc80651eeb2c5b7885d3ab6 | c54423255e2ed4cc2872289ddb6515b109983417edc80651eeb2c5b7885d3ab6 | none |
| data/literature_points_v2.csv | 886b374f4f3a8c417af84ddb22527e87aea41e3bff5b2e4484d30b8ca3fe6e42 | 886b374f4f3a8c417af84ddb22527e87aea41e3bff5b2e4484d30b8ca3fe6e42 | 886b374f4f3a8c417af84ddb22527e87aea41e3bff5b2e4484d30b8ca3fe6e42 | none |
| data/model_summary.json | 1d5c656d69a954165fcd47ca8b88402c0952ae1a658a070c68534119315313b7 | 1d5c656d69a954165fcd47ca8b88402c0952ae1a658a070c68534119315313b7 | 1d5c656d69a954165fcd47ca8b88402c0952ae1a658a070c68534119315313b7 | none |
| data/predictions.csv | 929e288cb90016d7cedae4737fbc1cd0ea0289694c45b0647f330c6b63916226 | 929e288cb90016d7cedae4737fbc1cd0ea0289694c45b0647f330c6b63916226 | 929e288cb90016d7cedae4737fbc1cd0ea0289694c45b0647f330c6b63916226 | none |
| data/resolved_contract_v1_0.json | 829b7b4c83bbb2275da93f2a848bd2857d5d249012d66d0ea94afb752a32682b | 829b7b4c83bbb2275da93f2a848bd2857d5d249012d66d0ea94afb752a32682b | 829b7b4c83bbb2275da93f2a848bd2857d5d249012d66d0ea94afb752a32682b | none |
| data/target_1e15_analysis.json | fff1c67c8b35f294de34e0f324dd2f3fe501d1eb8ca75ce84afb2b0440c31db1 | fff1c67c8b35f294de34e0f324dd2f3fe501d1eb8ca75ce84afb2b0440c31db1 | fff1c67c8b35f294de34e0f324dd2f3fe501d1eb8ca75ce84afb2b0440c31db1 | none |
| data/target_1e15_decision.json | 0edbce3e83478a7bb753ffd219028351e6deafe265d0cf3ea8841dc38374691a | 0edbce3e83478a7bb753ffd219028351e6deafe265d0cf3ea8841dc38374691a | 0edbce3e83478a7bb753ffd219028351e6deafe265d0cf3ea8841dc38374691a | none |
| data/target_1e15_noise_budget.json | 54f9ac35cd42b051405b0bec1490e9334aa92fc7766a18e3aed576ccb0f0d51a | 54f9ac35cd42b051405b0bec1490e9334aa92fc7766a18e3aed576ccb0f0d51a | 54f9ac35cd42b051405b0bec1490e9334aa92fc7766a18e3aed576ccb0f0d51a | none |
| data/target_1e15_sensitivity.json | 8dca4e919902067abb6bdfb9d286df04edb564831e97b8d0ad21a5db3e10dcfe | 8dca4e919902067abb6bdfb9d286df04edb564831e97b8d0ad21a5db3e10dcfe | 8dca4e919902067abb6bdfb9d286df04edb564831e97b8d0ad21a5db3e10dcfe | none |
| data/target_1e15_thermal_gate.json | d5d9902215fc1cd2dae5a9fdcf1ba2079b44e2b3d15a93250abf874bffc8239d | d5d9902215fc1cd2dae5a9fdcf1ba2079b44e2b3d15a93250abf874bffc8239d | d5d9902215fc1cd2dae5a9fdcf1ba2079b44e2b3d15a93250abf874bffc8239d | none |
| data/target_priority_report.json | f10b87049f72535cf4d6f0bacc2cf820ac1203cf5c5a7b3bd3ee96e86070e02f | f10b87049f72535cf4d6f0bacc2cf820ac1203cf5c5a7b3bd3ee96e86070e02f | f10b87049f72535cf4d6f0bacc2cf820ac1203cf5c5a7b3bd3ee96e86070e02f | none |
| reports/figures/01_predictions.png | f431357ca05f00c6e19d0383829e702f872f0cae38737e1e4f3528c2aaa166a0 | f431357ca05f00c6e19d0383829e702f872f0cae38737e1e4f3528c2aaa166a0 | f431357ca05f00c6e19d0383829e702f872f0cae38737e1e4f3528c2aaa166a0 | none |
| reports/figures/02_literature_points.png | 959c51cf9498abc8af54072c456ba60572aabc175621d3c39ca7d63ba30b03e6 | 959c51cf9498abc8af54072c456ba60572aabc175621d3c39ca7d63ba30b03e6 | 959c51cf9498abc8af54072c456ba60572aabc175621d3c39ca7d63ba30b03e6 | none |
| reports/figures/03_target_1e15_visibility.png | 0c5ea84e639b18bca0ad9b5511992f20beeb2056d3950c14a468bd5429d4cea2 | 0c5ea84e639b18bca0ad9b5511992f20beeb2056d3950c14a468bd5429d4cea2 | 0c5ea84e639b18bca0ad9b5511992f20beeb2056d3950c14a468bd5429d4cea2 | none |
| reports/figures/04_thermal_gate.png | a5e72df1061dd85322af12b47a0d03e5340c6334a63bf5c8194aee6fb3465c2a | a5e72df1061dd85322af12b47a0d03e5340c6334a63bf5c8194aee6fb3465c2a | a5e72df1061dd85322af12b47a0d03e5340c6334a63bf5c8194aee6fb3465c2a | none |
| reports/figures/05_bohr_window_map.png | cdc9aa619b8702bab2fbd42d7f21ba5be3861ae42effbfd3495cbb866cddc25b | cdc9aa619b8702bab2fbd42d7f21ba5be3861ae42effbfd3495cbb866cddc25b | cdc9aa619b8702bab2fbd42d7f21ba5be3861ae42effbfd3495cbb866cddc25b | none |
| reports/figures/bohr_window_loop.gif | c647f5b1a1a3d485daeaa451656674814a2bd08955f8998207bbcbd3f572ab67 | c647f5b1a1a3d485daeaa451656674814a2bd08955f8998207bbcbd3f572ab67 | c647f5b1a1a3d485daeaa451656674814a2bd08955f8998207bbcbd3f572ab67 | none |
| reports/figures/threshold_activation_loop.gif | 6fe43287d7e4878f53e4f5ff81865c40d0a9d6da5f3b5565d75445474610ca94 | 6fe43287d7e4878f53e4f5ff81865c40d0a9d6da5f3b5565d75445474610ca94 | 6fe43287d7e4878f53e4f5ff81865c40d0a9d6da5f3b5565d75445474610ca94 | none |
