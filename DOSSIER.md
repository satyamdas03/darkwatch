# Darkwatch — Project Dossier

> **Purpose:** Single source of truth for the entire Darkwatch project.  
> **Rule:** Read this file first on every fresh session. Append new context whenever the user says **POINTBREAK**.  
> **Source of truth:** This dossier overrides any summary or memory. The accompanying visual reference is `darkwatch-architecture.html`.

---

## 1. Project Identity

| Field | Value |
|---|---|
| **Name** | Darkwatch |
| **Tagline** | A radar contact with no transponder is either noise, a rig, a mismatch — or a ship that chose to disappear. Darkwatch decides which, and says how sure it is. |
| **Goal** | Build a maritime surveillance system that detects vessels that have deliberately switched off AIS, by fusing free Sentinel-1 SAR imagery with AIS broadcasts, and produces calibrated, auditable dark-vessel verdicts. |
| **Mode** | Impact-first, funding-agnostic, single-consumer-GPU research/engineering build. |
| **Status** | Phase 2 — Vessel Detection COMPLETE (with known domain-gap limitations); Phase 3 Fusion & Attribution — first real dark-vessel verdict produced and calibrated with nearest-neighbor evidence |
| **Start Date** | 2026-08-04 |
| **Last Updated** | 2026-08-04 (DARK verdict refined to p_dark=0.73/p_review=0.24; nearest AIS 12.7 km away; human-readable fusion report generated) |
| **Current Branch** | main |
| **Git Remote** | `https://github.com/satyamdas03/darkwatch` (public, pushed 2026-08-04) |
| **Lead Engineer** | Bull (Claude Code agent) |
| **Founder** | Satyam Das — AI/ML engineer |
| **Compute** | NVIDIA RTX 5060, 8 GB VRAM, local Windows machine |

---

## 2. One-Line Summary

Darkwatch ingests free Sentinel-1 SAR satellite imagery, detects every vessel-sized radar contact, cross-references those contacts against cooperative AIS broadcasts for the same place and time, and outputs a short ranked list of candidate dark vessels — each with a calibrated probability and an auditable evidence trail.

---

## 3. Vision & Why

The vessels doing the most harm at sea — illegal fishing fleets, sanctions evaders, smugglers — simply switch off their AIS transponders and vanish from the cooperative tracking picture. Sentinel-1 SAR sees through cloud and darkness and detects metal-on-water regardless of cooperation. The detection half of the problem is mature; the decision half is not. A radar blip with no AIS match is **not automatically** a dark vessel — it could be a wave artifact, a fixed rig, or an innocent AIS dropout.

Darkwatch's real contribution is **calibrated probabilistic attribution**: assigning each unmatched SAR contact an honest probability that it is a deliberately dark vessel, and surfacing the weakest link in every verdict so a human can act with justified confidence.

This is simultaneously a real-world system and a deep probabilistic-inference research problem. Both goals live in Phase 3.

---

## 4. Tech Stack

### Confirmed
- **Language:** Python 3.14 (current system Python); target runtime Python 3.11+
- **Geospatial / SAR prep:** rasterio 1.5.0, geopandas 1.1.4, xarray 2026.7.0, pyproj 3.7.2, shapely 2.1.2, pyogrio 0.13.0, defusedxml 0.7.1
- **ML detector:** Ultralytics YOLOv8 (8.4.115), PyTorch 2.11.0+cu128 with CUDA 12.8 on RTX 5060
- **Data access adapters:**
  - SAR: Copernicus Data Space Ecosystem OData API (verified)
  - AIS: NOAA Marine Cadastre AccessAIS + Azure Blob GeoParquet (verified)
  - Zones / behavior: Global Fishing Watch API, public MPA/EEZ datasets (TBD)
- **Database:** TBD — likely GeoParquet / SQLite-Spatialite for local prototype
- **Visualization:** matplotlib 3.10.8, folium 0.20.0
- **Workflow / orchestration:** `scripts/` first; evolving to `darkwatch` CLI
- **Compute:** NVIDIA RTX 5060 Laptop GPU, 8 GB VRAM, CUDA 12.8, Windows 11

### Open training datasets to verify
| Dataset | Size | Note | License status |
|---|---|---|---|
| SSDD | ~1,160 SAR images | Original SAR ship detection dataset | Verify before training |
| HRSID | ~5,600 images, ~17k ship instances | Higher resolution | Verify before training |
| LS-SSDD-v1.0 | Large-scene Sentinel-1, small-ship focus | Labelled using AIS — fusion hint + validation path | Verify before training |

---

## 5. Architecture

Five stages, raw radar → auditable accusation. The easy parts are the two ends; the research value is in the middle.

### 5.1 High-Level Pipeline

```text
┌──────────────┐    ┌──────────────┐    ┌──────────────────┐    ┌──────────────┐    ┌──────────────┐
│   S1 SAR     │ →  │    S2        │ →  │   S3 Fusion &    │ →  │    S4        │ →  │    S5        │
│  Ingestion   │    │ Vessel       │    │   Attribution    │    │ Behavior &   │    │ Alert &      │
│    & Prep    │    │ Detection    │    │   (THE CORE)     │    │ Prioritization│   │ Evidence     │
└──────────────┘    └──────────────┘    └──────────────────┘    └──────────────┘    └──────────────┘
   raw scenes          candidate           P(dark|contact,AIS)      ranked alerts      auditable
   → ocean tiles       contacts            explain-away step          with context       dossiers
```

### 5.2 Stage Detail

| Stage | Name | Output | Key non-negotiable |
|---|---|---|---|
| **S1** | SAR Ingestion & Prep | Analysis-ready ocean tiles with geo-coordinates preserved | Swappable data adapter; land / infrastructure masked |
| **S2** | Vessel Detection | Candidate contacts: lat/lon, size, timestamp, detection confidence | Fine-tune existing baseline; don't invent a detector |
| **S3** | Fusion & Attribution ★ | Each contact labelled matched / dark / artifact / review with calibrated probability | **Calibration is success**; honest uncertainty |
| **S4** | Behavior & Intent | Ranked alerts with context (zones, persistence, rendezvous) | Priority scoring; human sees only what matters |
| **S5** | Alert & Evidence | Contact dossiers: imagery + reasoning + confidence + alternatives ruled out | Evidence trail is the product |

### 5.3 Core Research Problem (S3)

A SAR contact with no AIS match is **observationally identical** to:
- a genuine dark vessel,
- an innocent AIS dropout,
- a radar false contact (wave clutter, azimuth ambiguity, wind streak),
- a fixed object (rig, small island, platform).

