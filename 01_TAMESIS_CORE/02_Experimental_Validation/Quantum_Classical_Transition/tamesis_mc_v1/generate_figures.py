from __future__ import annotations

import csv
import json
import math
import shutil
from pathlib import Path

import imageio.v2 as imageio
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from config import load_v1_contract, reject_runtime_overrides
from provenance import provenance_record, require_current_artifact, write_sidecar


BASE = Path(__file__).resolve().parent
REPO_ROOT = BASE.parents[3]
DATA = BASE / "data"
REPORT_FIGURES = BASE / "reports" / "figures"
ROOT_OUTPUTS = REPO_ROOT / "02_TAMESIS_MC_V1_OUTPUTS"
CONTRACT = load_v1_contract()

for folder in (REPORT_FIGURES, ROOT_OUTPUTS / "figures", ROOT_OUTPUTS / "animations"):
    folder.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", context="talk")


def load_json(name: str) -> dict:
    path = DATA / name
    require_current_artifact(path, CONTRACT)
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(name: str) -> list[dict]:
    path = DATA / name
    if name != "literature_points.csv":
        require_current_artifact(path, CONTRACT)
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def savefig(fig: plt.Figure, name: str, inputs: list[Path]) -> Path:
    out = REPORT_FIGURES / name
    fig.savefig(out, dpi=220, bbox_inches="tight")
    shutil.copy2(out, ROOT_OUTPUTS / "figures" / name)
    prov = provenance_record(
        output_path=out,
        contract=CONTRACT,
        script="generate_figures.py",
        inputs=[str(path) for path in inputs],
        arguments={"figure": name},
        status="illustrative_only",
        epistemic_status="illustrative_only",
    )
    write_sidecar(out, prov)
    write_sidecar(ROOT_OUTPUTS / "figures" / name, prov)
    plt.close(fig)
    return out


def copy_animation(path: Path) -> None:
    shutil.copy2(path, ROOT_OUTPUTS / "animations" / path.name)


def tamesis_rate(mass_ratio: np.ndarray, tau_c: float) -> np.ndarray:
    return np.where(mass_ratio <= 1.0, 0.0, (mass_ratio**CONTRACT.exponent) / tau_c)


def plot_predictions() -> None:
    rows = read_csv("predictions.csv")
    x = np.array([float(r["M_over_Mc"]) for r in rows])
    rate = np.array([float(r["rate_s-1"]) for r in rows])
    vis = np.array([float(r["V_at_1s"]) for r in rows])

    fig, ax1 = plt.subplots(figsize=(11, 6.5))
    ax1.set_xscale("log")
    ax1.set_yscale("symlog", linthresh=1e-3)
    ax1.plot(x, rate, marker="o", linewidth=3, label="intrinsic rate", color="#2563eb")
    ax1.axvline(1, color="#dc2626", linestyle="--", linewidth=2, label=r"$M = M_c$")
    ax1.set_xlabel(r"$M / M_c$")
    ax1.set_ylabel("intrinsic rate (s$^{-1}$)")

    ax2 = ax1.twinx()
    ax2.plot(x, vis, marker="s", linewidth=3, label="visibility at 1 s", color="#16a34a")
    ax2.set_ylabel("visibility at 1 s")
    ax2.set_ylim(-0.02, 1.05)

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc="center right")
    fig.suptitle(r"Tamesis $M_c$ v1 — threshold prediction")
    savefig(fig, "01_predictions.png", [DATA / "predictions.csv"])


def plot_literature() -> None:
    rows = read_csv("literature_points.csv")
    mc = CONTRACT.mc_kg

    ratios = []
    coherences = []
    statuses = []
    labels = []
    for r in rows:
        ratios.append(float(r["mass_kg"]) / mc)
        coherences.append(float(r["observed_coherence"]))
        statuses.append(r["status"])
        labels.append(r["experiment"])

    fig, ax = plt.subplots(figsize=(12, 6.5))
    colors = {"observed": "#16a34a", "planned": "#f59e0b"}
    markers = {"observed": "o", "planned": "s"}
    for status in sorted(set(statuses)):
        idx = [i for i, s in enumerate(statuses) if s == status]
        ax.scatter(
            [ratios[i] for i in idx],
            [coherences[i] for i in idx],
            s=110,
            color=colors.get(status, "gray"),
            marker=markers.get(status, "o"),
            label=status,
            edgecolor="black",
            linewidth=0.7,
        )
    ax.axvline(1, color="#dc2626", linestyle="--", linewidth=2, label=r"$M = M_c$")
    ax.set_xscale("log")
    ax.set_ylim(-0.05, 1.08)
    ax.set_xlabel(r"mass / $M_c$")
    ax.set_ylabel("observed coherence")
    ax.set_title("Known and planned matter-wave points relative to M_c")
    ax.legend(loc="center right")
    savefig(fig, "02_literature_points.png", [DATA / "literature_points.csv"])


