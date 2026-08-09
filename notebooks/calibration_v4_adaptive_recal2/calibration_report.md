# Darkwatch Calibration Report

**Generated:** 2026-08-09T01:22:43.295594Z
**Labeled contacts:** 46
**Label source:** `data\processed\calibration_labels_v4_adaptive_recal2.json`

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
- Mean predicted p_dark: 0.3394
- Brier score: 0.0929

| Predicted probability bin | Count | Observed DARK fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 15 | 0.000 | 0.151 |
| 0.20 – 0.40 | 18 | 0.000 | 0.265 |
| 0.40 – 0.60 | 1 | 0.000 | 0.578 |
| 0.60 – 0.80 | 12 | 0.750 | 0.667 |

### CLEAR

- Labeled positives: 7
- Mean predicted p_clear: 0.1168
- Brier score: 0.0259

| Predicted probability bin | Count | Observed CLEAR fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 38 | 0.000 | 0.000 |
| 0.60 – 0.80 | 8 | 0.875 | 0.672 |

### ARTIFACT

- Labeled positives: 27
- Mean predicted p_artifact: 0.4411
- Brier score: 0.0945

| Predicted probability bin | Count | Observed ARTIFACT fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 20 | 0.100 | 0.132 |
| 0.20 – 0.40 | 1 | 0.000 | 0.229 |
| 0.40 – 0.60 | 6 | 1.000 | 0.563 |
| 0.60 – 0.80 | 15 | 1.000 | 0.708 |
| 0.80 – 1.00 | 4 | 1.000 | 0.857 |

---

## 3. Verdict-vs-Label Confusion

| Verdict | Labels | Count |
|---|---|---|
| ARTIFACT | ARTIFACT | 25 |
| CLEAR | ARTIFACT | 1 |
| CLEAR | CLEAR | 7 |
| DARK | ARTIFACT | 1 |
| DARK | DARK | 9 |
| DARK | UNKNOWN | 2 |
| REVIEW | UNKNOWN | 1 |

---

## 4. Key Findings

- A well-calibrated model has Brier scores near 0 and reliability points hugging the diagonal.
- With only 46 labeled contacts, these metrics are noisy; collecting more scenes is the top priority.
- The current model tends to assign moderate `p_dark` and `p_artifact` to platform-adjacent contacts; strong ARTIFACT labels (near platforms) help validate whether those probabilities are too low or too high.

---

## 5. Per-Contact Detail

