# Darkwatch Fusion Report

**Scene time:** 2024-07-08T00:02:23.149597
**AIS file:** `data\external\ais\ais_2024-07-08_clipped.csv`
**Association gate:** 2000.0 m
**Contacts fused:** 58
**AIS tracks loaded:** 5
**Verdict counts:** {'CLEAR': 3, 'DARK': 54, 'ARTIFACT': 1}

---

## 1. SAR Contacts

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12978_r4767_det0000`

| Field | Value |
|---|---|
| Center | `-89.55073, 28.66157` |
| Estimated size | 310 m × 543 m |
| Detector confidence | 0.766 |
| **Verdict** | **CLEAR** |
| p_artifact | 0.0513 |
| p_clear | 0.7477 |
| p_dark | 0.201 |
| p_review | 0.0 |
| Tracks within gate | 1 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- Size/shape artifact evidence: max_dim=543 m, aspect=1.8, confidence=0.085.
- Artifact evidence discounted by AIS match probability: (1 - 0.786)^1.00 = 0.214.
- Artifact evidence (0.018) shifted 0.014 real-vessel probability to artifact.
- Artifact evidence also shifted 0.002 dark-vessel probability to artifact.
- Best AIS match: MMSI 367373000 at 76 m (σ=468 m), P(match)=0.786.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12978_r7455_det0000`

| Field | Value |
|---|---|
| Center | `-89.60056, 28.85163` |
| Estimated size | 150 m × 409 m |
| Detector confidence | 0.746 |
| **Verdict** | **DARK** |
| p_artifact | 0.0381 |
| p_clear | 0.0 |
| p_dark | 0.7215 |
| p_review | 0.2405 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c8498_r4767_det0000`

| Field | Value |
|---|---|
| Center | `-89.92915, 28.54639` |
| Estimated size | 177 m × 421 m |
| Detector confidence | 0.715 |
| **Verdict** | **DARK** |
| p_artifact | 0.0428 |
| p_clear | 0.0 |
| p_dark | 0.7179 |
| p_review | 0.2393 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c8498_r2975_det0000`

| Field | Value |
|---|---|
| Center | `-89.89020, 28.45197` |
| Estimated size | 318 m × 550 m |
| Detector confidence | 0.702 |
| **Verdict** | **CLEAR** |
| p_artifact | 0.0622 |
| p_clear | 0.7394 |
| p_dark | 0.1984 |
| p_review | 0.0 |
| Tracks within gate | 1 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- Size/shape artifact evidence: max_dim=550 m, aspect=1.7, confidence=0.099.
- Artifact evidence discounted by AIS match probability: (1 - 0.786)^1.00 = 0.214.
- Artifact evidence (0.021) shifted 0.015 real-vessel probability to artifact.
- Artifact evidence also shifted 0.003 dark-vessel probability to artifact.
- Best AIS match: MMSI 354721000 at 65 m (σ=708 m), P(match)=0.786.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c10290_r4767_det0000`

| Field | Value |
|---|---|
| Center | `-89.79389, 28.64274` |
| Estimated size | 188 m × 248 m |
| Detector confidence | 0.677 |
| **Verdict** | **DARK** |
| p_artifact | 0.0484 |
| p_clear | 0.0 |
| p_dark | 0.7137 |
| p_review | 0.2379 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c9394_r2079_det0000`

| Field | Value |
|---|---|
| Center | `-89.82618, 28.37489` |
| Estimated size | 209 m × 493 m |
| Detector confidence | 0.676 |
| **Verdict** | **DARK** |
| p_artifact | 0.0486 |
| p_clear | 0.0 |
| p_dark | 0.7136 |
| p_review | 0.2379 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c10290_r6559_det0000`

| Field | Value |
|---|---|
| Center | `-89.80121, 28.80524` |
| Estimated size | 179 m × 411 m |
| Detector confidence | 0.676 |
| **Verdict** | **DARK** |
| p_artifact | 0.0486 |
| p_clear | 0.0 |
| p_dark | 0.7136 |
| p_review | 0.2379 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12082_r7455_det0001`