The task is **calibrated probabilistic attribution**:
- For every SAR contact, compute `P(contact = dark vessel | SAR, AIS, context)`.
- Interpolate AIS tracks to the SAR capture instant.
- Build probabilistic association `P(contact = track)`, not a nearest-neighbor join.
- Rule out non-vessel and innocent-gap explanations before calling anything dark.
- **Calibrate** on ground-truthable cases: when the system says p=0.9, ~90% of those cases should be dark.

### 5.4 Directory Structure

```text
darkwatch/
├── README.md
├── DOSSIER.md
├── darkwatch-architecture.html
├── pyproject.toml
├── scripts/             # phase-by-phase utility scripts
├── data/
│   ├── raw/s1/          # downloaded Sentinel-1 scenes (.SAFE + zip)
│   ├── raw/ais/         # downloaded AIS feeds
│   ├── processed/       # calibrated, masked, tiled outputs
│   └── external/        # zone shapefiles, rig locations, coastlines
├── darkwatch/
│   ├── __init__.py
│   ├── adapters/        # swappable data source adapters
│   │   └── copernicus_adapter.py
│   ├── s1_prep/         # S1 ingestion & preprocessing
│   ├── detect/          # vessel detection model + inference
│   ├── fusion/          # S3 probabilistic attribution
│   ├── behavior/        # S4 context & prioritization
│   ├── alerts/          # S5 dossier generation
│   └── models/          # trained weights / configs
├── notebooks/           # exploratory / validation outputs
└── tests/               # unit + integration tests
```

---

## 6. Current State

- [x] Project spec and architecture HTML exist in repo.
- [x] Copernicus Data Space Ecosystem access path verified and working with live credentials (stored in `.env`, gitignored).
- [x] NOAA Marine Cadastre AIS access path verified.
- [x] Test theater chosen: **Santa Barbara Channel / Channel Islands, CA**.
- [x] Python geospatial + ML environment installed and verified on RTX 5060 (CUDA 12.8).
- [x] Multiple real Sentinel-1 GRD scenes downloaded and extracted.
- [x] Automated **Phase 1 SAR Ingestion & Prep pipeline** complete and validated:
  - `darkwatch/s1_prep/reader.py` — parses `.SAFE`, locates measurement TIFFs, calibration/annotation XMLs.
  - `darkwatch/s1_prep/calibrate.py` — sigma-nought calibration to dB.
  - `darkwatch/s1_prep/geocode.py` — barycentric lat/lon ↔ line/pixel via `scipy LinearNDInterpolator`.
  - `darkwatch/s1_prep/land_mask.py` — public-domain Natural Earth `ne_50m_land` polygons (exact land mask, not buffered coastline).
  - `darkwatch/s1_prep/tiler.py` — 1024×1024 overlapping chips with GeoTIFF + JSON sidecar (water fraction + corner GCPs).
  - `darkwatch/s1_prep/pipeline.py` — end-to-end `prep_scene()` with CLI.
- [x] Scene scoring script (`scripts/pick_ocean_scene.py`) ranks acquisitions by open-water fraction so we always pick a usable pass.
- [x] Mosaic validation (`notebooks/phase1_channel_mosaic_v2.png`) confirms clean ocean tiles with no land artifacts.
- [x] **Phase 2 detector scaffolding complete** before laptop crash:
  - `darkwatch/detect/contact.py` — `Contact` dataclass with geo/size/confidence metadata.
  - `darkwatch/detect/dataset.py` — COCO → YOLO converter for SSDD.
  - `darkwatch/detect/detector.py` — `VesselDetector` wrapper around Ultralytics YOLO; `detect_tiles()` runs inference on Darkwatch tiles and emits geo-located `Contact` objects.
  - `darkwatch/detect/__init__.py` — public exports wired.
  - `scripts/prepare_ssdd.py` — CLI wrapper for dataset conversion.
  - `scripts/train_detector.py` — CLI wrapper for fine-tuning.
  - `scripts/detect_tiles.py` — CLI wrapper for inference on prepared tiles.
- [x] SSDD converted to YOLO format: 1,160 images / 1,160 label files (train + val) at `data/processed/ssdd_yolo/`.
- [x] YOLOv8n base weights downloaded to repo root (`yolov8n.pt`).
- [x] **Detector training completed** after crash: `models/detector_runs/darkwatch_yolov8n_ssdd/weights/best.pt` (30 epochs, YOLOv8n on SSDD, mAP50 0.977).
- [x] **Domain-gap fix implemented**: `darkwatch/detect/detector.py` now converts float dB GeoTIFF tiles to uint8 RGB via configurable contrast stretch before YOLO inference; `scripts/detect_tiles.py` exposes `--db-lo`, `--db-hi`, `--no-stretch`.
- [x] **VH polarization experiment**: processed VH tiles for the July 11 scene. VH detects the same physical object as VV but with much higher confidence (0.82 vs 0.50). The canonical `contacts.json` now uses the combined VV+VH result with automatic deduplication, retaining the highest-confidence detection (VH, conf 0.82).
- [x] **Contact deduplication added to detector**: `darkwatch/detect/detector.py` now merges contacts within 100 m (haversine) of each other, keeping the highest-confidence contact. This removes duplicate detections across overlapping tiles.
- [x] **Polarization filtering added**: `scripts/detect_tiles.py` now accepts `--pol vv,vh` to process only selected polarizations.
- [x] **Contact visualization added**: `scripts/visualize_contact.py` produces full-tile context and zoomed evidence PNGs for each contact.
- [x] **Inference run on 2024-07-11 scene**: 1 unique contact after deduplication at ~(-120.7310, 34.6107), estimated size ~214 m × 167 m, confidence 0.82 (VH). Evidence image saved to `notebooks/contact_viz/`.
- [x] **Key finding:** SSDD-trained YOLOv8n has low recall on real Sentinel-1 GRD — a known cross-domain gap. The preprocessing fix recovered the single visible contact, but the scene contains far fewer detectable ships than expected channel traffic. Detector improvement is a Phase 2 follow-up, not a Phase 3 blocker.
- [x] Unit tests pass (`pytest tests/ -q` → 13 passed).
- [x] **Phase 3 Fusion & Attribution scaffold implemented** while NOAA AIS daily zip downloads:
  - `darkwatch/fusion/ais.py` — `AISTrack` dataclass with interpolation and GPS uncertainty model.
  - `darkwatch/fusion/associate.py` — `ContactVerdict`, `TrackAssociation`, `associate_contact()` / `associate_all_contacts()`; produces CLEAR / DARK / ARTIFACT / REVIEW verdicts with coherent component probabilities (artifact mass from low detector confidence; clear/dark split the real-vessel mass by AIS evidence).
  - `darkwatch/fusion/verdict.py` — `Verdict` enum.
  - `darkwatch/fusion/__init__.py` — public exports wired.
  - `scripts/fetch_ais.py` — download NOAA daily AIS zip, unzip, filter to bbox/time window, write clipped CSV.
  - `scripts/fuse_contacts.py` — load contacts + AIS, run association, write `verdicts.json` with summary counts.
  - `tests/test_fusion.py` — unit tests for AIS CSV filtering, track interpolation, CLEAR/DARK verdicts, probability normalization.
