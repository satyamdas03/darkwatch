# Darkwatch Calibration Report

**Generated:** 2026-08-08T23:00:57.235755Z
**Labeled contacts:** 26
**Label source:** `data\processed\calibration_labels_v4_adaptive.json`

---

## 1. Label Counts

- **ARTIFACT:** 11
- **CLEAR:** 6
- **DARK:** 8
- **UNKNOWN:** 1

---

## 2. Per-Class Calibration

### DARK

- Labeled positives: 8
- Mean predicted p_dark: 0.5366
- Brier score: 0.2235

| Predicted probability bin | Count | Observed DARK fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 5 | 0.000 | 0.181 |
| 0.20 – 0.40 | 1 | 0.000 | 0.205 |
| 0.40 – 0.60 | 2 | 0.000 | 0.526 |
| 0.60 – 0.80 | 18 | 0.444 | 0.655 |

### CLEAR

- Labeled positives: 6
- Mean predicted p_clear: 0.1572
- Brier score: 0.0238

| Predicted probability bin | Count | Observed CLEAR fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 20 | 0.000 | 0.000 |
| 0.60 – 0.80 | 6 | 1.000 | 0.681 |

### ARTIFACT

- Labeled positives: 11
- Mean predicted p_artifact: 0.1415
- Brier score: 0.3001

| Predicted probability bin | Count | Observed ARTIFACT fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 24 | 0.375 | 0.128 |
| 0.20 – 0.40 | 2 | 1.000 | 0.299 |

---

## 3. Verdict-vs-Label Confusion

| Verdict | Labels | Count |
|---|---|---|
| CLEAR | CLEAR | 6 |
| DARK | ARTIFACT | 9 |
| DARK | DARK | 8 |
| DARK | UNKNOWN | 1 |
| REVIEW | ARTIFACT | 2 |

---

## 4. Key Findings

- A well-calibrated model has Brier scores near 0 and reliability points hugging the diagonal.
- With only 26 labeled contacts, these metrics are noisy; collecting more scenes is the top priority.
- The current model tends to assign moderate `p_dark` and `p_artifact` to platform-adjacent contacts; strong ARTIFACT labels (near platforms) help validate whether those probabilities are too low or too high.

---

## 5. Per-Contact Detail

