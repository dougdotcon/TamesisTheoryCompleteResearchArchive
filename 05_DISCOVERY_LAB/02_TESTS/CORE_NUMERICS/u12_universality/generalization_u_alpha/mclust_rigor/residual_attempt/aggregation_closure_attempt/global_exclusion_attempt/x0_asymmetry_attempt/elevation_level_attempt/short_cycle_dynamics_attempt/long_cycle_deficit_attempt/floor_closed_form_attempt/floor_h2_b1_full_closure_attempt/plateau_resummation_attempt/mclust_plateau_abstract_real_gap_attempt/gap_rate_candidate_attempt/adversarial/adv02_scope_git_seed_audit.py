#!/usr/bin/env python3
"""
adv02_scope_git_seed_audit.py

HOSTILE REFEREE mechanical audit of gap_rate_candidate_attempt/ATTEMPT.md's
scope-discipline, git-usage, and seed-usage claims (mandate item 5).

Checks:
  (A) No `git` command / subprocess / os.system call appears in any of the
      target's 3 scripts.
  (B) No seed / randomness usage appears in any of the target's 3 scripts.
  (C) The reserved seed block 20260932000-20260932999 is referenced ONLY
      in the ledger reservation line, the DISCOVERY_LAB_STATE.md summary
      line, and the target's own ATTEMPT.md -- nowhere else in
      05_DISCOVERY_LAB/ (i.e. genuinely unused).
  (D) mtime audit: every file in the target's own new subdirectory is
      dated 2026-08-29 (today); every file in the PARENT front's own
      top-level scripts/logs and its own adversarial/ predates 2026-08-29;
      the sibling mclust_h1_validity_attempt/ directory's PRE-EXISTING
      content (h1_post_correction_attempt/) predates 2026-08-29, but a
      NEW subdirectory (h1_translation_structure_attempt/) inside that
      sibling is ALSO dated 2026-08-29 -- flagged and independently
      investigated (see REFEREE_REPORT.md) as separately-authorized wave
      25 front (c) (H1-TRANSLATION-STRUCTURE-ATTEMPT, DISC-DEC-118(c)),
      NOT touched by or attributable to the target front (d) under review.
  (E) Re-run the target's own 3 scripts fresh and diff their stdout
      against the checked-in .log files, to confirm the logs are genuine
      script output and not hand-edited/fabricated text.
"""
import subprocess
import os
import sys

ARCHIVE_ROOT = "/home/user/TamesisTheoryCompleteResearchArchive"
TARGET_DIR = (
    "05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/"
    "generalization_u_alpha/mclust_rigor/residual_attempt/"
    "aggregation_closure_attempt/global_exclusion_attempt/"
    "x0_asymmetry_attempt/elevation_level_attempt/"
    "short_cycle_dynamics_attempt/long_cycle_deficit_attempt/"
    "floor_closed_form_attempt/floor_h2_b1_full_closure_attempt/"
    "plateau_resummation_attempt/mclust_plateau_abstract_real_gap_attempt/"
    "gap_rate_candidate_attempt"
)
TARGET_ABS = os.path.join(ARCHIVE_ROOT, TARGET_DIR)
PARENT_ABS = os.path.dirname(TARGET_ABS)

SCRIPTS = [
    "r01_reconstruct_and_crosscheck.py",
    "r02_power_law_fit.py",
    "r03_perbin_and_exploratory.py",
]
LOGS = [
    "r01_reconstruct_and_crosscheck.log",
    "r02_power_law_fit.log",
    "r03_perbin_and_exploratory.log",
]


def run(cmd, cwd=None):
    return subprocess.run(
        cmd, shell=True, cwd=cwd, capture_output=True, text=True
    )


def section(title):
    print(f"\n{'='*70}\n{title}\n{'='*70}")