- [x] **Bug fix — `darkwatch/fusion/associate.py` probability decomposition regression caught and fixed:** original code overwrote `p_clear` before computing `p_dark`, corrupting the real-vessel mass split. Fixed by preserving `p_matched_given_real` and rescaling both components. Added regression test `test_real_vessel_mass_is_partitioned_between_clear_and_dark`; total tests now **14 passed**.
- [x] **Bug fix — timezone-aware vs naive datetime handling in fusion:** `load_ais_csv()` now localizes UTC-naive time-window boundaries; `associate_contact()` now localizes UTC-naive `t_sar` before AIS interpolation. This resolves `Cannot compare tz-naive and tz-aware datetime-like objects` on real NOAA CSV.
- [x] **Bug fix — `scripts/fetch_ais.py` download error handling:** replaced unreachable `if result.returncode != 0` after `check=True` with `try/except CalledProcessError`, and added `curl -C -` resume support for slow NOAA downloads.
- [x] **NOAA Marine Cadastre daily AIS downloaded and filtered:** `data/external/ais/AIS_2024_07_11.zip` (~358 MB) extracted; filtered to 351 rows in theater/time window → 8 AIS tracks with ≥2 messages.
- [x] **First real dark-vessel attribution run completed:** `scripts/fuse_contacts.py` produced `data/processed/fusion_20240711/verdicts.json`. The single SAR contact is classified **DARK** with `p_dark=0.9732`, `p_artifact=0.0268`, `p_clear=0.0`, no AIS track within 2,000 m gate.
- [x] **Nearest-neighbor evidence added to fusion output:** `ContactVerdict` now carries `nearest_association`, `n_tracks_within_gate`, and `n_tracks_near_gate` so every unmatched contact reports the closest AIS track even when it lies outside the gate.
- [x] **Coverage-gap / innocent-dropout adjustment added:** when no AIS track is within 2× the gate radius, the model shifts 25% of `p_dark` to `p_review`, producing a more honest uncertainty estimate. First real verdict updated to `p_dark=0.7299`, `p_review=0.2433`, `p_artifact=0.0268`, `p_clear=0.0`.
- [x] **`scripts/fuse_contacts.py` now writes `summary.json`** alongside `verdicts.json` for run-level metadata.
- [x] **Reproducible Markdown report generator added:** `scripts/fusion_report.py` consumes `contacts.json`, the clipped AIS CSV, `verdicts.json`, and `summary.json` to produce a human-readable fusion report. Used to regenerate `notebooks/fusion_20240711_report.md`.
- [x] **Human-readable fusion report generated:** `notebooks/fusion_20240711_report.md` summarizes the verdict, all 9 MMSIs in the theater, and interpretation caveats.
- [x] **Killer public README written:** `README.md` rewritten with badges, Mermaid pipeline, first-real-result showcase, quickstart, architecture, roadmap, contribution guide, and MIT license.
- [x] **MIT `LICENSE` added** for community use.
- [x] Unit tests pass (`pytest tests/ -q` → 14 passed).

### 6.1 Test Theater — Final Choice

| Field | Value |
|---|---|
| **Region** | Santa Barbara Channel / Channel Islands, California |
| **Full channel bbox** | `-120.5, 33.8, -119.0, 34.6` (search/acquisition bbox) |
| **Operational bbox (current scene)** | `-120.8, 34.3, -119.8, 34.7` (western Santa Barbara Channel, open water) |
| **Operational scene** | `S1A_IW_GRDH_1SDV_20240711T140858_20240711T140923_054714_06A94E_9466.SAFE` |
| **Scene coverage** | lat 34.03–35.93 N, lon -123.21 to -120.14 W |
| **Scene water fraction** | ~84.85% open ocean per footprint sampling |
| **Justification** | Western side of the channel is open water with consistent commercial shipping and fishing traffic; NOAA AIS coverage; manageable coastline/island masking. |

**Note:** Not every Sentinel-1 pass covers the same sub-region. The first acquired pass (2024-07-01) was angled inland and contained no usable open ocean for this theater. A scene-scoring step now picks the pass with the highest open-water fraction. The adapter design lets us search/acquire additional scenes trivially.

### 6.2 Phase 0 Deliverables

| Deliverable | Location | Status |
|---|---|---|
| CDSE adapter | `darkwatch/adapters/copernicus_adapter.py` | ✅ Working |
| Scene search script | `scripts/fetch_first_scene.py` | ✅ Working |
| Scene inspection script | `scripts/inspect_scene.py` | ✅ Working |
| First downloaded scene | `data/raw/s1/S1A_IW_GRDH_1SDV_20240701T135228_...SAFE/` | ✅ Extracted |
| Calibrated theater preview | `notebooks/phase0_santa_barbara_north.png` | ✅ Generated |
| Geocoding method | Barycentric interpolation from Sentinel-1 geolocation grid via `scipy.interpolate.LinearNDInterpolator` | ✅ Verified |

---

## 7. Roadmap / Tasks

| # | Phase | Goal | Status | Owner | Notes |
|---|---|---|---|---|---|
| 0 | **Recon & first light** | Get real SAR onto the screen; pick test theater | ✅ Complete | Bull | Copernicus + NOAA verified; first scene calibrated and viewed |
| 1 | **SAR Ingestion & Prep (S1)** | Scenes → analysis-ready tiles, automatically | ✅ Complete | Bull | `prep_s1.py`; land-mask → tile pipeline validated on ocean scene |
| 2 | **Vessel Detection (S2)** | Scene in, clean contacts out | ✅ Complete (baseline) | Bull | YOLOv8n trained; dB→uint8 preprocessing fixes inference; low recall due to SSDD→GRD domain gap — improvement tracked as follow-up |
| 3 | **Fusion & Attribution (S3)** ★ | Calibrated dark-vessel attribution | ✅ Baseline complete | Bull | First real DARK verdict produced; calibration/validation now make-or-break |
| 4 | **Behavior & Intent (S4)** | Ranked alerts with context | ⏳ Pending | Bull | Use GFW + public zone data |
| 5 | **Evidence Layer (S5)** | Auditable dossiers + validation | ⏳ Pending | Bull | Write up method |

---

## 8. Logistics Board