| Field | Value |
|---|---|
| Center | `-89.60706, 28.86537` |
| Estimated size | 133 m × 351 m |
| Detector confidence | 0.668 |
| **Verdict** | **DARK** |
| p_artifact | 0.0499 |
| p_clear | 0.0 |
| p_dark | 0.7126 |
| p_review | 0.2375 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c4914_r287_det0000`

| Field | Value |
|---|---|
| Center | `-90.20161, 28.10133` |
| Estimated size | 160 m × 370 m |
| Detector confidence | 0.664 |
| **Verdict** | **DARK** |
| p_artifact | 0.0504 |
| p_clear | 0.0 |
| p_dark | 0.7122 |
| p_review | 0.2374 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c11186_r6559_det0000`

| Field | Value |
|---|---|
| Center | `-89.71500, 28.75177` |
| Estimated size | 199 m × 382 m |
| Detector confidence | 0.651 |
| **Verdict** | **DARK** |
| p_artifact | 0.0523 |
| p_clear | 0.0 |
| p_dark | 0.7108 |
| p_review | 0.2369 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c11186_r7455_det0000`

| Field | Value |
|---|---|
| Center | `-89.77974, 28.83169` |
| Estimated size | 166 m × 496 m |
| Detector confidence | 0.648 |
| **Verdict** | **DARK** |
| p_artifact | 0.0528 |
| p_clear | 0.0 |
| p_dark | 0.7104 |
| p_review | 0.2368 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c6706_r6559_det0000`

| Field | Value |
|---|---|
| Center | `-90.14795, 28.68405` |
| Estimated size | 133 m × 364 m |
| Detector confidence | 0.647 |
| **Verdict** | **DARK** |
| p_artifact | 0.0529 |
| p_clear | 0.0 |
| p_dark | 0.7103 |
| p_review | 0.2368 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c6706_r2079_det0000`

| Field | Value |
|---|---|
| Center | `-90.07009, 28.30963` |
| Estimated size | 207 m × 433 m |
| Detector confidence | 0.628 |
| **Verdict** | **DARK** |
| p_artifact | 0.0559 |
| p_clear | 0.0 |
| p_dark | 0.7081 |
| p_review | 0.236 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c11186_r4767_det0000`

| Field | Value |
|---|---|
| Center | `-89.69951, 28.58792` |
| Estimated size | 186 m × 473 m |
| Detector confidence | 0.624 |
| **Verdict** | **DARK** |
| p_artifact | 0.0563 |
| p_clear | 0.0 |
| p_dark | 0.7077 |
| p_review | 0.2359 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c4914_r1183_det0000`

| Field | Value |
|---|---|
| Center | `-90.21940, 28.22044` |
| Estimated size | 151 m × 350 m |
| Detector confidence | 0.620 |
| **Verdict** | **DARK** |
| p_artifact | 0.0569 |
| p_clear | 0.0 |
| p_dark | 0.7073 |
| p_review | 0.2358 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c4914_r3871_det0000`

| Field | Value |
|---|---|
| Center | `-90.30724, 28.42960` |
| Estimated size | 170 m × 508 m |
| Detector confidence | 0.619 |
| **Verdict** | **DARK** |
| p_artifact | 0.075 |
| p_clear | 0.0 |
| p_dark | 0.6938 |
| p_review | 0.2313 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Size/shape artifact evidence: max_dim=508 m, aspect=3.0, confidence=0.015.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (0.015) shifted 0.009 real-vessel probability to artifact.
- Artifact evidence also shifted 0.008 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c11186_r5663_det0000`

| Field | Value |
|---|---|
| Center | `-89.70141, 28.71178` |
| Estimated size | 148 m × 402 m |
| Detector confidence | 0.614 |
| **Verdict** | **DARK** |
| p_artifact | 0.0579 |
| p_clear | 0.0 |
| p_dark | 0.7066 |
| p_review | 0.2355 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12082_r7455_det0002`

| Field | Value |
|---|---|
| Center | `-89.66253, 28.88041` |
| Estimated size | 157 m × 339 m |
| Detector confidence | 0.600 |
| **Verdict** | **DARK** |
| p_artifact | 0.06 |
| p_clear | 0.0 |
| p_dark | 0.705 |
| p_review | 0.235 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c10290_r6559_det0001`

| Field | Value |
|---|---|
| Center | `-89.79780, 28.81709` |
| Estimated size | 135 m × 489 m |
| Detector confidence | 0.600 |
| **Verdict** | **DARK** |
| p_artifact | 0.06 |
| p_clear | 0.0 |
| p_dark | 0.705 |
| p_review | 0.235 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12978_r6559_det0000`

