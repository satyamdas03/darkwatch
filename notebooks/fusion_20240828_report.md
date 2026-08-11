# Darkwatch Fusion Report

**Scene time:** 2024-08-28T02:07:13.717760
**AIS file:** `data\external\ais\ais_2024-08-28_clipped.csv`
**Association gate:** 2000.0 m
**Contacts fused:** 12
**AIS tracks loaded:** 10
**Verdict counts:** {'DARK': 9, 'CLEAR': 2, 'ARTIFACT': 1}

---

## 1. SAR Contacts

### `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vv_c21042_r14225_det0000`

| Field | Value |
|---|---|
| Center | `-120.79635, 34.70863` |
| Estimated size | 59 m × 31 m |
| Detector confidence | 0.702 |
| **Verdict** | **DARK** |
| p_artifact | 0.0447 |
| p_clear | 0.0 |
| p_dark | 0.7165 |
| p_review | 0.2388 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vh_c20146_r9745_det0000`

| Field | Value |
|---|---|
| Center | `-120.75604, 34.37546` |
| Estimated size | 295 m × 216 m |
| Detector confidence | 0.669 |
| **Verdict** | **CLEAR** |
| p_artifact | 0.0497 |
| p_clear | 0.7472 |
| p_dark | 0.2031 |
| p_review | 0.0 |
| Tracks within gate | 1 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- Best AIS match: MMSI 477035100 at 476 m (σ=328 m), P(match)=0.786.

### `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vv_c21042_r14225_det0001`

| Field | Value |
|---|---|
| Center | `-120.79303, 34.70785` |
| Estimated size | 51 m × 64 m |
| Detector confidence | 0.650 |
| **Verdict** | **DARK** |
| p_artifact | 0.0525 |
| p_clear | 0.0 |
| p_dark | 0.7106 |
| p_review | 0.2369 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vv_c21042_r14225_det0002`

| Field | Value |
|---|---|
| Center | `-120.79196, 34.70936` |
| Estimated size | 37 m × 39 m |
| Detector confidence | 0.566 |
| **Verdict** | **DARK** |
| p_artifact | 0.0652 |
| p_clear | 0.0 |
| p_dark | 0.7011 |
| p_review | 0.2337 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vv_c21042_r14225_det0005`

| Field | Value |
|---|---|
| Center | `-120.79192, 34.70719` |
| Estimated size | 44 m × 25 m |
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

### `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vv_c21042_r14225_det0006`

| Field | Value |
|---|---|
| Center | `-120.79483, 34.70786` |
| Estimated size | 87 m × 52 m |
| Detector confidence | 0.372 |
| **Verdict** | **DARK** |
| p_artifact | 0.0942 |
| p_clear | 0.0 |
| p_dark | 0.6794 |
| p_review | 0.2265 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vh_c20146_r9745_det0001`

| Field | Value |
|---|---|
| Center | `-120.75623, 34.37711` |
| Estimated size | 254 m × 518 m |
| Detector confidence | 0.249 |
| **Verdict** | **CLEAR** |
| p_artifact | 0.1153 |
| p_clear | 0.6963 |
| p_dark | 0.1884 |
| p_review | 0.0 |
| Tracks within gate | 1 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- Size/shape artifact evidence: max_dim=518 m, aspect=2.0, confidence=0.036.
- Artifact evidence discounted by AIS match probability: (1 - 0.786)^1.00 = 0.214.
- Artifact evidence (0.008) shifted 0.002 real-vessel probability to artifact.
- Artifact evidence also shifted 0.001 dark-vessel probability to artifact.
- Best AIS match: MMSI 477035100 at 305 m (σ=385 m), P(match)=0.786.

### `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vv_c21042_r14225_det0009`

| Field | Value |
|---|---|
| Center | `-120.79080, 34.70792` |
| Estimated size | 39 m × 31 m |
| Detector confidence | 0.127 |
| **Verdict** | **DARK** |
| p_artifact | 0.1309 |
| p_clear | 0.0 |
| p_dark | 0.6518 |
| p_review | 0.2173 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vv_c21042_r14225_det0010`

| Field | Value |
|---|---|
| Center | `-120.79442, 34.70895` |
| Estimated size | 76 m × 50 m |
| Detector confidence | 0.125 |
| **Verdict** | **DARK** |
| p_artifact | 0.1313 |
| p_clear | 0.0 |
| p_dark | 0.6515 |
| p_review | 0.2172 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vv_c21042_r14225_det0014`

