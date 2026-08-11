# Darkwatch Fusion Report

**Scene time:** 2024-07-18T01:59:06.301185
**AIS file:** `data\external\ais\ais_2024-07-18_clipped.csv`
**Association gate:** 2000.0 m
**Contacts fused:** 15
**AIS tracks loaded:** 7
**Verdict counts:** {'CLEAR': 3, 'ARTIFACT': 11, 'DARK': 1}

---

## 1. SAR Contacts

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r8843_det0000`

| Field | Value |
|---|---|
| Center | `-120.64811, 34.38970` |
| Estimated size | 381 m × 714 m |
| Detector confidence | 0.730 |
| **Verdict** | **CLEAR** |
| p_artifact | 0.0908 |
| p_clear | 0.8618 |
| p_dark | 0.0474 |
| p_review | 0.0 |
| Tracks within gate | 1 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- Size/shape artifact evidence: max_dim=714 m, aspect=1.9, confidence=0.429.
- Artifact evidence discounted by AIS match probability: (1 - 0.786)^1.00 = 0.214.
- Artifact evidence (0.092) shifted 0.067 real-vessel probability to artifact.
- Artifact evidence also shifted 0.010 dark-vessel probability to artifact.
- Best AIS match: MMSI 636023268 at 126 m (σ=574 m), P(match)=0.786.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c9548_r7947_det0000`

| Field | Value |
|---|---|
| Center | `-119.90420, 34.39000` |
| Estimated size | 146 m × 197 m |
| Detector confidence | 0.538 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.8063 |
| p_clear | 0.0 |
| p_dark | 0.157 |
| p_review | 0.0366 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Holly (207 m away); scaled static confidence 0.557.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (0.557) shifted 0.299 real-vessel probability to artifact.
- Artifact evidence also shifted 0.211 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r9739_det0000`

| Field | Value |
|---|---|
| Center | `-120.68083, 34.46928` |
| Estimated size | 219 m × 434 m |
| Detector confidence | 0.436 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.9606 |
| p_clear | 0.0 |
| p_dark | 0.029 |
| p_review | 0.0104 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Harvest (93 m away); scaled static confidence 1.000.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (1.000) shifted 0.436 real-vessel probability to artifact.
- Artifact evidence also shifted 0.287 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vv_c9548_r7947_det0000`

| Field | Value |
|---|---|
| Center | `-119.92027, 34.43176` |
| Estimated size | 244 m × 376 m |
| Detector confidence | 0.366 |
| **Verdict** | **DARK** |
| p_artifact | 0.0705 |
| p_clear | 0.0 |
| p_dark | 0.8009 |
| p_review | 0.1286 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c6860_r8843_det0000`

| Field | Value |
|---|---|
| Center | `-120.16845, 34.47143` |
| Estimated size | 934 m × 383 m |
| Detector confidence | 0.297 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.9017 |
| p_clear | 0.0 |
| p_dark | 0.0767 |
| p_review | 0.0216 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Size/shape artifact evidence: max_dim=934 m, aspect=2.4, confidence=0.867.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (0.867) shifted 0.258 real-vessel probability to artifact.
- Artifact evidence also shifted 0.331 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vv_c2380_r9739_det0000`

| Field | Value |
|---|---|
| Center | `-120.64638, 34.45567` |
| Estimated size | 214 m × 248 m |
| Detector confidence | 0.229 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.9277 |
| p_clear | 0.0 |
| p_dark | 0.0553 |
| p_review | 0.017 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Hermosa (114 m away); scaled static confidence 1.000.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (1.000) shifted 0.229 real-vessel probability to artifact.
- Artifact evidence also shifted 0.393 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vv_c5068_r9739_det0000`

| Field | Value |
|---|---|
| Center | `-120.35517, 34.47627` |
| Estimated size | 314 m × 989 m |
| Detector confidence | 0.159 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.9073 |
| p_clear | 0.0 |
| p_dark | 0.072 |
| p_review | 0.0207 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Size/shape artifact evidence: max_dim=989 m, aspect=3.1, confidence=0.978.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (0.978) shifted 0.156 real-vessel probability to artifact.
- Artifact evidence also shifted 0.421 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c6860_r7947_det0000`

