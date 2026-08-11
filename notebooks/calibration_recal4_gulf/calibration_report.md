# Darkwatch Calibration Report

**Generated:** 2026-08-11T01:46:07.082537Z
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
- Mean predicted p_dark: 0.4037
- Brier score: 0.2593

| Predicted probability bin | Count | Observed DARK fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 4 | 0.000 | 0.063 |
| 0.20 – 0.40 | 15 | 0.400 | 0.383 |
| 0.40 – 0.60 | 39 | 0.923 | 0.447 |

### CLEAR

- Labeled positives: 3
- Mean predicted p_clear: 0.0331
- Brier score: 0.0067

| Predicted probability bin | Count | Observed CLEAR fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 55 | 0.000 | 0.000 |
| 0.60 – 0.80 | 3 | 1.000 | 0.641 |

### ARTIFACT

- Labeled positives: 13
- Mean predicted p_artifact: 0.4446
- Brier score: 0.1932

| Predicted probability bin | Count | Observed ARTIFACT fraction | Mean predicted |
|---|---|---|---|
| 0.20 – 0.40 | 13 | 0.000 | 0.369 |
| 0.40 – 0.60 | 44 | 0.273 | 0.457 |
| 0.80 – 1.00 | 1 | 1.000 | 0.881 |

---

## 3. Verdict-vs-Label Confusion

| Verdict | Labels | Count |
|---|---|---|
| ARTIFACT | ARTIFACT | 9 |
| ARTIFACT | DARK | 1 |
| CLEAR | CLEAR | 3 |
| REVIEW | ARTIFACT | 4 |
| REVIEW | DARK | 41 |

---

## 4. Key Findings

- A well-calibrated model has Brier scores near 0 and reliability points hugging the diagonal.
- With only 58 labeled contacts, these metrics are noisy; collecting more scenes is the top priority.
- The current model tends to assign moderate `p_dark` and `p_artifact` to platform-adjacent contacts; strong ARTIFACT labels (near platforms) help validate whether those probabilities are too low or too high.

---

## 5. Per-Contact Detail