| Field | Value |
|---|---|
| Center | `-89.55762, 28.83222` |
| Estimated size | 192 m × 339 m |
| Detector confidence | 0.599 |
| **Verdict** | **DARK** |
| p_artifact | 0.0601 |
| p_clear | 0.0 |
| p_dark | 0.7049 |
| p_review | 0.235 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12978_r2079_det0000`

| Field | Value |
|---|---|
| Center | `-89.45298, 28.39272` |
| Estimated size | 272 m × 384 m |
| Detector confidence | 0.593 |
| **Verdict** | **DARK** |
| p_artifact | 0.061 |
| p_clear | 0.0 |
| p_dark | 0.7042 |
| p_review | 0.2347 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c10290_r4767_det0001`

| Field | Value |
|---|---|
| Center | `-89.78601, 28.65182` |
| Estimated size | 214 m × 348 m |
| Detector confidence | 0.585 |
| **Verdict** | **DARK** |
| p_artifact | 0.0622 |
| p_clear | 0.0 |
| p_dark | 0.7034 |
| p_review | 0.2345 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c5810_r5663_det0000`

| Field | Value |
|---|---|
| Center | `-90.24166, 28.61843` |
| Estimated size | 113 m × 303 m |
| Detector confidence | 0.584 |
| **Verdict** | **DARK** |
| p_artifact | 0.0623 |
| p_clear | 0.0 |
| p_dark | 0.7032 |
| p_review | 0.2344 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c7602_r2079_det0000`

| Field | Value |
|---|---|
| Center | `-90.02145, 28.30793` |
| Estimated size | 130 m × 409 m |
| Detector confidence | 0.567 |
| **Verdict** | **DARK** |
| p_artifact | 0.065 |
| p_clear | 0.0 |
| p_dark | 0.7013 |
| p_review | 0.2338 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12978_r7455_det0002`

| Field | Value |
|---|---|
| Center | `-89.53122, 28.90507` |
| Estimated size | 117 m × 261 m |
| Detector confidence | 0.557 |
| **Verdict** | **DARK** |
| p_artifact | 0.0665 |
| p_clear | 0.0 |
| p_dark | 0.7001 |
| p_review | 0.2334 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c7602_r287_det0000`

| Field | Value |
|---|---|
| Center | `-89.94791, 28.16085` |
| Estimated size | 288 m × 329 m |
| Detector confidence | 0.546 |
| **Verdict** | **DARK** |
| p_artifact | 0.0682 |
| p_clear | 0.0 |
| p_dark | 0.6989 |
| p_review | 0.233 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c5810_r5663_det0001`

| Field | Value |
|---|---|
| Center | `-90.24859, 28.61607` |
| Estimated size | 287 m × 440 m |
| Detector confidence | 0.533 |
| **Verdict** | **DARK** |
| p_artifact | 0.07 |
| p_clear | 0.0 |
| p_dark | 0.6975 |
| p_review | 0.2325 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c4914_r287_det0001`

| Field | Value |
|---|---|
| Center | `-90.22714, 28.16162` |
| Estimated size | 207 m × 419 m |
| Detector confidence | 0.532 |
| **Verdict** | **DARK** |
| p_artifact | 0.0702 |
| p_clear | 0.0 |
| p_dark | 0.6973 |
| p_review | 0.2324 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12978_r6559_det0001`

| Field | Value |
|---|---|
| Center | `-89.56908, 28.82739` |
| Estimated size | 108 m × 339 m |
| Detector confidence | 0.510 |
| **Verdict** | **DARK** |
| p_artifact | 0.0736 |
| p_clear | 0.0 |
| p_dark | 0.6948 |
| p_review | 0.2316 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12082_r3871_det0000`

