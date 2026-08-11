# Darkwatch Calibration Report

**Generated:** 2026-08-11T01:46:22.138725Z
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
- Mean predicted p_dark: 0.6523
- Brier score: 0.1606

| Predicted probability bin | Count | Observed DARK fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 2 | 0.000 | 0.197 |
| 0.20 – 0.40 | 2 | 0.000 | 0.216 |
| 0.60 – 0.80 | 54 | 0.778 | 0.685 |

### CLEAR

- Labeled positives: 3
- Mean predicted p_clear: 0.0380
- Brier score: 0.0036

| Predicted probability bin | Count | Observed CLEAR fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 55 | 0.000 | 0.000 |
| 0.60 – 0.80 | 3 | 1.000 | 0.735 |

### ARTIFACT

- Labeled positives: 13
- Mean predicted p_artifact: 0.0956
- Brier score: 0.1653

| Predicted probability bin | Count | Observed ARTIFACT fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 57 | 0.211 | 0.085 |
| 0.60 – 0.80 | 1 | 1.000 | 0.692 |

---

## 3. Verdict-vs-Label Confusion

| Verdict | Labels | Count |
|---|---|---|
| ARTIFACT | ARTIFACT | 1 |
| CLEAR | CLEAR | 3 |
| DARK | ARTIFACT | 12 |
| DARK | DARK | 42 |

---

## 4. Key Findings

- A well-calibrated model has Brier scores near 0 and reliability points hugging the diagonal.
- With only 58 labeled contacts, these metrics are noisy; collecting more scenes is the top priority.
- The current model tends to assign moderate `p_dark` and `p_artifact` to platform-adjacent contacts; strong ARTIFACT labels (near platforms) help validate whether those probabilities are too low or too high.

---

## 5. Per-Contact Detail

