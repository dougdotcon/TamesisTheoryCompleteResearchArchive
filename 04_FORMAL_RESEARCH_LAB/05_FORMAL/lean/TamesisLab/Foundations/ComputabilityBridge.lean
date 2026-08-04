import TamesisLab.Foundations.ComputabilityBridge.Encoding
import TamesisLab.Foundations.ComputabilityBridge.ResultCodes
import TamesisLab.Foundations.ComputabilityBridge.Classification
import TamesisLab.Foundations.ComputabilityBridge.WitnessBound
import TamesisLab.Foundations.ComputabilityBridge.Instance

/-!
# FOUND-COMPUTABILITY-BRIDGE-001

```text
Encoding.lean        a ponte Primcodable, e a armadilha n = 0
ResultCodes.lean     codificar o resultado do laboratorio
Classification.lean  Primrec, Computable, e o limite NEGATIVO
WitnessBound.lean    a cota do certificado
Instance.lean        TEST_ONLY, o caso positivo e o vacuo
```

Dezenove declarações públicas, um auxiliar privado, duas `TEST_ONLY`.
Quatro instâncias. **O resultado central é negativo**: a classificação é
constante sobre domínio finito e não carrega informação algorítmica.
-/
