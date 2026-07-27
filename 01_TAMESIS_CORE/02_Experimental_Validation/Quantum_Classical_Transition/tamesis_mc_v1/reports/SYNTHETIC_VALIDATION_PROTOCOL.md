# Synthetic validation protocol

Frozen Tamesis protocol: `tamesis-mc-v1.0:d3d9b22cdb62a335a9cfe14d4a066d7f4ea314881892453e7594b3fa7a546d0e`. Synthetic protocol: `tamesis-synthetic-v1.0:c11dce74f55d478ac5f14fb0ca98771094342fe020ee01ed4fd4a760ecd260c7`.

Primary inference is exclusively H0 = QM + environment versus H1 = Tamesis M_c v1.0 + environment. Rival collapse models are excluded. The generator emits independent Poisson phase counts and the inferer receives only measured fields. Decision rules were fixed in `config/synthetic_validation_v1.yaml`: |LR| > 3.84, at least 200 counts, visibility sigma <= 0.15. Standard runs use 1000 replicas per truth/scenario.