| Field | Value |
|---|---|
| Center | `-89.61438, 28.53970` |
| Estimated size | 152 m × 286 m |
| Detector confidence | 0.508 |
| **Verdict** | **DARK** |
| p_artifact | 0.0738 |
| p_clear | 0.0 |
| p_dark | 0.6946 |
| p_review | 0.2315 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c5810_r2975_det0000`

| Field | Value |
|---|---|
| Center | `-90.20128, 28.36624` |
| Estimated size | 163 m × 309 m |
| Detector confidence | 0.471 |
| **Verdict** | **DARK** |
| p_artifact | 0.0793 |
| p_clear | 0.0 |
| p_dark | 0.6905 |
| p_review | 0.2302 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c8498_r6559_det0000`

| Field | Value |
|---|---|
| Center | `-90.02593, 28.73884` |
| Estimated size | 171 m × 367 m |
| Detector confidence | 0.453 |
| **Verdict** | **DARK** |
| p_artifact | 0.0821 |
| p_clear | 0.0 |
| p_dark | 0.6884 |
| p_review | 0.2295 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c6706_r287_det0000`

| Field | Value |
|---|---|
| Center | `-90.07807, 28.16725` |
| Estimated size | 224 m × 486 m |
| Detector confidence | 0.447 |
| **Verdict** | **DARK** |
| p_artifact | 0.0829 |
| p_clear | 0.0 |
| p_dark | 0.6878 |
| p_review | 0.2293 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c11186_r6559_det0001`

| Field | Value |
|---|---|
| Center | `-89.70881, 28.79661` |
| Estimated size | 194 m × 454 m |
| Detector confidence | 0.425 |
| **Verdict** | **CLEAR** |
| p_artifact | 0.0863 |
| p_clear | 0.7184 |
| p_dark | 0.1953 |
| p_review | 0.0 |
| Tracks within gate | 1 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- Best AIS match: MMSI 338032000 at 174 m (σ=296 m), P(match)=0.786.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c5810_r5663_det0002`

| Field | Value |
|---|---|
| Center | `-90.26900, 28.61676` |
| Estimated size | 171 m × 314 m |
| Detector confidence | 0.395 |
| **Verdict** | **DARK** |
| p_artifact | 0.0907 |
| p_clear | 0.0 |
| p_dark | 0.682 |
| p_review | 0.2273 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c6706_r5663_det0000`

| Field | Value |
|---|---|
| Center | `-90.18296, 28.59623` |
| Estimated size | 121 m × 324 m |
| Detector confidence | 0.353 |
| **Verdict** | **DARK** |
| p_artifact | 0.097 |
| p_clear | 0.0 |
| p_dark | 0.6772 |
| p_review | 0.2257 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c6706_r7455_det0000`

| Field | Value |
|---|---|
| Center | `-90.23010, 28.79572` |
| Estimated size | 130 m × 308 m |
| Detector confidence | 0.348 |
| **Verdict** | **DARK** |
| p_artifact | 0.0977 |
| p_clear | 0.0 |
| p_dark | 0.6767 |
| p_review | 0.2256 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c5810_r6559_det0000`

| Field | Value |
|---|---|
| Center | `-90.24506, 28.66799` |
| Estimated size | 133 m × 249 m |
| Detector confidence | 0.346 |
| **Verdict** | **DARK** |
| p_artifact | 0.098 |
| p_clear | 0.0 |
| p_dark | 0.6765 |
| p_review | 0.2255 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c4914_r3871_det0001`

| Field | Value |
|---|---|
| Center | `-90.34627, 28.43344` |
| Estimated size | 127 m × 298 m |
| Detector confidence | 0.313 |
| **Verdict** | **DARK** |
| p_artifact | 0.1031 |
| p_clear | 0.0 |
| p_dark | 0.6727 |
| p_review | 0.2242 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12082_r5663_det0000`

| Field | Value |
|---|---|
| Center | `-89.61628, 28.70907` |
| Estimated size | 97 m × 319 m |
| Detector confidence | 0.301 |
| **Verdict** | **DARK** |
| p_artifact | 0.1049 |
| p_clear | 0.0 |
| p_dark | 0.6713 |
| p_review | 0.2238 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c6706_r2975_det0000`

| Field | Value |
|---|---|
| Center | `-90.08843, 28.38994` |
| Estimated size | 251 m × 411 m |
| Detector confidence | 0.287 |
| **Verdict** | **DARK** |
| p_artifact | 0.107 |
| p_clear | 0.0 |
| p_dark | 0.6698 |
| p_review | 0.2233 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c8498_r5663_det0000`

