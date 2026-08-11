# Darkwatch Calibration Report

**Generated:** 2026-08-11T01:46:52.126362Z
**Labeled contacts:** 64
**Label source:** `data\processed\calibration_labels_v4_adaptive_recal4_auto.json`

---

## 1. Label Counts

- **ARTIFACT:** 43
- **CLEAR:** 9
- **DARK:** 9
- **UNKNOWN:** 3

---

## 2. Per-Class Calibration

### DARK

- Labeled positives: 9
- Mean predicted p_dark: 0.2203
- Brier score: 0.0842

| Predicted probability bin | Count | Observed DARK fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 36 | 0.000 | 0.036 |
| 0.20 – 0.40 | 11 | 0.000 | 0.378 |
| 0.40 – 0.60 | 16 | 0.500 | 0.497 |
| 0.60 – 0.80 | 1 | 1.000 | 0.683 |

### CLEAR

- Labeled positives: 9
- Mean predicted p_clear: 0.0601
- Brier score: 0.0590

| Predicted probability bin | Count | Observed CLEAR fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 58 | 0.052 | 0.000 |
| 0.40 – 0.60 | 1 | 1.000 | 0.597 |
| 0.60 – 0.80 | 5 | 1.000 | 0.650 |

### ARTIFACT

- Labeled positives: 43
- Mean predicted p_artifact: 0.6796
- Brier score: 0.1599

| Predicted probability bin | Count | Observed ARTIFACT fraction | Mean predicted |
|---|---|---|---|
| 0.20 – 0.40 | 12 | 0.167 | 0.351 |
| 0.40 – 0.60 | 21 | 0.667 | 0.476 |
| 0.60 – 0.80 | 2 | 0.500 | 0.703 |
| 0.80 – 1.00 | 29 | 0.897 | 0.962 |

---

## 3. Verdict-vs-Label Confusion

| Verdict | Labels | Count |
|---|---|---|
| ARTIFACT | ARTIFACT | 35 |
| ARTIFACT | CLEAR | 3 |
| ARTIFACT | UNKNOWN | 1 |
| CLEAR | CLEAR | 5 |
| DARK | DARK | 1 |
| REVIEW | ARTIFACT | 8 |
| REVIEW | CLEAR | 1 |
| REVIEW | DARK | 8 |
| REVIEW | UNKNOWN | 2 |

---

## 4. Key Findings

- A well-calibrated model has Brier scores near 0 and reliability points hugging the diagonal.
- With only 64 labeled contacts, these metrics are noisy; collecting more scenes is the top priority.
- The current model tends to assign moderate `p_dark` and `p_artifact` to platform-adjacent contacts; strong ARTIFACT labels (near platforms) help validate whether those probabilities are too low or too high.

---

## 5. Per-Contact Detail

