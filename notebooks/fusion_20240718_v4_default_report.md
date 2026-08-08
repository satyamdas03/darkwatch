# Darkwatch Fusion Report

**Scene time:** 2024-07-18T01:59:06.301185
**AIS file:** `data\external\ais\ais_2024-07-18_clipped.csv`
**Association gate:** 2000.0 m
**Contacts fused:** 11
**AIS tracks loaded:** 7
**Verdict counts:** {'CLEAR': 3, 'REVIEW': 6, 'DARK': 2}

---

## 1. SAR Contacts

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r8843_det0000`

| Field | Value |
|---|---|
| Center | `-120.64816, 34.38939` |
| Estimated size | 410 m × 648 m |
| Detector confidence | 0.768 |
| **Verdict** | **CLEAR** |
| p_artifact | 0.0347 |
| p_clear | 0.759 |
| p_dark | 0.2063 |
| p_review | 0.0 |
| Tracks within gate | 1 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- Best AIS match: MMSI 636023268 at 97 m (σ=617 m), P(match)=0.786.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c5068_r7947_det0000`

| Field | Value |
|---|---|
| Center | `-120.41044, 34.33743` |
| Estimated size | 339 m × 246 m |
| Detector confidence | 0.754 |
| **Verdict** | **CLEAR** |
| p_artifact | 0.0369 |
| p_clear | 0.7573 |
| p_dark | 0.2058 |
| p_review | 0.0 |
| Tracks within gate | 1 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- Best AIS match: MMSI 636016306 at 301 m (σ=373 m), P(match)=0.786.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r9739_det0000`

| Field | Value |
|---|---|
| Center | `-120.70223, 34.49494` |
| Estimated size | 188 m × 341 m |
| Detector confidence | 0.696 |
| **Verdict** | **REVIEW** |
| p_artifact | 0.4687 |
| p_clear | 0.0 |
| p_dark | 0.3985 |
| p_review | 0.1328 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Hidalgo (98 m away); shifting 0.423 probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c6860_r7947_det0000`

| Field | Value |
|---|---|
| Center | `-120.16718, 34.37693` |
| Estimated size | 210 m × 253 m |
| Detector confidence | 0.674 |
| **Verdict** | **REVIEW** |
| p_artifact | 0.3848 |
| p_clear | 0.4837 |
| p_dark | 0.1315 |
| p_review | 0.0 |
| Tracks within gate | 1 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- Static object nearby: Platform Harmony (125 m away); shifting 0.336 probability to artifact.
- Best AIS match: MMSI 367421980 at 429 m (σ=319 m), P(match)=0.786.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c7756_r7947_det0000`

| Field | Value |
|---|---|
| Center | `-120.11937, 34.39107` |
| Estimated size | 156 m × 284 m |
| Detector confidence | 0.645 |
| **Verdict** | **CLEAR** |
| p_artifact | 0.1825 |
| p_clear | 0.6428 |
| p_dark | 0.1747 |
| p_review | 0.0 |
| Tracks within gate | 1 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- Static object nearby: Platform Hondo (200 m away); shifting 0.129 probability to artifact.
- Best AIS match: MMSI 367104050 at 294 m (σ=239 m), P(match)=0.786.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c9548_r7947_det0000`

| Field | Value |
|---|---|
| Center | `-119.90421, 34.38999` |
| Estimated size | 152 m × 186 m |
| Detector confidence | 0.635 |
| **Verdict** | **DARK** |
| p_artifact | 0.1646 |
| p_clear | 0.0 |
| p_dark | 0.6266 |
| p_review | 0.2089 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Holly (207 m away); shifting 0.110 probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r9739_det0001`

| Field | Value |
|---|---|
| Center | `-120.64639, 34.45533` |
| Estimated size | 183 m × 264 m |
| Detector confidence | 0.625 |
| **Verdict** | **REVIEW** |
| p_artifact | 0.4399 |
| p_clear | 0.0 |
| p_dark | 0.4201 |
| p_review | 0.14 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Hermosa (97 m away); shifting 0.384 probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r11531_det0000`

