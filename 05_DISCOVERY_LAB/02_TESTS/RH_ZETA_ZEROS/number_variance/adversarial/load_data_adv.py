"""
Carrega zeros1.txt e zeros3.txt (dado real, tocado pela primeira vez aqui,
depois de todas as validacoes sinteticas terem passado) e renormaliza para
x_m, seguindo EXATAMENTE a Secao 3 do pre-registro.

zeros1.txt: uma linha por gamma absoluto. x_m = N(gamma_m).
zeros3.txt: cabecalho em prosa + offsets de base=267653395647.
            x_m = offset_m * N'(base), N'(E) = (1/2pi)*log(E/2pi).

zeros4.txt: NAO TOCADO (nenhuma linha numerica lida).
"""
import numpy as np
from estimator_adv import N_riemann_von_mangoldt, N_prime

DATA_DIR = "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/RH_ZETA_ZEROS/data"


def load_zeros1():
    path = f"{DATA_DIR}/zeros1.txt"
    gammas = np.loadtxt(path, dtype=np.float64)
    assert gammas.size == 100000, f"esperado 100000 zeros, achei {gammas.size}"
    x = N_riemann_von_mangoldt(gammas)
    return gammas, x


def load_zeros3():
    path = f"{DATA_DIR}/zeros3.txt"
    base = 267653395647.0
    offsets = []
    with open(path) as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            try:
                v = float(s.replace(",", ""))
            except ValueError:
                continue
            offsets.append(v)
    offsets = np.array(offsets, dtype=np.float64)
    assert offsets.size == 10000, f"esperado 10000 offsets, achei {offsets.size}"
    Nprime_base = N_prime(base)
    x = offsets * Nprime_base
    return offsets, base, Nprime_base, x


if __name__ == "__main__":
    gammas1, x1 = load_zeros1()
    print(f"zeros1: n={gammas1.size}  gamma range=[{gammas1.min():.4f}, {gammas1.max():.4f}]  "
          f"T(max gamma)={gammas1.max():.6f}")
    print(f"  x1 range=[{x1.min():.6f}, {x1.max():.6f}]  x_range={x1.max()-x1.min():.6f}")
    print(f"  (DESIGN.json declara T=74920.827498994, x_range=99998.95581061838)")
    print(f"  logT (meu calculo, ln) = {np.log(gammas1.max()):.10f}")
    print(f"  (DESIGN.json declara logT=11.22418720159839)")

    offsets3, base3, Nprime_base3, x3 = load_zeros3()
    print(f"\nzeros3: n={offsets3.size}  base={base3}  offset range=[{offsets3.min():.4f},{offsets3.max():.4f}]")
    print(f"  N'(base) = {Nprime_base3:.10f}")
    print(f"  x3 range=[{x3.min():.6f}, {x3.max():.6f}]  x_range={x3.max()-x3.min():.6f}")
    print(f"  (DESIGN.json declara x_range=10000.086866729916)")
    T3 = base3  # T usado no design e a altura (aprox = base, offset desprezivel p/ logT)
    print(f"  logT (ln(base)) = {np.log(base3):.10f}")
    print(f"  (DESIGN.json declara logT=26.312958680598655)")