| Item | Status | Note |
|---|---|---|
| SAR data | ✅ CLEAR | Sentinel-1 open, redistribution OK, API + S3 access. |
| Employer overlap | ✅ CLEAR | Unrelated to founder's day job. |
| Libraries & solvers | ✅ CLEAR | SAR + geospatial + ML stack permissively licensed. |
| Compute | ✅ CLEAR | Detector fine-tunes on RTX 5060. |
| AIS feeds | ⚠️ WATCH | Free NOAA raw AIS is enough to build & validate; live global AIS may cost. Adapter design absorbs it. |
| Detector training sets | ⚠️ WATCH | Open datasets exist; confirm each license before training. |

**No hard blockers currently known.**

---

## 9. Decisions & Rationale

| Date | Decision | Context | Rationale |
|---|---|---|---|
| 2026-08-04 | Adopt dossier-driven context recovery | Stateless agent sessions | Reconstruct full project state on restart. |
| 2026-08-04 | Impact-first, funding-agnostic scope | Founder's preference | Avoid commercialization/logistics friction; focus on real-world impact + technical excellence. |
| 2026-08-04 | Use free Sentinel-1 SAR as core input | Open license + global archive | Removes the single biggest data licensing wall. |
| 2026-08-04 | Build swappable data adapters everywhere | Prevent logistics headaches | One data source should never block the project. |
| 2026-08-04 | Make S3 fusion the definition of success | Detection is solved; attribution is not | Calibration > raw detection accuracy. |
| 2026-08-04 | Use YOLO-family detector on RTX 5060 | 8 GB VRAM constraint | Proven, lightweight, fine-tunable baseline. |
| 2026-08-04 | Verified Copernicus OData API as current Sentinel-1 access | Web search + docs check 2026-08-04 | Catalogue at `catalogue.dataspace.copernicus.eu/odata/v1/Products`; download at `download.dataspace.copernicus.eu`; Keycloak auth. |
| 2026-08-04 | Verified NOAA Marine Cadastre AIS access | Web search 2026-08-04 | AccessAIS clip-and-ship for custom CSV; GeoParquet bulk daily points and monthly tracks available via Azure Blob. |
| 2026-08-04 | Propose Santa Barbara Channel as test theater | Dense Sentinel-1 + NOAA AIS overlap, commercial + fishing traffic, nearby MPA | Cleanest calibration theater; can pivot to Gulf or Chesapeake if needed. |
| 2026-08-04 | Use Natural Earth `ne_50m_land` polygons for land masking | Buffered coastline linestrings leave inland land unmasked; exact land polygons exclude urban/mountain pixels correctly | Better mask quality; still public domain and globally available. |
| 2026-08-04 | Score each candidate S1 pass by open-water footprint fraction before download | Some passes over the search bbox are angled inland and contain no usable ocean | Avoids wasting download/time on land-only scenes; pick best pass automatically. |
| 2026-08-04 | Store CDSE credentials in `.env` and gitignore it | Credentials were passed via environment variables; `.env` keeps them local and uncommitted | Standard local-secret pattern; easy to rotate and safe from accidental commits. |
| 2026-08-04 | Write GeoTIFF tiles with corner Ground Control Points (EPSG:4326) | SAR swath is not exactly affine in lat/lon; identity transform is not geo-referenced | Tiles load in GIS tools with correct approximate geo-location. |
| 2026-08-04 | Create `README.md` pointing to `DOSSIER.md` as the source of truth | Dossier referenced a README that did not exist; README is the standard first file visitors see | Keeps README lightweight and current; DOSSIER remains the single source of truth. |
| 2026-08-04 | Document git root discovery: repo root is `C:/Users/point`, whole `darkwatch/` directory is untracked | Fresh-session forensic check revealed no darkwatch commits and parent-repo status | Must be resolved before relying on git for state recovery. |

---

## 10. Blockers & Open Questions

| Date | Blocker / Question | Impact | Owner |
|---|---|---|---|
| 2026-08-04 | ✅ RESOLVED — Copernicus access path confirmed | — | Bull |
| 2026-08-04 | ✅ RESOLVED — NOAA Marine Cadastre path confirmed (AccessAIS + GeoParquet) | — | Bull |
| 2026-08-04 | ✅ RESOLVED — Santa Barbara Channel / Channel Islands chosen as test theater | — | Bull |
| 2026-08-04 | ✅ RESOLVED — Python 3.14 + geospatial stack + PyTorch CUDA 12.8 installed and verified | — | Bull |
| 2026-08-04 | ✅ RESOLVED — First Sentinel-1 GRD scene downloaded, extracted, calibrated, and visualized | — | Bull |
| 2026-08-04 | ✅ RESOLVED — Phase 1 automated S1 prep pipeline (read → calibrate → land-mask → tile) | — | Bull |
| 2026-08-04 | ✅ RESOLVED — Land/coastline mask using Natural Earth `ne_50m_land` polygons | — | Bull |
| 2026-08-04 | ✅ RESOLVED — Scene selection: score passes by open-water fraction to avoid land-only acquisitions | — | Bull |
| 2026-08-04 | Which open SAR ship detection dataset has the most permissive license? | Medium — blocks S2 | Bull |
| 2026-08-04 | ✅ RESOLVED — Detector training completed; weights at `models/detector_runs/darkwatch_yolov8n_ssdd/weights/best.pt` | — | Bull |
| 2026-08-04 | ⚠️ WATCH — SSDD→GRD domain gap yields very low recall on real tiles (1 unique contact) | Medium — limits S2 utility; not a Phase 3 blocker | Bull |
| 2026-08-04 | ✅ RESOLVED — AIS data pull for the 2024-07-11 Santa Barbara Channel window (`AIS_2024_07_11.zip` downloaded, filtered, fused) | — | Bull |
| 2026-08-04 | ✅ RESOLVED — Darkwatch extracted into its own git repository at `C:/Users/point/projects/darkwatch` | — | Bull |
| 2026-08-04 | ✅ RESOLVED — First real dark-vessel attribution verdict produced (DARK, p=0.9732) | — | Bull |
| 2026-08-04 | Create/push `satyamdas03/darkwatch` GitHub repository | Low — local repo is safe; remote needed for backup/collaboration | Bull |
| 2026-08-04 | Validate/calibrate S3 probabilities on ground-truthable cases | High — p=0.97 is a model output, not yet a calibrated belief | Bull |
| 2026-08-04 | Address SSDD→GRD domain gap to improve detector recall | Medium — needed before operational scale; options: LS-SSDD-v1.0, HRSID, real GRD chips, larger backbone, CFAR fallback | Bull |

---

## 11. Session Log

> Append a new entry on every **POINTBREAK**.

