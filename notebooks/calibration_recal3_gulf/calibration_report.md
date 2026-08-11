# Darkwatch Calibration Report

**Generated:** 2026-08-11T01:46:38.166148Z
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
- Mean predicted p_dark: 0.7547
- Brier score: 0.1472

| Predicted probability bin | Count | Observed DARK fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 4 | 0.000 | 0.063 |
| 0.60 – 0.80 | 22 | 0.545 | 0.772 |
| 0.80 – 1.00 | 32 | 0.938 | 0.830 |

### CLEAR

- Labeled positives: 3
- Mean predicted p_clear: 0.0467
- Brier score: 0.0005

| Predicted probability bin | Count | Observed CLEAR fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 55 | 0.000 | 0.000 |
| 0.80 – 1.00 | 3 | 1.000 | 0.902 |

### ARTIFACT

- Labeled positives: 13
- Mean predicted p_artifact: 0.0775
- Brier score: 0.1674

| Predicted probability bin | Count | Observed ARTIFACT fraction | Mean predicted |
|---|---|---|---|
| 0.00 – 0.20 | 57 | 0.211 | 0.063 |
| 0.80 – 1.00 | 1 | 1.000 | 0.900 |

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
| `4662_06A78F_F3B2_vh_c12978_r4767_det0000` | 2024-07-08-gulf | CLEAR | CLEAR | 0.0265 | 0.9140 | 0.0595 | 0.0000 | 76 | — |
| `4662_06A78F_F3B2_vh_c12978_r7455_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0174 | 0.0000 | 0.8459 | 0.1366 | 12138 | — |
| `54662_06A78F_F3B2_vh_c8498_r4767_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0208 | 0.0000 | 0.8432 | 0.1361 | 11118 | — |
| `54662_06A78F_F3B2_vh_c8498_r2975_det0000` | 2024-07-08-gulf | CLEAR | CLEAR | 0.0353 | 0.9067 | 0.0580 | 0.0000 | 65 | — |
| `4662_06A78F_F3B2_vh_c10290_r4767_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0250 | 0.0000 | 0.8396 | 0.1354 | 19153 | — |
| `54662_06A78F_F3B2_vh_c9394_r2079_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0252 | 0.0000 | 0.8394 | 0.1354 | 10674 | — |
| `4662_06A78F_F3B2_vh_c10290_r6559_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0252 | 0.0000 | 0.8394 | 0.1354 | 9002 | — |
| `4662_06A78F_F3B2_vh_c12082_r7455_det0001` | 2024-07-08-gulf | DARK | DARK | 0.0262 | 0.0000 | 0.8386 | 0.1351 | 12443 | — |
| `054662_06A78F_F3B2_vh_c4914_r287_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0266 | 0.0000 | 0.8383 | 0.1351 | 49491 | — |
| `4662_06A78F_F3B2_vh_c11186_r6559_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0282 | 0.0000 | 0.8370 | 0.1348 | 5187 | — |
| `4662_06A78F_F3B2_vh_c11186_r7455_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0286 | 0.0000 | 0.8366 | 0.1348 | 7822 | — |
| `54662_06A78F_F3B2_vh_c6706_r6559_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0287 | 0.0000 | 0.8365 | 0.1348 | 35987 | — |
| `54662_06A78F_F3B2_vh_c6706_r2079_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0312 | 0.0000 | 0.8345 | 0.1343 | 23649 | — |
| `4662_06A78F_F3B2_vh_c11186_r4767_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0315 | 0.0000 | 0.8342 | 0.1343 | 16604 | — |
| `54662_06A78F_F3B2_vh_c4914_r1183_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0320 | 0.0000 | 0.8337 | 0.1343 | 41219 | — |
| `54662_06A78F_F3B2_vh_c4914_r3871_det0000` | 2024-07-08-gulf | ARTIFACT | DARK | 0.0489 | 0.0000 | 0.8194 | 0.1317 | 40798 | — |
| `4662_06A78F_F3B2_vh_c11186_r5663_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0329 | 0.0000 | 0.8330 | 0.1341 | 9633 | — |
| `4662_06A78F_F3B2_vh_c12082_r7455_det0002` | 2024-07-08-gulf | DARK | DARK | 0.0347 | 0.0000 | 0.8314 | 0.1338 | 10215 | — |
| `4662_06A78F_F3B2_vh_c10290_r6559_det0001` | 2024-07-08-gulf | DARK | DARK | 0.0347 | 0.0000 | 0.8314 | 0.1338 | 8888 | — |
| `4662_06A78F_F3B2_vh_c12978_r6559_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0348 | 0.0000 | 0.8313 | 0.1338 | 15244 | — |
| `4662_06A78F_F3B2_vh_c12978_r2079_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0356 | 0.0000 | 0.8307 | 0.1337 | 31403 | — |
| `4662_06A78F_F3B2_vh_c10290_r4767_det0001` | 2024-07-08-gulf | DARK | DARK | 0.0367 | 0.0000 | 0.8297 | 0.1335 | 17912 | — |
| `54662_06A78F_F3B2_vh_c5810_r5663_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0368 | 0.0000 | 0.8297 | 0.1335 | 38940 | — |
| `54662_06A78F_F3B2_vh_c7602_r2079_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0393 | 0.0000 | 0.8276 | 0.1332 | 20519 | — |
| `4662_06A78F_F3B2_vh_c12978_r7455_det0002` | 2024-07-08-gulf | DARK | DARK | 0.0407 | 0.0000 | 0.8264 | 0.1329 | 21018 | — |
| `054662_06A78F_F3B2_vh_c7602_r287_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0423 | 0.0000 | 0.8250 | 0.1327 | 32884 | — |
| `54662_06A78F_F3B2_vh_c5810_r5663_det0001` | 2024-07-08-gulf | DARK | DARK | 0.0440 | 0.0000 | 0.8236 | 0.1324 | 39416 | — |
| `054662_06A78F_F3B2_vh_c4914_r287_det0001` | 2024-07-08-gulf | DARK | DARK | 0.0442 | 0.0000 | 0.8234 | 0.1324 | 46140 | — |
| `4662_06A78F_F3B2_vh_c12978_r6559_det0001` | 2024-07-08-gulf | DARK | DARK | 0.0475 | 0.0000 | 0.8206 | 0.1319 | 14032 | — |
| `4662_06A78F_F3B2_vh_c12082_r3871_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0477 | 0.0000 | 0.8204 | 0.1318 | 14873 | — |
| `54662_06A78F_F3B2_vh_c5810_r2975_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0533 | 0.0000 | 0.8156 | 0.1311 | 31840 | — |
| `54662_06A78F_F3B2_vh_c8498_r6559_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0563 | 0.0000 | 0.8131 | 0.1306 | 31570 | — |
| `054662_06A78F_F3B2_vh_c6706_r287_det0000` | 2024-07-08-gulf | ARTIFACT | DARK | 0.0571 | 0.0000 | 0.8124 | 0.1305 | 36614 | — |
| `4662_06A78F_F3B2_vh_c11186_r6559_det0001` | 2024-07-08-gulf | CLEAR | CLEAR | 0.0575 | 0.8863 | 0.0562 | 0.0000 | 174 | — |
| `54662_06A78F_F3B2_vh_c5810_r5663_det0002` | 2024-07-08-gulf | DARK | DARK | 0.0656 | 0.0000 | 0.8051 | 0.1293 | 41228 | — |
| `54662_06A78F_F3B2_vh_c6706_r5663_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0729 | 0.0000 | 0.7989 | 0.1283 | 32728 | — |
| `54662_06A78F_F3B2_vh_c6706_r7455_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0737 | 0.0000 | 0.7981 | 0.1282 | 50552 | — |
| `54662_06A78F_F3B2_vh_c5810_r6559_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0740 | 0.0000 | 0.7979 | 0.1281 | 42103 | — |
| `54662_06A78F_F3B2_vh_c4914_r3871_det0001` | 2024-07-08-gulf | ARTIFACT | DARK | 0.0801 | 0.0000 | 0.7927 | 0.1273 | 44584 | — |
| `4662_06A78F_F3B2_vh_c12082_r5663_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0822 | 0.0000 | 0.7907 | 0.1270 | 8237 | — |
| `54662_06A78F_F3B2_vh_c6706_r2975_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0848 | 0.0000 | 0.7885 | 0.1267 | 20535 | — |
| `54662_06A78F_F3B2_vh_c8498_r5663_det0000` | 2024-07-08-gulf | DARK | DARK | 0.0858 | 0.0000 | 0.7877 | 0.1265 | 24942 | — |
| `54662_06A78F_F3B2_vh_c5810_r6559_det0001` | 2024-07-08-gulf | DARK | DARK | 0.0923 | 0.0000 | 0.7820 | 0.1257 | 44500 | — |
| `54662_06A78F_F3B2_vh_c5810_r5663_det0003` | 2024-07-08-gulf | DARK | DARK | 0.0950 | 0.0000 | 0.7797 | 0.1253 | 38598 | — |
| `54662_06A78F_F3B2_vh_c5810_r6559_det0002` | 2024-07-08-gulf | DARK | DARK | 0.0990 | 0.0000 | 0.7762 | 0.1248 | 44499 | — |
| `54662_06A78F_F3B2_vh_c6706_r2975_det0001` | 2024-07-08-gulf | DARK | DARK | 0.0990 | 0.0000 | 0.7762 | 0.1248 | 25059 | — |
| `4662_06A78F_F3B2_vh_c10290_r7455_det0002` | 2024-07-08-gulf | ARTIFACT | DARK | 0.1033 | 0.0000 | 0.7725 | 0.1242 | 13170 | — |
| `54662_06A78F_F3B2_vh_c5810_r6559_det0003` | 2024-07-08-gulf | DARK | DARK | 0.1120 | 0.0000 | 0.7649 | 0.1230 | 42546 | — |
| `54662_06A78F_F3B2_vh_c4914_r6559_det0000` | 2024-07-08-gulf | ARTIFACT | DARK | 0.1153 | 0.0000 | 0.7621 | 0.1226 | 50508 | — |
| `054662_06A78F_F3B2_vh_c4914_r287_det0002` | 2024-07-08-gulf | ARTIFACT | DARK | 0.1204 | 0.0000 | 0.7576 | 0.1220 | 47515 | — |
| `54662_06A78F_F3B2_vh_c4914_r5663_det0000` | 2024-07-08-gulf | ARTIFACT | ARTIFACT | 0.9000 | 0.0000 | 0.0781 | 0.0219 | 50957 | — |
| `4662_06A78F_F3B2_vh_c11186_r5663_det0001` | 2024-07-08-gulf | ARTIFACT | DARK | 0.1273 | 0.0000 | 0.7516 | 0.1210 | 5351 | — |
| `4662_06A78F_F3B2_vh_c12082_r6559_det0001` | 2024-07-08-gulf | ARTIFACT | DARK | 0.1273 | 0.0000 | 0.7516 | 0.1210 | 12004 | — |
| `4662_06A78F_F3B2_vh_c10290_r3871_det0000` | 2024-07-08-gulf | ARTIFACT | DARK | 0.1294 | 0.0000 | 0.7497 | 0.1208 | 15716 | — |
| `4662_06A78F_F3B2_vh_c11186_r7455_det0001` | 2024-07-08-gulf | ARTIFACT | DARK | 0.1296 | 0.0000 | 0.7497 | 0.1208 | 11046 | — |
| `54662_06A78F_F3B2_vh_c6706_r1183_det0000` | 2024-07-08-gulf | DARK | DARK | 0.1307 | 0.0000 | 0.7486 | 0.1207 | 30610 | — |
| `4662_06A78F_F3B2_vh_c11186_r3871_det0000` | 2024-07-08-gulf | ARTIFACT | DARK | 0.1311 | 0.0000 | 0.7483 | 0.1206 | 16669 | — |
| `4662_06A78F_F3B2_vh_c12978_r7455_det0003` | 2024-07-08-gulf | ARTIFACT | DARK | 0.1314 | 0.0000 | 0.7481 | 0.1205 | 14688 | — |

---

*Generated by `scripts/evaluate_calibration.py`.*
