# Darkwatch Calibration Report

**Generated:** 2026-08-08T23:56:32.948253Z
**Labeled contacts:** 26
**Label source:** `data\processed\calibration_labels_v4_adaptive_recal.json`

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
- Mean predicted p_dark: 0.3452
- Brier score: 0.0988

| Predicted probability bin | Count | Observed DARK fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.10 | 4 | 0.000 | 0.067 |
| 0.10 – 0.20 | 4 | 0.000 | 0.141 |
| 0.20 – 0.30 | 6 | 0.167 | 0.242 |
| 0.30 – 0.40 | 4 | 0.000 | 0.336 |
| 0.60 – 0.70 | 7 | 0.857 | 0.661 |
| 0.70 – 0.80 | 1 | 1.000 | 0.723 |

### CLEAR

- Labeled positives: 6
- Mean predicted p_clear: 0.1378
- Brier score: 0.0379

| Predicted probability bin | Count | Observed CLEAR fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.10 | 20 | 0.000 | 0.000 |
| 0.50 – 0.60 | 2 | 1.000 | 0.539 |
| 0.60 – 0.70 | 4 | 1.000 | 0.626 |

### ARTIFACT

- Labeled positives: 11
- Mean predicted p_artifact: 0.4083
- Brier score: 0.0960

| Predicted probability bin | Count | Observed ARTIFACT fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.10 | 3 | 0.000 | 0.075 |
| 0.10 – 0.20 | 5 | 0.000 | 0.129 |
| 0.20 – 0.30 | 1 | 0.000 | 0.240 |
| 0.30 – 0.40 | 5 | 0.000 | 0.337 |
| 0.50 – 0.60 | 4 | 1.000 | 0.552 |
| 0.60 – 0.70 | 5 | 0.800 | 0.672 |
| 0.70 – 0.80 | 2 | 1.000 | 0.721 |
| 0.80 – 0.90 | 1 | 1.000 | 0.808 |

---

## 3. Verdict-vs-Label Confusion

| Verdict | Labels | Count |
|---|---|---|
| ARTIFACT | ARTIFACT | 11 |
| ARTIFACT | DARK | 1 |
| CLEAR | CLEAR | 4 |
| DARK | DARK | 7 |
| DARK | UNKNOWN | 1 |
| REVIEW | CLEAR | 2 |

---

## 4. Key Findings

- A well-calibrated model has Brier scores near 0 and reliability points hugging the diagonal.
- With only 26 labeled contacts, these metrics are noisy; collecting more scenes is the top priority.
- The current model tends to assign moderate `p_dark` and `p_artifact` to platform-adjacent contacts; strong ARTIFACT labels (near platforms) help validate whether those probabilities are too low or too high.

---

## 5. Per-Contact Detail

