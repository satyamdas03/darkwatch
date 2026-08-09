# Darkwatch Fusion Report

**Scene time:** 2024-08-11T01:59:06.140494
**AIS file:** `data\external\ais\ais_2024-08-11_clipped.csv`
**Association gate:** 2000.0 m
**Contacts fused:** 20
**AIS tracks loaded:** 3
**Verdict counts:** {'ARTIFACT': 15, 'CLEAR': 2, 'DARK': 2, 'REVIEW': 1}

---

## 1. SAR Contacts

### `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c2397_r9735_det0000`

| Field | Value |
|---|---|
| Center | `-120.70207, 34.49515` |
| Estimated size | 197 m × 523 m |
| Detector confidence | 0.650 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.8809 |
| p_clear | 0.0 |
| p_dark | 0.0893 |
| p_review | 0.0298 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Hidalgo (114 m away); scaled static confidence 1.000.
- Size/shape artifact evidence: max_dim=523 m, aspect=2.6, confidence=0.045.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (1.000) shifted 0.650 real-vessel probability to artifact.
- Artifact evidence also shifted 0.179 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c2397_r9735_det0001`

| Field | Value |
|---|---|
| Center | `-120.64624, 34.45569` |
| Estimated size | 166 m × 452 m |
| Detector confidence | 0.638 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.8768 |
| p_clear | 0.0 |
| p_dark | 0.0924 |
| p_review | 0.0308 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Hermosa (126 m away); scaled static confidence 1.000.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (1.000) shifted 0.638 real-vessel probability to artifact.
- Artifact evidence also shifted 0.185 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c5981_r7943_det0000`

| Field | Value |
|---|---|
| Center | `-120.27891, 34.35071` |
| Estimated size | 285 m × 241 m |
| Detector confidence | 0.596 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.8626 |
| p_clear | 0.0 |
| p_dark | 0.1031 |
| p_review | 0.0344 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Heritage (121 m away); scaled static confidence 1.000.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (1.000) shifted 0.596 real-vessel probability to artifact.
- Artifact evidence also shifted 0.206 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c9565_r7943_det0000`

| Field | Value |
|---|---|
| Center | `-119.90417, 34.38986` |
| Estimated size | 147 m × 210 m |
| Detector confidence | 0.596 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.5893 |
| p_clear | 0.0 |
| p_dark | 0.308 |
| p_review | 0.1027 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Holly (209 m away); scaled static confidence 0.549.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (0.549) shifted 0.327 real-vessel probability to artifact.
- Artifact evidence also shifted 0.202 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vv_c7773_r7943_det0000`

| Field | Value |
|---|---|
| Center | `-120.11937, 34.39117` |
| Estimated size | 193 m × 251 m |
| Detector confidence | 0.579 |
| **Verdict** | **CLEAR** |
| p_artifact | 0.1499 |
| p_clear | 0.6793 |
| p_dark | 0.1707 |
| p_review | 0.0 |
| Tracks within gate | 1 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- Static object nearby: Platform Hondo (202 m away); scaled static confidence 0.589.
- Artifact evidence discounted by AIS match probability: (1 - 0.786)^1.00 = 0.214.
- Artifact evidence (0.126) shifted 0.073 real-vessel probability to artifact.
- Artifact evidence also shifted 0.014 dark-vessel probability to artifact.
- Best AIS match: MMSI 367104050 at 281 m (σ=294 m), P(match)=0.786.

### `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c9565_r7943_det0001`