| Field | Value |
|---|---|
| Center | `-120.79658, 34.70772` |
| Estimated size | 33 m × 105 m |
| Detector confidence | 0.066 |
| **Verdict** | **ARTIFACT** |
| p_artifact | 0.5282 |
| p_clear | 0.0 |
| p_dark | 0.3539 |
| p_review | 0.118 |
| Tracks within gate | 0 |
| Tracks near gate (1×–2×) | 0 |

**Reasoning:**
- No AIS track within gate radius.
- Size/shape artifact evidence: max_dim=105 m, aspect=3.1, confidence=0.700.
- Artifact evidence discounted by AIS match probability: (1 - 0.000)^1.00 = 1.000.
- Artifact evidence (0.700) shifted 0.046 real-vessel probability to artifact.
- Artifact evidence also shifted 0.342 dark-vessel probability to artifact.
- No AIS tracks within 2x gate radius; reducing dark confidence due to possible coverage gap.
- No AIS match within gate; contact is candidate dark vessel if real.

### `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vv_c21042_r14225_det0017`

| Field | Value |
|---|---|
| Center | `-120.79581, 34.70680` |
| Estimated size | 27 m × 10 m |
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

### `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vv_c21042_r14225_det0018`

| Field | Value |
|---|---|
| Center | `-120.79421, 34.70692` |
| Estimated size | 58 m × 20 m |
| Detector confidence | 0.055 |
| **Verdict** | **DARK** |
| p_artifact | 0.1417 |
| p_clear | 0.0 |
| p_dark | 0.6437 |
| p_review | 0.2146 |
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
| `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vv_c21042_r14225_det0000` | DARK | 0.0447 | 0.0 | 0.7165 | 0.2388 | 477117900 | 35738.8 |
| `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vh_c20146_r9745_det0000` | CLEAR | 0.0497 | 0.7472 | 0.2031 | 0.0 | 477035100 | 476.0 |
| `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vv_c21042_r14225_det0001` | DARK | 0.0525 | 0.0 | 0.7106 | 0.2369 | 477117900 | 35579.5 |
| `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vv_c21042_r14225_det0002` | DARK | 0.0652 | 0.0 | 0.7011 | 0.2337 | 477117900 | 35718.7 |
| `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vv_c21042_r14225_det0005` | DARK | 0.0781 | 0.0 | 0.6914 | 0.2305 | 477117900 | 35483.6 |
| `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vv_c21042_r14225_det0006` | DARK | 0.0942 | 0.0 | 0.6794 | 0.2265 | 477117900 | 35620.7 |
| `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vh_c20146_r9745_det0001` | CLEAR | 0.1153 | 0.6963 | 0.1884 | 0.0 | 477035100 | 304.6 |
| `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vv_c21042_r14225_det0009` | DARK | 0.1309 | 0.0 | 0.6518 | 0.2173 | 477117900 | 35537.4 |
| `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vv_c21042_r14225_det0010` | DARK | 0.1313 | 0.0 | 0.6515 | 0.2172 | 477117900 | 35729.1 |
| `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vv_c21042_r14225_det0014` | ARTIFACT | 0.5282 | 0.0 | 0.3539 | 0.118 | 477117900 | 35646.2 |
| `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vv_c21042_r14225_det0017` | DARK | 0.1414 | 0.0 | 0.644 | 0.2147 | 477117900 | 35529.8 |
| `S1A_IW_GRDH_1SDV_20240828T020701_20240828T020726_055407_06C206_BADB_vv_c21042_r14225_det0018` | DARK | 0.1417 | 0.0 | 0.6437 | 0.2146 | 477117900 | 35505.3 |

---

## 3. AIS Tracks in Theater

| MMSI | Name | Messages | Avg SOG (kn) | Status(es) | Distance to contact (m) |
|---|---|---|---|---|---|
| 338140285 | FISH THREE | 5 | 12.2 | n/a | ~93,449 |
| 367104040 | KNOX T | 112 | 8.4 | 15 | ~95,315 |
| 367104050 | RYAN T | 109 | 8.6 | 0 | ~72,132 |
| 367421980 | JACKIE C | 12 | 14.1 | n/a | ~91,600 |
| 367534910 | OCEAN SENTINEL | 34 | 0.7 | 1 | ~50,643 |
| 367653910 | ADRENALIN | 13 | 6.4 | n/a | ~92,220 |
| 403698000 | ALJAZI | 58 | 11.8 | 0 | ~48,396 |
| 477035100 | OSAKA BAY | 64 | 11.3 | 0 | ~40,710 |
| 477117900 | CSCL AUTUMN | 81 | 9.8 | 0 | ~37,841 |
| 636023250 | YM WELLSPRING | 92 | 9.4 | 0 | ~53,382 |

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

*Generated by `scripts/fusion_report.py` on 2026-08-11T01:12:05.619737Z.*