| Contact | Scene | True label | Verdict | p_artifact | p_clear | p_dark | p_review | Nearest AIS (m) | Static object |
|---|---|---|---|---|---|---|---|---|---|
| `4714_06A94E_9466_vh_c4210_r14398_det0000` | 2024-07-11 | ARTIFACT | ARTIFACT | 0.5273 | 0.0000 | 0.3545 | 0.1182 | 37733 | — |
| `4714_06A94E_9466_vh_c3314_r10814_det0000` | 2024-07-11 | ARTIFACT | ARTIFACT | 0.6815 | 0.0000 | 0.2389 | 0.0796 | 12710 | Platform Irene |
| `54809_06ACA2_D01B_vh_c2380_r8843_det0000` | 2024-07-18 | CLEAR | CLEAR | 0.1178 | 0.7019 | 0.1803 | 0.0000 | 126 | — |
| `54809_06ACA2_D01B_vh_c9548_r7947_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.5795 | 0.0000 | 0.3154 | 0.1051 | 7660 | Platform Holly |
| `54809_06ACA2_D01B_vh_c2380_r9739_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.8084 | 0.0000 | 0.1437 | 0.0479 | 9412 | Platform Harvest |
| `54809_06ACA2_D01B_vv_c9548_r7947_det0000` | 2024-07-18 | UNKNOWN | DARK | 0.0950 | 0.0000 | 0.6787 | 0.2262 | 9076 | — |
| `54809_06ACA2_D01B_vh_c6860_r8843_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.6945 | 0.0000 | 0.2291 | 0.0764 | 10291 | — |
| `54809_06ACA2_D01B_vv_c2380_r9739_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.7378 | 0.0000 | 0.1967 | 0.0656 | 7437 | Platform Hermosa |
| `54809_06ACA2_D01B_vv_c5068_r9739_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.7032 | 0.0000 | 0.2226 | 0.0742 | 8880 | — |
| `54809_06ACA2_D01B_vh_c6860_r7947_det0000` | 2024-07-18 | CLEAR | CLEAR | 0.1802 | 0.6618 | 0.1580 | 0.0000 | 450 | Platform Harmony |
| `54809_06ACA2_D01B_vh_c7756_r7947_det0000` | 2024-07-18 | CLEAR | CLEAR | 0.1580 | 0.6715 | 0.1705 | 0.0000 | 313 | Platform Hondo |
| `54809_06ACA2_D01B_vh_c5964_r8843_det0000` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.6913 | 0.0000 | 0.2316 | 0.0772 | 13843 | — |
| `54809_06ACA2_D01B_vh_c9548_r7947_det0002` | 2024-07-18 | CLEAR | CLEAR | 0.1786 | 0.6641 | 0.1574 | 0.0000 | 1336 | — |
| `54809_06ACA2_D01B_vh_c2380_r9739_det0001` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.6839 | 0.0000 | 0.2371 | 0.0790 | 12831 | Platform Hidalgo |
| `4809_06ACA2_D01B_vv_c10444_r7947_det0000` | 2024-07-18 | CLEAR | CLEAR | 0.1773 | 0.6651 | 0.1576 | 0.0000 | 1498 | — |
| `54809_06ACA2_D01B_vh_c4172_r8843_det0000` | 2024-07-18 | CLEAR | CLEAR | 0.1771 | 0.6652 | 0.1576 | 0.0000 | 1644 | — |
| `54809_06ACA2_D01B_vh_c6860_r8843_det0001` | 2024-07-18 | ARTIFACT | ARTIFACT | 0.5519 | 0.0000 | 0.3361 | 0.1120 | 12536 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0000` | 2024-07-23 | DARK | DARK | 0.0354 | 0.0000 | 0.7234 | 0.2411 | 23994 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0001` | 2024-07-23 | DARK | DARK | 0.0945 | 0.0000 | 0.6791 | 0.2264 | 24023 | — |
| `882_06AF26_69FC_vv_c21010_r14232_det0000` | 2024-07-23 | DARK | DARK | 0.1011 | 0.0000 | 0.6742 | 0.2247 | 23724 | — |
| `882_06AF26_69FC_vv_c21010_r14232_det0001` | 2024-07-23 | DARK | DARK | 0.1165 | 0.0000 | 0.6626 | 0.2209 | 23894 | — |
| `882_06AF26_69FC_vv_c21010_r14232_det0002` | 2024-07-23 | DARK | DARK | 0.1190 | 0.0000 | 0.6607 | 0.2202 | 24165 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0002` | 2024-07-23 | ARTIFACT | DARK | 0.1304 | 0.0000 | 0.6522 | 0.2174 | 23987 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0003` | 2024-07-23 | DARK | DARK | 0.1342 | 0.0000 | 0.6494 | 0.2165 | 23912 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0005` | 2024-07-23 | DARK | DARK | 0.1364 | 0.0000 | 0.6477 | 0.2159 | 23859 | — |
| `882_06AF26_69FC_vh_c21010_r14232_det0009` | 2024-07-23 | DARK | DARK | 0.1394 | 0.0000 | 0.6455 | 0.2152 | 24072 | — |
| `55159_06B8DF_48C3_vh_c2397_r9735_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.8809 | 0.0000 | 0.0893 | 0.0298 | 37668 | Platform Hidalgo |
| `55159_06B8DF_48C3_vh_c2397_r9735_det0001` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.8768 | 0.0000 | 0.0924 | 0.0308 | 32442 | Platform Hermosa |
| `55159_06B8DF_48C3_vh_c5981_r7943_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.8626 | 0.0000 | 0.1031 | 0.0344 | 12894 | Platform Heritage |
| `55159_06B8DF_48C3_vh_c9565_r7943_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.5893 | 0.0000 | 0.3080 | 0.1027 | 7491 | Platform Holly |
| `55159_06B8DF_48C3_vv_c7773_r7943_det0000` | 2024-08-11 | CLEAR | CLEAR | 0.1499 | 0.6793 | 0.1707 | 0.0000 | 281 | Platform Hondo |
| `55159_06B8DF_48C3_vh_c9565_r7943_det0001` | 2024-08-11 | DARK | DARK | 0.0781 | 0.0000 | 0.6914 | 0.2305 | 8681 | — |
| `55159_06B8DF_48C3_vh_c4189_r8839_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.7873 | 0.0000 | 0.1595 | 0.0532 | 15525 | — |
| `55159_06B8DF_48C3_vh_c2397_r9735_det0002` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.7794 | 0.0000 | 0.1655 | 0.0552 | 35583 | Platform Harvest |
| `55159_06B8DF_48C3_vh_c6877_r7943_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.7265 | 0.0000 | 0.2051 | 0.0684 | 4799 | Platform Harmony |
| `5159_06B8DF_48C3_vh_c2397_r11527_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.6846 | 0.0000 | 0.2365 | 0.0788 | 43038 | Platform Irene |
| `55159_06B8DF_48C3_vh_c5981_r8839_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.7178 | 0.0000 | 0.2415 | 0.0407 | 2847 | — |
| `55159_06B8DF_48C3_vh_c6877_r8839_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.5864 | 0.0000 | 0.3102 | 0.1034 | 10228 | — |
| `55159_06B8DF_48C3_vh_c5085_r8839_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.5460 | 0.0000 | 0.3405 | 0.1135 | 12420 | — |
| `55159_06B8DF_48C3_vh_c3293_r9735_det0001` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.6776 | 0.0000 | 0.2418 | 0.0806 | 32432 | Platform Hermosa |
| `55159_06B8DF_48C3_vh_c4189_r8839_det0001` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.6870 | 0.0000 | 0.2348 | 0.0783 | 15903 | — |
| `55159_06B8DF_48C3_vv_c9565_r7943_det0002` | 2024-08-11 | ARTIFACT | CLEAR | 0.1781 | 0.6645 | 0.1575 | 0.0000 | 995 | — |
| `55159_06B8DF_48C3_vv_c8669_r8839_det0000` | 2024-08-11 | UNKNOWN | DARK | 0.1404 | 0.0000 | 0.6447 | 0.2149 | 12737 | — |
| `55159_06B8DF_48C3_vh_c4189_r9735_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.6806 | 0.0000 | 0.2395 | 0.0798 | 15537 | — |
| `55159_06B8DF_48C3_vh_c8669_r7943_det0000` | 2024-08-11 | ARTIFACT | ARTIFACT | 0.6799 | 0.0000 | 0.2401 | 0.0800 | 10590 | — |
| `55159_06B8DF_48C3_vh_c9565_r7047_det0000` | 2024-08-11 | UNKNOWN | REVIEW | 0.2294 | 0.0000 | 0.5780 | 0.1927 | 6644 | — |

---

*Generated by `scripts/evaluate_calibration.py`.*