| Field | Value |
|---|---|
| Center | `-89.96913, 28.66575` |
| Estimated size | 186 m × 261 m |
| Detector confidence | 0.281 |
| **Verdict** | **DARK** |
| p_artifact | 0.1078 |
| p_clear | 0.0 |
| p_dark | 0.6691 |
| p_review | 0.223 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c5810_r6559_det0001`

| Field | Value |
|---|---|
| Center | `-90.26825, 28.67643` |
| Estimated size | 154 m × 342 m |
| Detector confidence | 0.247 |
| **Verdict** | **DARK** |
| p_artifact | 0.113 |
| p_clear | 0.0 |
| p_dark | 0.6653 |
| p_review | 0.2218 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c5810_r5663_det0003`

| Field | Value |
|---|---|
| Center | `-90.23234, 28.62678` |
| Estimated size | 121 m × 294 m |
| Detector confidence | 0.232 |
| **Verdict** | **DARK** |
| p_artifact | 0.1151 |
| p_clear | 0.0 |
| p_dark | 0.6636 |
| p_review | 0.2212 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c5810_r6559_det0002`

| Field | Value |
|---|---|
| Center | `-90.28164, 28.65788` |
| Estimated size | 118 m × 288 m |
| Detector confidence | 0.212 |
| **Verdict** | **DARK** |
| p_artifact | 0.1182 |
| p_clear | 0.0 |
| p_dark | 0.6614 |
| p_review | 0.2205 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c6706_r2975_det0001`

| Field | Value |
|---|---|
| Center | `-90.13574, 28.38616` |
| Estimated size | 155 m × 374 m |
| Detector confidence | 0.212 |
| **Verdict** | **DARK** |
| p_artifact | 0.1182 |
| p_clear | 0.0 |
| p_dark | 0.6614 |
| p_review | 0.2205 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c10290_r7455_det0002`

| Field | Value |
|---|---|
| Center | `-89.81001, 28.87705` |
| Estimated size | 105 m × 351 m |
| Detector confidence | 0.190 |
| **Verdict** | **DARK** |
| p_artifact | 0.1215 |
| p_clear | 0.0 |
| p_dark | 0.6589 |
| p_review | 0.2196 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c5810_r6559_det0003`

| Field | Value |
|---|---|
| Center | `-90.25966, 28.65576` |
| Estimated size | 109 m × 211 m |
| Detector confidence | 0.147 |
| **Verdict** | **DARK** |
| p_artifact | 0.128 |
| p_clear | 0.0 |
| p_dark | 0.654 |
| p_review | 0.218 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c4914_r6559_det0000`

| Field | Value |
|---|---|
| Center | `-90.33168, 28.68974` |
| Estimated size | 141 m × 294 m |
| Detector confidence | 0.131 |
| **Verdict** | **DARK** |
| p_artifact | 0.1304 |
| p_clear | 0.0 |
| p_dark | 0.6522 |
| p_review | 0.2174 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c4914_r287_det0002`

| Field | Value |
|---|---|
| Center | `-90.23176, 28.14821` |
| Estimated size | 116 m × 225 m |
| Detector confidence | 0.106 |
| **Verdict** | **DARK** |
| p_artifact | 0.1341 |
| p_clear | 0.0 |
| p_dark | 0.6494 |
| p_review | 0.2165 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c4914_r5663_det0000`

| Field | Value |
|---|---|
| Center | `-90.39170, 28.57980` |
| Estimated size | 113 m × 1045 m |
| Detector confidence | 0.094 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.6919 |
| p_clear | 0.0 |
| p_dark | 0.2311 |
| p_review | 0.077 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Size/shape artifact evidence: max_dim=1045 m, aspect=9.3, confidence=1.000.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (1.000) shifted 0.094 real-vessel probability to artifact.
- Artifact evidence also shifted 0.462 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c11186_r5663_det0001`

