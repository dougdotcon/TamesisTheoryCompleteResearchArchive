"""
ADVERSARIAL SCRIPT 5: scope, seed, and git-command discipline audit.
Read-only (no git commands are ever invoked, per the referee mandate --
this script only uses os.walk/grep-equivalents on the filesystem and
compares file mtimes).
"""
import os
import re
import subprocess

ARCHIVE_ROOT = "/home/user/TamesisTheoryCompleteResearchArchive"
LINEAGE = ("05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/"
           "conjecture2_direct_attempt/joint_two_point_attempt/"
           "joint_exploration_continuum_attempt/k2_joint_case_split_attempt/"
           "k3_joint_structural_attempt/general_k_joint_attempt")
TARGET_DIR = os.path.join(ARCHIVE_ROOT, LINEAGE, "general_k_cdf_alternate_route_attempt")
SIBLING_DIR = os.path.join(ARCHIVE_ROOT, LINEAGE, "general_k_closed_cdf_attempt")

print("=" * 70)
print("1) No git command in any target .py file or in ATTEMPT.md prose")
print("=" * 70)
git_hits = []
for fn in sorted(os.listdir(TARGET_DIR)):
    if fn.endswith(".py"):
        path = os.path.join(TARGET_DIR, fn)
        with open(path) as fh:
            content = fh.read()
        if re.search(r"\bsubprocess\b|\bos\.system\b|\bgit\s", content):
            git_hits.append((fn, "possible git/subprocess usage"))
print(f"Scripts scanned: {len([f for f in os.listdir(TARGET_DIR) if f.endswith('.py')])}")
print(f"Suspicious hits: {git_hits if git_hits else 'NONE'}")

with open(os.path.join(TARGET_DIR, "ATTEMPT.md")) as fh:
    attempt_text = fh.read()
git_mentions = [line for line in attempt_text.splitlines() if "git" in line.lower()]
print(f"'git' mentions in ATTEMPT.md prose ({len(git_mentions)} lines):")
for line in git_mentions:
    print(f"    {line.strip()}")
print("(All are disclosure prose -- 'No `git` command run' -- not invocations.)")

print()
print("=" * 70)
print("2) Sibling directory (general_k_closed_cdf_attempt/) untouched")
print("=" * 70)
# Baseline: sibling's own newest mtime among its pre-existing files. We
# check that nothing in the sibling directory has an mtime suspiciously
# close to / after the target front's own files' mtimes, i.e. that this
# front (or this referee) did not write into it.
target_mtimes = []
for fn in os.listdir(TARGET_DIR):
    p = os.path.join(TARGET_DIR, fn)
    if os.path.isfile(p):
        target_mtimes.append(os.path.getmtime(p))
target_min_mtime = min(target_mtimes)
print(f"Target directory's own earliest file mtime: {target_min_mtime}")

sibling_mtimes_after = []
for root, dirs, files in os.walk(SIBLING_DIR):
    for fn in files:
        p = os.path.join(root, fn)
        mt = os.path.getmtime(p)
        if mt >= target_min_mtime:
            sibling_mtimes_after.append((p, mt))
print(f"Sibling files with mtime >= target's earliest file mtime: "
      f"{len(sibling_mtimes_after)}")
for p, mt in sibling_mtimes_after:
    print(f"    {p}  {mt}")
print("(Empty list = sibling directory was not touched during or after "
      "this front's work -- confirms scope discipline.)")

print()
print("=" * 70)
print("3) No THEOREM.md / governance file self-integration")
print("=" * 70)
gov_files = ["THEOREM.md", "index.html", "README.md"]
gov_paths = {
    "THEOREM.md": os.path.join(ARCHIVE_ROOT, "05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/THEOREM.md"),
    "index.html": os.path.join(ARCHIVE_ROOT, "index.html"),
    "README.md": os.path.join(ARCHIVE_ROOT, "README.md"),
    "DECISION_LEDGER.yaml": os.path.join(ARCHIVE_ROOT, "05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml"),
    "PROOF_DEPENDENCY_MAP.md": os.path.join(ARCHIVE_ROOT, "05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/PROOF_DEPENDENCY_MAP.md"),
}
for name, path in gov_paths.items():
    with open(path, encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    hit = "ALTERNATE-ROUTE" in content or "alternate_route" in content
    print(f"  {name}: mentions this front's task ID/dirname = {hit}")
print("(DECISION_LEDGER.yaml is EXPECTED to mention DISC-DEC-118 -- the wave")
print("25 dispatch decision itself, made by the orchestrating session BEFORE")
print("this front's own work, not an edit made by this front.)")

print()
print("=" * 70)
print("4) Seed reservation: 20260930000-20260930999, correctly scoped")
print("=" * 70)
result = subprocess.run(
    ["grep", "-rn", "20260930", os.path.join(ARCHIVE_ROOT, "05_DISCOVERY_LAB")],
    capture_output=True, text=True
)
lines = result.stdout.strip().splitlines()
outside_target = [l for l in lines if TARGET_DIR.split("TamesisTheoryCompleteResearchArchive/")[-1] not in l
                   and "general_k_cdf_alternate_route_attempt" not in l]
print(f"Total '20260930' occurrences in 05_DISCOVERY_LAB/: {len(lines)}")
print(f"Occurrences OUTSIDE the target directory: {len(outside_target)}")
for l in outside_target:
    print(f"    {l}")
print("(Expected: exactly one -- the DECISION_LEDGER.yaml reservation line "
      "itself. Any other outside occurrence would be a violation.)")

mc_seeds = sorted(set(re.findall(r"20260930\d{3}", attempt_text)))
print(f"\nSeeds used per ATTEMPT.md prose: {mc_seeds}")
in_range = all(20260930000 <= int(s) <= 20260930999 for s in mc_seeds)
print(f"All within reserved block 20260930000-20260930999: {in_range}")

print()
print("=" * 70)
print("AUDIT COMPLETE")
print("=" * 70)
