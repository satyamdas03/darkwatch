# Darkwatch Fusion Report

**Scene time:** 2024-07-18T01:59:06.301185
**AIS file:** `data\external\ais\ais_2024-07-18_clipped.csv`
**Association gate:** 2000.0 m
**Contacts fused:** 12
**AIS tracks loaded:** 7
**Verdict counts:** {'CLEAR': 3, 'REVIEW': 5, 'DARK': 3, 'ARTIFACT': 1}

---

## 1. SAR Contacts

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r8843_det0000`

| Field | Value |
|---|---|
| Center | `-120.64816, 34.38953` |
| Estimated size | 426 m × 622 m |
| Detector confidence | 0.828 |
| **Verdict** | **CLEAR** |
| p_artifact | 0.0259 |
| p_clear | 0.7659 |
| p_dark | 0.2082 |
| p_review | 0.0 |
| Tracks within gate | 1 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- Best AIS match: MMSI 636023268 at 108 m (σ=641 m), P(match)=0.786.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c5068_r7947_det0000`

| Field | Value |
|---|---|
| Center | `-120.41048, 34.33748` |
| Estimated size | 349 m × 242 m |
| Detector confidence | 0.814 |
| **Verdict** | **CLEAR** |
| p_artifact | 0.0279 |
| p_clear | 0.7644 |
| p_dark | 0.2078 |
| p_review | 0.0 |
| Tracks within gate | 1 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- Best AIS match: MMSI 636016306 at 308 m (σ=366 m), P(match)=0.786.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c6860_r7947_det0000`

| Field | Value |
|---|---|
| Center | `-120.16718, 34.37697` |
| Estimated size | 208 m × 271 m |
| Detector confidence | 0.738 |
| **Verdict** | **REVIEW** |
| p_artifact | 0.4062 |
| p_clear | 0.4669 |
| p_dark | 0.1269 |
| p_review | 0.0 |
| Tracks within gate | 1 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- Static object nearby: Platform Harmony (126 m away); shifting 0.367 probability to artifact.
- Best AIS match: MMSI 367421980 at 432 m (σ=315 m), P(match)=0.786.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c9548_r7947_det0000`

| Field | Value |
|---|---|
| Center | `-119.90424, 34.39007` |
| Estimated size | 179 m × 199 m |
| Detector confidence | 0.699 |
| **Verdict** | **DARK** |
| p_artifact | 0.1719 |
| p_clear | 0.0 |
| p_dark | 0.6211 |
| p_review | 0.207 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Holly (205 m away); shifting 0.127 probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r9739_det0000`

| Field | Value |
|---|---|
| Center | `-120.68095, 34.46893` |
| Estimated size | 239 m × 355 m |
| Detector confidence | 0.681 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.5043 |
| p_clear | 0.0 |
| p_dark | 0.3718 |
| p_review | 0.1239 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Harvest (82 m away); shifting 0.456 probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r11531_det0000`

| Field | Value |
|---|---|
| Center | `-120.72916, 34.61019` |
| Estimated size | 196 m × 328 m |
| Detector confidence | 0.670 |
| **Verdict** | **REVIEW** |
| p_artifact | 0.4008 |
| p_clear | 0.0 |
| p_dark | 0.4494 |
| p_review | 0.1498 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Irene (119 m away); shifting 0.351 probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r9739_det0001`

| Field | Value |
|---|---|
| Center | `-120.70224, 34.49479` |
| Estimated size | 198 m × 333 m |
| Detector confidence | 0.650 |
| **Verdict** | **REVIEW** |
| p_artifact | 0.4435 |
| p_clear | 0.0 |
| p_dark | 0.4174 |
| p_review | 0.1391 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Hidalgo (100 m away); shifting 0.391 probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c7756_r7947_det0000`

| Field | Value |
|---|---|
| Center | `-120.11934, 34.39109` |
| Estimated size | 188 m × 287 m |
| Detector confidence | 0.630 |
| **Verdict** | **CLEAR** |
| p_artifact | 0.1736 |
| p_clear | 0.6498 |
| p_dark | 0.1766 |
| p_review | 0.0 |
| Tracks within gate | 1 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- Static object nearby: Platform Hondo (203 m away); shifting 0.118 probability to artifact.
- Best AIS match: MMSI 367104050 at 295 m (σ=286 m), P(match)=0.786.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r9739_det0002`

| Field | Value |
|---|---|
| Center | `-120.64644, 34.45541` |
| Estimated size | 206 m × 317 m |
| Detector confidence | 0.621 |
| **Verdict** | **REVIEW** |
| p_artifact | 0.4403 |
| p_clear | 0.0 |
| p_dark | 0.4198 |
| p_review | 0.1399 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Hermosa (96 m away); shifting 0.384 probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c5964_r7947_det0000`

