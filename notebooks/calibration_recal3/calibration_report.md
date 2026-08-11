# Darkwatch Calibration Report

**Generated:** 2026-08-11T00:08:50.758334Z
**Labeled contacts:** 46
**Label source:** `data\processed\calibration_labels_v4_adaptive_recal3.json`

---

## 1. Label Counts

- **ARTIFACT:** 27
- **CLEAR:** 7
- **DARK:** 9
- **UNKNOWN:** 3

---

## 2. Per-Class Calibration

### DARK

- Labeled positives: 9
- Mean predicted p_dark: 0.2815
- Brier score: 0.0641

| Predicted probability bin | Count | Observed DARK fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 32 | 0.000 | 0.085 |
| 0.20 – 0.40 | 1 | 0.000 | 0.206 |
| 0.60 – 0.80 | 9 | 0.667 | 0.750 |
| 0.80 – 1.00 | 4 | 0.750 | 0.817 |

### CLEAR

- Labeled positives: 7
- Mean predicted p_clear: 0.0718
- Brier score: 0.0679

| Predicted probability bin | Count | Observed CLEAR fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 42 | 0.071 | 0.000 |
| 0.60 – 0.80 | 1 | 1.000 | 0.792 |
| 0.80 – 1.00 | 3 | 1.000 | 0.837 |

### ARTIFACT

- Labeled positives: 27
- Mean predicted p_artifact: 0.5995
- Brier score: 0.0793

| Predicted probability bin | Count | Observed ARTIFACT fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 16 | 0.062 | 0.102 |
| 0.20 – 0.40 | 1 | 0.000 | 0.272 |
| 0.60 – 0.80 | 3 | 1.000 | 0.765 |
| 0.80 – 1.00 | 26 | 0.885 | 0.899 |

---

## 3. Verdict-vs-Label Confusion

| Verdict | Labels | Count |
|---|---|---|
| ARTIFACT | ARTIFACT | 26 |
| ARTIFACT | CLEAR | 3 |
| CLEAR | CLEAR | 4 |
| DARK | ARTIFACT | 1 |
| DARK | DARK | 9 |
| DARK | UNKNOWN | 3 |

---

## 4. Key Findings

- A well-calibrated model has Brier scores near 0 and reliability points hugging the diagonal.
- With only 46 labeled contacts, these metrics are noisy; collecting more scenes is the top priority.
- The current model tends to assign moderate `p_dark` and `p_artifact` to platform-adjacent contacts; strong ARTIFACT labels (near platforms) help validate whether those probabilities are too low or too high.

---

## 5. Per-Contact Detail