| Contact | Scene | True label | Verdict | p_artifact | p_clear | p_dark | p_review | Nearest AIS (m) | Static object |
|---|---|---|---|---|---|---|---|---|---|
| `4714_06A94E_9466_vh_c4210_r14398_det0000` | 2024-07-11 | ARTIFACT | DARK | 0.1404 | 0.0000 | 0.6447 | 0.2149 | 37733 | — |
| `4714_06A94E_9466_vh_c3314_r10814_det0000` | 2024-07-11 | ARTIFACT | DARK | 0.1856 | 0.0000 | 0.6108 | 0.2036 | 12710 | Platform Irene |
| `54809_06ACA2_D01B_vh_c2380_r8843_det0000` | 2024-07-18 | CLEAR | CLEAR | 0.0404 | 0.7545 | 0.2051 | 0.0000 | 126 | — |
| `54809_06ACA2_D01B_vh_c9548_r7947_det0000` | 2024-07-18 | ARTIFACT | DARK | 0.1613 | 0.0000 | 0.6290 | 0.2097 | 7660 | Platform Holly |
| `54809_06ACA2_D01B_vh_c2380_r9739_det0000` | 2024-07-18 | ARTIFACT | REVIEW | 0.3585 | 0.0000 | 0.4811 | 0.1604 | 9412 | Platform Harvest |
| `54809_06ACA2_D01B_vv_c9548_r7947_det0000` | 2024-07-18 | UNKNOWN | DARK | 0.0950 | 0.0000 | 0.6787 | 0.2262 | 9076 | — |
| `54809_06ACA2_D01B_vh_c6860_r8843_det0000` | 2024-07-18 | ARTIFACT | DARK | 0.1054 | 0.0000 | 0.6710 | 0.2237 | 10291 | — |
| `54809_06ACA2_D01B_vv_c2380_r9739_det0000` | 2024-07-18 | ARTIFACT | REVIEW | 0.2400 | 0.0000 | 0.5700 | 0.1900 | 7437 | Platform Hermosa |
| `54809_06ACA2_D01B_vv_c5068_r9739_det0000` | 2024-07-18 | ARTIFACT | DARK | 0.1261 | 0.0000 | 0.6554 | 0.2185 | 8880 | — |
| `54809_06ACA2_D01B_vh_c6860_r7947_det0000` | 2024-07-18 | CLEAR | CLEAR | 0.1941 | 0.6337 | 0.1722 | 0.0000 | 450 | Platform Harmony |
| `54809_06ACA2_D01B_vh_c7756_r7947_det0000` | 2024-07-18 | CLEAR | CLEAR | 0.1493 | 0.6689 | 0.1818 | 0.0000 | 313 | Platform Hondo |
| `54809_06ACA2_D01B_vh_c5964_r8843_det0000` | 2024-07-18 | ARTIFACT | DARK | 0.1362 | 0.0000 | 0.6478 | 0.2159 | 13843 | — |
| `54809_06ACA2_D01B_vh_c9548_r7947_det0002` | 2024-07-18 | CLEAR | CLEAR | 0.1373 | 0.6783 | 0.1844 | 0.0000 | 1336 | — |
| `54809_06ACA2_D01B_vh_c2380_r9739_det0001` | 2024-07-18 | ARTIFACT | DARK | 0.1797 | 0.0000 | 0.6152 | 0.2051 | 12831 | Platform Hidalgo |
| `4809_06ACA2_D01B_vv_c10444_r7947_det0000` | 2024-07-18 | CLEAR | CLEAR | 0.1403 | 0.6759 | 0.1837 | 0.0000 | 1498 | — |
| `54809_06ACA2_D01B_vh_c4172_r8843_det0000` | 2024-07-18 | CLEAR | CLEAR | 0.1407 | 0.6756 | 0.1837 | 0.0000 | 1644 | — |
| `54809_06ACA2_D01B_vh_c6860_r8843_det0001` | 2024-07-18 | ARTIFACT | DARK | 0.1423 | 0.0000 | 0.6433 | 0.2144 | 12536 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0000` | 2024-07-23 | DARK | DARK | 0.0354 | 0.0000 | 0.7234 | 0.2411 | 23994 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0001` | 2024-07-23 | DARK | DARK | 0.0945 | 0.0000 | 0.6791 | 0.2264 | 24023 | — |
| `882_06AF26_69FC_vv_c21010_r14232_det0000` | 2024-07-23 | DARK | DARK | 0.1011 | 0.0000 | 0.6742 | 0.2247 | 23724 | — |
| `882_06AF26_69FC_vv_c21010_r14232_det0001` | 2024-07-23 | DARK | DARK | 0.1165 | 0.0000 | 0.6626 | 0.2209 | 23894 | — |
| `882_06AF26_69FC_vv_c21010_r14232_det0002` | 2024-07-23 | DARK | DARK | 0.1190 | 0.0000 | 0.6607 | 0.2202 | 24165 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0002` | 2024-07-23 | ARTIFACT | DARK | 0.1304 | 0.0000 | 0.6522 | 0.2174 | 23987 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0003` | 2024-07-23 | DARK | DARK | 0.1342 | 0.0000 | 0.6494 | 0.2165 | 23912 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0005` | 2024-07-23 | DARK | DARK | 0.1364 | 0.0000 | 0.6477 | 0.2159 | 23859 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0009` | 2024-07-23 | DARK | DARK | 0.1394 | 0.0000 | 0.6455 | 0.2152 | 24072 | — |

---

*Generated by `scripts/evaluate_calibration.py`.*