| Field | Value |
|---|---|
| Center | `-120.27931, 34.35086` |
| Estimated size | 200 m × 327 m |
| Detector confidence | 0.574 |
| **Verdict** | **REVIEW** |
| p_artifact | 0.4212 |
| p_clear | 0.0 |
| p_dark | 0.4341 |
| p_review | 0.1447 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Heritage (94 m away); shifting 0.357 probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c5964_r8843_det0000`

| Field | Value |
|---|---|
| Center | `-120.25997, 34.46972` |
| Estimated size | 1700 m × 606 m |
| Detector confidence | 0.362 |
| **Verdict** | **DARK** |
| p_artifact | 0.0958 |
| p_clear | 0.0 |
| p_dark | 0.6782 |
| p_review | 0.2261 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c9548_r7947_det0001`

| Field | Value |
|---|---|
| Center | `-119.92025, 34.43219` |
| Estimated size | 283 m × 397 m |
| Detector confidence | 0.326 |
| **Verdict** | **DARK** |
| p_artifact | 0.1012 |
| p_clear | 0.0 |
| p_dark | 0.6741 |
| p_review | 0.2247 |
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
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r8843_det0000` | CLEAR | 0.0259 | 0.7659 | 0.2082 | 0.0 | 636023268 | 108.1 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c5068_r7947_det0000` | CLEAR | 0.0279 | 0.7644 | 0.2078 | 0.0 | 636016306 | 307.7 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c6860_r7947_det0000` | REVIEW | 0.4062 | 0.4669 | 0.1269 | 0.0 | 367421980 | 432.2 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c9548_r7947_det0000` | DARK | 0.1719 | 0.0 | 0.6211 | 0.207 | 367104040 | 7661.7 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r9739_det0000` | ARTIFACT | 0.5043 | 0.0 | 0.3718 | 0.1239 | 636023268 | 9378.7 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r11531_det0000` | REVIEW | 0.4008 | 0.0 | 0.4494 | 0.1498 | 636023268 | 25689.3 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r9739_det0001` | REVIEW | 0.4435 | 0.0 | 0.4174 | 0.1391 | 636023268 | 12755.8 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c7756_r7947_det0000` | CLEAR | 0.1736 | 0.6498 | 0.1766 | 0.0 | 367104050 | 294.7 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r9739_det0002` | REVIEW | 0.4403 | 0.0 | 0.4198 | 0.1399 | 636023268 | 7408.6 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c5964_r7947_det0000` | REVIEW | 0.4212 | 0.0 | 0.4341 | 0.1447 | 367421980 | 10891.9 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c5964_r8843_det0000` | DARK | 0.0958 | 0.0 | 0.6782 | 0.2261 | 367421980 | 13803.4 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c9548_r7947_det0001` | DARK | 0.1012 | 0.0 | 0.6741 | 0.2247 | 367104040 | 9086.1 |

---

## 3. AIS Tracks in Theater

| MMSI | Name | Messages | Avg SOG (kn) | Status(es) | Distance to contact (m) |
|---|---|---|---|---|---|
| 311039000 | CRYSTAL RAY | 1 | 9.1 | 0 | ~14,070 |
| 367104040 | KNOX T | 115 | 7.3 | 15 | ~75,566 |
| 367104050 | RYAN T | 115 | 7.8 | 0 | ~48,690 |
| 367421980 | JACKIE C | 56 | 7.9 | n/a | ~41,086 |
| 367534910 | OCEAN SENTINEL | 106 | 0.7 | 0 | ~19,720 |
| 368245430 | WMT | 35 | 8.0 | 0 | ~69,530 |
| 636016306 | MSC SOFIA PAZ | 96 | 9.1 | 0 | ~21,417 |
| 636023268 | MSC GIUSY | 97 | 9.7 | 0 | ~1,797 |

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

*Generated by `scripts/fusion_report.py` on 2026-08-05T22:54:38.957762Z.*
