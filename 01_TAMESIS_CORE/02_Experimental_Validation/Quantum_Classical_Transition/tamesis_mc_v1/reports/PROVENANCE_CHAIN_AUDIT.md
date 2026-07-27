# Provenance chain audit

Cada elo abaixo usa hash; nomes de arquivo isolados não são tratados como prova.

| Artefato | Cadeia | Status |
| --- | --- | --- |
| reports/figures/05_bohr_window_map.png | config hash -> target_1e15_analysis.json hash -> generate_figures.py:plot_bohr_window_map -> PNG SHA -> sidecar artifact_sha256/input_hashes -> manifest entry | completa |
| reports/figures/threshold_activation_loop.gif | config hash -> generate_figures.py:make_threshold_animation -> GIF SHA -> sidecar -> manifest entry | completa |
| data/target_1e15_analysis.json | config -> analyze_target_1e15.py:analyze -> JSON SHA -> sidecar -> manifest entry | completa |
| data/predictions.csv | config -> run_predictions.py:main -> model_summary.json hash -> CSV SHA -> sidecar -> manifest entry | completa; summary é input derivado obrigatório |
| data/coverage_v1_0.json | test files -> coverage --branch -> JSON SHA -> sidecar -> manifest entry | completa |