| Field | Value |
|---|---|
| Center | `-89.71475, 28.75026` |
| Estimated size | 165 m × 109 m |
| Detector confidence | 0.073 |
| **Verdict** | **DARK** |
| p_artifact | 0.139 |
| p_clear | 0.0 |
| p_dark | 0.6457 |
| p_review | 0.2152 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12082_r6559_det0001`

| Field | Value |
|---|---|
| Center | `-89.60161, 28.85081` |
| Estimated size | 413 m × 291 m |
| Detector confidence | 0.073 |
| **Verdict** | **DARK** |
| p_artifact | 0.139 |
| p_clear | 0.0 |
| p_dark | 0.6457 |
| p_review | 0.2152 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c10290_r3871_det0000`

| Field | Value |
|---|---|
| Center | `-89.80092, 28.56950` |
| Estimated size | 87 m × 158 m |
| Detector confidence | 0.063 |
| **Verdict** | **DARK** |
| p_artifact | 0.1405 |
| p_clear | 0.0 |
| p_dark | 0.6446 |
| p_review | 0.2149 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c11186_r7455_det0001`

| Field | Value |
|---|---|
| Center | `-89.70091, 28.89722` |
| Estimated size | 131 m × 137 m |
| Detector confidence | 0.062 |
| **Verdict** | **DARK** |
| p_artifact | 0.1406 |
| p_clear | 0.0 |
| p_dark | 0.6445 |
| p_review | 0.2148 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c6706_r1183_det0000`

| Field | Value |
|---|---|
| Center | `-90.09384, 28.24288` |
| Estimated size | 117 m × 286 m |
| Detector confidence | 0.057 |
| **Verdict** | **DARK** |
| p_artifact | 0.1414 |
| p_clear | 0.0 |
| p_dark | 0.644 |
| p_review | 0.2147 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c11186_r3871_det0000`

| Field | Value |
|---|---|
| Center | `-89.69917, 28.58622` |
| Estimated size | 134 m × 118 m |
| Detector confidence | 0.056 |
| **Verdict** | **DARK** |
| p_artifact | 0.1417 |
| p_clear | 0.0 |
| p_dark | 0.6438 |
| p_review | 0.2146 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12978_r7455_det0003`

| Field | Value |
|---|---|
| Center | `-89.60125, 28.89040` |
| Estimated size | 123 m × 388 m |
| Detector confidence | 0.054 |
| **Verdict** | **DARK** |
| p_artifact | 0.1419 |
| p_clear | 0.0 |
| p_dark | 0.6436 |
| p_review | 0.2145 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

---

## 2. Verdict Summary Table

