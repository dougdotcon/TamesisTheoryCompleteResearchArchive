# Gate de prontidão A1

Marcar `pass` ou registrar exceção assinada:

- [ ] instrumento/serial e cadeia de calibração documentados;
- [ ] referência e estágio comparados;
- [ ] faixa 5–20 K demonstrada;
- [ ] espectrômetro, wavelength reference e detector caracterizados;
- [ ] potência na partícula estimável;
- [ ] partícula relocável e persistente;
- [ ] dark/background e raw storage verificados;
- [ ] estabilidade, drift e Allan deviation calculados;
- [ ] spectral diffusion e cross-sensitivities avaliadas;
- [ ] limite de autoaquecimento derivado;
- [ ] decisão A0 `advance_to_A1`;
- [ ] custodiante separado, ordem randomizada e metadata sanitizada;
- [ ] modelo, exclusões e critérios de sucesso congelados.

```text
a1_status: authorized | blocked
blocking_items:
protocol_amendment_id:
custodian:
analyst:
date:
```

`authorized` significa apenas autorização para A1 metrológico; não autoriza
levitação, interferometria ou inferência Tamesis.

