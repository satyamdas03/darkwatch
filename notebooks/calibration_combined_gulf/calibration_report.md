# Darkwatch Calibration Report

**Generated:** 2026-08-11T01:47:25.670223Z
**Labeled contacts:** 58
**Label source:** `data\processed\calibration_labels_v4_adaptive_gulf_reviewed.json`

---

## 1. Label Counts

- **ARTIFACT:** 13
- **CLEAR:** 3
- **DARK:** 42

---

## 2. Per-Class Calibration

### DARK

- Labeled positives: 42
- Mean predicted p_dark: 0.5927
- Brier score: 0.1631

| Predicted probability bin | Count | Observed DARK fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 4 | 0.000 | 0.092 |
| 0.40 – 0.60 | 17 | 0.471 | 0.575 |
| 0.60 – 0.80 | 37 | 0.919 | 0.655 |

### CLEAR

- Labeled positives: 3
- Mean predicted p_clear: 0.0364
- Brier score: 0.0045

| Predicted probability bin | Count | Observed CLEAR fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 55 | 0.000 | 0.000 |
| 0.60 – 0.80 | 3 | 1.000 | 0.705 |

### ARTIFACT

- Labeled positives: 13
- Mean predicted p_artifact: 0.2848
- Brier score: 0.1450

| Predicted probability bin | Count | Observed ARTIFACT fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 2 | 0.000 | 0.190 |
| 0.20 – 0.40 | 55 | 0.218 | 0.278 |
| 0.80 – 1.00 | 1 | 1.000 | 0.856 |

---

## 3. Verdict-vs-Label Confusion

| Verdict | Labels | Count |
|---|---|---|
| ARTIFACT | ARTIFACT | 1 |
| CLEAR | CLEAR | 3 |
| DARK | ARTIFACT | 3 |
| DARK | DARK | 34 |
| REVIEW | ARTIFACT | 9 |
| REVIEW | DARK | 8 |

---

## 4. Key Findings

- A well-calibrated model has Brier scores near 0 and reliability points hugging the diagonal.
- With only 58 labeled contacts, these metrics are noisy; collecting more scenes is the top priority.
- The current model tends to assign moderate `p_dark` and `p_artifact` to platform-adjacent contacts; strong ARTIFACT labels (near platforms) help validate whether those probabilities are too low or too high.

---

## 5. Per-Contact Detail

