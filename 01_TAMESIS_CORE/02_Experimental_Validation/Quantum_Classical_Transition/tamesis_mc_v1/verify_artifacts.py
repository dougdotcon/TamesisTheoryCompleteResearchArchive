from __future__ import annotations

import json
from pathlib import Path

from build_manifest import BASE, MANIFEST_REL, inspect_sidecar, iter_artifacts, sha256_file, sidecar_for
from config import V1Contract, load_v1_contract, reject_runtime_overrides


class ArtifactVerificationError(RuntimeError):
    pass


def verify_manifest(
    manifest_path: Path | None = None,
    *,
    base: Path = BASE,
    contract: V1Contract | None = None,
) -> dict:
    base = base.resolve()
    contract = contract or load_v1_contract()
    manifest_path = manifest_path or (base / MANIFEST_REL)
    if not manifest_path.exists():
        raise ArtifactVerificationError(f"missing manifest: {manifest_path}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ArtifactVerificationError(f"malformed manifest: {exc}") from exc
    errors: list[str] = []
    if manifest.get("protocol_id") != contract.protocol_id() or manifest.get("config_hash") != contract.config_hash():
        errors.append("manifest contract identity mismatch")
    entries = {entry.get("path"): entry for entry in manifest.get("entries", [])}
    current_paths = {path.relative_to(base).as_posix() for path in iter_artifacts(base)}
    listed_paths = set(entries)
    for rel in sorted(listed_paths - current_paths):
        errors.append(f"manifest entry missing artifact: {rel}")
    for rel in sorted(current_paths - listed_paths):
        errors.append(f"unlisted artifact: {rel}")
    for rel in sorted(current_paths & listed_paths):
        path = base / Path(rel)
        entry = entries[rel]
        if entry.get("status") in {"invalid", "canonical_stale"}:
            errors.append(f"manifest contains disallowed status {entry.get('status')}: {rel}")
        if entry.get("hash") != sha256_file(path):
            errors.append(f"manifest artifact hash mismatch: {rel}")
        sidecar = sidecar_for(path)
        recorded_sidecar_hash = entry.get("sidecar_hash")
        if recorded_sidecar_hash is not None:
            if not sidecar.exists():
                errors.append(f"sidecar removed: {rel}")
            elif sha256_file(sidecar) != recorded_sidecar_hash:
                errors.append(f"manifest sidecar hash mismatch: {rel}")
        if entry.get("status") == "canonical_current":
            state, _, sidecar_errors = inspect_sidecar(path, base, contract)
            if state != "current":
                errors.append(f"canonical artifact is {state}: {rel}: {', '.join(sidecar_errors)}")
    if errors:
        raise ArtifactVerificationError("artifact verification failed:\n- " + "\n- ".join(errors))
    return manifest


def main() -> None:
    reject_runtime_overrides()
    contract = load_v1_contract()
    manifest = verify_manifest(contract=contract)
    print(json.dumps({
        "protocol_id": contract.protocol_id(),
        "config_hash": contract.config_hash(),
        "entries": len(manifest["entries"]),
        "summary": manifest["summary"],
        "verification": "passed_without_rebuilding_manifest",
    }, indent=2))


if __name__ == "__main__":
    main()