| Contact | Scene | True label | Verdict | p_artifact | p_clear | p_dark | p_review | Nearest AIS (m) | Static object |
|---|---|---|---|---|---|---|---|---|---|
| `4662_06A78F_F3B2_vh_c12978_r4767_det0000` | 2024-07-08-gulf | CLEAR | CLEAR | 0.2875 | 0.6577 | 0.0548 | 0.0000 | 76 | — |
| `4662_06A78F_F3B2_vh_c12978_r7455_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.3652 | 0.0000 | 0.4919 | 0.1429 | 12138 | — |
| `54662_06A78F_F3B2_vh_c8498_r4767_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.3762 | 0.0000 | 0.4831 | 0.1406 | 11118 | — |
| `54662_06A78F_F3B2_vh_c8498_r2975_det0000` | 2024-07-08-gulf | CLEAR | CLEAR | 0.3020 | 0.6446 | 0.0534 | 0.0000 | 65 | — |
| `4662_06A78F_F3B2_vh_c10290_r4767_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.3881 | 0.0000 | 0.4737 | 0.1382 | 19153 | — |
| `54662_06A78F_F3B2_vh_c9394_r2079_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.3885 | 0.0000 | 0.4733 | 0.1382 | 10674 | — |
| `4662_06A78F_F3B2_vh_c10290_r6559_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.3885 | 0.0000 | 0.4733 | 0.1382 | 9002 | — |
| `4662_06A78F_F3B2_vh_c12082_r7455_det0001` | 2024-07-08-gulf | DARK | REVIEW | 0.3911 | 0.0000 | 0.4713 | 0.1376 | 12443 | — |
| `054662_06A78F_F3B2_vh_c4914_r287_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.3921 | 0.0000 | 0.4705 | 0.1374 | 49491 | — |
| `4662_06A78F_F3B2_vh_c11186_r6559_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.3958 | 0.0000 | 0.4676 | 0.1366 | 5187 | — |
| `4662_06A78F_F3B2_vh_c11186_r7455_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.3968 | 0.0000 | 0.4668 | 0.1365 | 7822 | — |
| `54662_06A78F_F3B2_vh_c6706_r6559_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.3970 | 0.0000 | 0.4666 | 0.1364 | 35987 | — |
| `54662_06A78F_F3B2_vh_c6706_r2079_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.4025 | 0.0000 | 0.4622 | 0.1353 | 23649 | — |
| `4662_06A78F_F3B2_vh_c11186_r4767_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.4033 | 0.0000 | 0.4615 | 0.1351 | 16604 | — |
| `54662_06A78F_F3B2_vh_c4914_r1183_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.4044 | 0.0000 | 0.4607 | 0.1349 | 41219 | — |
| `54662_06A78F_F3B2_vh_c4914_r3871_det0000` | 2024-07-08-gulf | ARTIFACT | REVIEW | 0.4338 | 0.0000 | 0.4372 | 0.1290 | 40798 | — |
| `4662_06A78F_F3B2_vh_c11186_r5663_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.4061 | 0.0000 | 0.4593 | 0.1345 | 9633 | — |
| `4662_06A78F_F3B2_vh_c12082_r7455_det0002` | 2024-07-08-gulf | DARK | REVIEW | 0.4098 | 0.0000 | 0.4564 | 0.1338 | 10215 | — |
| `4662_06A78F_F3B2_vh_c10290_r6559_det0001` | 2024-07-08-gulf | DARK | REVIEW | 0.4098 | 0.0000 | 0.4564 | 0.1338 | 8888 | — |
| `4662_06A78F_F3B2_vh_c12978_r6559_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.4100 | 0.0000 | 0.4562 | 0.1338 | 15244 | — |
| `4662_06A78F_F3B2_vh_c12978_r2079_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.4116 | 0.0000 | 0.4550 | 0.1334 | 31403 | — |
| `4662_06A78F_F3B2_vh_c10290_r4767_det0001` | 2024-07-08-gulf | DARK | REVIEW | 0.4136 | 0.0000 | 0.4534 | 0.1331 | 17912 | — |
| `54662_06A78F_F3B2_vh_c5810_r5663_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.4138 | 0.0000 | 0.4532 | 0.1330 | 38940 | — |
| `54662_06A78F_F3B2_vh_c7602_r2079_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.4182 | 0.0000 | 0.4497 | 0.1321 | 20519 | — |
| `4662_06A78F_F3B2_vh_c12978_r7455_det0002` | 2024-07-08-gulf | DARK | REVIEW | 0.4207 | 0.0000 | 0.4477 | 0.1316 | 21018 | — |
| `054662_06A78F_F3B2_vh_c7602_r287_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.4234 | 0.0000 | 0.4455 | 0.1311 | 32884 | — |
| `54662_06A78F_F3B2_vh_c5810_r5663_det0001` | 2024-07-08-gulf | DARK | REVIEW | 0.4262 | 0.0000 | 0.4433 | 0.1305 | 39416 | — |
| `054662_06A78F_F3B2_vh_c4914_r287_det0001` | 2024-07-08-gulf | DARK | REVIEW | 0.4266 | 0.0000 | 0.4430 | 0.1304 | 46140 | — |
| `4662_06A78F_F3B2_vh_c12978_r6559_det0001` | 2024-07-08-gulf | DARK | REVIEW | 0.4317 | 0.0000 | 0.4389 | 0.1294 | 14032 | — |
| `4662_06A78F_F3B2_vh_c12082_r3871_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.4321 | 0.0000 | 0.4386 | 0.1293 | 14873 | — |
| `54662_06A78F_F3B2_vh_c5810_r2975_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.4401 | 0.0000 | 0.4322 | 0.1277 | 31840 | — |
| `54662_06A78F_F3B2_vh_c8498_r6559_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.4440 | 0.0000 | 0.4290 | 0.1269 | 31570 | — |
| `054662_06A78F_F3B2_vh_c6706_r287_det0000` | 2024-07-08-gulf | ARTIFACT | REVIEW | 0.4451 | 0.0000 | 0.4282 | 0.1267 | 36614 | — |
| `4662_06A78F_F3B2_vh_c11186_r6559_det0001` | 2024-07-08-gulf | CLEAR | CLEAR | 0.3287 | 0.6196 | 0.0517 | 0.0000 | 174 | — |
| `54662_06A78F_F3B2_vh_c5810_r5663_det0002` | 2024-07-08-gulf | DARK | REVIEW | 0.4556 | 0.0000 | 0.4198 | 0.1245 | 41228 | — |
| `54662_06A78F_F3B2_vh_c6706_r5663_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.4638 | 0.0000 | 0.4133 | 0.1229 | 32728 | — |
| `54662_06A78F_F3B2_vh_c6706_r7455_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.4646 | 0.0000 | 0.4126 | 0.1228 | 50552 | — |
| `54662_06A78F_F3B2_vh_c5810_r6559_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.4650 | 0.0000 | 0.4124 | 0.1227 | 42103 | — |
| `54662_06A78F_F3B2_vh_c4914_r3871_det0001` | 2024-07-08-gulf | ARTIFACT | REVIEW | 0.4713 | 0.0000 | 0.4074 | 0.1214 | 44584 | — |
| `4662_06A78F_F3B2_vh_c12082_r5663_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.4734 | 0.0000 | 0.4056 | 0.1210 | 8237 | — |
| `54662_06A78F_F3B2_vh_c6706_r2975_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.4759 | 0.0000 | 0.4037 | 0.1205 | 20535 | — |
| `54662_06A78F_F3B2_vh_c8498_r5663_det0000` | 2024-07-08-gulf | DARK | REVIEW | 0.4769 | 0.0000 | 0.4029 | 0.1202 | 24942 | — |
| `54662_06A78F_F3B2_vh_c5810_r6559_det0001` | 2024-07-08-gulf | DARK | REVIEW | 0.4829 | 0.0000 | 0.3981 | 0.1190 | 44500 | — |
| `54662_06A78F_F3B2_vh_c5810_r5663_det0003` | 2024-07-08-gulf | DARK | REVIEW | 0.4854 | 0.0000 | 0.3961 | 0.1185 | 38598 | — |
| `54662_06A78F_F3B2_vh_c5810_r6559_det0002` | 2024-07-08-gulf | DARK | REVIEW | 0.4888 | 0.0000 | 0.3934 | 0.1178 | 44499 | — |
| `54662_06A78F_F3B2_vh_c6706_r2975_det0001` | 2024-07-08-gulf | DARK | REVIEW | 0.4888 | 0.0000 | 0.3934 | 0.1178 | 25059 | — |
| `4662_06A78F_F3B2_vh_c10290_r7455_det0002` | 2024-07-08-gulf | ARTIFACT | REVIEW | 0.4925 | 0.0000 | 0.3905 | 0.1170 | 13170 | — |
| `54662_06A78F_F3B2_vh_c5810_r6559_det0003` | 2024-07-08-gulf | DARK | REVIEW | 0.4995 | 0.0000 | 0.3849 | 0.1156 | 42546 | — |
| `54662_06A78F_F3B2_vh_c4914_r6559_det0000` | 2024-07-08-gulf | ARTIFACT | ARTIFACT | 0.5021 | 0.0000 | 0.3828 | 0.1151 | 50508 | — |
| `054662_06A78F_F3B2_vh_c4914_r287_det0002` | 2024-07-08-gulf | ARTIFACT | ARTIFACT | 0.5060 | 0.0000 | 0.3797 | 0.1143 | 47515 | — |
| `54662_06A78F_F3B2_vh_c4914_r5663_det0000` | 2024-07-08-gulf | ARTIFACT | ARTIFACT | 0.8811 | 0.0000 | 0.0937 | 0.0252 | 50957 | — |
| `4662_06A78F_F3B2_vh_c11186_r5663_det0001` | 2024-07-08-gulf | ARTIFACT | ARTIFACT | 0.5111 | 0.0000 | 0.3757 | 0.1132 | 5351 | — |
| `4662_06A78F_F3B2_vh_c12082_r6559_det0001` | 2024-07-08-gulf | ARTIFACT | ARTIFACT | 0.5111 | 0.0000 | 0.3757 | 0.1132 | 12004 | — |
| `4662_06A78F_F3B2_vh_c10290_r3871_det0000` | 2024-07-08-gulf | ARTIFACT | ARTIFACT | 0.5126 | 0.0000 | 0.3745 | 0.1129 | 15716 | — |
| `4662_06A78F_F3B2_vh_c11186_r7455_det0001` | 2024-07-08-gulf | ARTIFACT | ARTIFACT | 0.5127 | 0.0000 | 0.3744 | 0.1129 | 11046 | — |
| `54662_06A78F_F3B2_vh_c6706_r1183_det0000` | 2024-07-08-gulf | DARK | ARTIFACT | 0.5134 | 0.0000 | 0.3738 | 0.1128 | 30610 | — |
| `4662_06A78F_F3B2_vh_c11186_r3871_det0000` | 2024-07-08-gulf | ARTIFACT | ARTIFACT | 0.5137 | 0.0000 | 0.3736 | 0.1127 | 16669 | — |
| `4662_06A78F_F3B2_vh_c12978_r7455_det0003` | 2024-07-08-gulf | ARTIFACT | ARTIFACT | 0.5140 | 0.0000 | 0.3734 | 0.1126 | 14688 | — |

---

*Generated by `scripts/evaluate_calibration.py`.*
