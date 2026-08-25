#!/usr/bin/env python3
"""Deterministic generator for the Discovery Lab README/index figures.

Every curve below is computed directly from formulas already PROVED (and
adversarially refereed) in
05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/THEOREM.md,
or from the dated entries of 00_GOVERNANCE/DECISION_LEDGER.yaml.
No fitted, simulated-only, or fabricated values are plotted.

Usage:  python3 make_assets.py   (writes the SVGs next to this script)
"""
import math
import os
from datetime import datetime

import numpy as np
import yaml
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "none"
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))


# ----------------------------------------------------------------------
# Figure 1: Conjecture 1's proved density instances (THEOREM.md §5.3, §8,
# Estágios 15 and 17): f_{M_K}(x) = 2K x (1-x^2)^(K-1), K = 1, 2, 3.
# ----------------------------------------------------------------------
def fig_conjecture1():
    def f_MK(x, K):
        return 2 * K * x * (1 - x**2) ** (K - 1)

    x = np.linspace(0, 1, 2000)
    fig, ax = plt.subplots(figsize=(7.5, 5.2), dpi=200)
    colors = {1: "#1f6f5c", 2: "#2f8f6a", 3: "#8c5a1f"}
    labels = {
        1: r"K=1:  $f_{M_1}(x)=2x$  (base case, §5.3)",
        2: r"K=2:  $f_{M_2}(x)=4x(1-x^2)$  (Estágio 15, 2026-08-23)",
        3: r"K=3:  $f_{M_3}(x)=6x(1-x^2)^2$  (Estágio 17, 2026-08-24)",
    }
    for K in (1, 2, 3):
        ax.plot(x, f_MK(x, K), color=colors[K], linewidth=2.4, label=labels[K])
        ax.fill_between(x, f_MK(x, K), color=colors[K], alpha=0.06)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, None)
    ax.set_xlabel("x", fontsize=12)
    ax.set_ylabel(r"$f_{M_K}(x)$", fontsize=12)
    ax.set_title(
        "Conjecture 1 — the general-K distributional law\n"
        r"$f_{M_K}(x) = 2Kx(1-x^2)^{K-1}$ — PROVED at K=1, 2, 3",
        fontsize=12.5,
    )
    ax.legend(loc="upper left", fontsize=9.5, frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(alpha=0.15)
    fig.text(
        0.5, -0.02,
        "u12_universality/theorem/THEOREM.md, §§5.3 and 8, Estágios 15-17 — each instance PROVED modulo the same\n"
        "classical PD(1) residual/size-biased citation (McCloskey 1965; Patil-Taillie 1977), each independently hostile-refereed.",
        ha="center", fontsize=7.8, color="#555555",
    )
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "conjecture1_densities.svg"), bbox_inches="tight")
    plt.close(fig)


# ----------------------------------------------------------------------
# Figure 2: the sharp-constant question (THEOREM.md Estágios 12-13).
# Q(n) is the classical Ramanujan Q-function; phi_K is the Wallis-integral
# mean (proved for every K, independent of the density conjecture);
# M_K = Q(K+1) - (K+1) phi_K is the exact finite quantity of Estágio 12.
# ----------------------------------------------------------------------
def fig_sharp_constant():
    def Q(n):
        total, prod = 0.0, 1.0
        for j in range(n):
            total += prod
            prod *= (1 - (j + 1) / n)
        return total

    def phi_K(K):
        return K * math.exp(math.lgamma(1.5) + math.lgamma(K) - math.lgamma(K + 1.5))

    def M_K(K):
        return Q(K + 1) - (K + 1) * phi_K(K)

    a_star = math.sqrt(math.pi) * (1 / math.sqrt(2) - 0.5)
    a_nonsharp = 1 + math.sqrt(math.pi / 2)
    Ks = np.arange(1, 601)
    vals = np.array([M_K(int(K)) / math.sqrt(K) for K in Ks])

    fig, ax = plt.subplots(figsize=(7.5, 5.0), dpi=200)
    ax.plot(Ks, vals, color="#1f6f5c", linewidth=1.8,
            label=r"$M_K/\sqrt{K}$  (exact, computed from $Q(n)$ and $\varphi_K$)")
    ax.axhline(a_star, color="#8c5a1f", linewidth=1.6, linestyle="--",
               label=r"$a^*=\sqrt{\pi}(1/\sqrt{2}-1/2)\approx%.7f$  —  $\lim_{K\to\infty}M_K/\sqrt{K}=a^*$ (PROVED, Estágio 13)" % a_star)
    ax.set_xlim(1, Ks[-1])
    ax.set_xlabel("K", fontsize=12)
    ax.set_ylabel(r"$M_K/\sqrt{K}$", fontsize=12)
    ax.set_title(
        "The sharp-constant question: does $\\sup_K M_K/\\sqrt{K} = a^*$?\n"
        "Limit is PROVED (Estágio 13); the supremum/monotonicity is OPEN (wave 16, front b)",
        fontsize=11.8,
    )
    ax.legend(loc="lower right", fontsize=8.8, frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(alpha=0.15)
    fig.text(
        0.5, -0.03,
        "Curve strictly increasing and never reaching a* up to K=600 is numerical/heuristic evidence only, not a proof —\n"
        "this archive's own honest framing (THEOREM.md Estágio 13). The gap between this limit and the non-sharp constant\n"
        "a=1+sqrt(pi/2)≈%.4f actually proved in hypothesis (U') is exactly what wave 16 front (b) is attempting to close."
        % a_nonsharp,
        ha="center", fontsize=7.6, color="#555555",
    )
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "sharp_constant_astar.svg"), bbox_inches="tight")
    plt.close(fig)


# ----------------------------------------------------------------------
# Figure 3: cumulative governance decisions over time, read directly from
# the dated entries of DECISION_LEDGER.yaml.
# ----------------------------------------------------------------------
def fig_governance():
    with open(os.path.join(REPO, "05_DISCOVERY_LAB", "00_GOVERNANCE",
                           "DECISION_LEDGER.yaml")) as f:
        data = yaml.safe_load(f)

    def to_dt(v):
        if isinstance(v, str):
            return datetime.strptime(v, "%Y-%m-%d")
        return datetime(v.year, v.month, v.day)

    dates = sorted(to_dt(d["date"]) for d in data["decisions"])
    cum_x = [dates[0]] + dates
    cum_y = list(range(0, len(dates) + 1))

    fig, ax = plt.subplots(figsize=(7.6, 4.6), dpi=200)
    ax.step(cum_x, cum_y, where="post", color="#1f6f5c", linewidth=2.2)
    ax.fill_between(cum_x, cum_y, step="post", color="#1f6f5c", alpha=0.08)
    ax.set_ylabel("Cumulative governance decisions logged", fontsize=11)
    ax.set_xlabel("Date", fontsize=11)
    ax.set_title(
        "Discovery Lab governance activity — DECISION_LEDGER.yaml\n"
        "%d decisions logged, %s to %s, none yet quiet" % (
            len(dates), dates[0].strftime("%Y-%m-%d"), dates[-1].strftime("%Y-%m-%d")),
        fontsize=12,
    )
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(alpha=0.15)
    ax.set_ylim(0, len(dates) + 3)
    fig.text(
        0.5, -0.03,
        "Every entry is a logged governance action (result integration, wave authorization, or honest closure) —\n"
        "not every one is a positive mathematical result; see DECISION_LEDGER.yaml for the individual verdicts.",
        ha="center", fontsize=7.6, color="#555555",
    )
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "governance_velocity.svg"), bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_conjecture1()
    fig_sharp_constant()
    fig_governance()
    print("assets regenerated in", HERE)