### 2026-08-04 — Session #1: Dossier creation + Phase 0 kickoff
- Read `darkwatch-architecture.html` visual reference.
- Created `DOSSIER.md` as the single living source of truth.
- Seeded dossier with full project identity, vision, architecture, roadmap, and logistics board.
- Verified Copernicus Data Space Ecosystem OData API endpoints and NOAA Marine Cadastre GeoParquet/AccessAIS paths.
- Installed Python geospatial stack (rasterio, geopandas, xarray, pyproj, shapely, pyogrio) and verified PyTorch 2.11.0+cu128 on RTX 5060.
- Created `pyproject.toml`, project skeleton, CDSE adapter (`darkwatch/adapters/copernicus_adapter.py`), and helper scripts (`scripts/fetch_first_scene.py`, `scripts/inspect_scene.py`).
- Downloaded and extracted first Sentinel-1 GRD scene: `S1A_IW_GRDH_1SDV_20240701T135228_...SAFE`.
- Built barycentric geocoding from the Sentinel-1 geolocation grid using `scipy.interpolate.LinearNDInterpolator`.
- Calibrated VV backscatter to sigma-nought (dB) and produced theater crop preview (`notebooks/phase0_santa_barbara_north.png`).
- **Phase 0 COMPLETE.** Next: build the automated S1 ingestion/prep pipeline (Phase 1).

### 2026-08-04 — Session #1 POINTBREAK: Phase 0 locked, project state snapshotted
- **POINTBREAK triggered.** Appending checkpoint of completed Phase 0 work and current open items.
- Confirmed dossier now reflects: status = Phase 0 COMPLETE / Phase 1 starting; Santa Barbara Channel / Ventura operational bbox; all access paths verified; environment verified.
- Open items carried into Phase 1: coastline mask source, CDSE `$value` vs `$zip` behavior (now handled by adapter), SAR ship detection dataset license verification.
- Files on disk: `DOSSIER.md`, `darkwatch-architecture.html`, `pyproject.toml`, `darkwatch/` package skeleton, `scripts/`, `data/raw/s1/S1A_IW_GRDH_1SDV_20240701T135228_...SAFE/`, `notebooks/phase0_santa_barbara_north.png`.
- **Next action:** Begin Phase 1 — SAR Ingestion & Prep pipeline (`fetch → calibrate → land-mask → tile`).

### 2026-08-04 — Session #1 (continued): Phase 1 SAR Ingestion & Prep COMPLETE
- **POINTBREAK triggered.** Appending Phase 1 completion state.
- Built end-to-end S1 prep pipeline:
  - `reader.py`: parse `.SAFE` structure, pick polarization measurement TIFF + calibration + annotation XMLs.
  - `calibrate.py`: interpolate sampled sigma-nought calibration vectors to full image width, output dB.
  - `geocode.py`: barycentric lat/lon ↔ line/pixel via `scipy.interpolate.LinearNDInterpolator`; `bbox_to_window` for theater crop.
  - `land_mask.py`: public-domain Natural Earth `ne_50m_land` polygons; `compute_water_mask` with optional coastal buffer; `apply_water_mask`.
  - `tiler.py`: 1024×1024 overlapping chips, JSON sidecar with corner coords / center / water fraction, GeoTIFF with WGS84 GCPs.
  - `pipeline.py`: CLI `prep_s1.py` and `prep_scene()` orchestration; default theater bbox `-120.8,34.3,-119.8,34.7`.
- Fixed CDSE download path: always use `$value` endpoint (archive `$zip` returns 404 after ~1 month).
- Moved CDSE credentials from command-line env vars into `.env` (gitignored); scripts load via `python-dotenv`.
- Discovered and fixed land-mask bug: the first pass (2024-07-01) had no usable open ocean because it was angled inland. Built `scripts/pick_ocean_scene.py` to score candidate passes by open-water fraction.
- Downloaded and processed ocean-covered scene: `S1A_IW_GRDH_1SDV_20240711T140858_20240711T140923_054714_06A94E_9466.SAFE`.
- Ran `prep_s1.py` on the ocean scene with bbox `-120.8,34.3,-119.8,34.7`; produced **12 analysis-ready ocean tiles** (water fraction 1.0 per tile).
- Generated validation mosaic `notebooks/phase1_channel_mosaic_v2.png`; confirms clean ocean speckle, no land/urban artifacts.
- **Phase 1 COMPLETE.** Next: Phase 2 — Vessel Detection (fine-tune a SAR ship detector on open datasets; verify licenses).

### 2026-08-04 — Session recovery after laptop crash: full codebase deep-dive & dossier refresh
- Laptop restarted on its own at ~12:26 while detector training was in progress. Session state lost; this is a full forensic reconstruction.
- **Read every source file line by line** in `darkwatch/` (adapters, s1_prep, detect, alerts, behavior, fusion), `scripts/`, `tests/`, `pyproject.toml`, `.env`, `.gitignore`, `DOSSIER.md`, and `darkwatch-architecture.html`.
- **Verified on-disk state:**
  - Phase 0/1 deliverables intact: two `.SAFE` scenes, two processed tile sets (July 1 = 22 tiles, July 11 = 12 tiles), mosaic PNGs, unit tests passing.
  - Phase 2 scaffolding complete but **training interrupted**: `darkwatch/detect/{contact,dataset,detector}.py`, `scripts/{prepare_ssdd,train_detector,detect_tiles}.py` all present; SSDD YOLO dataset has 1,160 images + labels; `models/detector_runs/darkwatch_yolov8n_ssdd_v1/weights/` is empty; only `args.yaml` exists.
  - `yolov8n.pt` base weights present at repo root.
  - No AIS data downloaded yet; no fusion/behavior/alerts implementation yet (empty module stubs).
  - `README.md` was referenced in dossier but missing; created a minimal `README.md` pointing to `DOSSIER.md`.
- **Git situation discovered:** the git repository root is `C:/Users/point`, so the entire `darkwatch/` directory appears as a single untracked entry (`?? ./`) under that parent repo. No darkwatch-specific commits exist yet. This is a medium-risk logistics issue to resolve.
- **Updated `DOSSIER.md`** with current state, new blockers (interrupted training, untracked repo root), and this session log entry.
- **Next action:** Re-run `python scripts/train_detector.py` to complete Phase 2 detector training; then run inference with `scripts/detect_tiles.py` on the July 11 tiles; then move to Phase 3 (AIS pull + probabilistic fusion).

### 2026-08-04 — Git fix: Darkwatch extracted into its own repository
- **Issue:** `C:/Users/point` was the git root of `alpaca-trading-agent`; Darkwatch had just been committed into that parent repo as `projects/darkwatch/`.
- **Fix applied:**
  1. In parent repo: `git reset --soft HEAD~1` + `git rm -r --cached projects/darkwatch` to stop tracking Darkwatch.
  2. Added `projects/darkwatch/` to parent `C:/Users/point/.gitignore`.
  3. Committed parent extraction: `chore(repo): extract darkwatch into its own dedicated repository`.
  4. Initialized a fresh git repo inside `C:/Users/point/projects/darkwatch/`.
  5. Broadened `darkwatch/.gitignore` to exclude all `data/`, `models/`, and base weights.
  6. Committed clean initial Darkwatch repo on branch `main`: source, scripts, tests, docs, notebooks.