| Field | Value |
|---|---|
| Center | `-120.72918, 34.61017` |
| Estimated size | 192 m × 315 m |
| Detector confidence | 0.574 |
| **Verdict** | **REVIEW** |
| p_artifact | 0.3666 |
| p_clear | 0.0 |
| p_dark | 0.475 |
| p_review | 0.1583 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Irene (118 m away); shifting 0.303 probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r9739_det0002`

| Field | Value |
|---|---|
| Center | `-120.68089, 34.46891` |
| Estimated size | 211 m × 336 m |
| Detector confidence | 0.552 |
| **Verdict** | **REVIEW** |
| p_artifact | 0.422 |
| p_clear | 0.0 |
| p_dark | 0.4335 |
| p_review | 0.1445 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Harvest (89 m away); shifting 0.355 probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c5964_r7947_det0000`

| Field | Value |
|---|---|
| Center | `-120.27921, 34.35048` |
| Estimated size | 182 m × 274 m |
| Detector confidence | 0.501 |
| **Verdict** | **REVIEW** |
| p_artifact | 0.3988 |
| p_clear | 0.0 |
| p_dark | 0.4509 |
| p_review | 0.1503 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Static object nearby: Platform Heritage (88 m away); shifting 0.324 probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vv_c9548_r7947_det0000`

| Field | Value |
|---|---|
| Center | `-119.92025, 34.43174` |
| Estimated size | 260 m × 366 m |
| Detector confidence | 0.501 |
| **Verdict** | **DARK** |
| p_artifact | 0.0749 |
| p_clear | 0.0 |
| p_dark | 0.6939 |
| p_review | 0.2313 |
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
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r8843_det0000` | CLEAR | 0.0347 | 0.759 | 0.2063 | 0.0 | 636023268 | 97.2 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c5068_r7947_det0000` | CLEAR | 0.0369 | 0.7573 | 0.2058 | 0.0 | 636016306 | 301.4 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r9739_det0000` | REVIEW | 0.4687 | 0.0 | 0.3985 | 0.1328 | 636023268 | 12771.1 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c6860_r7947_det0000` | REVIEW | 0.3848 | 0.4837 | 0.1315 | 0.0 | 367421980 | 428.6 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c7756_r7947_det0000` | CLEAR | 0.1825 | 0.6428 | 0.1747 | 0.0 | 367104050 | 294.5 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c9548_r7947_det0000` | DARK | 0.1646 | 0.0 | 0.6266 | 0.2089 | 367104040 | 7661.2 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r9739_det0001` | REVIEW | 0.4399 | 0.0 | 0.4201 | 0.14 | 636023268 | 7399.7 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r11531_det0000` | REVIEW | 0.3666 | 0.0 | 0.475 | 0.1583 | 636023268 | 25687.3 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c2380_r9739_det0002` | REVIEW | 0.422 | 0.0 | 0.4335 | 0.1445 | 636023268 | 9374.1 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vh_c5964_r7947_det0000` | REVIEW | 0.3988 | 0.0 | 0.4509 | 0.1503 | 367421980 | 10892.8 |
| `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B_vv_c9548_r7947_det0000` | DARK | 0.0749 | 0.0 | 0.6939 | 0.2313 | 367104040 | 9073.8 |

---

## 3. AIS Tracks in Theater

| MMSI | Name | Messages | Avg SOG (kn) | Status(es) | Distance to contact (m) |
|---|---|---|---|---|---|
| 311039000 | CRYSTAL RAY | 1 | 9.1 | 0 | ~14,074 |
| 367104040 | KNOX T | 115 | 7.3 | 15 | ~75,567 |
| 367104050 | RYAN T | 115 | 7.8 | 0 | ~48,690 |
| 367421980 | JACKIE C | 56 | 7.9 | n/a | ~41,085 |
| 367534910 | OCEAN SENTINEL | 106 | 0.7 | 0 | ~19,724 |
| 368245430 | WMT | 35 | 8.0 | 0 | ~69,529 |
| 636016306 | MSC SOFIA PAZ | 96 | 9.1 | 0 | ~21,413 |
| 636023268 | MSC GIUSY | 97 | 9.7 | 0 | ~1,791 |

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

*Generated by `scripts/fusion_report.py` on 2026-08-08T22:56:22.428824Z.*