def plot_target_1e15() -> None:
    data = load_json("target_1e15_decision.json")
    rows = data["decision_rows"]
    labels = [r["scenario"] for r in rows]
    values = {
        "Tamesis": [r["tamesis_visibility_at_0p1s"] for r in rows],
        "noise": [r["normalized_noise_visibility_at_0p1s"] for r in rows],
        "combined": [r["combined_visibility_at_0p1s"] for r in rows],
    }

    x = np.arange(len(labels))
    width = 0.25
    fig, ax = plt.subplots(figsize=(11, 6.5))
    for i, (name, series) in enumerate(values.items()):
        ax.bar(x + (i - 1) * width, series, width, label=name)
    ax.set_xticks(x)
    ax.set_xticklabels([label.replace("_", " ") for label in labels])
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("visibility at 0.1 s")
    ax.set_title("1e-15 kg target — visibility budget")
    ax.legend()
    savefig(fig, "03_target_1e15_visibility.png", [DATA / "target_1e15_decision.json"])


def plot_thermal_gate() -> None:
    data = load_json("target_1e15_thermal_gate.json")
    rows = data["temperature_rows"]
    color_map = {
        "low_blackbody_risk": "#16a34a",
        "borderline_blackbody_risk": "#f59e0b",
        "blackbody_dominant": "#dc2626",
    }
    temps = [r["temperature_k"] for r in rows]
    classes = [r["classification"] for r in rows]

    fig, ax = plt.subplots(figsize=(10, 5.8))
    ax.bar([str(t) for t in temps], [1] * len(temps), color=[color_map[c] for c in classes])
    for i, c in enumerate(classes):
        ax.text(i, 1.02, c.replace("_", " "), ha="center", va="bottom", rotation=12, fontsize=11)
    ax.set_ylim(0, 1.25)
    ax.set_yticks([])
    ax.set_xlabel("temperature (K)")
    ax.set_title("Thermal gate for the 1e-15 kg candidate")
    savefig(fig, "04_thermal_gate.png", [DATA / "target_1e15_thermal_gate.json"])


def plot_bohr_window_map() -> None:
    analysis = load_json("target_1e15_analysis.json")
    mc = CONTRACT.mc_kg
    tau_c = CONTRACT.tau_c_s
    gas_equal = analysis["pressure_requirements"]["gas_pressure_for_environment_equal_tamesis_rate_pa"]

    masses = np.logspace(-18, -14, 180)
    times = np.logspace(-3, 1, 180)
    M, T = np.meshgrid(masses, times)
    R = M / mc
    rate = tamesis_rate(R, tau_c)
    visibility = np.exp(-rate * T)
    measurable_loss = 1 - visibility

    fig, ax = plt.subplots(figsize=(11, 7))
    im = ax.contourf(M, T, measurable_loss, levels=np.linspace(0, 1, 21), cmap="viridis")
    ax.contour(M, T, measurable_loss, levels=[0.05, 0.15, 0.5], colors="white", linewidths=1.8)
    ax.axvline(mc, color="#ef4444", linestyle="--", linewidth=2, label=r"$M_c$")
    ax.scatter([1e-15], [0.1], color="#f97316", edgecolor="black", s=120, label="1e-15 kg candidate")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("mass (kg)")
    ax.set_ylabel("observation time (s)")
    ax.set_title("Bohr-window map: intrinsic visibility loss")
    fig.colorbar(im, ax=ax, label="1 - visibility")
    ax.legend(loc="upper left")
    savefig(fig, "05_bohr_window_map.png", [DATA / "target_1e15_analysis.json"])