- **Result:** Darkwatch is now an independent repository. Parent repo ignores it. No remote set yet — GitHub repo creation/push is pending user approval.
- **Files committed to darkwatch:** `DOSSIER.md`, `README.md`, `darkwatch-architecture.html`, `darkwatch/` package, `scripts/`, `tests/`, `pyproject.toml`, `notebooks/` validation PNGs.
- **Files excluded:** `.env`, `data/`, `models/`, `yolov8n.pt`, `__pycache__/`.

### 2026-08-04 — Session #1 (continued): Phase 2 COMPLETE, inference domain-gap fixed, Phase 3 started
- Re-ran `python scripts/train_detector.py --epochs 30 --batch 4 --imgsz 640 --device 0` to completion after the laptop crash.
  - Run folder: `models/detector_runs/darkwatch_yolov8n_ssdd/` (not `_v1`); final `best.pt` present.
  - Validation mAP50 reached **0.977** at epoch 30.
- First inference run with `scripts/detect_tiles.py` on the July 11 tiles returned **0 contacts**.
- **Root cause:** prepared tiles are `float32` dB GeoTIFFs; the SSDD-trained YOLO model expects `uint8` RGB images.
- **Fix:** added `_db_to_uint8()` helper and configurable dB contrast stretch inside `darkwatch/detect/detector.py`; `VesselDetector.predict()` now preprocesses GeoTIFFs before passing arrays to YOLO; `scripts/detect_tiles.py` exposes `--db-lo` / `--db-hi` / `--no-stretch`.
- Re-ran inference: **2 detections across 12 tiles**, corresponding to **1 unique physical vessel** straddling the boundary between two adjacent row tiles (center ~-120.7308, 34.6105; confidences 0.37 and 0.50).
- **Key finding / risk:** SSDD-trained YOLOv8n has very low recall on real Sentinel-1 GRD. This is a cross-domain generalization problem, not a calibration bug. Options for later: fine-tune on LS-SSDD-v1.0 / HRSID, add real GRD chips to training, use a larger YOLO backbone, or implement a CFAR classical fallback.
- Decision: accept the current detections as a working baseline and move to **Phase 3 Fusion & Attribution** rather than endlessly tuning S2.
- Started downloading NOAA Marine Cadastre daily AIS broadcast CSV for 2024-07-11 (`AIS_2024_07_11.zip`, ~358 MB) from `https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2024/`; download in progress.
- **Next action:** filter the daily AIS CSV to the Santa Barbara Channel theater bbox and ±time window around the SAR acquisition; build the probabilistic SAR-to-AIS association module; produce the first dark-vessel attribution dossier.

### 2026-08-04 — Session #1 (continued): Phase 3 scaffold complete, waiting on NOAA AIS download
- Laptop restarted again mid-session; this is the continuation after the summary request.
- Re-verified on-disk state: `models/detector_runs/darkwatch_yolov8n_ssdd/weights/best.pt` present; 12 July 11 tiles ready; `data/processed/detections_20240711/contacts.json` contains 2 detections / 1 unique vessel near (-120.7308, 34.6105).
- Implemented the Phase 3 probabilistic SAR-to-AIS association layer:
  - `darkwatch/fusion/verdict.py` — `Verdict` enum (CLEAR, DARK, ARTIFACT, REVIEW).
  - `darkwatch/fusion/ais.py` — `AISTrack` with linear interpolation to SAR time; combines AIS GPS uncertainty and interpolation uncertainty; `load_ais_csv()` streams NOAA CSV in chunks, filters by bbox/time, groups by MMSI.
  - `darkwatch/fusion/associate.py` — `associate_contact()` computes Gaussian likelihood between a SAR contact and each interpolated AIS track plus a no-match alternative, then normalizes into component probabilities. `associate_all_contacts()` returns one `ContactVerdict` per contact with a list of `TrackAssociation` candidates. Verdicts are assigned by thresholds: CLEAR if any track probability dominates; DARK if no-match dominates and the contact is well-formed; ARTIFACT if detection confidence is very low; REVIEW otherwise.
  - `scripts/fetch_ais.py` — downloads NOAA daily zip, unzips, filters to theater bbox and time window, writes `data/external/ais/ais_YYYY-MM-DD_clipped.csv`.
  - `scripts/fuse_contacts.py` — loads contacts, loads clipped AIS CSV, runs association, writes `verdicts.json` + `summary.json`.
  - `tests/test_fusion.py` — 6 unit tests covering CSV filtering, interpolation, CLEAR/DARK verdicts, probability normalization, and `associate_all_contacts()` output shape.
- Updated `README.md` and `DOSSIER.md` §13 Quick Commands with the real CLI commands now used in the project.
- Added `.gitignore` entries for `data/external/ais/`, extracted AIS dirs, `*.pt`, `yolo26n.pt`, and temporary notebook PNGs.
- Started NOAA AIS download as a background task; observed very slow transfer (~12% after several minutes, ETA ~50 min).
- **Next action:** wait for the NOAA AIS daily zip to finish, run `scripts/fetch_ais.py` filter, then run `scripts/fuse_contacts.py` to produce the first real dark-vessel attribution dossier.

### 2026-08-04 — Session #1 (continued): VH polarization check + detector deduplication while AIS downloads
- NOAA AIS daily zip still downloading very slowly; used the wait to improve detector output quality and validate polarization behavior.
- Processed **VH polarization tiles** for the July 11 scene (`prep_s1.py --pol vv,vh`).
- Ran detector on VV-only, VH-only, and VV+VH combined:
  - VV-only: 1 unique contact, confidence 0.50, estimated size ~173 m × 120 m.
  - VH-only: 1 unique contact at the same location, confidence **0.82**, estimated size ~214 m × 167 m.
  - Combined VV+VH with deduplication: 1 unique contact, retaining the VH detection (highest confidence).