| Field | Value |
|---|---|
| Center | `-120.16712, 34.37723` |
| Estimated size | 264 m × 353 m |
| Detector confidence | 0.155 |
| **Verdict** | **CLEAR** |
| p_artifact | 0.1706 |
| p_clear | 0.7919 |
| p_dark | 0.0376 |
| p_review | 0.0 |
| Tracks within gate | 1 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- Physical-plausibility gate: SAR max_dim incompatible with AIS vessel length (30 m); match confidence reduced to 0.990.
- Static object nearby: Platform Harmony (141 m away); scaled static confidence 0.951.
- Artifact evidence discounted by AIS match probability: (1 - 0.779)^1.00 = 0.221.
- Artifact evidence (0.211) shifted 0.033 real-vessel probability to artifact.
- Artifact evidence also shifted 0.024 dark-vessel probability to artifact.
- Best AIS match: MMSI 367421980 at 450 m (σ=399 m), P(match)=0.786.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c7756_r7947_det0000`

| Field | Value |
|---|---|
| Center | `-120.11929, 34.39134` |
| Estimated size | 219 m × 352 m |
| Detector confidence | 0.099 |
| **Verdict** | **CLEAR** |
| p_artifact | 0.1389 |
| p_clear | 0.8193 |
| p_dark | 0.0418 |
| p_review | 0.0 |
| Tracks within gate | 1 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- Static object nearby: Platform Hondo (214 m away); scaled static confidence 0.514.
- Artifact evidence discounted by AIS match probability: (1 - 0.786)^1.00 = 0.214.
- Artifact evidence (0.110) shifted 0.011 real-vessel probability to artifact.
- Artifact evidence also shifted 0.012 dark-vessel probability to artifact.
- Best AIS match: MMSI 367104050 at 313 m (σ=332 m), P(match)=0.786.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c5964_r8843_det0000`

| Field | Value |
|---|---|
| Center | `-120.26080, 34.46961` |
| Estimated size | 1788 m × 582 m |
| Detector confidence | 0.092 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.8995 |
| p_clear | 0.0 |
| p_dark | 0.0785 |
| p_review | 0.022 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Size/shape artifact evidence: max_dim=1788 m, aspect=3.1, confidence=1.000.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (1.000) shifted 0.092 real-vessel probability to artifact.
- Artifact evidence also shifted 0.463 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c9548_r7947_det0002`

| Field | Value |
|---|---|
| Center | `-119.83824, 34.41512` |
| Estimated size | 1520 m × 1563 m |
| Detector confidence | 0.085 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.8593 |
| p_clear | 0.0 |
| p_dark | 0.1407 |
| p_review | 0.0 |
| Tracks within gate | 1 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- Physical-plausibility gate: SAR max_dim incompatible with AIS vessel length (32 m); match confidence reduced to 0.000.
- Size/shape artifact evidence: max_dim=1563 m, aspect=1.0, confidence=1.000.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (1.000) shifted 0.085 real-vessel probability to artifact.
- Artifact evidence also shifted 0.467 dark-vessel probability to artifact.
- Best AIS match: MMSI 367104040 at 1337 m (σ=2281 m), P(match)=0.786.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r9739_det0001`

| Field | Value |
|---|---|
| Center | `-120.70230, 34.49550` |
| Estimated size | 205 m × 362 m |
| Detector confidence | 0.070 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.8945 |
| p_clear | 0.0 |
| p_dark | 0.0826 |
| p_review | 0.0228 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Hidalgo (107 m away); scaled static confidence 1.000.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (1.000) shifted 0.070 real-vessel probability to artifact.
- Artifact evidence also shifted 0.474 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vv_c10444_r7947_det0000`

| Field | Value |
|---|---|
| Center | `-119.81090, 34.41815` |
| Estimated size | 1483 m × 454 m |
| Detector confidence | 0.065 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.8527 |
| p_clear | 0.0 |
| p_dark | 0.1473 |
| p_review | 0.0 |
| Tracks within gate | 1 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- Physical-plausibility gate: SAR max_dim incompatible with AIS vessel length (32 m); match confidence reduced to 0.000.
- Size/shape artifact evidence: max_dim=1483 m, aspect=3.3, confidence=1.000.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (1.000) shifted 0.065 real-vessel probability to artifact.
- Artifact evidence also shifted 0.477 dark-vessel probability to artifact.
- Best AIS match: MMSI 367104040 at 1498 m (σ=682 m), P(match)=0.786.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c4172_r8843_det0000`