| Field | Value |
|---|---|
| Center | `-119.92019, 34.43186` |
| Estimated size | 270 m × 355 m |
| Detector confidence | 0.479 |
| **Verdict** | **DARK** |
| p_artifact | 0.0781 |
| p_clear | 0.0 |
| p_dark | 0.6914 |
| p_review | 0.2305 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c4189_r8839_det0000`

| Field | Value |
|---|---|
| Center | `-120.46036, 34.44706` |
| Estimated size | 1722 m × 1301 m |
| Detector confidence | 0.374 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.7873 |
| p_clear | 0.0 |
| p_dark | 0.1595 |
| p_review | 0.0532 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Size/shape artifact evidence: max_dim=1722 m, aspect=1.3, confidence=1.000.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (1.000) shifted 0.374 real-vessel probability to artifact.
- Artifact evidence also shifted 0.319 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c2397_r9735_det0002`

| Field | Value |
|---|---|
| Center | `-120.68075, 34.46933` |
| Estimated size | 199 m × 425 m |
| Detector confidence | 0.351 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.7794 |
| p_clear | 0.0 |
| p_dark | 0.1655 |
| p_review | 0.0552 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Harvest (101 m away); scaled static confidence 1.000.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (1.000) shifted 0.351 real-vessel probability to artifact.
- Artifact evidence also shifted 0.331 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c6877_r7943_det0000`

| Field | Value |
|---|---|
| Center | `-120.16693, 34.37689` |
| Estimated size | 256 m × 260 m |
| Detector confidence | 0.308 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.7265 |
| p_clear | 0.0 |
| p_dark | 0.2051 |
| p_review | 0.0684 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Harmony (146 m away); scaled static confidence 0.922.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (0.922) shifted 0.284 real-vessel probability to artifact.
- Artifact evidence also shifted 0.339 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c2397_r11527_det0000`

| Field | Value |
|---|---|
| Center | `-120.72878, 34.61006` |
| Estimated size | 167 m × 495 m |
| Detector confidence | 0.276 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.6846 |
| p_clear | 0.0 |
| p_dark | 0.2365 |
| p_review | 0.0788 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Irene (156 m away); scaled static confidence 0.862.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (0.862) shifted 0.238 real-vessel probability to artifact.
- Artifact evidence also shifted 0.338 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c5981_r8839_det0000`

| Field | Value |
|---|---|
| Center | `-120.26184, 34.46953` |
| Estimated size | 1573 m × 581 m |
| Detector confidence | 0.170 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.7178 |
| p_clear | 0.0 |
| p_dark | 0.2415 |
| p_review | 0.0407 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 1 |

**Reasoning:**
- No AIS track within gate radius.
- Size/shape artifact evidence: max_dim=1573 m, aspect=2.7, confidence=1.000.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (1.000) shifted 0.170 real-vessel probability to artifact.
- Artifact evidence also shifted 0.423 dark-vessel probability to artifact.
- Nearest AIS track MMSI 367546320 is 2847 m from contact (outside gate); shifting 0.041 probability from dark to review.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c6877_r8839_det0000`

| Field | Value |
|---|---|
| Center | `-120.16819, 34.47132` |
| Estimated size | 877 m × 354 m |
| Detector confidence | 0.156 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.5864 |
| p_clear | 0.0 |
| p_dark | 0.3102 |
| p_review | 0.1034 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Size/shape artifact evidence: max_dim=877 m, aspect=2.5, confidence=0.754.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (0.754) shifted 0.118 real-vessel probability to artifact.
- Artifact evidence also shifted 0.342 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c5085_r8839_det0000`

| Field | Value |
|---|---|
| Center | `-120.42700, 34.45194` |
| Estimated size | 856 m × 452 m |
| Detector confidence | 0.103 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.546 |
| p_clear | 0.0 |
| p_dark | 0.3405 |
| p_review | 0.1135 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Size/shape artifact evidence: max_dim=856 m, aspect=1.9, confidence=0.711.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (0.711) shifted 0.074 real-vessel probability to artifact.
- Artifact evidence also shifted 0.338 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c3293_r9735_det0001`