| Contact | Scene | True label | Verdict | p_artifact | p_clear | p_dark | p_review | Nearest AIS (m) | Static object |
|---|---|---|---|---|---|---|---|---|---|
| `4714_06A94E_9466_vh_c4210_r14398_det0000` | 2024-07-11 | ARTIFACT | ARTIFACT | 0.5273 | 0.0000 | 0.3545 | 0.1182 | 37733 | — |
| `4714_06A94E_9466_vh_c3314_r10814_det0000` | 2024-07-11 | ARTIFACT | ARTIFACT | 0.6815 | 0.0000 | 0.2389 | 0.0796 | 12710 | Platform Irene |
| `54809_06ACA2_D01B_vh_c2380_r8843_det0000` | 2024-07-18 | CLEAR | REVIEW | 0.3890 | 0.5083 | 0.1026 | 0.0000 | 126 | — |
| `54809_06ACA2_D01B_vh_c9548_r7947_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.5795 | 0.0000 | 0.3154 | 0.1051 | 7660 | Platform Holly |
| `54809_06ACA2_D01B_vh_c2380_r9739_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.8084 | 0.0000 | 0.1437 | 0.0479 | 9412 | Platform Harvest |
| `54809_06ACA2_D01B_vv_c9548_r7947_det0000` | 2024-07-18 | UNKNOWN | DARK | 0.0950 | 0.0000 | 0.6787 | 0.2262 | 9076 | — |
| `54809_06ACA2_D01B_vh_c6860_r8843_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.6945 | 0.0000 | 0.2291 | 0.0764 | 10291 | — |
| `54809_06ACA2_D01B_vv_c2380_r9739_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.7378 | 0.0000 | 0.1967 | 0.0656 | 7437 | Platform Hermosa |
| `54809_06ACA2_D01B_vv_c5068_r9739_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.7032 | 0.0000 | 0.2226 | 0.0742 | 8880 | — |
| `54809_06ACA2_D01B_vh_c6860_r7947_det0000` | 2024-07-18 | CLEAR | REVIEW | 0.3629 | 0.5706 | 0.0666 | 0.0000 | 450 | Platform Harmony |
| `54809_06ACA2_D01B_vh_c7756_r7947_det0000` | 2024-07-18 | CLEAR | CLEAR | 0.2397 | 0.6400 | 0.1203 | 0.0000 | 313 | Platform Hondo |
| `54809_06ACA2_D01B_vh_c5964_r8843_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.6913 | 0.0000 | 0.2316 | 0.0772 | 13843 | — |
| `54809_06ACA2_D01B_vh_c9548_r7947_det0002` | 2024-07-18 | CLEAR | CLEAR | 0.3219 | 0.6116 | 0.0665 | 0.0000 | 1336 | — |
| `54809_06ACA2_D01B_vh_c2380_r9739_det0001` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.6839 | 0.0000 | 0.2371 | 0.0790 | 12831 | Platform Hidalgo |
| `4809_06ACA2_D01B_vv_c10444_r7947_det0000` | 2024-07-18 | CLEAR | CLEAR | 0.3069 | 0.6252 | 0.0680 | 0.0000 | 1498 | — |
| `54809_06ACA2_D01B_vh_c4172_r8843_det0000` | 2024-07-18 | CLEAR | CLEAR | 0.3049 | 0.6269 | 0.0682 | 0.0000 | 1644 | — |
| `54809_06ACA2_D01B_vh_c6860_r8843_det0001` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.5519 | 0.0000 | 0.3361 | 0.1120 | 12536 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0000` | 2024-07-23 | DARK | DARK | 0.0354 | 0.0000 | 0.7234 | 0.2411 | 23994 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0001` | 2024-07-23 | DARK | DARK | 0.0945 | 0.0000 | 0.6791 | 0.2264 | 24023 | — |
| `882_06AF26_69FC_vv_c21010_r14232_det0000` | 2024-07-23 | DARK | ARTIFACT | 0.6111 | 0.0000 | 0.2917 | 0.0972 | 23724 | — |
| `882_06AF26_69FC_vv_c21010_r14232_det0001` | 2024-07-23 | DARK | DARK | 0.1165 | 0.0000 | 0.6626 | 0.2209 | 23894 | — |
| `882_06AF26_69FC_vv_c21010_r14232_det0002` | 2024-07-23 | DARK | DARK | 0.1190 | 0.0000 | 0.6607 | 0.2202 | 24165 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0002` | 2024-07-23 | ARTIFACT | ARTIFACT | 0.5487 | 0.0000 | 0.3385 | 0.1128 | 23987 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0003` | 2024-07-23 | DARK | DARK | 0.1342 | 0.0000 | 0.6494 | 0.2165 | 23912 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0005` | 2024-07-23 | DARK | DARK | 0.1364 | 0.0000 | 0.6477 | 0.2159 | 23859 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0009` | 2024-07-23 | DARK | DARK | 0.1394 | 0.0000 | 0.6455 | 0.2152 | 24072 | — |

---

*Generated by `scripts/evaluate_calibration.py`.*