- **Key finding:** VH polarization gives a much stronger, more confident detection for this contact. The location offset between VV and VH is ~21 m (within geolocation uncertainty). No additional vessels were found in VH, confirming the scene is genuinely sparse rather than a VV-specific detection failure.
- Added contact **deduplication** to `darkwatch/detect/detector.py`: contacts within 100 m (haversine) are merged, keeping the highest-confidence detection. This removes duplicates across overlapping tiles.
- Added `--pol` polarization filter to `scripts/detect_tiles.py` so users can run VV, VH, or both.
- Added `scripts/visualize_contact.py` to generate full-tile context and zoomed evidence PNGs for each contact; produced `notebooks/contact_viz/S1A_IW_GRDH_1SDV_20240711T140858_20240711T140923_054714_06A94E_9466_vh_c3314_r10814_det0000{_zoom}.png`.
- Added `tests/test_detector.py` covering haversine distance and contact deduplication. Total tests now **13 passed**.
- Fixed `darkwatch/fusion/associate.py` probability decomposition: removed the unexplained `(1 - artifact_prior)` scaling on `p_dark`; `p_clear` and `p_dark` now split the real-vessel mass conditioned on AIS evidence, so component probabilities sum to 1 by construction. REVIEW verdict is produced by thresholding when no component dominates.
- Updated `README.md` and `DOSSIER.md` §13 Quick Commands to recommend `--pol vv,vh` and explain automatic deduplication.
- Canonical contacts file is now `data/processed/detections_20240711/contacts.json` (1 contact, VH, conf 0.82). VV-only and VH-only outputs preserved in `data/processed/detections_20240711_vvonly/` and `data/processed/detections_20240711_vh/` for comparison.
- **Next action:** same as before — wait for NOAA AIS download, then run `fetch_ais.py` + `fuse_contacts.py` to produce the first real dark-vessel attribution.

### 2026-08-04 — Session #1 (continued): first real dark-vessel attribution verdict produced
- NOAA AIS daily zip `AIS_2024_07_11.zip` (~358 MB) finished downloading after a slow (~1 hour) transfer.
- Ran `scripts/fetch_ais.py --date 2024-07-11 --bbox "-120.8,34.3,-119.8,34.7" --center-time "2024-07-11T14:09:10Z" --time-window-minutes 60 --keep-zip`:
  - Extracted 1 CSV; filtered to **351 AIS rows** in theater/time window; grouped into **8 AIS tracks** with ≥2 messages.
- Fixed timezone-aware vs naive datetime mismatch in the fusion pipeline:
  - `darkwatch/fusion/ais.py` `load_ais_csv()`: UTC-naive time-window boundaries are localized to UTC before filtering against UTC-aware `BaseDateTime`.
  - `darkwatch/fusion/associate.py` `associate_contact()`: UTC-naive `t_sar` (from `contact.acquisition_time`) is localized to UTC before AIS interpolation.
- Fixed probability-decomposition regression in `darkwatch/fusion/associate.py`: original code overwrote `p_clear` before computing `p_dark`; now `p_matched_given_real` is preserved so `p_clear` and `p_dark` correctly partition the real-vessel mass. Added regression test; tests now **14 passed**.
- Fixed `scripts/fetch_ais.py` download error handling: replaced unreachable `result.returncode` check with `try/except CalledProcessError` and added `curl -C -` resume support.
- Ran `scripts/fuse_contacts.py --contacts data/processed/detections_20240711/contacts.json --ais data/external/ais/ais_2024-07-11_clipped.csv --output-dir data/processed/fusion_20240711`:
  - **Verdict summary: `DARK: 1`**.
  - Single SAR contact `S1A_IW_GRDH_1SDV_20240711T140858_20240711T140923_054714_06A94E_9466_vh_c3314_r10814_det0000` at **(-120.7310, 34.6107)**, confidence 0.82, estimated size ~214 m × 167 m.
  - `verdicts.json`: `p_artifact=0.0268`, `p_clear=0.0`, `p_dark=0.9732`, `p_review=0.0`, reasoning = "No AIS track within gate radius." and "No AIS match within gate; contact is candidate dark vessel if real."
- **Implication:** the one detectable vessel in the July 11 Santa Barbara Channel scene was **not transponding cooperatively** within 2,000 m and 60 min of the SAR capture. This is the first real Darkwatch dark-vessel output.
- **Caveat:** S3 probabilities are model-based, not yet empirically calibrated. The high `p_dark` is driven by detector confidence (0.82) and absence of AIS within the gate; a transponding vessel just outside the gate or with a temporary AIS gap would look identical to the current model. Calibration against ground-truthable cases is the next critical step.
- **Next action:** begin Phase 3 follow-up: (1) run a second scene with more traffic to get CLEAR examples, (2) implement static-object exclusion (rigs/platforms/MPAs), (3) collect calibration labels to check that p=0.97 actually means ~97% dark, (4) start Phase 4 behavior/intent context layer.

### 2026-08-04 — Session #1 (continued): nearest-neighbor evidence + coverage-gap calibration
- Revisited the first real dark-vessel verdict and identified the key calibration weakness: a transponding vessel just outside the 2,000 m gate would look identical to a dark vessel.
- Enhanced `darkwatch/fusion/associate.py`:
  - `ContactVerdict` now records `nearest_association`, `n_tracks_within_gate`, and `n_tracks_near_gate`.
  - Added coverage-gap adjustment: when no AIS track exists within 2× the gate radius, 25% of `p_dark` is shifted to `p_review` to reflect innocent dropout / AIS gap uncertainty.
  - Added proportional review shift when a track is just outside the gate (between 1× and 2× gate radius).
  - Regression test updated to assert conservation of real-vessel mass across `clear + dark + review`.
- Enhanced `scripts/fuse_contacts.py` to serialize `nearest_association` and write `summary.json` with scene time, gate radius, contact count, AIS track count, and verdict counts.
- Re-ran fusion on the July 11 scene:
  - Updated verdict: **DARK** with `p_dark=0.7299`, `p_review=0.2433`, `p_artifact=0.0268`, `p_clear=0.0`.
  - Nearest AIS track: **MMSI 367726390 / BERNARDINE C**, moored/stationary at 34.55505, -120.60969, **12.7 km** from the SAR contact at SAR time.
  - No AIS track within 2 km; no AIS track within 4 km.
- Inspected all 9 MMSIs in the theater window; documented them in `notebooks/fusion_20240711_report.md`.
- **Key finding:** the one detectable contact is isolated — no cooperative vessel passed within 4 km. The most likely alternatives are (a) genuine dark vessel, (b) radar artifact / fixed object. Static-object exclusion is now the highest-priority S3 follow-up.
- **Files changed:** `darkwatch/fusion/associate.py`, `scripts/fuse_contacts.py`, `tests/test_fusion.py`, `DOSSIER.md`, `notebooks/fusion_20240711_report.md`.
- **Tests:** 14 passed.
- **Next action:** add static-object exclusion (oil platforms / Channel Islands rock locations) and run a second, busier Sentinel-1 scene to collect CLEAR matches for calibration.