| Field | Value |
|---|---|
| Center | `-120.64603, 34.45345` |
| Estimated size | 250 m × 973 m |
| Detector confidence | 0.093 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.6776 |
| p_clear | 0.0 |
| p_dark | 0.2418 |
| p_review | 0.0806 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Hermosa (220 m away); scaled static confidence 0.482.
- Size/shape artifact evidence: max_dim=973 m, aspect=3.9, confidence=0.945.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (0.972) shifted 0.091 real-vessel probability to artifact.
- Artifact evidence also shifted 0.451 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c4189_r8839_det0001`

| Field | Value |
|---|---|
| Center | `-120.46475, 34.44849` |
| Estimated size | 1039 m × 823 m |
| Detector confidence | 0.079 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.687 |
| p_clear | 0.0 |
| p_dark | 0.2348 |
| p_review | 0.0783 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Size/shape artifact evidence: max_dim=1039 m, aspect=1.3, confidence=1.000.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (1.000) shifted 0.079 real-vessel probability to artifact.
- Artifact evidence also shifted 0.470 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vv_c9565_r7943_det0002`

| Field | Value |
|---|---|
| Center | `-119.83868, 34.41578` |
| Estimated size | 1591 m × 1543 m |
| Detector confidence | 0.077 |
| **Verdict** | **CLEAR** |
| p_artifact | 0.1781 |
| p_clear | 0.6645 |
| p_dark | 0.1575 |
| p_review | 0.0 |
| Tracks within gate | 1 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- Size/shape artifact evidence: max_dim=1591 m, aspect=1.0, confidence=1.000.
- Artifact evidence discounted by AIS match probability: (1 - 0.786)^1.00 = 0.214.
- Artifact evidence (0.214) shifted 0.016 real-vessel probability to artifact.
- Artifact evidence also shifted 0.023 dark-vessel probability to artifact.
- Best AIS match: MMSI 367104040 at 995 m (σ=2315 m), P(match)=0.786.

### `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vv_c8669_r8839_det0000`

| Field | Value |
|---|---|
| Center | `-120.03811, 34.48391` |
| Estimated size | 411 m × 398 m |
| Detector confidence | 0.064 |
| **Verdict** | **DARK** |
| p_artifact | 0.1404 |
| p_clear | 0.0 |
| p_dark | 0.6447 |
| p_review | 0.2149 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c4189_r9735_det0000`

| Field | Value |
|---|---|
| Center | `-120.46065, 34.44801` |
| Estimated size | 1681 m × 1494 m |
| Detector confidence | 0.061 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.6806 |
| p_clear | 0.0 |
| p_dark | 0.2395 |
| p_review | 0.0798 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Size/shape artifact evidence: max_dim=1681 m, aspect=1.1, confidence=1.000.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (1.000) shifted 0.061 real-vessel probability to artifact.
- Artifact evidence also shifted 0.479 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c8669_r7943_det0000`

