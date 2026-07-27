from .loader import load_regimes


def main() -> None:
    for regime_id, regime in load_regimes().items():
        print(f"{regime_id}\t{regime.epistemic_status.value}\t{regime.name}")


if __name__ == "__main__":
    main()