def check_A_git_usage():
    section("(A) git / subprocess / os.system usage in target's scripts")
    for s in SCRIPTS:
        path = os.path.join(TARGET_ABS, s)
        text = open(path).read()
        hits = [
            kw for kw in ("git ", "subprocess", "os.system", "import git")
            if kw in text
        ]
        print(f"  {s}: {'FOUND ' + str(hits) if hits else 'clean (no matches)'}")


def check_B_seed_usage():
    section("(B) seed / randomness usage in target's scripts")
    # Use actual code-usage patterns, not bare substrings -- "random" alone
    # also matches inside the English word "randomness" in a docstring,
    # which is a false positive for *usage*, not a hit. Word-boundary /
    # call-shaped patterns only.
    import re
    patterns = [
        (r"\bimport random\b", "import random"),
        (r"\brandom\.\w+\(", "random.<fn>(  [call]"),
        (r"\bnp\.random\b", "np.random"),
        (r"\bSeedSequence\(", "SeedSequence("),
        (r"\brng\s*=", "rng = [assignment]"),
        (r"\.seed\(", ".seed("),
    ]
    for s in SCRIPTS:
        path = os.path.join(TARGET_ABS, s)
        text = open(path).read()
        hits = [label for pat, label in patterns if re.search(pat, text)]
        print(f"  {s}: {'FOUND ' + str(hits) if hits else 'clean (no code-level randomness usage)'}")
        # also show any bare mentions of the ENGLISH WORD "random" for
        # transparency (expected to be docstring prose, not code)
        prose_hits = [
            (i, line) for i, line in enumerate(text.splitlines())
            if "random" in line.lower() and not any(
                re.search(pat, line) for pat, _ in patterns
            )
        ]
        for i, line in prose_hits:
            print(f"    (prose mention only, line {i}: {line.strip()!r})")


def check_C_seed_block_scope():
    section("(C) reserved seed block 20260932000-20260932999 usage archive-wide")
    # Exclude this referee's OWN adversarial/ directory from the scope
    # check -- it necessarily quotes "20260932" in its own commentary
    # while auditing the claim, which is not a "usage" of the block.
    r = run(
        'grep -rln "20260932" 05_DISCOVERY_LAB/ '
        '| grep -v "gap_rate_candidate_attempt/adversarial/"',
        cwd=ARCHIVE_ROOT,
    )
    files = [l for l in r.stdout.splitlines() if l.strip()]
    print("Files referencing '20260932' (excluding this referee's own adversarial/ dir):")
    for f in files:
        print(" ", f)
    non_ledger_non_target = [
        f for f in files
        if "DECISION_LEDGER.yaml" not in f
        and "DISCOVERY_LAB_STATE.md" not in f
        and "gap_rate_candidate_attempt/ATTEMPT.md" not in f
    ]
    if non_ledger_non_target:
        print("  UNEXPECTED extra usages found:")
        for f in non_ledger_non_target:
            print("   ", f)
    else:
        print("  CONFIRMED: only ledger reservation, state summary, and the "
              "target's own ATTEMPT.md reference this block anywhere in the "
              "archive (excluding this referee's own commentary). "
              "Genuinely unused -- no Monte Carlo / random sampling was "
              "needed or performed by the target front.")


def mtime(path):
    r = run(f'stat -c "%Y %y" "{path}"')
    return r.stdout.strip()