| Contact | Scene | True label | Verdict | p_artifact | p_clear | p_dark | p_review | Nearest AIS (m) | Static object |
|---|---|---|---|---|---|---|---|---|---|
| `4714_06A94E_9466_vh_c4210_r14398_det0000` | 2024-07-11 | ARTIFACT | ARTIFACT | 0.9070 | 0.0000 | 0.0817 | 0.0113 | 37733 | — |
| `4714_06A94E_9466_vh_c3314_r10814_det0000` | 2024-07-11 | ARTIFACT | ARTIFACT | 0.9667 | 0.0000 | 0.0291 | 0.0042 | 12710 | Platform Irene |
| `54809_06ACA2_D01B_vh_c2380_r8843_det0000` | 2024-07-18 | CLEAR | CLEAR | 0.3133 | 0.6764 | 0.0103 | 0.0000 | 126 | — |
| `54809_06ACA2_D01B_vh_c9548_r7947_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.9324 | 0.0000 | 0.0592 | 0.0084 | 7660 | Platform Holly |
| `54809_06ACA2_D01B_vh_c2380_r9739_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.9896 | 0.0000 | 0.0091 | 0.0013 | 9412 | Platform Harvest |
| `54809_06ACA2_D01B_vv_c9548_r7947_det0000` | 2024-07-18 | UNKNOWN | REVIEW | 0.3979 | 0.0000 | 0.5543 | 0.0477 | 9076 | — |
| `54809_06ACA2_D01B_vh_c6860_r8843_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.9699 | 0.0000 | 0.0263 | 0.0038 | 10291 | — |
| `54809_06ACA2_D01B_vv_c2380_r9739_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.9790 | 0.0000 | 0.0183 | 0.0027 | 7437 | Platform Hermosa |
| `54809_06ACA2_D01B_vv_c5068_r9739_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.9719 | 0.0000 | 0.0245 | 0.0036 | 8880 | — |
| `54809_06ACA2_D01B_vh_c6860_r7947_det0000` | 2024-07-18 | CLEAR | CLEAR | 0.3687 | 0.6234 | 0.0079 | 0.0000 | 450 | Platform Harmony |
| `54809_06ACA2_D01B_vh_c7756_r7947_det0000` | 2024-07-18 | CLEAR | CLEAR | 0.3490 | 0.6421 | 0.0089 | 0.0000 | 313 | Platform Hondo |
| `54809_06ACA2_D01B_vh_c5964_r8843_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.9691 | 0.0000 | 0.0270 | 0.0039 | 13843 | — |
| `54809_06ACA2_D01B_vh_c9548_r7947_det0002` | 2024-07-18 | CLEAR | ARTIFACT | 0.9485 | 0.0000 | 0.0515 | 0.0000 | 1336 | — |
| `54809_06ACA2_D01B_vh_c2380_r9739_det0001` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.9673 | 0.0000 | 0.0285 | 0.0042 | 12831 | Platform Hidalgo |
| `4809_06ACA2_D01B_vv_c10444_r7947_det0000` | 2024-07-18 | CLEAR | ARTIFACT | 0.9457 | 0.0000 | 0.0543 | 0.0000 | 1498 | — |
| `54809_06ACA2_D01B_vh_c4172_r8843_det0000` | 2024-07-18 | CLEAR | ARTIFACT | 0.9453 | 0.0000 | 0.0547 | 0.0000 | 1644 | — |
| `54809_06ACA2_D01B_vh_c6860_r8843_det0001` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.9197 | 0.0000 | 0.0704 | 0.0099 | 12536 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0000` | 2024-07-23 | DARK | DARK | 0.2605 | 0.0000 | 0.6829 | 0.0566 | 23994 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0001` | 2024-07-23 | DARK | REVIEW | 0.3971 | 0.0000 | 0.5551 | 0.0478 | 24023 | — |
| `882_06AF26_69FC_vv_c21010_r14232_det0000` | 2024-07-23 | DARK | REVIEW | 0.4091 | 0.0000 | 0.5438 | 0.0471 | 23724 | — |
| `882_06AF26_69FC_vv_c21010_r14232_det0001` | 2024-07-23 | DARK | REVIEW | 0.4362 | 0.0000 | 0.5182 | 0.0456 | 23894 | — |
| `882_06AF26_69FC_vv_c21010_r14232_det0002` | 2024-07-23 | DARK | REVIEW | 0.4403 | 0.0000 | 0.5143 | 0.0454 | 24165 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0002` | 2024-07-23 | ARTIFACT | REVIEW | 0.4596 | 0.0000 | 0.4961 | 0.0443 | 23987 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0003` | 2024-07-23 | DARK | REVIEW | 0.4658 | 0.0000 | 0.4901 | 0.0440 | 23912 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0005` | 2024-07-23 | DARK | REVIEW | 0.4695 | 0.0000 | 0.4867 | 0.0438 | 23859 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0009` | 2024-07-23 | DARK | REVIEW | 0.4744 | 0.0000 | 0.4820 | 0.0436 | 24072 | — |
| `55159_06B8DF_48C3_vh_c2397_r9735_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9961 | 0.0000 | 0.0034 | 0.0005 | 37668 | Platform Hidalgo |
| `55159_06B8DF_48C3_vh_c2397_r9735_det0001` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9958 | 0.0000 | 0.0037 | 0.0005 | 32442 | Platform Hermosa |
| `55159_06B8DF_48C3_vh_c5981_r7943_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9948 | 0.0000 | 0.0046 | 0.0006 | 12894 | Platform Heritage |
| `55159_06B8DF_48C3_vh_c9565_r7943_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9365 | 0.0000 | 0.0556 | 0.0079 | 7491 | Platform Holly |
| `55159_06B8DF_48C3_vv_c7773_r7943_det0000` | 2024-08-11 | CLEAR | CLEAR | 0.3420 | 0.6490 | 0.0089 | 0.0000 | 281 | Platform Hondo |
| `55159_06B8DF_48C3_vh_c9565_r7943_det0001` | 2024-08-11 | DARK | REVIEW | 0.3655 | 0.0000 | 0.5848 | 0.0497 | 8681 | — |
| `55159_06B8DF_48C3_vh_c4189_r8839_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9869 | 0.0000 | 0.0115 | 0.0016 | 15525 | — |
| `55159_06B8DF_48C3_vh_c2397_r9735_det0002` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9858 | 0.0000 | 0.0124 | 0.0018 | 35583 | Platform Harvest |
| `55159_06B8DF_48C3_vh_c6877_r7943_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9768 | 0.0000 | 0.0202 | 0.0029 | 4799 | Platform Harmony |
| `5159_06B8DF_48C3_vh_c2397_r11527_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9675 | 0.0000 | 0.0284 | 0.0042 | 43038 | Platform Irene |
| `55159_06B8DF_48C3_vh_c5981_r8839_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9701 | 0.0000 | 0.0289 | 0.0010 | 2847 | — |
| `55159_06B8DF_48C3_vh_c6877_r8839_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9353 | 0.0000 | 0.0566 | 0.0081 | 10228 | — |
| `55159_06B8DF_48C3_vh_c5085_r8839_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9168 | 0.0000 | 0.0730 | 0.0102 | 12420 | — |
| `55159_06B8DF_48C3_vh_c3293_r9735_det0001` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9657 | 0.0000 | 0.0299 | 0.0044 | 32432 | Platform Hermosa |
| `55159_06B8DF_48C3_vh_c4189_r8839_det0001` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9680 | 0.0000 | 0.0279 | 0.0041 | 15903 | — |
| `55159_06B8DF_48C3_vv_c9565_r7943_det0002` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9475 | 0.0000 | 0.0525 | 0.0000 | 995 | — |
| `55159_06B8DF_48C3_vv_c8669_r8839_det0000` | 2024-08-11 | UNKNOWN | REVIEW | 0.4761 | 0.0000 | 0.4805 | 0.0435 | 12737 | — |
| `55159_06B8DF_48C3_vh_c4189_r9735_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9665 | 0.0000 | 0.0293 | 0.0043 | 15537 | — |
| `55159_06B8DF_48C3_vh_c8669_r7943_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9663 | 0.0000 | 0.0294 | 0.0043 | 10590 | — |
| `55159_06B8DF_48C3_vh_c9565_r7047_det0000` | 2024-08-11 | UNKNOWN | ARTIFACT | 0.6121 | 0.0000 | 0.3520 | 0.0359 | 6644 | — |
| `232_06BB8A_EEBC_vv_c21028_r14228_det0000` | 2024-08-16 | ARTIFACT | REVIEW | 0.4887 | 0.0000 | 0.3934 | 0.1179 | 45282 | — |
| `232_06BB8A_EEBC_vv_c21028_r14228_det0001` | 2024-08-16 | ARTIFACT | REVIEW | 0.4915 | 0.0000 | 0.3912 | 0.1172 | 45613 | — |
| `232_06BB8A_EEBC_vv_c21028_r14228_det0003` | 2024-08-16 | ARTIFACT | ARTIFACT | 0.5001 | 0.0000 | 0.3844 | 0.1155 | 45401 | — |
| `232_06BB8A_EEBC_vv_c21028_r14228_det0005` | 2024-08-16 | ARTIFACT | ARTIFACT | 0.5070 | 0.0000 | 0.3790 | 0.1140 | 45523 | — |
| `232_06BB8A_EEBC_vv_c21028_r14228_det0006` | 2024-08-16 | ARTIFACT | ARTIFACT | 0.5092 | 0.0000 | 0.3772 | 0.1136 | 45453 | — |
| `232_06BB8A_EEBC_vv_c21028_r14228_det0009` | 2024-08-16 | ARTIFACT | ARTIFACT | 0.5142 | 0.0000 | 0.3732 | 0.1126 | 45720 | — |
| `407_06C206_BADB_vv_c21042_r14225_det0000` | 2024-08-28 | ARTIFACT | REVIEW | 0.3804 | 0.0000 | 0.4799 | 0.1398 | 35739 | — |
| `5407_06C206_BADB_vh_c20146_r9745_det0000` | 2024-08-28 | CLEAR | CLEAR | 0.2853 | 0.6590 | 0.0556 | 0.0000 | 476 | — |
| `407_06C206_BADB_vv_c21042_r14225_det0001` | 2024-08-28 | ARTIFACT | REVIEW | 0.3962 | 0.0000 | 0.4672 | 0.1366 | 35580 | — |
| `407_06C206_BADB_vv_c21042_r14225_det0002` | 2024-08-28 | ARTIFACT | REVIEW | 0.4186 | 0.0000 | 0.4494 | 0.1320 | 35719 | — |
| `407_06C206_BADB_vv_c21042_r14225_det0005` | 2024-08-28 | ARTIFACT | REVIEW | 0.4384 | 0.0000 | 0.4336 | 0.1281 | 35484 | — |
| `407_06C206_BADB_vv_c21042_r14225_det0006` | 2024-08-28 | ARTIFACT | REVIEW | 0.4601 | 0.0000 | 0.4162 | 0.1237 | 35621 | — |
| `5407_06C206_BADB_vh_c20146_r9745_det0001` | 2024-08-28 | CLEAR | REVIEW | 0.3543 | 0.5966 | 0.0492 | 0.0000 | 305 | — |
| `407_06C206_BADB_vv_c21042_r14225_det0009` | 2024-08-28 | ARTIFACT | ARTIFACT | 0.5026 | 0.0000 | 0.3824 | 0.1150 | 35537 | — |
| `407_06C206_BADB_vv_c21042_r14225_det0010` | 2024-08-28 | ARTIFACT | ARTIFACT | 0.5030 | 0.0000 | 0.3821 | 0.1149 | 35729 | — |
| `407_06C206_BADB_vv_c21042_r14225_det0014` | 2024-08-28 | ARTIFACT | ARTIFACT | 0.7938 | 0.0000 | 0.1588 | 0.0474 | 35646 | — |
| `407_06C206_BADB_vv_c21042_r14225_det0017` | 2024-08-28 | ARTIFACT | ARTIFACT | 0.5134 | 0.0000 | 0.3738 | 0.1128 | 35530 | — |
| `407_06C206_BADB_vv_c21042_r14225_det0018` | 2024-08-28 | ARTIFACT | ARTIFACT | 0.5138 | 0.0000 | 0.3735 | 0.1127 | 35505 | — |

---

*Generated by `scripts/evaluate_calibration.py`.*