| Field | Value |
|---|---|
| Center | `-119.94009, 34.43704` |
| Estimated size | 1367 m × 380 m |
| Detector confidence | 0.058 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.6799 |
| p_clear | 0.0 |
| p_dark | 0.2401 |
| p_review | 0.08 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Size/shape artifact evidence: max_dim=1367 m, aspect=3.6, confidence=1.000.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (1.000) shifted 0.058 real-vessel probability to artifact.
- Artifact evidence also shifted 0.480 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c9565_r7047_det0000`

| Field | Value |
|---|---|
| Center | `-119.81850, 34.35493` |
| Estimated size | 88 m × 508 m |
| Detector confidence | 0.050 |
| **Verdict** | **REVIEW** |
| p_artifact | 0.2294 |
| p_clear | 0.0 |
| p_dark | 0.578 |
| p_review | 0.1927 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Size/shape artifact evidence: max_dim=508 m, aspect=5.8, confidence=0.155.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (0.155) shifted 0.008 real-vessel probability to artifact.
- Artifact evidence also shifted 0.079 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

---

## 2. Verdict Summary Table

| Contact | Verdict | p_artifact | p_clear | p_dark | p_review | Nearest MMSI | Nearest dist (m) |
|---|---|---|---|---|---|---|---|
| `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c2397_r9735_det0000` | ARTIFACT | 0.8809 | 0.0 | 0.0893 | 0.0298 | 367546320 | 37668.4 |
| `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c2397_r9735_det0001` | ARTIFACT | 0.8768 | 0.0 | 0.0924 | 0.0308 | 367546320 | 32441.5 |
| `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c5981_r7943_det0000` | ARTIFACT | 0.8626 | 0.0 | 0.1031 | 0.0344 | 367546320 | 12893.6 |
| `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c9565_r7943_det0000` | ARTIFACT | 0.5893 | 0.0 | 0.308 | 0.1027 | 367104040 | 7491.2 |
| `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vv_c7773_r7943_det0000` | CLEAR | 0.1499 | 0.6793 | 0.1707 | 0.0 | 367104050 | 280.7 |
| `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c9565_r7943_det0001` | DARK | 0.0781 | 0.0 | 0.6914 | 0.2305 | 367104040 | 8680.7 |
| `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c4189_r8839_det0000` | ARTIFACT | 0.7873 | 0.0 | 0.1595 | 0.0532 | 367546320 | 15525.1 |
| `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c2397_r9735_det0002` | ARTIFACT | 0.7794 | 0.0 | 0.1655 | 0.0552 | 367546320 | 35583.3 |
| `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c6877_r7943_det0000` | ARTIFACT | 0.7265 | 0.0 | 0.2051 | 0.0684 | 367104050 | 4799.3 |
| `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c2397_r11527_det0000` | ARTIFACT | 0.6846 | 0.0 | 0.2365 | 0.0788 | 367546320 | 43037.9 |
| `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c5981_r8839_det0000` | ARTIFACT | 0.7178 | 0.0 | 0.2415 | 0.0407 | 367546320 | 2847.3 |
| `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c6877_r8839_det0000` | ARTIFACT | 0.5864 | 0.0 | 0.3102 | 0.1034 | 367104050 | 10228.4 |
| `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c5085_r8839_det0000` | ARTIFACT | 0.546 | 0.0 | 0.3405 | 0.1135 | 367546320 | 12420.3 |
| `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c3293_r9735_det0001` | ARTIFACT | 0.6776 | 0.0 | 0.2418 | 0.0806 | 367546320 | 32432.1 |
| `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c4189_r8839_det0001` | ARTIFACT | 0.687 | 0.0 | 0.2348 | 0.0783 | 367546320 | 15902.6 |
| `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vv_c9565_r7943_det0002` | CLEAR | 0.1781 | 0.6645 | 0.1575 | 0.0 | 367104040 | 994.7 |
| `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vv_c8669_r8839_det0000` | DARK | 0.1404 | 0.0 | 0.6447 | 0.2149 | 367104050 | 12736.6 |
| `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c4189_r9735_det0000` | ARTIFACT | 0.6806 | 0.0 | 0.2395 | 0.0798 | 367546320 | 15537.3 |
| `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c8669_r7943_det0000` | ARTIFACT | 0.6799 | 0.0 | 0.2401 | 0.08 | 367104040 | 10589.8 |
| `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3_vh_c9565_r7047_det0000` | REVIEW | 0.2294 | 0.0 | 0.578 | 0.1927 | 367104040 | 6643.5 |

---

## 3. AIS Tracks in Theater

| MMSI | Name | Messages | Avg SOG (kn) | Status(es) | Distance to contact (m) |
|---|---|---|---|---|---|
| 367104040 | KNOX T | 110 | 7.3 | 15 | ~80,743 |
| 367104050 | RYAN T | 115 | 0.7 | 0 | ~54,923 |
| 367546320 | OCEAN DEFENDER | 38 | 0.9 | 1 | ~37,668 |

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

*Generated by `scripts/fusion_report.py` on 2026-08-09T01:18:28.219085Z.*
