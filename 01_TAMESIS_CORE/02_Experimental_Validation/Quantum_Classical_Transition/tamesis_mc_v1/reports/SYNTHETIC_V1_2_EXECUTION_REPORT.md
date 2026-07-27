ROBUST_JOINT_IDENTIFIABILITY_NOT_ESTABLISHED

# Synthetic v1.2 execution report

Protocol `tamesis-synthetic-v1.2:aceb5a8af5e98497411642dce828fd006b39e6529092fde20bc409f0081b6967`. Baseline fail-closed passed and reproduced 75/1000. L1 improves isolated contamination, but mass-correlated and above-Mc contamination remain confounded with the physical signature; robust identification is therefore not established.

| Question | Result | Evidence | Limitation |
|---|---|---|---|
| L0 reproduces 7.5%? | Yes | 75/1000 baseline | Historical synthetic result |
| L1 controls isolated outliers? | Yes | O1 family | Does not control O12 |
| Control without erasing H1? | No | O12 signal-outlier rate | Signal resembles contamination |
| epsilon/kappa identifiable? | Weak/boundary | multi-start profiles | correlated with mu_T |
| mu_T robustly identifiable? | No | adversarial profiles | O9/O12 multimodal |
| D4 discriminates or identifies? | Discriminates | fixed H0/H1 | rank 4/5 |
| D5 remains ill-conditioned? | Yes | condition 517445 | external calibration needed |
| 1e-15 kg robust? | Not established | O12 ambiguity | telemetry missing |