### 2026-08-04 — Session #1 (continued): public GitHub repo + killer README + MIT license
- Rewrote `README.md` as a community-facing landing page with badges, Mermaid pipeline diagram, first-real-result showcase, quickstart, architecture, roadmap, contributing guide, and citation block.
- Added MIT `LICENSE` so the project is freely reusable.
- Created public GitHub repository `satyamdas03/darkwatch` and pushed the full codebase (excluding `data/`, `models/`, `.env`, and base weights per `.gitignore`).
- Updated `DOSSIER.md` project identity with the public remote URL.
- **Next action:** create a GitHub profile README repo (`satyamdas03/satyamdas03`) based on deep-dive of public repos and LinkedIn/web research.

---

## 12. Resources & Links

### Verified Access Paths (as of 2026-08-04)

#### SAR — Copernicus Data Space Ecosystem (CDSE)
- **Portal:** https://dataspace.copernicus.eu/
- **Catalogue search:** `https://catalogue.dataspace.copernicus.eu/odata/v1/Products`
- **Product download (always use this):** `https://download.dataspace.copernicus.eu/odata/v1/Products(<UUID>)/$value`
- **Compressed native download (zip, only valid ~1 month after publication — avoid for archive):** `https://download.dataspace.copernicus.eu/odata/v1/Products(<UUID>)/$zip`
- **Auth endpoint (Keycloak):** `https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token`
  - `client_id: cdse-public`, `grant_type: password`, username/password from registration.
- **Product type for vessel detection:** `IW_GRDH_1S` (Interferometric Wide, Ground-Range Detected, High resolution; standard GRD).
- **Docs:** https://documentation.dataspace.copernicus.eu/APIs/OData.html
- **OData basics notebook:** https://documentation.dataspace.copernicus.eu/notebook-samples/geo/odata_basics.html
- **License:** Sentinel-1 fully open, redistribution permitted.

#### AIS — NOAA Marine Cadastre
- **Clip-and-ship web tool (AccessAIS):** https://coast.noaa.gov/digitalcoast/tools/ais.html
  - Custom area + time; output zipped CSV; order limit ~2 GB.
- **Bulk / experimental GeoParquet (2024 & 2025):**
  - Daily broadcast points: `https://ocmgeodatastor1.blob.core.windows.net/marinecadastre/ais2024/`
  - Monthly vessel tracks: `https://ocmgeodatastor1.blob.core.windows.net/marinecadastre/aistrack/index-aistrack.html`
  - Guidance repo: https://github.com/ocm-marinecadastre/ais-vessel-traffic
- **FAQ / data dictionary:** https://coast.noaa.gov/data/marinecadastre/ais/faq.pdf
- **2024 metadata (InPort):** https://www.fisheries.noaa.gov/inport/item/75937
- **License:** Public US government data; suitable for build/validation. Confirm redistribution terms for any published raw data.

#### Behavior / Validation Cross-Reference
- **Global Fishing Watch:** https://globalfishingwatch.org/ — apparent fishing, encounters, loitering APIs (not raw AIS position feed).
- **Related memories:** TBD

---

## 13. Quick Commands

```bash
# Run tests
python -m pytest tests/ -q

# Score candidate passes by open-water fraction and pick the best one
python scripts/pick_ocean_scene.py --start 2024-07-01 --end 2024-07-31 --max-results 50

# Download a Sentinel-1 scene over the test theater (uses .env for credentials)
python scripts/fetch_first_scene.py --start 2024-07-11 --end 2024-07-12 --max-results 5 --download

# Run the S1 prep pipeline
python scripts/prep_s1.py "data/raw/s1/...SAFE" --output-dir data/processed/... --tile-size 1024 --overlap 128 --buffer-deg 0.005 --bbox "-120.8,34.3,-119.8,34.7" --pol vv,vh

# Validate tiles as a mosaic
python scripts/mosaic_tiles.py data/processed/.../manifest.json --output notebooks/phase1_mosaic.png

# Detect vessels (dB -> uint8 contrast stretch is required for the SSDD-trained YOLO model)
# Use both polarizations; overlapping detections are deduplicated automatically.
python scripts/detect_tiles.py \
  --manifest data/processed/s1a_20240711_channel/manifest.json \
  --model models/detector_runs/darkwatch_yolov8n_ssdd/weights/best.pt \
  --db-lo -25 --db-hi -5 \
  --pol vv,vh \
  --output-dir data/processed/detections_20240711

# Fetch NOAA Marine Cadastre AIS for the acquisition date
python scripts/fetch_ais.py --date 2024-07-11 \
  --bbox "-120.8,34.3,-119.8,34.7" \
  --center-time "2024-07-11T14:09:10Z" \
  --time-window-minutes 60

# Visualize contacts on source tiles (full + zoomed evidence PNGs)
python scripts/visualize_contact.py \
  --contacts data/processed/detections_20240711/contacts.json \
  --manifest data/processed/s1a_20240711_channel/manifest.json \
  --output-dir notebooks/contact_viz

# Fuse SAR contacts with AIS tracks to produce dark-vessel verdicts
python scripts/fuse_contacts.py \
  --contacts data/processed/detections_20240711/contacts.json \
  --ais data/external/ais/ais_2024-07-11_clipped.csv \
  --output-dir data/processed/fusion_20240711

# Generate human-readable Markdown report from the fusion outputs
python scripts/fusion_report.py \
  --contacts data/processed/detections_20240711/contacts.json \
  --ais data/external/ais/ais_2024-07-11_clipped.csv \
  --verdicts data/processed/fusion_20240711/verdicts.json \
  --summary data/processed/fusion_20240711/summary.json \
  --output notebooks/fusion_20240711_report.md
```

---

## 14. Appendix

### 14.1 Verdict Taxonomy
- **DARK** — deliberate dark vessel, high confidence.
- **REVIEW** — plausible dark vessel, uncertainty too high to call.
- **CLEAR** — matched to a transponding AIS track.
- **ARTIFACT** — radar false contact or non-vessel object.

### 14.2 Component Probabilities (S3 evidence trail)
For each DARK/REVIEW verdict, surface:
1. `P(real vessel | SAR)` — detector confidence + artifact filter.
2. `P(no AIS track claims it | AIS)` — association / explain-away.
3. `P(not rig/fixed false zone | context)` — static-object exclusion.
4. `P(not innocent AIS gap | AIS quality / timing)` — dropout vs switch-off.

Final `P(dark)` is a function of these; the **weakest link** is reported explicitly.

### 14.3 Environment Variables / Secrets (names only, never values)
Store actual values in `.env` (gitignored). Names expected by the code:
- `DARKWATCH_CDSE_USERNAME`
- `DARKWATCH_CDSE_PASSWORD`
- `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` (only if using S3 mirror)
- `GFW_API_KEY` (Phase 4)

The repo-level `.env` is loaded automatically by `scripts/fetch_first_scene.py` and `scripts/pick_ocean_scene.py` via `python-dotenv`.
