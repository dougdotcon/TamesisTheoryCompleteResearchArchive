# Auditoria do pipeline visual

`generate_figures.py:23` carrega `CONTRACT = load_v1_contract()` no import; contrato inválido falha antes de gerar figuras. Não há argumentos CLI estruturais. `model_summary.json` não é lido por essa implementação; somente `predictions.csv` declara cadeia derivada para a primeira figura. A fórmula visual em `generate_figures.py:68` foi corrigida para `mass_ratio**CONTRACT.exponent/tau_c`; antes havia divergência comprovada.

| Artefato | Script/função | Parâmetros estruturais | Fonte | Sidecar | Hash válido |
| --- | --- | --- | --- | --- | --- |
| 01_predictions.png | plot_predictions | M_c, tau_c, exponent | config.py:CONTRACT; predictions.csv validado | sidecar + predictions.csv | sim |
| 02_literature_points.png | plot_literature | M_c | config.py:CONTRACT.mc_kg | sidecar + literature_points.csv | sim |
| 03_target_1e15_visibility.png | plot_target_1e15 | nenhum adicional; input derivado | target_1e15_decision.json | sidecar + decision JSON | sim |
| 04_thermal_gate.png | plot_thermal_gate | nenhum adicional; input derivado | target_1e15_thermal_gate.json | sidecar + thermal JSON | sim |
| 05_bohr_window_map.png | plot_bohr_window_map | M_c, tau_c, exponent | config.py:CONTRACT | sidecar + target analysis JSON | sim |
| threshold_activation_loop.gif | make_threshold_animation | M_c, tau_c, exponent | config.py:CONTRACT | sidecar; inputs=[] | sim |
| bohr_window_loop.gif | make_bohr_window_animation | M_c, tau_c, exponent | config.py:CONTRACT | sidecar; inputs=[] | sim |

GIFs e PNGs foram regenerados no protocolo atual; manifesto detecta sidecar/config antigos como `canonical_stale`.
