# Árvore de decisão

```text
O artefato está no LAB-0?
 ├─ não → não executar; registrar como legado
 └─ sim
    ├─ modifica legado? → parar: LAB0_LEGACY_MODIFICATION_DETECTED
    ├─ é prova nova? → verificar autorização específica
    ├─ depende de toolchain ausente? → BLOCKED
    ├─ procura contraexemplo/valida artefato? → pode executar no gate
    └─ promove claim? → exigir revisão e gate explícitos
```

