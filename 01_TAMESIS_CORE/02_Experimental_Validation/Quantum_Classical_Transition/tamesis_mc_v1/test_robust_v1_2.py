import numpy as np
from synthetic_validation.robust_v1_2 import baseline,l0_nominal,l1_mixture,l2_student_t

def test_v11_baseline_is_reproduced_fail_closed(): assert baseline()[0]["fail_closed_passed"]
def test_mixture_semantics_downweight_extreme_residual():
    x=np.ones(20); y=np.zeros(20); y[-1]=15
    _,q=l1_mixture(y,x)
    assert q[-1]>q[0]
def test_truth_label_is_not_an_estimator_input():
    x=np.arange(1,6,dtype=float); y=.7*x
    assert abs(l0_nominal(y,x)[0]-.7)<1e-12
    assert abs(l2_student_t(y,x)[0]-.7)<1e-6
