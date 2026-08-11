# Darkwatch Calibration Report

**Generated:** 2026-08-11T01:47:29.605694Z
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
- Mean predicted p_dark: 0.3053
- Brier score: 0.1245

| Predicted probability bin | Count | Observed DARK fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 35 | 0.000 | 0.038 |
| 0.20 – 0.40 | 1 | 0.000 | 0.238 |
| 0.40 – 0.60 | 11 | 0.000 | 0.564 |
| 0.60 – 0.80 | 16 | 0.500 | 0.682 |
| 0.80 – 1.00 | 1 | 1.000 | 0.854 |

### CLEAR

- Labeled positives: 9
- Mean predicted p_clear: 0.0659
- Brier score: 0.0552

| Predicted probability bin | Count | Observed CLEAR fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 58 | 0.052 | 0.000 |
| 0.60 – 0.80 | 6 | 1.000 | 0.703 |

### ARTIFACT

- Labeled positives: 43
- Mean predicted p_artifact: 0.6011
- Brier score: 0.1837

| Predicted probability bin | Count | Observed ARTIFACT fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 2 | 0.000 | 0.148 |
| 0.20 – 0.40 | 31 | 0.516 | 0.296 |
| 0.40 – 0.60 | 1 | 0.000 | 0.469 |
| 0.60 – 0.80 | 1 | 1.000 | 0.731 |
| 0.80 – 1.00 | 29 | 0.897 | 0.959 |

---

## 3. Verdict-vs-Label Confusion

| Verdict | Labels | Count |
|---|---|---|
| ARTIFACT | ARTIFACT | 27 |
| ARTIFACT | CLEAR | 3 |
| CLEAR | CLEAR | 6 |
| DARK | ARTIFACT | 6 |
| DARK | DARK | 9 |
| DARK | UNKNOWN | 2 |
| REVIEW | ARTIFACT | 10 |
| REVIEW | UNKNOWN | 1 |

---

## 4. Key Findings

- A well-calibrated model has Brier scores near 0 and reliability points hugging the diagonal.
- With only 64 labeled contacts, these metrics are noisy; collecting more scenes is the top priority.
- The current model tends to assign moderate `p_dark` and `p_artifact` to platform-adjacent contacts; strong ARTIFACT labels (near platforms) help validate whether those probabilities are too low or too high.

---

## 5. Per-Contact Detail