| Field | Value |
|---|---|
| Center | `-120.46068, 34.44775` |
| Estimated size | 1950 m × 1129 m |
| Detector confidence | 0.062 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.8518 |
| p_clear | 0.0 |
| p_dark | 0.1482 |
| p_review | 0.0 |
| Tracks within gate | 1 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- Physical-plausibility gate: SAR max_dim incompatible with AIS vessel length (20 m); match confidence reduced to 0.000.
- Size/shape artifact evidence: max_dim=1950 m, aspect=1.7, confidence=1.000.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (1.000) shifted 0.062 real-vessel probability to artifact.
- Artifact evidence also shifted 0.478 dark-vessel probability to artifact.
- Best AIS match: MMSI 367534910 at 1644 m (σ=1694 m), P(match)=0.786.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c6860_r8843_det0001`

| Field | Value |
|---|---|
| Center | `-120.23315, 34.47135` |
| Estimated size | 877 m × 325 m |
| Detector confidence | 0.052 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.7771 |
| p_clear | 0.0 |
| p_dark | 0.1821 |
| p_review | 0.0408 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Size/shape artifact evidence: max_dim=877 m, aspect=2.7, confidence=0.755.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (0.755) shifted 0.039 real-vessel probability to artifact.
- Artifact evidence also shifted 0.371 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

---

## 2. Verdict Summary Table

| Contact | Verdict | p_artifact | p_clear | p_dark | p_review | Nearest MMSI | Nearest dist (m) |
|---|---|---|---|---|---|---|---|
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r8843_det0000` | CLEAR | 0.0908 | 0.8618 | 0.0474 | 0.0 | 636023268 | 125.7 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c9548_r7947_det0000` | ARTIFACT | 0.8063 | 0.0 | 0.157 | 0.0366 | 367104040 | 7660.5 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r9739_det0000` | ARTIFACT | 0.9606 | 0.0 | 0.029 | 0.0104 | 636023268 | 9412.4 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vv_c9548_r7947_det0000` | DARK | 0.0705 | 0.0 | 0.8009 | 0.1286 | 367104040 | 9076.0 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c6860_r8843_det0000` | ARTIFACT | 0.9017 | 0.0 | 0.0767 | 0.0216 | 367104050 | 10290.8 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vv_c2380_r9739_det0000` | ARTIFACT | 0.9277 | 0.0 | 0.0553 | 0.017 | 636023268 | 7437.2 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vv_c5068_r9739_det0000` | ARTIFACT | 0.9073 | 0.0 | 0.072 | 0.0207 | 367534910 | 8880.2 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c6860_r7947_det0000` | CLEAR | 0.1706 | 0.7919 | 0.0376 | 0.0 | 367421980 | 450.2 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c7756_r7947_det0000` | CLEAR | 0.1389 | 0.8193 | 0.0418 | 0.0 | 367104050 | 313.3 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c5964_r8843_det0000` | ARTIFACT | 0.8995 | 0.0 | 0.0785 | 0.022 | 367421980 | 13842.9 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c9548_r7947_det0002` | ARTIFACT | 0.8593 | 0.0 | 0.1407 | 0.0 | 367104040 | 1336.5 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r9739_det0001` | ARTIFACT | 0.8945 | 0.0 | 0.0826 | 0.0228 | 636023268 | 12831.0 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vv_c10444_r7947_det0000` | ARTIFACT | 0.8527 | 0.0 | 0.1473 | 0.0 | 367104040 | 1497.7 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c4172_r8843_det0000` | ARTIFACT | 0.8518 | 0.0 | 0.1482 | 0.0 | 367534910 | 1644.0 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c6860_r8843_det0001` | ARTIFACT | 0.7771 | 0.0 | 0.1821 | 0.0408 | 367421980 | 12536.5 |

---

## 3. AIS Tracks in Theater

| MMSI | Name | Messages | Avg SOG (kn) | Status(es) | Distance to contact (m) |
|---|---|---|---|---|---|
| 311039000 | CRYSTAL RAY | 1 | 9.1 | 0 | ~14,071 |
| 367104040 | KNOX T | 115 | 7.3 | 15 | ~75,561 |
| 367104050 | RYAN T | 115 | 7.8 | 0 | ~48,686 |
| 367421980 | JACKIE C | 56 | 7.9 | n/a | ~41,083 |
| 367534910 | OCEAN SENTINEL | 106 | 0.7 | 0 | ~19,709 |
| 368245430 | WMT | 35 | 8.0 | 0 | ~69,525 |
| 636016306 | MSC SOFIA PAZ | 96 | 9.1 | 0 | ~21,418 |
| 636023268 | MSC GIUSY | 97 | 9.7 | 0 | ~1,799 |

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

*Generated by `scripts/fusion_report.py` on 2026-08-11T00:09:32.615383Z.*