| Contact | Scene | True label | Verdict | p_artifact | p_clear | p_dark | p_review | Nearest AIS (m) | Static object |
|---|---|---|---|---|---|---|---|---|---|
| `4662_06A78F_F3B2_vh_c12978_r4767_det0000` | 2024-07-08-gulf | CLEAR | CLEAR | 0.0513 | 0.7477 | 0.2010 | 0.0000 | 76 | — |
| `4662_06A78F_F3B2_vh_c12978_r7455_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0381 | 0.0000 | 0.7215 | 0.2405 | 12138 | — |
| `54662_06A78F_F3B2_vh_c8498_r4767_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0428 | 0.0000 | 0.7179 | 0.2393 | 11118 | — |
| `54662_06A78F_F3B2_vh_c8498_r2975_det0000` | 2024-07-08-gulf | CLEAR | CLEAR | 0.0622 | 0.7394 | 0.1984 | 0.0000 | 65 | — |
| `4662_06A78F_F3B2_vh_c10290_r4767_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0484 | 0.0000 | 0.7137 | 0.2379 | 19153 | — |
| `54662_06A78F_F3B2_vh_c9394_r2079_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0486 | 0.0000 | 0.7136 | 0.2379 | 10674 | — |
| `4662_06A78F_F3B2_vh_c10290_r6559_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0486 | 0.0000 | 0.7136 | 0.2379 | 9002 | — |
| `4662_06A78F_F3B2_vh_c12082_r7455_det0001` | 2024-07-08-gulf | DARK | DARK | 0.0499 | 0.0000 | 0.7126 | 0.2375 | 12443 | — |
| `054662_06A78F_F3B2_vh_c4914_r287_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0504 | 0.0000 | 0.7122 | 0.2374 | 49491 | — |
| `4662_06A78F_F3B2_vh_c11186_r6559_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0523 | 0.0000 | 0.7108 | 0.2369 | 5187 | — |
| `4662_06A78F_F3B2_vh_c11186_r7455_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0528 | 0.0000 | 0.7104 | 0.2368 | 7822 | — |
| `54662_06A78F_F3B2_vh_c6706_r6559_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0529 | 0.0000 | 0.7103 | 0.2368 | 35987 | — |
| `54662_06A78F_F3B2_vh_c6706_r2079_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0559 | 0.0000 | 0.7081 | 0.2360 | 23649 | — |
| `4662_06A78F_F3B2_vh_c11186_r4767_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0563 | 0.0000 | 0.7077 | 0.2359 | 16604 | — |
| `54662_06A78F_F3B2_vh_c4914_r1183_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0569 | 0.0000 | 0.7073 | 0.2358 | 41219 | — |
| `54662_06A78F_F3B2_vh_c4914_r3871_det0000` | 2024-07-08-gulf | ARTIFACT | DARK | 0.0750 | 0.0000 | 0.6938 | 0.2313 | 40798 | — |
| `4662_06A78F_F3B2_vh_c11186_r5663_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0579 | 0.0000 | 0.7066 | 0.2355 | 9633 | — |
| `4662_06A78F_F3B2_vh_c12082_r7455_det0002` | 2024-07-08-gulf | DARK | DARK | 0.0600 | 0.0000 | 0.7050 | 0.2350 | 10215 | — |
| `4662_06A78F_F3B2_vh_c10290_r6559_det0001` | 2024-07-08-gulf | DARK | DARK | 0.0600 | 0.0000 | 0.7050 | 0.2350 | 8888 | — |
| `4662_06A78F_F3B2_vh_c12978_r6559_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0601 | 0.0000 | 0.7049 | 0.2350 | 15244 | — |
| `4662_06A78F_F3B2_vh_c12978_r2079_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0610 | 0.0000 | 0.7042 | 0.2347 | 31403 | — |
| `4662_06A78F_F3B2_vh_c10290_r4767_det0001` | 2024-07-08-gulf | DARK | DARK | 0.0622 | 0.0000 | 0.7034 | 0.2345 | 17912 | — |
| `54662_06A78F_F3B2_vh_c5810_r5663_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0623 | 0.0000 | 0.7032 | 0.2344 | 38940 | — |
| `54662_06A78F_F3B2_vh_c7602_r2079_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0650 | 0.0000 | 0.7013 | 0.2338 | 20519 | — |
| `4662_06A78F_F3B2_vh_c12978_r7455_det0002` | 2024-07-08-gulf | DARK | DARK | 0.0665 | 0.0000 | 0.7001 | 0.2334 | 21018 | — |
| `054662_06A78F_F3B2_vh_c7602_r287_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0682 | 0.0000 | 0.6989 | 0.2330 | 32884 | — |
| `54662_06A78F_F3B2_vh_c5810_r5663_det0001` | 2024-07-08-gulf | DARK | DARK | 0.0700 | 0.0000 | 0.6975 | 0.2325 | 39416 | — |
| `054662_06A78F_F3B2_vh_c4914_r287_det0001` | 2024-07-08-gulf | DARK | DARK | 0.0702 | 0.0000 | 0.6973 | 0.2324 | 46140 | — |
| `4662_06A78F_F3B2_vh_c12978_r6559_det0001` | 2024-07-08-gulf | DARK | DARK | 0.0736 | 0.0000 | 0.6948 | 0.2316 | 14032 | — |
| `4662_06A78F_F3B2_vh_c12082_r3871_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0738 | 0.0000 | 0.6946 | 0.2315 | 14873 | — |
| `54662_06A78F_F3B2_vh_c5810_r2975_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0793 | 0.0000 | 0.6905 | 0.2302 | 31840 | — |
| `54662_06A78F_F3B2_vh_c8498_r6559_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0821 | 0.0000 | 0.6884 | 0.2295 | 31570 | — |
| `054662_06A78F_F3B2_vh_c6706_r287_det0000` | 2024-07-08-gulf | ARTIFACT | DARK | 0.0829 | 0.0000 | 0.6878 | 0.2293 | 36614 | — |
| `4662_06A78F_F3B2_vh_c11186_r6559_det0001` | 2024-07-08-gulf | CLEAR | CLEAR | 0.0863 | 0.7184 | 0.1953 | 0.0000 | 174 | — |
| `54662_06A78F_F3B2_vh_c5810_r5663_det0002` | 2024-07-08-gulf | DARK | DARK | 0.0907 | 0.0000 | 0.6820 | 0.2273 | 41228 | — |
| `54662_06A78F_F3B2_vh_c6706_r5663_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0970 | 0.0000 | 0.6772 | 0.2257 | 32728 | — |
| `54662_06A78F_F3B2_vh_c6706_r7455_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0977 | 0.0000 | 0.6767 | 0.2256 | 50552 | — |
| `54662_06A78F_F3B2_vh_c5810_r6559_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0980 | 0.0000 | 0.6765 | 0.2255 | 42103 | — |
| `54662_06A78F_F3B2_vh_c4914_r3871_det0001` | 2024-07-08-gulf | ARTIFACT | DARK | 0.1031 | 0.0000 | 0.6727 | 0.2242 | 44584 | — |
| `4662_06A78F_F3B2_vh_c12082_r5663_det0000` | 2024-07-08-gulf | DARK | DARK | 0.1049 | 0.0000 | 0.6713 | 0.2238 | 8237 | — |
| `54662_06A78F_F3B2_vh_c6706_r2975_det0000` | 2024-07-08-gulf | DARK | DARK | 0.1070 | 0.0000 | 0.6698 | 0.2233 | 20535 | — |
| `54662_06A78F_F3B2_vh_c8498_r5663_det0000` | 2024-07-08-gulf | DARK | DARK | 0.1078 | 0.0000 | 0.6691 | 0.2230 | 24942 | — |
| `54662_06A78F_F3B2_vh_c5810_r6559_det0001` | 2024-07-08-gulf | DARK | DARK | 0.1130 | 0.0000 | 0.6653 | 0.2218 | 44500 | — |
| `54662_06A78F_F3B2_vh_c5810_r5663_det0003` | 2024-07-08-gulf | DARK | DARK | 0.1151 | 0.0000 | 0.6636 | 0.2212 | 38598 | — |
| `54662_06A78F_F3B2_vh_c5810_r6559_det0002` | 2024-07-08-gulf | DARK | DARK | 0.1182 | 0.0000 | 0.6614 | 0.2205 | 44499 | — |
| `54662_06A78F_F3B2_vh_c6706_r2975_det0001` | 2024-07-08-gulf | DARK | DARK | 0.1182 | 0.0000 | 0.6614 | 0.2205 | 25059 | — |
| `4662_06A78F_F3B2_vh_c10290_r7455_det0002` | 2024-07-08-gulf | ARTIFACT | DARK | 0.1215 | 0.0000 | 0.6589 | 0.2196 | 13170 | — |
| `54662_06A78F_F3B2_vh_c5810_r6559_det0003` | 2024-07-08-gulf | DARK | DARK | 0.1280 | 0.0000 | 0.6540 | 0.2180 | 42546 | — |
| `54662_06A78F_F3B2_vh_c4914_r6559_det0000` | 2024-07-08-gulf | ARTIFACT | DARK | 0.1304 | 0.0000 | 0.6522 | 0.2174 | 50508 | — |
| `054662_06A78F_F3B2_vh_c4914_r287_det0002` | 2024-07-08-gulf | ARTIFACT | DARK | 0.1341 | 0.0000 | 0.6494 | 0.2165 | 47515 | — |
| `54662_06A78F_F3B2_vh_c4914_r5663_det0000` | 2024-07-08-gulf | ARTIFACT | ARTIFACT | 0.6919 | 0.0000 | 0.2311 | 0.0770 | 50957 | — |
| `4662_06A78F_F3B2_vh_c11186_r5663_det0001` | 2024-07-08-gulf | ARTIFACT | DARK | 0.1390 | 0.0000 | 0.6457 | 0.2152 | 5351 | — |
| `4662_06A78F_F3B2_vh_c12082_r6559_det0001` | 2024-07-08-gulf | ARTIFACT | DARK | 0.1390 | 0.0000 | 0.6457 | 0.2152 | 12004 | — |
| `4662_06A78F_F3B2_vh_c10290_r3871_det0000` | 2024-07-08-gulf | ARTIFACT | DARK | 0.1405 | 0.0000 | 0.6446 | 0.2149 | 15716 | — |
| `4662_06A78F_F3B2_vh_c11186_r7455_det0001` | 2024-07-08-gulf | ARTIFACT | DARK | 0.1406 | 0.0000 | 0.6445 | 0.2148 | 11046 | — |
| `54662_06A78F_F3B2_vh_c6706_r1183_det0000` | 2024-07-08-gulf | DARK | DARK | 0.1414 | 0.0000 | 0.6440 | 0.2147 | 30610 | — |
| `4662_06A78F_F3B2_vh_c11186_r3871_det0000` | 2024-07-08-gulf | ARTIFACT | DARK | 0.1417 | 0.0000 | 0.6438 | 0.2146 | 16669 | — |
| `4662_06A78F_F3B2_vh_c12978_r7455_det0003` | 2024-07-08-gulf | ARTIFACT | DARK | 0.1419 | 0.0000 | 0.6436 | 0.2145 | 14688 | — |

---

*Generated by `scripts/evaluate_calibration.py`.*
