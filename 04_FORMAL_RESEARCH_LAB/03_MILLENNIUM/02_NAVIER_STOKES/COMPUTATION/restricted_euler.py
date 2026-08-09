"""
Restricted Euler equation (Vieillefosse 1982; Cantwell 1992 exact solution)
for the velocity-gradient tensor, used here ONLY as a finite-dimensional
test case for the NS-PRESSURE-001 audit question:

    Does a bounded alignment gap between vorticity and the MOST EXTENSIVE
    eigenvector of the strain tensor (e1), i.e. <alpha_1> <= 1 - delta_0,
    by itself prevent finite-time blow-up?

Construction (finite-dimensional ODE, NOT the full PDE):
  M = grad(u) = A + Omega,  A = sym(M) traceless (rate of strain),
  Omega antisymmetric with associated vector omega (vorticity), Omega x = omega x x.
  Restricted Euler closes the pressure Hessian by its ISOTROPIC part only
  (drops the anisotropic, nonlocal part and viscosity):
      dM/dt = -M^2 + (1/3) tr(M^2) I
  Using Omega^2 = omega omega^T - |omega|^2 I  (standard identity for the
  cross-product antisymmetric matrix) and tr(A Omega) = 0 for symmetric A,
  antisymmetric Omega, this splits into:
      dA/dt   = -A^2 + (1/3) tr(A^2) I  -  (omega omega^T - (1/3)|omega|^2 I)
      domega/dt = A omega                          (vortex stretching)

This reproduces the classical Vieillefosse restricted-Euler dynamics
(finite-time blow-up for generic initial data, "Vieillefosse tail").
We are NOT claiming this models full Navier-Stokes; the anisotropic
pressure Hessian (the exact nonlocal, unclosed term) is precisely what is
dropped here. The point of the experiment is narrower and rigorous on its
own terms: in this well-defined 8-dof ODE system, does the alignment
cosine between omega and e1 (top eigenvector of A) stay in a "gap" (well
below 1) WHILE the solution still blows up in finite time? If yes, that
is a concrete, checkable demonstration that "bounded alignment with e1"
is not, by itself, a sufficient mechanism to rule out blow-up -- more
must be assumed about the RATE at which alignment stays bounded relative
to stretching, exactly the gap the legacy document calls Lemma 3.1.
"""
import numpy as np
from scipy.integrate import solve_ivp

def rhs(t, y):
    A = y[:9].reshape(3, 3)
    A = 0.5 * (A + A.T)  # keep numerically symmetric
    A -= np.trace(A) / 3.0 * np.eye(3)  # keep numerically traceless
    omega = y[9:12]

    A2 = A @ A
    trA2 = np.trace(A2)
    omega_outer = np.outer(omega, omega)
    omega2 = np.dot(omega, omega)

    dA = -A2 + (trA2 / 3.0) * np.eye(3) - omega_outer + (omega2 / 3.0) * np.eye(3)
    domega = A @ omega

    return np.concatenate([dA.flatten(), domega])

def run_case(A0, omega0, t_max=50.0, label=""):
    y0 = np.concatenate([A0.flatten(), omega0])

    def blowup_event(t, y):
        A = y[:9].reshape(3, 3)
        return 1000.0 - np.linalg.norm(A)
    blowup_event.terminal = True
    blowup_event.direction = -1

    sol = solve_ivp(rhs, [0, t_max], y0, method="RK45",
                     max_step=0.001, events=blowup_event,
                     rtol=1e-10, atol=1e-12, dense_output=False)

    ts = sol.t
    Anorms = []
    align_e1 = []
    align_emid = []
    align_emin = []
    for i in range(len(ts)):
        y = sol.y[:, i]
        A = y[:9].reshape(3, 3)
        A = 0.5 * (A + A.T)
        omega = y[9:12]
        no = np.linalg.norm(omega)
        evals, evecs = np.linalg.eigh(A)  # ascending order
        # ascending: evals[0] <= evals[1] <= evals[2]; e1 = most extensive = evals[2]
        e_min, e_mid, e_max = evecs[:, 0], evecs[:, 1], evecs[:, 2]
        Anorms.append(np.linalg.norm(A))
        if no > 1e-12:
            align_e1.append(abs(np.dot(omega, e_max)) / no)
            align_emid.append(abs(np.dot(omega, e_mid)) / no)
            align_emin.append(abs(np.dot(omega, e_min)) / no)
        else:
            align_e1.append(np.nan)
            align_emid.append(np.nan)
            align_emin.append(np.nan)

    blew_up = sol.status == 1  # terminal event fired
    print(f"--- case {label} ---")
    print(f"  blew up (|A| reached 1000): {blew_up}, t_final = {ts[-1]:.6f}, steps = {len(ts)}")
    print(f"  |A|(t_final) = {Anorms[-1]:.3f}")
    # report alignment cosine^2 (= alpha_1 style quantity) over last 20% of trajectory
    n = len(ts)
    tail = slice(int(0.8 * n), n)
    a1_tail = np.array(align_e1[tail])
    amid_tail = np.array(align_emid[tail])
    amin_tail = np.array(align_emin[tail])
    print(f"  alignment |cos(omega,e_max)|  tail: mean={np.nanmean(a1_tail):.4f} max={np.nanmax(a1_tail):.4f}")
    print(f"  alignment |cos(omega,e_mid)|  tail: mean={np.nanmean(amid_tail):.4f} max={np.nanmax(amid_tail):.4f}")
    print(f"  alignment |cos(omega,e_min)|  tail: mean={np.nanmean(amin_tail):.4f} max={np.nanmax(amin_tail):.4f}")
    print(f"  alpha1 = cos^2(omega,e_max) at final step: {align_e1[-1]**2:.4f}")
    print()
    return dict(ts=ts, Anorms=Anorms, align_e1=align_e1, align_emid=align_emid,
                align_emin=align_emin, blew_up=blew_up)

if __name__ == "__main__":
    rng = np.random.default_rng(12345)
    results = []
    for k in range(6):
        # generic traceless symmetric A0, generic omega0 (not pre-aligned with any eigvec)
        M0 = rng.normal(size=(3, 3)) * 0.5
        A0 = 0.5 * (M0 + M0.T)
        A0 -= np.trace(A0) / 3.0 * np.eye(3)
        omega0 = rng.normal(size=3) * 0.5
        res = run_case(A0, omega0, label=f"random-{k}")
        results.append(res)

    n_blowup = sum(r["blew_up"] for r in results)
    print(f"SUMMARY: {n_blowup}/{len(results)} random restricted-Euler cases reached |A|=1000 in finite time")
