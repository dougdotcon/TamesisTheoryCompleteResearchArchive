# Restrições Termodinâmicas na Complexidade de Tempo Não-Polinomial

## Uma Prova Física de que P ≠ NP

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18131181.svg)](https://doi.org/10.5281/zenodo.18131181)

**Autor:** Douglas H. M. Fulber  
**Afiliação:** Universidade Federal do Rio de Janeiro  
**Email:** <dougdotcon@gmail.com>

---

## 📄 Artigos

| Arquivo | Descrição |
|---------|-----------|
| `paper_p_vs_np_ptbr.html` | Artigo completo em Português (HTML) |
| `paper_p_vs_np.html` | Artigo em Inglês (HTML) |
| `paper_p_vs_np.tex` | Código LaTeX |
| `paper_p_vs_np_ptbr.txt` | Versão texto puro |

---

## 🔬 Scripts de Validação

| Script | Experimento |
|--------|-------------|
| `thermodynamic_turing_machine.py` | Módulo base TTM |
| `exp1_gap_spectral.py` | Gap Espectral (α=3.40, R²=0.965) |
| `exp2_landauer_entropy.py` | Landauer (slope=1.00) |
| `exp3_anderson_localization.py` | Anderson (IPR crescente) |
| `appendix_a_rem_validation.py` | REM (slope=0.80 vs 0.83) |
| `appendix_b_optical_limits.py` | Limites Ópticos |

### Executar todos os experimentos

```bash
cd scripts
python exp1_gap_spectral.py
python exp2_landauer_entropy.py
python exp3_anderson_localization.py
python appendix_a_rem_validation.py
python appendix_b_optical_limits.py
```

---

## 📊 Figuras

| Figura | Descrição |
|--------|-----------|
| `fig1_entropy.png` | Custo termodinâmico da computação |
| `fig2_landscape.png` | Paisagens P vs NP |
| `fig3_gap_scaling.png` | Escala do gap espectral |
| `fig4_entropy_dissipation.png` | Entropia dissipada (Landauer) |
| `fig5_ipr_localization.png` | Localização de Anderson |
| `fig6_rem_validation.png` | Validação do REM |
| `fig7_optical_limits.png` | Limites do computador óptico |

---

## 📋 Resultados

| Experimento | Previsão | Resultado | Status |
|-------------|----------|-----------|--------|
| Gap Espectral | Δ ∝ e^(-αN) | α=3.40, R²=0.965 | ✓ VALIDADO |
| Landauer | ΔS = N | slope=1.00 | ✓ VALIDADO |
| Anderson | IPR → 1 | crescente | ✓ VALIDADO |
| REM | E₀ ∝ -N√(ln2) | 96% precisão | ✓ VALIDADO |
| Óptico | D ∝ 2^N | N>45 supera Terra | ✓ VALIDADO |

---

## 🎯 Conclusão

**P ≠ NP é uma consequência física das leis da termodinâmica e da mecânica quântica.**

---

## 📚 Referências Principais

1. Cook (1971) - Complexidade de prova de teoremas
2. Landauer (1961) - Custo termodinâmico da computação
3. Bekenstein (1981) - Limite entrópico
4. Altshuler et al. (2010) - Localização de Anderson em otimização quântica