| Contact | Scene | True label | Verdict | p_artifact | p_clear | p_dark | p_review | Nearest AIS (m) | Static object |
|---|---|---|---|---|---|---|---|---|---|
| `4714_06A94E_9466_vh_c4210_r14398_det0000` | 2024-07-11 | ARTIFACT | ARTIFACT | 0.7489 | 0.0000 | 0.2063 | 0.0448 | 37733 | — |
| `4714_06A94E_9466_vh_c3314_r10814_det0000` | 2024-07-11 | ARTIFACT | ARTIFACT | 0.8929 | 0.0000 | 0.0840 | 0.0231 | 12710 | Platform Irene |
| `54809_06ACA2_D01B_vh_c2380_r8843_det0000` | 2024-07-18 | CLEAR | CLEAR | 0.0908 | 0.8618 | 0.0474 | 0.0000 | 126 | — |
| `54809_06ACA2_D01B_vh_c9548_r7947_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.8063 | 0.0000 | 0.1570 | 0.0366 | 7660 | Platform Holly |
| `54809_06ACA2_D01B_vh_c2380_r9739_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.9606 | 0.0000 | 0.0290 | 0.0104 | 9412 | Platform Harvest |
| `54809_06ACA2_D01B_vv_c9548_r7947_det0000` | 2024-07-18 | UNKNOWN | DARK | 0.0705 | 0.0000 | 0.8009 | 0.1286 | 9076 | — |
| `54809_06ACA2_D01B_vh_c6860_r8843_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.9017 | 0.0000 | 0.0767 | 0.0216 | 10291 | — |
| `54809_06ACA2_D01B_vv_c2380_r9739_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.9277 | 0.0000 | 0.0553 | 0.0170 | 7437 | Platform Hermosa |
| `54809_06ACA2_D01B_vv_c5068_r9739_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.9073 | 0.0000 | 0.0720 | 0.0207 | 8880 | — |
| `54809_06ACA2_D01B_vh_c6860_r7947_det0000` | 2024-07-18 | CLEAR | CLEAR | 0.1706 | 0.7919 | 0.0376 | 0.0000 | 450 | Platform Harmony |
| `54809_06ACA2_D01B_vh_c7756_r7947_det0000` | 2024-07-18 | CLEAR | CLEAR | 0.1389 | 0.8193 | 0.0418 | 0.0000 | 313 | Platform Hondo |
| `54809_06ACA2_D01B_vh_c5964_r8843_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.8995 | 0.0000 | 0.0785 | 0.0220 | 13843 | — |
| `54809_06ACA2_D01B_vh_c9548_r7947_det0002` | 2024-07-18 | CLEAR | ARTIFACT | 0.8593 | 0.0000 | 0.1407 | 0.0000 | 1336 | — |
| `54809_06ACA2_D01B_vh_c2380_r9739_det0001` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.8945 | 0.0000 | 0.0826 | 0.0228 | 12831 | Platform Hidalgo |
| `4809_06ACA2_D01B_vv_c10444_r7947_det0000` | 2024-07-18 | CLEAR | ARTIFACT | 0.8527 | 0.0000 | 0.1473 | 0.0000 | 1498 | — |
| `54809_06ACA2_D01B_vh_c4172_r8843_det0000` | 2024-07-18 | CLEAR | ARTIFACT | 0.8518 | 0.0000 | 0.1482 | 0.0000 | 1644 | — |
| `54809_06ACA2_D01B_vh_c6860_r8843_det0001` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.7771 | 0.0000 | 0.1821 | 0.0408 | 12536 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0000` | 2024-07-23 | DARK | DARK | 0.0156 | 0.0000 | 0.8475 | 0.1369 | 23994 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0001` | 2024-07-23 | DARK | DARK | 0.0700 | 0.0000 | 0.8013 | 0.1287 | 24023 | — |
| `882_06AF26_69FC_vv_c21010_r14232_det0000` | 2024-07-23 | DARK | DARK | 0.0777 | 0.0000 | 0.7947 | 0.1276 | 23724 | — |
| `882_06AF26_69FC_vv_c21010_r14232_det0001` | 2024-07-23 | DARK | DARK | 0.0968 | 0.0000 | 0.7781 | 0.1251 | 23894 | — |
| `882_06AF26_69FC_vv_c21010_r14232_det0002` | 2024-07-23 | DARK | DARK | 0.1000 | 0.0000 | 0.7754 | 0.1246 | 24165 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0002` | 2024-07-23 | ARTIFACT | DARK | 0.1153 | 0.0000 | 0.7621 | 0.1226 | 23987 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0003` | 2024-07-23 | DARK | DARK | 0.1205 | 0.0000 | 0.7575 | 0.1220 | 23912 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0005` | 2024-07-23 | DARK | DARK | 0.1236 | 0.0000 | 0.7548 | 0.1215 | 23859 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0009` | 2024-07-23 | DARK | DARK | 0.1278 | 0.0000 | 0.7511 | 0.1210 | 24072 | — |
| `55159_06B8DF_48C3_vh_c2397_r9735_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9834 | 0.0000 | 0.0115 | 0.0051 | 37668 | Platform Hidalgo |
| `55159_06B8DF_48C3_vh_c2397_r9735_det0001` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9824 | 0.0000 | 0.0123 | 0.0054 | 32442 | Platform Hermosa |
| `55159_06B8DF_48C3_vh_c5981_r7943_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9786 | 0.0000 | 0.0151 | 0.0063 | 12894 | Platform Heritage |
| `55159_06B8DF_48C3_vh_c9565_r7943_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.8161 | 0.0000 | 0.1487 | 0.0352 | 7491 | Platform Holly |
| `55159_06B8DF_48C3_vv_c7773_r7943_det0000` | 2024-08-11 | CLEAR | CLEAR | 0.1287 | 0.8293 | 0.0420 | 0.0000 | 281 | Platform Hondo |
| `55159_06B8DF_48C3_vh_c9565_r7943_det0001` | 2024-08-11 | DARK | DARK | 0.0521 | 0.0000 | 0.8167 | 0.1313 | 8681 | — |
| `55159_06B8DF_48C3_vh_c4189_r8839_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9519 | 0.0000 | 0.0358 | 0.0122 | 15525 | — |
| `55159_06B8DF_48C3_vh_c2397_r9735_det0002` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9484 | 0.0000 | 0.0386 | 0.0130 | 35583 | Platform Harvest |
| `55159_06B8DF_48C3_vh_c6877_r7943_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9214 | 0.0000 | 0.0604 | 0.0181 | 4799 | Platform Harmony |
| `5159_06B8DF_48C3_vh_c2397_r11527_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.8951 | 0.0000 | 0.0822 | 0.0228 | 43038 | Platform Irene |
| `55159_06B8DF_48C3_vh_c5981_r8839_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9076 | 0.0000 | 0.0841 | 0.0083 | 2847 | — |
| `55159_06B8DF_48C3_vh_c6877_r8839_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.8132 | 0.0000 | 0.1511 | 0.0356 | 10228 | — |
| `55159_06B8DF_48C3_vh_c5085_r8839_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.7705 | 0.0000 | 0.1877 | 0.0418 | 12420 | — |
| `55159_06B8DF_48C3_vh_c3293_r9735_det0001` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.8902 | 0.0000 | 0.0862 | 0.0236 | 32432 | Platform Hermosa |
| `55159_06B8DF_48C3_vh_c4189_r8839_det0001` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.8966 | 0.0000 | 0.0809 | 0.0225 | 15903 | — |
| `55159_06B8DF_48C3_vv_c9565_r7943_det0002` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.8568 | 0.0000 | 0.1432 | 0.0000 | 995 | — |
| `55159_06B8DF_48C3_vv_c8669_r8839_det0000` | 2024-08-11 | UNKNOWN | DARK | 0.1293 | 0.0000 | 0.7499 | 0.1208 | 12737 | — |
| `55159_06B8DF_48C3_vh_c4189_r9735_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.8923 | 0.0000 | 0.0845 | 0.0232 | 15537 | — |
| `55159_06B8DF_48C3_vh_c8669_r7943_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.8918 | 0.0000 | 0.0849 | 0.0233 | 10590 | — |
| `55159_06B8DF_48C3_vh_c9565_r7047_det0000` | 2024-08-11 | UNKNOWN | DARK | 0.2724 | 0.0000 | 0.6242 | 0.1033 | 6644 | — |

---

*Generated by `scripts/evaluate_calibration.py`.*
