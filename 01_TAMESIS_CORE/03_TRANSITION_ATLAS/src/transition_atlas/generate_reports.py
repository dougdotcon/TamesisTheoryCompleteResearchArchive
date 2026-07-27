from __future__ import annotations

import json
from pathlib import Path

from .contract_bridge import tamesis_integration
from .loader import load_regimes, load_transitions
from .validator import validate


ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "reports"


def write(name: str, text: str) -> None:
    (REPORTS / name).write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    REPORTS.mkdir(exist_ok=True)
    regimes = load_regimes(); transitions = load_transitions(); findings = validate(regimes, transitions)
    ti = tamesis_integration()
    write("ATLAS_FORMAL_SPECIFICATION.md", "# Atlas de Transições v0.1 — especificação formal\n\n`A=(R,T,E,P)` é um multigrafo direcionado, tipado e atributado. Regimes possuem espaço de estados, álgebra de observáveis, dinâmica, invariantes, domínio e composição. Transições possuem espaço de controle, superfície crítica, mapa, gerador, parâmetro de ordem, observáveis, falsificação e estado da evidência. O peso é um vetor com completude matemática, reprodutibilidade computacional, suporte observacional, discriminação experimental, viabilidade técnica, replicação independente e incerteza; não há escalar único. Schemas são derivados de `src/transition_atlas/models.py`; extras são proibidos e quantidades físicas exigem unidade.")
    write("REGIME_ONTOLOGY.md", "# Ontologia de regimes\n\nRegimes iniciais: " + ", ".join(sorted(regimes)) + ". Quântico e clássico são descrições relacionadas por limites/reduções possíveis, não incompatibilidades absolutas. Bounce é candidato teórico; cosmologias inicial/tardia são dependentes de modelo.")
    write("TRANSITION_ONTOLOGY.md", "# Ontologia de transições\n\nTipos permitidos incluem isomorphism, reduction, singular_limit, coarse_graining, phase_transition, symmetry_breaking, environmental_decoherence, intrinsic_collapse, emergence, duality, effective_description_change e unknown. Classes de reversibilidade incluem reversible, effectively_irreversible, fundamentally_irreversible, non_markovian e unknown.")
    write("EPISTEMIC_STATUS_POLICY.md", "# Política epistemológica\n\nPromoções não são automáticas. `mathematically_specified` exige equações, símbolos e domínio; `computationally_reproduced` exige código e hashes; `preregistered_test` exige protocolo congelado; `transition_detected` exige observação prospectiva, controle de nuisance e rejeição de rivais; `independently_replicated` exige fonte independente. Queda de coerência reduzida não implica irreversibilidade fundamental.")
    write("INITIAL_ATLAS_AUDIT.md", "# Auditoria inicial\n\nRegimes: **" + str(len(regimes)) + "**. Transições: **" + str(len(transitions)) + "**. Findings: " + json.dumps([f.__dict__ for f in findings], ensure_ascii=False) + ".\n\nA tensão de Hubble está separada em anomalia observacional e mecanismo conjecturado. O limite holográfico está separado da dinâmica de bounce e da frequência proposta.")
    write("TAMESIS_EDGE_INTEGRATION.md", "# Integração da aresta Tamesis\n\nA aresta `tamesis_quantum_classical_v1` lê o contrato canônico em tempo de carga.\n\n- Protocol ID: `" + ti["protocol_id"] + "`\n- Config hash: `" + ti["config_hash"] + "`\n- M_c, tau_c, expoente, alpha e largura: importados, não duplicados\n- Equação de visibilidade: `" + ti["visibility_equation"] + "`\n- Status: `preregistered_test` / `preregistered_transition_candidate`\n- Limitações: separação, geometria, composição e dinâmica multipartícula não estão na v1.0\n\nA promoção exige múltiplas massas, variação temporal, variação de separação quando aplicável, orçamento ambiental fechado, rejeição de rivais e reprodução independente.")
    write("ATLAS_V0_1_EXECUTION_REPORT.md", "# Atlas v0.1 — relatório de execução\n\nO Atlas foi construído como camada paralela e somente leitura em relação ao Tamesis M_c v1.0. O validador estrito, os schemas, a ponte de contrato, o grafo e os testes executaram sem transformar conjecturas em descobertas.\n\nA classificação atual é: Tamesis = teste pré-registrado; tensão de Hubble = anomalia observacional; acoplamento 1/12 = conjectura legada; bounce = conjectura teórica. O grafo é cartografia formal, não evidência por proximidade visual.")
    print(f"generated reports for {len(regimes)} regimes and {len(transitions)} transitions")


if __name__ == "__main__":
    main()