| Contact | Scene | True label | Verdict | p_artifact | p_clear | p_dark | p_review | Nearest AIS (m) | Static object |
|---|---|---|---|---|---|---|---|---|---|
| `4714_06A94E_9466_vh_c4210_r14398_det0000` | 2024-07-11 | ARTIFACT | ARTIFACT | 0.8857 | 0.0000 | 0.1077 | 0.0065 | 37733 | — |
| `4714_06A94E_9466_vh_c3314_r10814_det0000` | 2024-07-11 | ARTIFACT | ARTIFACT | 0.9679 | 0.0000 | 0.0298 | 0.0023 | 12710 | Platform Irene |
| `54809_06ACA2_D01B_vh_c2380_r8843_det0000` | 2024-07-18 | CLEAR | CLEAR | 0.2388 | 0.7508 | 0.0104 | 0.0000 | 126 | — |
| `54809_06ACA2_D01B_vh_c9548_r7947_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.9227 | 0.0000 | 0.0726 | 0.0047 | 7660 | Platform Holly |
| `54809_06ACA2_D01B_vh_c2380_r9739_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.9924 | 0.0000 | 0.0069 | 0.0006 | 9412 | Platform Harvest |
| `54809_06ACA2_D01B_vv_c9548_r7947_det0000` | 2024-07-18 | UNKNOWN | DARK | 0.2371 | 0.0000 | 0.7319 | 0.0310 | 9076 | — |
| `54809_06ACA2_D01B_vh_c6860_r8843_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.9717 | 0.0000 | 0.0263 | 0.0020 | 10291 | — |
| `54809_06ACA2_D01B_vv_c2380_r9739_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.9819 | 0.0000 | 0.0167 | 0.0014 | 7437 | Platform Hermosa |
| `54809_06ACA2_D01B_vv_c5068_r9739_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.9740 | 0.0000 | 0.0241 | 0.0019 | 8880 | — |
| `54809_06ACA2_D01B_vh_c6860_r7947_det0000` | 2024-07-18 | CLEAR | CLEAR | 0.3158 | 0.6768 | 0.0074 | 0.0000 | 450 | Platform Harmony |
| `54809_06ACA2_D01B_vh_c7756_r7947_det0000` | 2024-07-18 | CLEAR | CLEAR | 0.2885 | 0.7030 | 0.0085 | 0.0000 | 313 | Platform Hondo |
| `54809_06ACA2_D01B_vh_c5964_r8843_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.9708 | 0.0000 | 0.0271 | 0.0021 | 13843 | — |
| `54809_06ACA2_D01B_vh_c9548_r7947_det0002` | 2024-07-18 | CLEAR | ARTIFACT | 0.9392 | 0.0000 | 0.0608 | 0.0000 | 1336 | — |
| `54809_06ACA2_D01B_vh_c2380_r9739_det0001` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.9686 | 0.0000 | 0.0292 | 0.0022 | 12831 | Platform Hidalgo |
| `4809_06ACA2_D01B_vv_c10444_r7947_det0000` | 2024-07-18 | CLEAR | ARTIFACT | 0.9351 | 0.0000 | 0.0649 | 0.0000 | 1498 | — |
| `54809_06ACA2_D01B_vh_c4172_r8843_det0000` | 2024-07-18 | CLEAR | ARTIFACT | 0.9345 | 0.0000 | 0.0655 | 0.0000 | 1644 | — |
| `54809_06ACA2_D01B_vh_c6860_r8843_det0001` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.9045 | 0.0000 | 0.0899 | 0.0056 | 12536 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0000` | 2024-07-23 | DARK | DARK | 0.1082 | 0.0000 | 0.8545 | 0.0374 | 23994 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0001` | 2024-07-23 | DARK | DARK | 0.2363 | 0.0000 | 0.7326 | 0.0311 | 24023 | — |
| `882_06AF26_69FC_vv_c21010_r14232_det0000` | 2024-07-23 | DARK | DARK | 0.2486 | 0.0000 | 0.7209 | 0.0305 | 23724 | — |
| `882_06AF26_69FC_vv_c21010_r14232_det0001` | 2024-07-23 | DARK | DARK | 0.2767 | 0.0000 | 0.6941 | 0.0292 | 23894 | — |
| `882_06AF26_69FC_vv_c21010_r14232_det0002` | 2024-07-23 | DARK | DARK | 0.2811 | 0.0000 | 0.6899 | 0.0290 | 24165 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0002` | 2024-07-23 | ARTIFACT | DARK | 0.3012 | 0.0000 | 0.6706 | 0.0281 | 23987 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0003` | 2024-07-23 | DARK | DARK | 0.3078 | 0.0000 | 0.6643 | 0.0279 | 23912 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0005` | 2024-07-23 | DARK | DARK | 0.3117 | 0.0000 | 0.6607 | 0.0277 | 23859 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0009` | 2024-07-23 | DARK | DARK | 0.3168 | 0.0000 | 0.6557 | 0.0275 | 24072 | — |
| `55159_06B8DF_48C3_vh_c2397_r9735_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9978 | 0.0000 | 0.0020 | 0.0002 | 37668 | Platform Hidalgo |
| `55159_06B8DF_48C3_vh_c2397_r9735_det0001` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9976 | 0.0000 | 0.0022 | 0.0002 | 32442 | Platform Hermosa |
| `55159_06B8DF_48C3_vh_c5981_r7943_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9968 | 0.0000 | 0.0029 | 0.0003 | 12894 | Platform Heritage |
| `55159_06B8DF_48C3_vh_c9565_r7943_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9284 | 0.0000 | 0.0671 | 0.0045 | 7491 | Platform Holly |
| `55159_06B8DF_48C3_vv_c7773_r7943_det0000` | 2024-08-11 | CLEAR | CLEAR | 0.2788 | 0.7125 | 0.0086 | 0.0000 | 281 | Platform Hondo |
| `55159_06B8DF_48C3_vh_c9565_r7943_det0001` | 2024-08-11 | DARK | DARK | 0.2042 | 0.0000 | 0.7631 | 0.0326 | 8681 | — |
| `55159_06B8DF_48C3_vh_c4189_r8839_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9900 | 0.0000 | 0.0092 | 0.0008 | 15525 | — |
| `55159_06B8DF_48C3_vh_c2397_r9735_det0002` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9889 | 0.0000 | 0.0102 | 0.0009 | 35583 | Platform Harvest |
| `55159_06B8DF_48C3_vh_c6877_r7943_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9796 | 0.0000 | 0.0189 | 0.0015 | 4799 | Platform Harmony |
| `5159_06B8DF_48C3_vh_c2397_r11527_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9688 | 0.0000 | 0.0289 | 0.0022 | 43038 | Platform Irene |
| `55159_06B8DF_48C3_vh_c5981_r8839_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9699 | 0.0000 | 0.0296 | 0.0005 | 2847 | — |
| `55159_06B8DF_48C3_vh_c6877_r8839_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9268 | 0.0000 | 0.0687 | 0.0045 | 10228 | — |
| `55159_06B8DF_48C3_vh_c5085_r8839_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9002 | 0.0000 | 0.0939 | 0.0059 | 12420 | — |
| `55159_06B8DF_48C3_vh_c3293_r9735_det0001` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9667 | 0.0000 | 0.0309 | 0.0023 | 32432 | Platform Hermosa |
| `55159_06B8DF_48C3_vh_c4189_r8839_det0001` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9695 | 0.0000 | 0.0283 | 0.0022 | 15903 | — |
| `55159_06B8DF_48C3_vv_c9565_r7943_det0002` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9376 | 0.0000 | 0.0624 | 0.0000 | 995 | — |
| `55159_06B8DF_48C3_vv_c8669_r8839_det0000` | 2024-08-11 | UNKNOWN | DARK | 0.3186 | 0.0000 | 0.6540 | 0.0274 | 12737 | — |
| `55159_06B8DF_48C3_vh_c4189_r9735_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9676 | 0.0000 | 0.0301 | 0.0023 | 15537 | — |
| `55159_06B8DF_48C3_vh_c8669_r7943_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.9674 | 0.0000 | 0.0303 | 0.0023 | 10590 | — |
| `55159_06B8DF_48C3_vh_c9565_r7047_det0000` | 2024-08-11 | UNKNOWN | REVIEW | 0.4693 | 0.0000 | 0.5090 | 0.0217 | 6644 | — |
| `232_06BB8A_EEBC_vv_c21028_r14228_det0000` | 2024-08-16 | ARTIFACT | REVIEW | 0.3298 | 0.0000 | 0.5855 | 0.0847 | 45282 | — |
| `232_06BB8A_EEBC_vv_c21028_r14228_det0001` | 2024-08-16 | ARTIFACT | REVIEW | 0.3332 | 0.0000 | 0.5826 | 0.0842 | 45613 | — |
| `232_06BB8A_EEBC_vv_c21028_r14228_det0003` | 2024-08-16 | ARTIFACT | REVIEW | 0.3435 | 0.0000 | 0.5737 | 0.0828 | 45401 | — |
| `232_06BB8A_EEBC_vv_c21028_r14228_det0005` | 2024-08-16 | ARTIFACT | REVIEW | 0.3519 | 0.0000 | 0.5666 | 0.0816 | 45523 | — |
| `232_06BB8A_EEBC_vv_c21028_r14228_det0006` | 2024-08-16 | ARTIFACT | REVIEW | 0.3545 | 0.0000 | 0.5643 | 0.0812 | 45453 | — |
| `232_06BB8A_EEBC_vv_c21028_r14228_det0009` | 2024-08-16 | ARTIFACT | REVIEW | 0.3606 | 0.0000 | 0.5590 | 0.0804 | 45720 | — |
| `407_06C206_BADB_vv_c21042_r14225_det0000` | 2024-08-28 | ARTIFACT | DARK | 0.2055 | 0.0000 | 0.6921 | 0.1024 | 35739 | — |
| `5407_06C206_BADB_vh_c20146_r9745_det0000` | 2024-08-28 | CLEAR | CLEAR | 0.1880 | 0.7271 | 0.0848 | 0.0000 | 476 | — |
| `407_06C206_BADB_vv_c21042_r14225_det0001` | 2024-08-28 | ARTIFACT | DARK | 0.2227 | 0.0000 | 0.6774 | 0.1000 | 35580 | — |
| `407_06C206_BADB_vv_c21042_r14225_det0002` | 2024-08-28 | ARTIFACT | DARK | 0.2477 | 0.0000 | 0.6559 | 0.0964 | 35719 | — |
| `407_06C206_BADB_vv_c21042_r14225_det0005` | 2024-08-28 | ARTIFACT | DARK | 0.2704 | 0.0000 | 0.6365 | 0.0932 | 35484 | — |
| `407_06C206_BADB_vv_c21042_r14225_det0006` | 2024-08-28 | ARTIFACT | DARK | 0.2958 | 0.0000 | 0.6146 | 0.0896 | 35621 | — |
| `5407_06C206_BADB_vh_c20146_r9745_det0001` | 2024-08-28 | CLEAR | CLEAR | 0.2794 | 0.6484 | 0.0723 | 0.0000 | 305 | — |
| `407_06C206_BADB_vv_c21042_r14225_det0009` | 2024-08-28 | ARTIFACT | REVIEW | 0.3465 | 0.0000 | 0.5711 | 0.0824 | 35537 | — |
| `407_06C206_BADB_vv_c21042_r14225_det0010` | 2024-08-28 | ARTIFACT | REVIEW | 0.3471 | 0.0000 | 0.5706 | 0.0823 | 35729 | — |
| `407_06C206_BADB_vv_c21042_r14225_det0014` | 2024-08-28 | ARTIFACT | ARTIFACT | 0.7307 | 0.0000 | 0.2381 | 0.0312 | 35646 | — |
| `407_06C206_BADB_vv_c21042_r14225_det0017` | 2024-08-28 | ARTIFACT | REVIEW | 0.3597 | 0.0000 | 0.5598 | 0.0805 | 35530 | — |
| `407_06C206_BADB_vv_c21042_r14225_det0018` | 2024-08-28 | ARTIFACT | REVIEW | 0.3601 | 0.0000 | 0.5594 | 0.0805 | 35505 | — |

---

*Generated by `scripts/evaluate_calibration.py`.*
