# Runbook do piloto A0

## Pré-condições

Q0 aprovado ou limitado por exceção documentada; `particle_id` persistente;
`instrument_id` e `calibration_id` registrados; relógio sincronizado; raw
storage, convenção de nomes e custodiante definidos.

## Sequência por partícula

1. Registrar imagem/localização e identidade persistente.
2. Registrar instrumento, calibração, operador, sessão e ambiente.
3. Adquirir dark e background.
4. Adquirir espectro inicial em potência mínima.
5. Executar níveis randomizados de potência e retornos à potência mínima.
6. Adquirir estabilidade temporal em condição fixa.
7. Testar saturação/linearidade do detector.
8. Medir posição, linewidth, intensidade e spectral diffusion.
9. Variar campo, polarização ou strain quando disponível.
10. Fechar com dark/background e hashes dos arquivos.

Saída A0, nunca uma alegação sobre `M_c`:

```text
advance_to_A1
repeat_A0
reject_candidate
inconclusive
```

Repetir se houver perda de identidade, saturação não caracterizada, potência
desconhecida, drift sem série utilizável, background ausente, timestamp
inconsistente ou arquivo bruto perdido. Runs inválidos nunca são apagados.

