from .loader import load_transitions


def main() -> None:
    for transition_id, transition in load_transitions().items():
        print(f"{transition_id}\t{transition.epistemic_status.value}\t{transition.source_regime}->{transition.target_regime}")


if __name__ == "__main__":
    main()