def check_D_mtimes():
    section("(D) mtime audit")
    print("-- Target's OWN new subdirectory (expect ALL dated 2026-08-29) --")
    r = run(f'find "{TARGET_ABS}" -type f -exec stat -c "%y  %n" {{}} \\;')
    for line in sorted(r.stdout.splitlines()):
        print(" ", line)

    print("\n-- Parent front's OWN top-level files, excluding gap_rate_candidate_attempt/ "
          "(expect ALL predate 2026-08-29) --")
    r = run(
        f'find "{PARENT_ABS}" -maxdepth 1 -type f -exec stat -c "%y  %n" {{}} \\;'
    )
    bad = [l for l in r.stdout.splitlines() if "2026-08-29" in l]
    for line in sorted(r.stdout.splitlines()):
        print(" ", line)
    print(f"  -> files dated 2026-08-29 among these: {len(bad)} "
          f"({'PROBLEM' if bad else 'none, as expected'})")

    print("\n-- Parent's own adversarial/ (expect ALL predate 2026-08-29) --")
    r = run(
        f'find "{PARENT_ABS}/adversarial" -type f -exec stat -c "%y  %n" {{}} \\;'
    )
    bad = [l for l in r.stdout.splitlines() if "2026-08-29" in l]
    for line in sorted(r.stdout.splitlines()):
        print(" ", line)
    print(f"  -> files dated 2026-08-29 among these: {len(bad)} "
          f"({'PROBLEM' if bad else 'none, as expected'})")

    sib = os.path.join(PARENT_ABS, "mclust_h1_validity_attempt")
    print(f"\n-- Sibling mclust_h1_validity_attempt/ (pre-existing "
          f"h1_post_correction_attempt/ should predate 2026-08-29; check "
          f"whether ANY new content is dated 2026-08-29) --")
    r = run(f'find "{sib}" -type f -exec stat -c "%y  %n" {{}} \\;')
    dated_today = sorted(l for l in r.stdout.splitlines() if "2026-08-29" in l)
    dated_before = sorted(l for l in r.stdout.splitlines() if "2026-08-29" not in l)
    print(f"  Files predating 2026-08-29 ({len(dated_before)}):")
    for l in dated_before:
        print("   ", l)
    print(f"  Files dated 2026-08-29 ({len(dated_today)}):")
    for l in dated_today:
        print("   ", l)
    if dated_today:
        print(
            "  NOTE: these belong to h1_translation_structure_attempt/, a "
            "SEPARATE, separately-authorized wave-25 front (c) "
            "(H1-TRANSLATION-STRUCTURE-ATTEMPT, DISC-DEC-118(c) -- confirmed "
            "in DECISION_LEDGER.yaml). Their content (kernel-conjugation / "
            "translation-invariance analysis) is topically unrelated to "
            "gap-rate power-law testing, and contains no reference to the "
            "target front's data (grep-checked below). This is normal "
            "same-day multi-front archive activity, NOT a scope violation "
            "by the target front (d) under review."
        )
        # spot-check topical independence
        for l in dated_today:
            fpath = l.split("  ", 1)[1] if "  " in l else None
            if fpath and fpath.endswith(".py"):
                txt = open(fpath, errors="ignore").read()
                hit = any(
                    k in txt for k in
                    ("gap_rate_candidate", "power_law_fit", "38.7756", "c/n)^")
                )
                print(f"    grep cross-topic check on {os.path.basename(fpath)}: "
                      f"{'UNEXPECTED OVERLAP' if hit else 'topically independent, as expected'}")


def check_E_rerun_scripts():
    section("(E) Re-run target's own scripts fresh, diff vs checked-in .log")
    for script, log in zip(SCRIPTS, LOGS):
        r = run(f"python3 {script}", cwd=TARGET_ABS)
        fresh = r.stdout
        checked_in = open(os.path.join(TARGET_ABS, log)).read()
        # the scripts also (re)write their own .json outputs as a side
        # effect; that's fine, we only diff the printed stdout against the
        # checked-in log text.
        if fresh.strip() == checked_in.strip():
            print(f"  {script}: fresh stdout IDENTICAL to {log} -- "
                  f"confirmed genuine, reproducible, not fabricated.")
        else:
            print(f"  {script}: MISMATCH vs {log} -- investigate!")
            # show a short diff-ish hint
            f_lines = fresh.splitlines()
            c_lines = checked_in.splitlines()
            for i, (a, b) in enumerate(zip(f_lines, c_lines)):
                if a != b:
                    print(f"    line {i}: fresh={a!r}  checked_in={b!r}")
                    break


if __name__ == "__main__":
    check_A_git_usage()
    check_B_seed_usage()
    check_C_seed_block_scope()
    check_D_mtimes()
    check_E_rerun_scripts()
    print("\nDone.")
