"""
Analise pre-registrada de DISC-COSMOLOGY-MOND-SPARC-001.

Implementa EXATAMENTE a Secao 4 de ../PREREGISTRATION.md sobre dado real:
- data/SPARC_Lelli2016c.mrt (classificacao de grupo via coluna f_D)
- data/Rotmod_LTG/<nome>_rotmod.dat (curvas de rotacao observadas)

Nao ha nenhum dado embutido/fabricado neste script. Qualquer falha de
leitura de arquivo e um erro fatal, nao um fallback silencioso.
"""
import json
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent / "data"
MRT_FILE = DATA_DIR / "SPARC_Lelli2016c.mrt"
ROTMOD_DIR = DATA_DIR / "Rotmod_LTG"


def load_catalog():
    """Parse SPARC_Lelli2016c.mrt: nome + f_D (metodo de distancia)."""
    with open(MRT_FILE) as f:
        lines = f.readlines()

    # As 98 primeiras linhas sao cabecalho/documentacao byte-a-byte do .mrt
    # (verificado por inspecao direta do arquivo nesta sessao).
    data_lines = [l for l in lines[98:] if l.strip()]
    if len(data_lines) != 175:
        raise RuntimeError(
            f"esperado 175 galaxias no catalogo, encontrado {len(data_lines)} "
            "-- proveniencia do dado pode ter mudado, parar e investigar"
        )

    catalog = {}
    for line in data_lines:
        parts = line.split()
        name = parts[0]
        f_d = parts[4]
        catalog[name] = f_d
    return catalog


def load_rotmod(name):
    """Le radii e velocidades observadas reais de um arquivo *_rotmod.dat."""
    path = ROTMOD_DIR / f"{name}_rotmod.dat"
    if not path.exists():
        return None
    radii, vobs = [], []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            cols = line.split()
            radii.append(float(cols[0]))
            vobs.append(float(cols[1]))
    return np.array(radii), np.array(vobs)


def outer_slope(radii, vobs):
    """Inclinacao log-log da metade externa da curva (Secao 4, passo 1-3)."""
    n = len(radii)
    mid = n // 2
    r_outer = radii[mid:]
    v_outer = vobs[mid:]
    if len(r_outer) < 2:
        return None
    log_r = np.log(r_outer)
    log_v = np.log(v_outer)
    coeffs = np.polyfit(log_r, log_v, 1)
    return float(coeffs[0])


def main():
    catalog = load_catalog()
    print(f"[1] Catalogo real carregado: {len(catalog)} galaxias")

    cluster_slopes = []
    field_slopes = []
    cluster_names = []
    field_names = []
    excluded = []

    for name, f_d in catalog.items():
        rc = load_rotmod(name)
        if rc is None:
            excluded.append((name, "sem arquivo rotmod"))
            continue
        radii, vobs = rc
        slope = outer_slope(radii, vobs)
        if slope is None:
            excluded.append((name, "menos de 2 pontos na metade externa"))
            continue

        if f_d == "4":
            cluster_slopes.append(slope)
            cluster_names.append(name)
        else:
            field_slopes.append(slope)
            field_names.append(name)

    print(f"[2] Grupo aglomerado (Ursa Maior, f_D=4): N={len(cluster_slopes)}")
    print(f"    Grupo campo (f_D != 4): N={len(field_slopes)}")
    print(f"    Excluidas: {len(excluded)} ({excluded})")

    cluster_slopes = np.array(cluster_slopes)
    field_slopes = np.array(field_slopes)

    cluster_mean = float(np.mean(cluster_slopes))
    cluster_std = float(np.std(cluster_slopes, ddof=1))
    field_mean = float(np.mean(field_slopes))
    field_std = float(np.std(field_slopes, ddof=1))

    # Welch t-test, uma cauda (Secao 4-5 do pre-registro): H1 = cluster < field
    t_stat, p_two_sided = stats.ttest_ind(
        cluster_slopes, field_slopes, equal_var=False
    )
    # p de uma cauda na direcao prevista (cluster_mean < field_mean)
    if t_stat < 0:
        p_one_sided = p_two_sided / 2
    else:
        p_one_sided = 1 - p_two_sided / 2

    direction_matches_efe = cluster_mean < field_mean
    efe_supported = direction_matches_efe and p_one_sided < 0.05

    print("\n[3] RESULTADO (calculado exatamente conforme PREREGISTRATION.md Secao 4-5)")
    print(f"    Aglomerado (Ursa Maior): mean slope = {cluster_mean:+.4f} +/- {cluster_std:.4f} (N={len(cluster_slopes)})")
    print(f"    Campo:                   mean slope = {field_mean:+.4f} +/- {field_std:.4f} (N={len(field_slopes)})")
    print(f"    t-statistic (Welch)    = {t_stat:.4f}")
    print(f"    p-value (uma cauda)    = {p_one_sided:.6f}")
    print(f"    Direcao bate com EFE (aglomerado < campo)? {direction_matches_efe}")
    print(f"    Veredito pre-registrado: {'SUPORTA EFE' if efe_supported else 'NAO SUPORTA / FALSIFICA EFE'}")

    result = {
        "test_id": "DISC-COSMOLOGY-MOND-SPARC-001",
        "n_cluster": len(cluster_slopes),
        "n_field": len(field_slopes),
        "cluster_names": sorted(cluster_names),
        "n_excluded": len(excluded),
        "excluded": excluded,
        "cluster_mean_slope": cluster_mean,
        "cluster_std_slope": cluster_std,
        "field_mean_slope": field_mean,
        "field_std_slope": field_std,
        "t_statistic": float(t_stat),
        "p_value_one_sided": float(p_one_sided),
        "p_value_two_sided": float(p_two_sided),
        "direction_matches_efe_prediction": bool(direction_matches_efe),
        "efe_supported_by_prereg_criterion": bool(efe_supported),
    }

    out_path = HERE / "result_primary.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n[4] Resultado salvo em: {out_path}")

    return result


if __name__ == "__main__":
    main()
