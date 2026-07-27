SYNTHETIC_VALIDATION_PASSED_WITH_LIMITATIONS

# Synthetic validation execution report

Protocol: `tamesis-mc-v1.0:d3d9b22cdb62a335a9cfe14d4a066d7f4ea314881892453e7594b3fa7a546d0e`
Synthetic protocol: `tamesis-synthetic-v1.0:c11dce74f55d478ac5f14fb0ca98771094342fe020ee01ed4fd4a760ecd260c7`
Standard rows: 60000 (1000 replicas per truth/scenario).
False-positive rate: 0.000%. Strong-subset power: 100.000%. Coverage proxy: 100.000% (over-conservative; outside the 90-98% target). Blind informative accuracy: 100.000%; overall accuracy: 27.900%, with 72.100% inconclusive.

The pipeline recovers strong injected Tamesis behavior under the nominal calibrated generator, rejects false discoveries in nominal H0 runs, and returns inconclusive decisions near/below threshold. It does **not** establish physical truth or structural separation from environmental decoherence. The next scientific step is a jointly fitted multi-time, multi-pressure design with a validated environment likelihood and then frozen analysis on real data.
