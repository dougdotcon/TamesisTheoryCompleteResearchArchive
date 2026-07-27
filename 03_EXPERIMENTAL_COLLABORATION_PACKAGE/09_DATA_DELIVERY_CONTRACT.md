# Contrato mínimo de entrega de dados

## O laboratório entrega

Dados espectrais brutos, dark/background, wavelength axis, unidades, timestamps,
potência e método de medição, temperaturas de referência e estágio,
identificadores de instrumento/partícula/calibração, eventos de saturação ou
intervenção, imagens para reencontrar a partícula, versão do software de
aquisição, hashes e lista de ausências.

## Custódia e cegamento

O custodiante conserva originais e setpoints. O analista cego recebe cópia
sanitizada. O reveal só ocorre depois de:

```text
model_locked
predictions_complete
prediction_hashes_verified
leakage_audit_passed
```

## Governança

Antes do A0, definir propriedade intelectual, embargo, autoria, custos,
segurança, uso futuro da amostra e direito de publicar resultado negativo ou
inconclusivo. Este contrato não pede endosso a Tamesis.