| Contact | Verdict | p_artifact | p_clear | p_dark | p_review | Nearest MMSI | Nearest dist (m) |
|---|---|---|---|---|---|---|---|
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12978_r4767_det0000` | CLEAR | 0.0513 | 0.7477 | 0.201 | 0.0 | 367373000 | 76.0 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12978_r7455_det0000` | DARK | 0.0381 | 0.0 | 0.7215 | 0.2405 | 338032000 | 12138.2 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c8498_r4767_det0000` | DARK | 0.0428 | 0.0 | 0.7179 | 0.2393 | 354721000 | 11117.8 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c8498_r2975_det0000` | CLEAR | 0.0622 | 0.7394 | 0.1984 | 0.0 | 354721000 | 64.6 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c10290_r4767_det0000` | DARK | 0.0484 | 0.0 | 0.7137 | 0.2379 | 338032000 | 19153.3 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c9394_r2079_det0000` | DARK | 0.0486 | 0.0 | 0.7136 | 0.2379 | 354721000 | 10673.7 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c10290_r6559_det0000` | DARK | 0.0486 | 0.0 | 0.7136 | 0.2379 | 338032000 | 9002.3 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12082_r7455_det0001` | DARK | 0.0499 | 0.0 | 0.7126 | 0.2375 | 338032000 | 12443.2 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c4914_r287_det0000` | DARK | 0.0504 | 0.0 | 0.7122 | 0.2374 | 354721000 | 49490.6 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c11186_r6559_det0000` | DARK | 0.0523 | 0.0 | 0.7108 | 0.2369 | 338032000 | 5186.6 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c11186_r7455_det0000` | DARK | 0.0528 | 0.0 | 0.7104 | 0.2368 | 338032000 | 7822.0 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c6706_r6559_det0000` | DARK | 0.0529 | 0.0 | 0.7103 | 0.2368 | 354721000 | 35987.2 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c6706_r2079_det0000` | DARK | 0.0559 | 0.0 | 0.7081 | 0.236 | 354721000 | 23649.4 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c11186_r4767_det0000` | DARK | 0.0563 | 0.0 | 0.7077 | 0.2359 | 367373000 | 16603.6 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c4914_r1183_det0000` | DARK | 0.0569 | 0.0 | 0.7073 | 0.2358 | 354721000 | 41218.9 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c4914_r3871_det0000` | DARK | 0.075 | 0.0 | 0.6938 | 0.2313 | 354721000 | 40797.9 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c11186_r5663_det0000` | DARK | 0.0579 | 0.0 | 0.7066 | 0.2355 | 338032000 | 9632.7 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12082_r7455_det0002` | DARK | 0.06 | 0.0 | 0.705 | 0.235 | 338032000 | 10214.6 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c10290_r6559_det0001` | DARK | 0.06 | 0.0 | 0.705 | 0.235 | 338032000 | 8887.8 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12978_r6559_det0000` | DARK | 0.0601 | 0.0 | 0.7049 | 0.235 | 338032000 | 15243.7 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12978_r2079_det0000` | DARK | 0.061 | 0.0 | 0.7042 | 0.2347 | 367373000 | 31402.6 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c10290_r4767_det0001` | DARK | 0.0622 | 0.0 | 0.7034 | 0.2345 | 338032000 | 17912.1 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c5810_r5663_det0000` | DARK | 0.0623 | 0.0 | 0.7032 | 0.2344 | 354721000 | 38939.9 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c7602_r2079_det0000` | DARK | 0.065 | 0.0 | 0.7013 | 0.2338 | 354721000 | 20519.1 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12978_r7455_det0002` | DARK | 0.0665 | 0.0 | 0.7001 | 0.2334 | 338032000 | 21018.1 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c7602_r287_det0000` | DARK | 0.0682 | 0.0 | 0.6989 | 0.233 | 354721000 | 32883.6 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c5810_r5663_det0001` | DARK | 0.07 | 0.0 | 0.6975 | 0.2325 | 354721000 | 39416.2 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c4914_r287_det0001` | DARK | 0.0702 | 0.0 | 0.6973 | 0.2324 | 354721000 | 46140.4 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12978_r6559_det0001` | DARK | 0.0736 | 0.0 | 0.6948 | 0.2316 | 338032000 | 14031.8 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12082_r3871_det0000` | DARK | 0.0738 | 0.0 | 0.6946 | 0.2315 | 367373000 | 14872.7 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c5810_r2975_det0000` | DARK | 0.0793 | 0.0 | 0.6905 | 0.2302 | 354721000 | 31840.0 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c8498_r6559_det0000` | DARK | 0.0821 | 0.0 | 0.6884 | 0.2295 | 338032000 | 31570.5 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c6706_r287_det0000` | DARK | 0.0829 | 0.0 | 0.6878 | 0.2293 | 354721000 | 36614.3 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c11186_r6559_det0001` | CLEAR | 0.0863 | 0.7184 | 0.1953 | 0.0 | 338032000 | 173.8 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c5810_r5663_det0002` | DARK | 0.0907 | 0.0 | 0.682 | 0.2273 | 354721000 | 41227.7 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c6706_r5663_det0000` | DARK | 0.097 | 0.0 | 0.6772 | 0.2257 | 354721000 | 32728.2 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c6706_r7455_det0000` | DARK | 0.0977 | 0.0 | 0.6767 | 0.2256 | 354721000 | 50552.0 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c5810_r6559_det0000` | DARK | 0.098 | 0.0 | 0.6765 | 0.2255 | 354721000 | 42103.3 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c4914_r3871_det0001` | DARK | 0.1031 | 0.0 | 0.6727 | 0.2242 | 354721000 | 44584.5 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12082_r5663_det0000` | DARK | 0.1049 | 0.0 | 0.6713 | 0.2238 | 367373000 | 8237.4 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c6706_r2975_det0000` | DARK | 0.107 | 0.0 | 0.6698 | 0.2233 | 354721000 | 20534.7 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c8498_r5663_det0000` | DARK | 0.1078 | 0.0 | 0.6691 | 0.223 | 354721000 | 24941.9 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c5810_r6559_det0001` | DARK | 0.113 | 0.0 | 0.6653 | 0.2218 | 354721000 | 44500.3 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c5810_r5663_det0003` | DARK | 0.1151 | 0.0 | 0.6636 | 0.2212 | 354721000 | 38597.9 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c5810_r6559_det0002` | DARK | 0.1182 | 0.0 | 0.6614 | 0.2205 | 354721000 | 44498.8 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c6706_r2975_det0001` | DARK | 0.1182 | 0.0 | 0.6614 | 0.2205 | 354721000 | 25059.0 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c10290_r7455_det0002` | DARK | 0.1215 | 0.0 | 0.6589 | 0.2196 | 338032000 | 13170.4 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c5810_r6559_det0003` | DARK | 0.128 | 0.0 | 0.654 | 0.218 | 354721000 | 42545.7 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c4914_r6559_det0000` | DARK | 0.1304 | 0.0 | 0.6522 | 0.2174 | 354721000 | 50508.4 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c4914_r287_det0002` | DARK | 0.1341 | 0.0 | 0.6494 | 0.2165 | 354721000 | 47514.6 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c4914_r5663_det0000` | ARTIFACT | 0.6919 | 0.0 | 0.2311 | 0.077 | 354721000 | 50956.7 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c11186_r5663_det0001` | DARK | 0.139 | 0.0 | 0.6457 | 0.2152 | 338032000 | 5351.0 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12082_r6559_det0001` | DARK | 0.139 | 0.0 | 0.6457 | 0.2152 | 338032000 | 12004.1 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c10290_r3871_det0000` | DARK | 0.1405 | 0.0 | 0.6446 | 0.2149 | 354721000 | 15716.2 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c11186_r7455_det0001` | DARK | 0.1406 | 0.0 | 0.6445 | 0.2148 | 338032000 | 11046.5 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c6706_r1183_det0000` | DARK | 0.1414 | 0.0 | 0.644 | 0.2147 | 354721000 | 30610.4 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c11186_r3871_det0000` | DARK | 0.1417 | 0.0 | 0.6438 | 0.2146 | 367373000 | 16669.4 |
| `S1A_IW_GRDH_1SDV_20240708T000210_20240708T000235_054662_06A78F_F3B2_vh_c12978_r7455_det0003` | DARK | 0.1419 | 0.0 | 0.6436 | 0.2145 | 338032000 | 14688.1 |

---

## 3. AIS Tracks in Theater

| MMSI | Name | Messages | Avg SOG (kn) | Status(es) | Distance to contact (m) |
|---|---|---|---|---|---|
| 338032000 | AGNES CANDIES | 76 | 8.6 | 0 | ~9,220 |
| 354721000 | BALDER | 8 | 5.0 | 3 | ~52,021 |
| 367327360 | MEDITERRANEAN | 31 | 7.8 | 0 | ~13,945 |
| 367373000 | WD143 SHELL RIG | 51 | 0.0 | 15 | ~78 |
| 367666910 | CAJUN IV | 7 | 16.5 | 0 | ~15,073 |
| 367693810 | DAUPHIN ISLAND | 2 | 8.7 | 15 | ~60,919 |
| 369336000 | AMBER | 2 | 10.1 | 0 | ~63,365 |
| 538009830 | PRESTIGE | 7 | 9.1 | 0 | ~64,281 |
| 636021124 | VEGA DABLAM | 8 | 9.5 | 0 | ~13,130 |

---

## 4. Interpretation Notes

- A SAR contact with no AIS track inside the gate is **not automatically dark**. It may be:
  - a genuine dark vessel,
  - a transponding vessel with a temporary AIS outage,
  - a radar artifact (wave clutter, azimuth ambiguity, wind streak),
  - a fixed object (oil platform, small island, navigation marker).
- `p_review` is raised when no AIS track exists within 2× the gate radius, reflecting the possibility of an innocent coverage gap.
- The **nearest association** column shows the closest cooperative track even when it lies outside the gate, so a human can judge whether the contact is plausibly explained by nearby traffic.

---

*Generated by `scripts/fusion_report.py` on 2026-08-11T03:06:05.519232Z.*