def make_threshold_animation() -> None:
    mc = CONTRACT.mc_kg
    tau_c = CONTRACT.tau_c_s
    ratios = np.logspace(-1, 1.2, 500)
    rates = tamesis_rate(ratios, tau_c)

    frames = []
    phase = np.r_[np.linspace(0, 1, 36), np.linspace(1, 0, 36)]
    for p in phase:
        cutoff = 10 ** (-1 + p * 2.2)
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.set_xscale("log")
        ax.set_yscale("symlog", linthresh=1e-3)
        mask = ratios <= cutoff
        ax.plot(ratios, rates, color="#d1d5db", linewidth=2)
        ax.plot(ratios[mask], rates[mask], color="#2563eb", linewidth=4)
        ax.axvline(1, color="#dc2626", linestyle="--", linewidth=2)
        ax.text(1.05, max(rates) * 0.4, "M_c", color="#dc2626")
        ax.set_xlim(ratios.min(), ratios.max())
        ax.set_ylim(-0.01, max(rates) * 1.08)
        ax.set_xlabel(r"$M / M_c$")
        ax.set_ylabel("intrinsic rate (s$^{-1}$)")
        ax.set_title("Loop: threshold activation around M_c")
        png = ROOT_OUTPUTS / "animations" / "_frame_threshold.png"
        fig.savefig(png, dpi=120, bbox_inches="tight")
        plt.close(fig)
        frames.append(imageio.imread(png))
    gif = REPORT_FIGURES / "threshold_activation_loop.gif"
    imageio.mimsave(gif, frames, duration=0.055, loop=0)
    copy_animation(gif)
    prov = provenance_record(
        output_path=gif,
        contract=CONTRACT,
        script="generate_figures.py",
        inputs=[],
        arguments={"animation": "threshold_activation_loop"},
        status="illustrative_only",
        epistemic_status="illustrative_only",
    )
    write_sidecar(gif, prov)
    write_sidecar(ROOT_OUTPUTS / "animations" / gif.name, prov)
    (ROOT_OUTPUTS / "animations" / "_frame_threshold.png").unlink(missing_ok=True)


def make_bohr_window_animation() -> None:
    mc = CONTRACT.mc_kg
    tau_c = CONTRACT.tau_c_s
    masses = np.logspace(-18, -14, 140)
    times = np.logspace(-3, 1, 140)
    M, T = np.meshgrid(masses, times)
    R = M / mc
    base_rate = tamesis_rate(R, tau_c)

    frames = []
    phase = np.r_[np.linspace(0, 1, 28), np.linspace(1, 0, 28)]
    for p in phase:
        horizon = 10 ** (-3 + p * 4)
        visibility = np.exp(-base_rate * np.minimum(T, horizon))
        loss = 1 - visibility
        fig, ax = plt.subplots(figsize=(8, 5.5))
        im = ax.contourf(M, T, loss, levels=np.linspace(0, 1, 18), cmap="mako")
        ax.axvline(mc, color="#ef4444", linestyle="--", linewidth=2)
        ax.scatter([1e-15], [0.1], color="#f97316", edgecolor="black", s=80)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("mass (kg)")
        ax.set_ylabel("time (s)")
        ax.set_title(f"Loop: Bohr-window emergence, horizon={horizon:.3g}s")
        fig.colorbar(im, ax=ax, label="1 - visibility")
        png = ROOT_OUTPUTS / "animations" / "_frame_window.png"
        fig.savefig(png, dpi=120, bbox_inches="tight")
        plt.close(fig)
        frames.append(imageio.imread(png))
    gif = REPORT_FIGURES / "bohr_window_loop.gif"
    imageio.mimsave(gif, frames, duration=0.07, loop=0)
    copy_animation(gif)
    prov = provenance_record(
        output_path=gif,
        contract=CONTRACT,
        script="generate_figures.py",
        inputs=[],
        arguments={"animation": "bohr_window_loop"},
        status="illustrative_only",
        epistemic_status="illustrative_only",
    )
    write_sidecar(gif, prov)
    write_sidecar(ROOT_OUTPUTS / "animations" / gif.name, prov)
    (ROOT_OUTPUTS / "animations" / "_frame_window.png").unlink(missing_ok=True)


def write_root_readme() -> None:
    text = """# Tamesis M_c v1 Outputs

Visible output folder for the active Tamesis M_c v1 research line.

Source module:

- `../01_TAMESIS_CORE/02_Experimental_Validation/Quantum_Classical_Transition/tamesis_mc_v1`

Static figures:

- `figures/01_predictions.png`
- `figures/02_literature_points.png`
- `figures/03_target_1e15_visibility.png`
- `figures/04_thermal_gate.png`
- `figures/05_bohr_window_map.png`

Loop animations:

- `animations/threshold_activation_loop.gif`
- `animations/bohr_window_loop.gif`

These files are mirrored here so the results are visible from the repository root.
"""
    (ROOT_OUTPUTS / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    reject_runtime_overrides()
    plot_predictions()
    plot_literature()
    plot_target_1e15()
    plot_thermal_gate()
    plot_bohr_window_map()
    make_threshold_animation()
    make_bohr_window_animation()
    write_root_readme()
    print(f"Saved report figures to {REPORT_FIGURES}")
    print(f"Mirrored visible outputs to {ROOT_OUTPUTS}")


if __name__ == "__main__":
    main()