| Contact | Scene | True label | Verdict | p_artifact | p_clear | p_dark | p_review | Nearest AIS (m) | Static object |
|---|---|---|---|---|---|---|---|---|---|
| `4662_06A78F_F3B2_vh_c12978_r4767_det0000` | 2024-07-08-gulf | CLEAR | CLEAR | 0.1909 | 0.7258 | 0.0833 | 0.0000 | 76 | — |
| `4662_06A78F_F3B2_vh_c12978_r7455_det0000` | 2024-07-08-gulf | DARK | DARK | 0.1895 | 0.0000 | 0.7058 | 0.1046 | 12138 | — |
| `54662_06A78F_F3B2_vh_c8498_r4767_det0000` | 2024-07-08-gulf | DARK | DARK | 0.2011 | 0.0000 | 0.6959 | 0.1030 | 11118 | — |
| `54662_06A78F_F3B2_vh_c8498_r2975_det0000` | 2024-07-08-gulf | CLEAR | CLEAR | 0.2095 | 0.7098 | 0.0807 | 0.0000 | 65 | — |
| `4662_06A78F_F3B2_vh_c10290_r4767_det0000` | 2024-07-08-gulf | DARK | DARK | 0.2139 | 0.0000 | 0.6850 | 0.1012 | 19153 | — |
| `54662_06A78F_F3B2_vh_c9394_r2079_det0000` | 2024-07-08-gulf | DARK | DARK | 0.2143 | 0.0000 | 0.6846 | 0.1012 | 10674 | — |
| `4662_06A78F_F3B2_vh_c10290_r6559_det0000` | 2024-07-08-gulf | DARK | DARK | 0.2143 | 0.0000 | 0.6846 | 0.1012 | 9002 | — |
| `4662_06A78F_F3B2_vh_c12082_r7455_det0001` | 2024-07-08-gulf | DARK | DARK | 0.2171 | 0.0000 | 0.6822 | 0.1007 | 12443 | — |
| `054662_06A78F_F3B2_vh_c4914_r287_det0000` | 2024-07-08-gulf | DARK | DARK | 0.2182 | 0.0000 | 0.6812 | 0.1006 | 49491 | — |
| `4662_06A78F_F3B2_vh_c11186_r6559_det0000` | 2024-07-08-gulf | DARK | DARK | 0.2222 | 0.0000 | 0.6778 | 0.1000 | 5187 | — |
| `4662_06A78F_F3B2_vh_c11186_r7455_det0000` | 2024-07-08-gulf | DARK | DARK | 0.2233 | 0.0000 | 0.6768 | 0.0999 | 7822 | — |
| `54662_06A78F_F3B2_vh_c6706_r6559_det0000` | 2024-07-08-gulf | DARK | DARK | 0.2235 | 0.0000 | 0.6766 | 0.0998 | 35987 | — |
| `54662_06A78F_F3B2_vh_c6706_r2079_det0000` | 2024-07-08-gulf | DARK | DARK | 0.2297 | 0.0000 | 0.6714 | 0.0989 | 23649 | — |
| `4662_06A78F_F3B2_vh_c11186_r4767_det0000` | 2024-07-08-gulf | DARK | DARK | 0.2305 | 0.0000 | 0.6706 | 0.0988 | 16604 | — |
| `54662_06A78F_F3B2_vh_c4914_r1183_det0000` | 2024-07-08-gulf | DARK | DARK | 0.2317 | 0.0000 | 0.6696 | 0.0987 | 41219 | — |
| `54662_06A78F_F3B2_vh_c4914_r3871_det0000` | 2024-07-08-gulf | ARTIFACT | DARK | 0.2651 | 0.0000 | 0.6410 | 0.0939 | 40798 | — |
| `4662_06A78F_F3B2_vh_c11186_r5663_det0000` | 2024-07-08-gulf | DARK | DARK | 0.2337 | 0.0000 | 0.6679 | 0.0984 | 9633 | — |
| `4662_06A78F_F3B2_vh_c12082_r7455_det0002` | 2024-07-08-gulf | DARK | DARK | 0.2378 | 0.0000 | 0.6644 | 0.0978 | 10215 | — |
| `4662_06A78F_F3B2_vh_c10290_r6559_det0001` | 2024-07-08-gulf | DARK | DARK | 0.2378 | 0.0000 | 0.6644 | 0.0978 | 8888 | — |
| `4662_06A78F_F3B2_vh_c12978_r6559_det0000` | 2024-07-08-gulf | DARK | DARK | 0.2380 | 0.0000 | 0.6642 | 0.0978 | 15244 | — |
| `4662_06A78F_F3B2_vh_c12978_r2079_det0000` | 2024-07-08-gulf | DARK | DARK | 0.2398 | 0.0000 | 0.6627 | 0.0975 | 31403 | — |
| `4662_06A78F_F3B2_vh_c10290_r4767_det0001` | 2024-07-08-gulf | DARK | DARK | 0.2420 | 0.0000 | 0.6608 | 0.0972 | 17912 | — |
| `54662_06A78F_F3B2_vh_c5810_r5663_det0000` | 2024-07-08-gulf | DARK | DARK | 0.2423 | 0.0000 | 0.6606 | 0.0972 | 38940 | — |
| `54662_06A78F_F3B2_vh_c7602_r2079_det0000` | 2024-07-08-gulf | DARK | DARK | 0.2473 | 0.0000 | 0.6562 | 0.0965 | 20519 | — |
| `4662_06A78F_F3B2_vh_c12978_r7455_det0002` | 2024-07-08-gulf | DARK | DARK | 0.2501 | 0.0000 | 0.6538 | 0.0961 | 21018 | — |
| `054662_06A78F_F3B2_vh_c7602_r287_det0000` | 2024-07-08-gulf | DARK | DARK | 0.2531 | 0.0000 | 0.6512 | 0.0956 | 32884 | — |
| `54662_06A78F_F3B2_vh_c5810_r5663_det0001` | 2024-07-08-gulf | DARK | DARK | 0.2564 | 0.0000 | 0.6485 | 0.0952 | 39416 | — |
| `054662_06A78F_F3B2_vh_c4914_r287_det0001` | 2024-07-08-gulf | DARK | DARK | 0.2568 | 0.0000 | 0.6481 | 0.0951 | 46140 | — |
| `4662_06A78F_F3B2_vh_c12978_r6559_det0001` | 2024-07-08-gulf | DARK | DARK | 0.2627 | 0.0000 | 0.6430 | 0.0943 | 14032 | — |
| `4662_06A78F_F3B2_vh_c12082_r3871_det0000` | 2024-07-08-gulf | DARK | DARK | 0.2631 | 0.0000 | 0.6427 | 0.0942 | 14873 | — |
| `54662_06A78F_F3B2_vh_c5810_r2975_det0000` | 2024-07-08-gulf | DARK | DARK | 0.2723 | 0.0000 | 0.6347 | 0.0929 | 31840 | — |
| `54662_06A78F_F3B2_vh_c8498_r6559_det0000` | 2024-07-08-gulf | DARK | DARK | 0.2769 | 0.0000 | 0.6308 | 0.0923 | 31570 | — |
| `054662_06A78F_F3B2_vh_c6706_r287_det0000` | 2024-07-08-gulf | ARTIFACT | DARK | 0.2782 | 0.0000 | 0.6297 | 0.0921 | 36614 | — |
| `4662_06A78F_F3B2_vh_c11186_r6559_det0001` | 2024-07-08-gulf | CLEAR | CLEAR | 0.2445 | 0.6781 | 0.0774 | 0.0000 | 174 | — |
| `54662_06A78F_F3B2_vh_c5810_r5663_det0002` | 2024-07-08-gulf | DARK | DARK | 0.2905 | 0.0000 | 0.6192 | 0.0903 | 41228 | — |
| `54662_06A78F_F3B2_vh_c6706_r5663_det0000` | 2024-07-08-gulf | DARK | DARK | 0.3001 | 0.0000 | 0.6110 | 0.0889 | 32728 | — |
| `54662_06A78F_F3B2_vh_c6706_r7455_det0000` | 2024-07-08-gulf | DARK | DARK | 0.3011 | 0.0000 | 0.6101 | 0.0888 | 50552 | — |
| `54662_06A78F_F3B2_vh_c5810_r6559_det0000` | 2024-07-08-gulf | DARK | DARK | 0.3015 | 0.0000 | 0.6097 | 0.0887 | 42103 | — |
| `54662_06A78F_F3B2_vh_c4914_r3871_det0001` | 2024-07-08-gulf | ARTIFACT | DARK | 0.3090 | 0.0000 | 0.6034 | 0.0877 | 44584 | — |
| `4662_06A78F_F3B2_vh_c12082_r5663_det0000` | 2024-07-08-gulf | DARK | DARK | 0.3116 | 0.0000 | 0.6011 | 0.0873 | 8237 | — |
| `54662_06A78F_F3B2_vh_c6706_r2975_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.3145 | 0.0000 | 0.5986 | 0.0869 | 20535 | — |
| `54662_06A78F_F3B2_vh_c8498_r5663_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.3157 | 0.0000 | 0.5976 | 0.0867 | 24942 | — |
| `54662_06A78F_F3B2_vh_c5810_r6559_det0001` | 2024-07-08-gulf | DARK | REVIEW | 0.3228 | 0.0000 | 0.5914 | 0.0857 | 44500 | — |
| `54662_06A78F_F3B2_vh_c5810_r5663_det0003` | 2024-07-08-gulf | DARK | REVIEW | 0.3258 | 0.0000 | 0.5889 | 0.0853 | 38598 | — |
| `54662_06A78F_F3B2_vh_c5810_r6559_det0002` | 2024-07-08-gulf | DARK | REVIEW | 0.3299 | 0.0000 | 0.5854 | 0.0847 | 44499 | — |
| `54662_06A78F_F3B2_vh_c6706_r2975_det0001` | 2024-07-08-gulf | DARK | REVIEW | 0.3299 | 0.0000 | 0.5854 | 0.0847 | 25059 | — |
| `4662_06A78F_F3B2_vh_c10290_r7455_det0002` | 2024-07-08-gulf | ARTIFACT | REVIEW | 0.3343 | 0.0000 | 0.5816 | 0.0841 | 13170 | — |
| `54662_06A78F_F3B2_vh_c5810_r6559_det0003` | 2024-07-08-gulf | DARK | REVIEW | 0.3428 | 0.0000 | 0.5743 | 0.0829 | 42546 | — |
| `54662_06A78F_F3B2_vh_c4914_r6559_det0000` | 2024-07-08-gulf | ARTIFACT | REVIEW | 0.3459 | 0.0000 | 0.5717 | 0.0824 | 50508 | — |
| `054662_06A78F_F3B2_vh_c4914_r287_det0002` | 2024-07-08-gulf | ARTIFACT | REVIEW | 0.3506 | 0.0000 | 0.5676 | 0.0818 | 47515 | — |
| `54662_06A78F_F3B2_vh_c4914_r5663_det0000` | 2024-07-08-gulf | ARTIFACT | ARTIFACT | 0.8559 | 0.0000 | 0.1283 | 0.0158 | 50957 | — |
| `4662_06A78F_F3B2_vh_c11186_r5663_det0001` | 2024-07-08-gulf | ARTIFACT | REVIEW | 0.3568 | 0.0000 | 0.5623 | 0.0809 | 5351 | — |
| `4662_06A78F_F3B2_vh_c12082_r6559_det0001` | 2024-07-08-gulf | ARTIFACT | REVIEW | 0.3568 | 0.0000 | 0.5623 | 0.0809 | 12004 | — |
| `4662_06A78F_F3B2_vh_c10290_r3871_det0000` | 2024-07-08-gulf | ARTIFACT | REVIEW | 0.3586 | 0.0000 | 0.5607 | 0.0807 | 15716 | — |
| `4662_06A78F_F3B2_vh_c11186_r7455_det0001` | 2024-07-08-gulf | ARTIFACT | REVIEW | 0.3588 | 0.0000 | 0.5606 | 0.0806 | 11046 | — |
| `54662_06A78F_F3B2_vh_c6706_r1183_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.3597 | 0.0000 | 0.5598 | 0.0805 | 30610 | — |
| `4662_06A78F_F3B2_vh_c11186_r3871_det0000` | 2024-07-08-gulf | ARTIFACT | REVIEW | 0.3600 | 0.0000 | 0.5595 | 0.0805 | 16669 | — |
| `4662_06A78F_F3B2_vh_c12978_r7455_det0003` | 2024-07-08-gulf | ARTIFACT | REVIEW | 0.3603 | 0.0000 | 0.5593 | 0.0804 | 14688 | — |

---

*Generated by `scripts/evaluate_calibration.py`.*
