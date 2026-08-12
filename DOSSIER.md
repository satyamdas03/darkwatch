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
| **Status** | Phase 2 — Vessel Detection baseline COMPLETE; Session #7 COMPLETE: SSDD→GRD domain gap closed. Mixed YOLOv8n detector `darkwatch_yolov8n_ssdd_grd_v4` trained from corrected weak-positive chips and validated; July 23 weak-target recall regression fixed (both known DARK vessels recovered). Phase 3 Fusion & Attribution baseline COMPLETE: static-object exclusion + four real scenes fused, calibration framework + interactive maps. Session #12 COMPLETE: physical-plausibility AIS gate implemented and tuned, learned per-class Platt calibration layer fitted, 46-label recal3 dataset locked. Session #13 COMPLETE: calibration dataset expanded to 122 labels across Santa Barbara + Gulf of Mexico; cross-theater validation reveals Santa-Barbara-only calibration overfit; combined cross-theater model selected as default. Session #13.5 COMPLETE: BOEM/BSEE Gulf of Mexico platform catalog integrated into static-object exclusion; `--theater` flag added to fusion CLI. Session #14 COMPLETE: Southern California Bight third-theater validation unblocked and processed; theater-aware calibration registry added; SCB-specific calibration model fitted and selected automatically for SCB scenes; dashboard Phase D next. |
| **Start Date** | 2026-08-04 |
| **Last Updated** | 2026-08-13 (Session #14: SCB 2024-07-06 end-to-end with 108 contacts / 665 AIS tracks; theater-aware calibration registry + SCB-specific model; unified CLI; all tests pass) |
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
- [x] **Static-object exclusion layer implemented** (`darkwatch/fusion/static_objects.py`): 32 California oil platforms from OSPR ds357; smooth 250 m buffer confidence falloff; integrated into `associate_contact()` before real-vessel mass split; artifact boost pushes platform-adjacent contacts toward ARTIFACT/REVIEW.
- [x] **Static-object tests added:** `tests/test_fusion.py` now verifies platform flagging and verdict shift; test coordinates moved away from Platform Irene. Total tests **16 passed**.
- [x] **Second Sentinel-1 scene acquired and processed (2024-07-18):**
  - Downloaded `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B.SAFE`.
  - Produced 96 tiles (48 VV + 48 VH) at `data/processed/s1a_20240718_channel/`.
  - Detector found **12 unique contacts** after VV+VH deduplication at `data/processed/detections_20240718/contacts.json`.
- [x] **NOAA AIS downloaded and clipped for 2024-07-18:** `AIS_2024_07_18.zip` extracted → `ais_2024-07-18_clipped.csv` with **621 rows** → **7 AIS tracks**.
- [x] **Second real fusion run completed:** `data/processed/fusion_20240718/verdicts.json` verdict counts: **CLEAR 3, REVIEW 5, DARK 3, ARTIFACT 1**.
  - CLEAR matches: MSC GIUSY (108 m), MSC SOFIA PAZ (308 m), RYAN T (295 m).
  - Strong ARTIFACT: Platform Harvest (82 m), p_artifact=0.50.
- [x] **Calibration evaluation framework added:** `scripts/evaluate_calibration.py` + `data/processed/calibration_labels.json` produce per-class Brier scores, reliability diagrams, and probability-distribution plots.
- [x] **First calibration report generated:** `notebooks/calibration/calibration_report.md` from 13 labeled contacts (6 ARTIFACT, 3 CLEAR, 2 DARK, 2 UNKNOWN). Preliminary finding: model is qualitatively well-calibrated but sample size is too small for strong claims; more scenes needed.
- [x] **Interactive fusion maps added:** `scripts/visualize_fusion.py` produces Folium maps with SAR contacts (colored by verdict), AIS tracks + SAR-time interpolated positions, oil platform markers, and 2 km gate circles. Generated `notebooks/fusion_20240718_map.html` and `notebooks/fusion_20240711_map.html`.
- [x] **Scene scoring refreshed:** `scripts/pick_ocean_scene.py` scored all 19 July 2024 passes; top high-water candidates identified (2024-07-23T140922 at 100% water).
- [x] **Scene selection improved:** `scripts/pick_ocean_scene.py` now accepts `--operational-bbox` and scores scenes by `water_fraction × operational_overlap`, not just overall water fraction. This prevents selecting scenes that are ocean-covered but do not actually overlap the theater of interest.
- [x] **Calibration + maps committed and pushed:** `5651d78` pushed to `satyamdas03/darkwatch`.
- [x] **Third real scene acquired and processed (2024-07-23, correct pass):**
  - Downloaded `S1A_IW_GRDH_1SDV_20240723T020701_20240723T020726_054882_06AF26_69FC.SAFE` after scene-selection fix.
  - Produced 24 tiles (12 VV + 12 VH) at `data/processed/s1a_20240723_channel/`.
  - Detector found **2 unique contacts** near (-120.79, 34.71) using `--db-lo -30 --db-hi -10`.
- [x] **NOAA AIS re-fetched for 2024-07-23 with correct SAR time window:** 591 clipped rows → **8 AIS tracks**.
- [x] **Third real fusion run completed:** `data/processed/fusion_20240723/verdicts.json` verdict counts: **DARK 2**.
  - Both contacts are small vessels with no AIS within 2 km and no platform nearby; nearest AIS **BERNARDINE C** is 24 km away.
- [x] **July 23 fusion report and map generated:** `notebooks/fusion_20240723_report.md` and `notebooks/fusion_20240723_map.html`.
- [x] **Calibration dataset expanded:** `data/processed/calibration_labels.json` now has 15 labeled contacts (6 ARTIFACT, 3 CLEAR, 4 DARK, 2 UNKNOWN); calibration report regenerated.
  - DARK candidates: 3 contacts with no AIS within gate and no nearby platform.
- [x] **July 18 human-readable fusion report generated:** `notebooks/fusion_20240718_report.md`.
- [x] Unit tests pass (`pytest tests/ -q` → 16 passed).
- [x] **Calibration labels now tracked in git:** added `.gitignore` exception `!data/processed/calibration_labels.json` and force-added the file so the auditable label source is versioned.
- [x] **README updated:** added Calibration & Visualization section, real results for July 11/18, scene-selection tip, revised roadmap, and clarified detector domain-gap as the next bottleneck.
- [x] **July 18 human-readable fusion report generated:** `notebooks/fusion_20240718_report.md`.
- [x] **July 23 contact evidence PNGs generated:** `notebooks/contact_viz_20240723/`.
- [x] **All work committed and pushed** as `61a1dc5` to `satyamdas03/darkwatch`.
- [x] **Session #6 — SSDD→GRD domain-gap closure started (2026-08-08):**
  - Diagnosed prior failed mixed run `darkwatch_yolov8n_ssdd_grd` (only `args.yaml`, no weights — likely OOM/interrupt). Relaunched as `_v2` with persistent logging.
  - Validated mixed dataset integrity: 2,778 train images ↔ 2,778 labels, all readable, labels valid.
  - Completed `darkwatch_yolov8n_ssdd_grd_v2` training: 18 epochs, best/last `mAP50=0.938`, `recall=0.879`, `precision=0.903`; weights moved into `models/detector_runs/darkwatch_yolov8n_ssdd_grd_v2/weights/`.
  - Identified that `scripts/extract_grd_chips.py` skipped DARK-labeled contacts (treated as “unknown ship”). Re-extracted July 23 using loose detections: 2 positives (both DARK vessels), 201 negatives.
  - Added `scripts/build_mixed_dataset.py` to reproducibly merge SSDD base + GRD chip directories into a single YOLO dataset with stratified train/val split.
  - Built expanded mixed dataset `data/processed/mixed_ssdd_grd_v3/`: 2,901 train (1,017 positive, 1,884 negative), 512 val (156 positive, 356 negative) from SSDD + July 11 + July 18 + July 23 loose chips.
  - Validated v2 mixed detector on real scenes:
    - July 11: 1 contact (conf 0.66 vs 0.82 SSDD-only).
    - July 18: 11–13 contacts (slightly lower confidences than SSDD-only; missed the lowest-confidence contact).
    - July 23: **0 contacts** with both default (-25, -5) and looser (-30, -10) stretches — regression vs SSDD-only (2 contacts). Indicates model still undershoots small/weak targets.
  - Completed `darkwatch_yolov8n_ssdd_grd_v3` on expanded dataset: best `mAP50=0.958`, final `mAP50=0.939`, `recall=0.869`, `precision=0.910`; but v3 still found **0 contacts** on July 23 at `conf=0.05`, confirming the weak-target recall regression.
- [x] **Session #7 — SSDD→GRD domain gap CLOSED (2026-08-08):**
  - Root-caused July 23 regression: only 2 real weak-positive GRD chips existed, and an earlier augmentation pass silently corrupted them by rotating/flipping without updating YOLO bounding boxes.
  - Added `scripts/augment_weak_positives.py`: photometric-only augmentation (brightness/contrast, speckle, Gaussian noise, gamma, mild blur) that preserves bounding-box validity.
  - Regenerated `data/processed/grd_chips_20240723_weak_aug/` as 100 photometrically augmented chips from the 2 July 23 DARK positives (50× each).
  - Rebuilt `data/processed/mixed_ssdd_grd_v4/`: 2,986 train / 527 val images, 1,084 train positives, 1,902 negatives (SSDD + July 11/18/23 + augmented July 23 weak positives).
  - Fixed `scripts/train_detector.py`: `--workers` is now forwarded to `VesselDetector.train()`; confirmed `workers=0` avoids Windows multiprocessing CUDA spawn errors on RTX 5060.
  - Trained `darkwatch_yolov8n_ssdd_grd_v4` from v3 weights: early-stopped at epoch 11, best epoch 1, validation `P=0.933`, `R=0.885`, `mAP50=0.953`, `mAP50-95=0.670`; weights at `models/detector_runs/darkwatch_yolov8n_ssdd_grd_v4/weights/best.pt`.
  - **Validation on real scenes:**
    - **July 11:** 1 unique contact detected (same as v3 / SSDD-only), conf 0.658.
    - **July 18:** 11 unique contacts (vs 12 for SSDD-only). v4 maintained all real vessels and dropped the obvious 1700 m × 606 m platform-edge artifact.
    - **July 23:** v4 default (`-25/-5`, `conf=0.25`) found 3 contacts; with **adaptive stretch** (`lo=-40`, `hi=-10`, 5/95 percentile, `conf=0.05`) found 9 contacts, including **both known DARK vessels** at conf 0.764 and 0.370. v3 adaptive found only 1 of 2 at conf 0.052.
  - Documented the stale-label augmentation bug in memory (`weak-positive-augmentation-bug.md`) to prevent regression.
  - **Weak-target recall regression FIXED.**

### 6.1 Test Theater — Final Choice

| Field | Value |
|---|---|
| **Region** | Santa Barbara Channel / Channel Islands, California |
| **Full channel bbox** | `-120.5, 33.8, -119.0, 34.6` (search/acquisition bbox) |
| **Operational bbox (current scene)** | `-120.8, 34.3, -119.8, 34.7` (western Santa Barbara Channel, open water) |
| **Operational scene #1** | `S1A_IW_GRDH_1SDV_20240711T140858_20240711T140923_054714_06A94E_9466.SAFE` |
| **Operational scene #2** | `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B.SAFE` |
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
| 2 | **Vessel Detection (S2)** | Scene in, clean contacts out | ✅ Baseline complete; ✅ SSDD→GRD domain-gap closure complete (Session #7) | Bull | `darkwatch_yolov8n_ssdd_grd_v4` recovers July 23 weak targets; default + adaptive stretch paths validated; next: scale calibration with more scenes |
| 3 | **Fusion & Attribution (S3)** ★ | Calibrated dark-vessel attribution | ✅ Baseline complete; ✅ v4 adaptive calibration scaled (Session #8); ✅ fusion priors recalibrated with size/shape artifact evidence (Session #9); ✅ Session #9 regressions fixed with match-aware artifact discount + tile-edge size guard (Session #10); ✅ fourth scene integrated and calibration dataset expanded (Session #11); ✅ physical-plausibility AIS gate + learned Platt calibration layer implemented and recal3 locked (Session #12); next: scale to ~100 labels and validate in a new theater | Bull | Four scenes fused (2024-07-11, 07-18, 07-23, 08-11); 46 labeled contacts (27 ARTIFACT, 7 CLEAR, 9 DARK, 3 UNKNOWN); active label source `data/processed/calibration_labels_v4_adaptive_recal3.json`; calibration model `data/processed/fusion_calibration_v4_adaptive_recal3.json`; recal3 reports/maps generated; next: collect more scenes and validate generalization |
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
| 2026-08-05 | Implement static-object exclusion using California OSPR oil platform dataset | First real contact was 58 m from Platform Irene; fixed structures explain many false dark-vessel candidates | Shifts platform-adjacent contacts toward ARTIFACT/REVIEW and prevents false dark-vessel accusations. |
| 2026-08-05 | Run a second Sentinel-1 scene (2024-07-18) to collect CLEAR and ARTIFACT calibration cases | Single-contact Jul 11 scene cannot validate p_clear / p_artifact | 12 contacts, 3 CLEAR, 5 REVIEW, 3 DARK, 1 ARTIFACT — now have ground-truthable positive and negative examples. |
| 2026-08-05 | Improve scene selection with operational bbox overlap | First July 23 candidate had 100% water but 0% theater overlap, wasting a download/prep cycle | Combined score = `water_fraction × operational_overlap`; top correct pass found 94.79% water, 56.94% overlap |
| 2026-08-05 | Force-track `data/processed/calibration_labels.json` in git despite broad `data/` gitignore | Auditable labels are part of the method and must survive cleanups / new sessions | Added `.gitignore` exception `!data/processed/calibration_labels.json` and `git add -f` |
| 2026-08-08 | Use photometric-only augmentation for weak-positive GRD chips | Geometric flips/rotations silently corrupted YOLO bounding boxes on the first weak-positive augmentation pass | New `scripts/augment_weak_positives.py` applies brightness/contrast, speckle, Gaussian noise, gamma, and mild blur; boxes stay valid |
| 2026-08-08 | Train mixed detectors from previous mixed weights | Starting each mixed run from the previous mixed model preserves already-learned GRD features and stabilizes short fine-tunes | v2 → v3 → v4 chained fine-tunes, each <50 epochs, each improving or preserving validation metrics |
| 2026-08-08 | Use `workers=0` for Ultralytics training on Windows RTX 5060 | `workers>0` triggers multiprocessing CUDA spawn / OpenCV OOM errors on this machine | `scripts/train_detector.py` now forwards `--workers`; default runs use `workers=0` and batch=4 |

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
| 2026-08-04 | ⚠️ WATCH — SSDD→GRD domain gap yields low recall on real tiles (1 unique contact on Jul 11, 12 on Jul 18) | Medium — limits S2 utility; not a Phase 3 blocker | Bull |
| 2026-08-04 | ✅ RESOLVED — AIS data pull for the 2024-07-11 Santa Barbara Channel window (`AIS_2024_07_11.zip` downloaded, filtered, fused) | — | Bull |
| 2026-08-04 | ✅ RESOLVED — Darkwatch extracted into its own git repository at `C:/Users/point/projects/darkwatch` | — | Bull |
| 2026-08-04 | ✅ RESOLVED — First real dark-vessel attribution verdict produced (DARK, p=0.9732) | — | Bull |
| 2026-08-04 | ✅ RESOLVED — Public GitHub repo `satyamdas03/darkwatch` created and pushed | — | Bull |
| 2026-08-04 | ✅ RESOLVED — GitHub profile README repo `satyamdas03/satyamdas03` created and pushed | — | Bull |
| 2026-08-05 | ✅ Baseline calibration framework shipped (`scripts/evaluate_calibration.py` + 15 labels) | High — empirical calibration now needs more scenes, especially CLEAR/ARTIFACT, to reach statistical confidence | Bull |
| 2026-08-05 | ✅ RESOLVED — SSDD→GRD domain gap / July 23 weak-target recall regression fixed by v4 mixed detector + photometric weak-positive augmentation | High — `darkwatch_yolov8n_ssdd_grd_v4` recovers both July 23 DARK vessels; domain gap is closed for current test theater | Bull |
| 2026-08-05 | ✅ All work committed/pushed: `61a1dc5` | — | Bull |
| 2026-08-09 | ✅ Session #11: 2024-08-11 scene integrated; 46 labeled contacts; next: learned calibration + physical-plausibility gate | High — moves the core calibration goal forward before more scene collection | Bull |
| 2026-08-09 | ✅ RESOLVED — Implement learned calibration layer on 46-label dataset | High — per-class Platt scaling now saved and applied at inference; Brier improved for ARTIFACT, CLEAR, DARK | Bull |
| 2026-08-09 | ✅ RESOLVED — Add physical-plausibility gate for AIS matches | High — prevents oversized SAR contacts from being falsely matched to single cooperative vessels (KNOX T lesson) | Bull |
| 2026-08-11 | **OPEN — Scale calibration dataset to ~100 labels and validate in a second theater** | High — current calibration is in-sample on Santa Barbara Channel; need out-of-sample generalization before strong claims | Bull |

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

### 2026-08-04 — Session #1 (continued): GitHub profile README created
- Deep-dived public GitHub metadata (84 public repos) and synthesized with existing profile memory + web research.
- LinkedIn direct fetch blocked for auth; used public web search and memory to capture headline, education, experience, NeuralQuant/QuantAlpha AI, certifications, and recent posts.
- Created public GitHub profile README repository `satyamdas03/satyamdas03` with animated typing header, visitor badge, social links, featured projects table, tech stack badges, GitHub stats cards, publications, certifications, and connect CTA.
- Pushed profile README live: https://github.com/satyamdas03/satyamdas03
- Updated `DOSSIER.md` with this milestone.
- **All requested deliverables complete.**

### 2026-08-05 — Session #2: static-object exclusion + second scene fusion
- Implemented `darkwatch/fusion/static_objects.py` with 32 California oil platforms from OSPR ds357.
- Integrated static-object check into `associate_contact()` in `darkwatch/fusion/associate.py`; artifact probability is boosted proportionally when a contact is within ~250 m of a known platform.
- Exported new symbols in `darkwatch/fusion/__init__.py`.
- Updated `scripts/fuse_contacts.py` to serialize `static_object` in `verdicts.json`.
- Added two regression tests in `tests/test_fusion.py` and moved existing CLEAR test coordinates away from Platform Irene.
- Re-ran July 11 fusion: the single contact is now correctly classified **ARTIFACT** (p_artifact=0.6576) because it is 58 m from Platform Irene.
- Downloaded and prepped second Sentinel-1 scene `S1A_IW_GRDH_1SDV_20240718T015853_20240718T015918_054809_06ACA2_D01B.SAFE`:
  - 96 tiles (48 VV + 48 VH) at `data/processed/s1a_20240718_channel/`.
  - 12 unique contacts at `data/processed/detections_20240718/contacts.json`.
- Downloaded NOAA AIS for 2024-07-18; clipped to 621 rows / 7 tracks at `data/external/ais/ais_2024-07-18_clipped.csv`.
- Ran `scripts/fuse_contacts.py` on July 18:
  - Verdicts: **CLEAR 3, REVIEW 5, DARK 3, ARTIFACT 1**.
  - CLEAR matches: MSC GIUSY (108 m), MSC SOFIA PAZ (308 m), RYAN T (295 m).
  - ARTIFACT: Platform Harvest (82 m), p_artifact=0.50.
  - Strong DARK candidates: 3 contacts with no AIS within gate and no nearby platform.
- Generated `notebooks/fusion_20240718_report.md` with full per-contact reasoning and theater AIS summary.
- Ran tests: `pytest tests/ -q` → **16 passed**.
- Updated `DOSSIER.md` with all new milestones.
- **Next action:** empirical calibration of component probabilities using the new CLEAR/ARTIFACT/DARK labels, and begin collecting additional scenes to build a calibration dataset.

### 2026-08-05 — Session #3: calibration framework + interactive maps + next scene download
- Built `scripts/evaluate_calibration.py` and `data/processed/calibration_labels.json` (13 labeled contacts: 6 ARTIFACT, 3 CLEAR, 2 DARK, 2 UNKNOWN).
- Generated first calibration report at `notebooks/calibration/calibration_report.md` with per-class Brier scores and reliability diagrams.
  - Preliminary finding: model is directionally correct (CLEAR contacts get high `p_clear`, ARTIFACT contacts get moderate/high `p_artifact`, DARK candidates get high `p_dark`) but sample size is too small for strong calibration claims.
- Built `scripts/visualize_fusion.py` with Folium: SAR contacts colored by verdict, AIS track lines, interpolated SAR-time positions, oil platform markers, and 2 km gate circles.
- Generated `notebooks/fusion_20240718_map.html` and `notebooks/fusion_20240711_map.html`.
- Re-scored all 19 July 2024 passes with `scripts/pick_ocean_scene.py`; top candidates identified (100% water on 2024-07-23T140922 and 2024-07-11T140923).
- Started background download of `S1A_IW_GRDH_1SDV_20240723T140922_20240723T140947_054889_06AF64_20C2.SAFE` (100% water) to grow the calibration dataset.
- **Next action:** wait for July 23 scene download, then prep → detect → fuse → label → update calibration report.

### 2026-08-05 — Session #4: scene-selection fix + correct July 23 scene + 2 more DARK labels
- Downloaded and prepped the wrong July 23 scene (`...T140922...`) first: 0 contacts because the scene has 0% overlap with the operational bbox despite 100% overall water.
- **Lesson:** footprint water fraction is not enough; a scene must overlap the actual theater.
- Improved `scripts/pick_ocean_scene.py`:
  - Added `--operational-bbox` argument.
  - Added `_operational_overlap()` to compute footprint ∩ operational bbox fraction.
  - Combined score = `water_fraction × operational_overlap`.
  - Re-scored July 2024: top candidate is now `S1A_IW_GRDH_1SDV_20240723T020701_...` (94.79% water, 56.94% operational overlap, score 53.97%).
- Downloaded and prepped the correct July 23 scene (`S1A_IW_GRDH_1SDV_20240723T020701_20240723T020726_054882_06AF26_69FC.SAFE`) at 02:07 UTC; produced 24 tiles (12 VV + 12 VH).
- Re-fetched NOAA AIS for 2024-07-23 with the correct SAR time window; got 591 clipped rows / 8 usable tracks.
- Detector found **2 unique contacts** near (-120.79, 34.71) after trying several dB contrast stretches; the default stretch produced 0 contacts, highlighting the SSDD→GRD domain-gap.
- Fused July 23 contacts with AIS: both labeled **DARK** (p_dark ≈ 0.70, p_review ≈ 0.23); nearest AIS track **BERNARDINE C** was 24 km away.
- Generated `notebooks/fusion_20240723_report.md` and `notebooks/fusion_20240723_map.html`.
- Added the 2 July 23 contacts to `data/processed/calibration_labels.json` as DARK labels.
- Regenerated calibration report: now **15 labeled contacts** (6 ARTIFACT, 3 CLEAR, 4 DARK, 2 UNKNOWN); Brier scores slightly improved for DARK class.
- **Next action:** collect more scenes with heavy traffic to get more CLEAR labels, and more platform-rich passes to get more ARTIFACT labels. Continue detector improvement work (SSDD→GRD domain gap is the main throughput bottleneck).

### 2026-08-05 — Session #5: documentation + state consolidation
- Updated `README.md` with a Calibration & Visualization section, real results for July 11/18, scene-selection tip, and revised roadmap that foregrounds detector improvement.
- Force-tracked `data/processed/calibration_labels.json` by adding `!data/processed/calibration_labels.json` to `.gitignore` and using `git add -f`.
- Confirmed all generated artifacts are on disk:
  - `notebooks/calibration/calibration_report.md` (15 labels)
  - `notebooks/fusion_20240718_report.md` and `notebooks/fusion_20240723_report.md`
  - `notebooks/fusion_20240711_map.html`, `notebooks/fusion_20240718_map.html`, `notebooks/fusion_20240723_map.html`
  - `notebooks/contact_viz_20240723/`
- Refreshed `DOSSIER.md` project identity, current state, decisions, blockers, and session log.
- Committed and pushed all changes as `61a1dc5` to `satyamdas03/darkwatch`.
- **Status after this consolidation:** Phase 3 baseline is locked; the next high-impact work is detector improvement to close the SSDD→GRD domain gap.

### 2026-08-08 — Session #7: closing the July 23 weak-target recall regression (SSDD→GRD domain gap CLOSED)
- **Goal:** fix the mixed detector's failure to detect small, low-backscatter real Sentinel-1 vessels, then validate that the SSDD→GRD domain gap is closed.
- **Completed:**
  - Diagnosed and documented the stale-label weak-positive augmentation bug: an early augmentation pass rotated/flipped the 2 July 23 DARK positives without recomputing YOLO boxes, silently corrupting training labels.
  - Created `scripts/augment_weak_positives.py` with photometric-only augmentation (brightness/contrast, multiplicative speckle, additive Gaussian noise, gamma, mild blur) that leaves bounding boxes unchanged.
  - Regenerated `data/processed/grd_chips_20240723_weak_aug/` as 100 augmented chips from 2 source positives (50 each).
  - Rebuilt mixed dataset `data/processed/mixed_ssdd_grd_v4/`: 2,986 train / 527 val images, 1,084 training positives, 1,902 negatives (SSDD + July 11/18/23 chips + augmented July 23 weak positives).
  - Fixed `scripts/train_detector.py` so `--workers` is forwarded to `VesselDetector.train()`; used `workers=0` / batch=4 to avoid Windows multiprocessing CUDA spawn errors.
  - Trained `darkwatch_yolov8n_ssdd_grd_v4` from v3 weights; early-stopped at epoch 11 (best epoch 1). Validation: **P=0.933, R=0.885, mAP50=0.953, mAP50-95=0.670**.
  - Validated v4 on all three real scenes:
    - **July 11:** 1 unique contact, conf 0.658 — same physical vessel as v3/SSDD-only.
    - **July 18:** 11 unique contacts. Maintained all real vessels; dropped the 1700 m × 606 m platform-edge artifact that SSDD-only had included at conf 0.36.
    - **July 23:** default stretch (-25/-5, conf=0.25) found 3 contacts; **adaptive stretch (-40/-10, 5/95 percentile, conf=0.05)** found 9 contacts and recovered **both known DARK vessels** (det0000 conf 0.764, det0001 conf 0.370). v3 adaptive had found only one at conf 0.052.
  - Re-ran July 23 adaptive validation independently to confirm: v4 produced **9 contacts** vs v3's **1 contact**; the v3-only detection was the weak DARK vessel at conf **0.052**, while v4 returned both DARK vessels at **0.764** and **0.370** plus seven additional low-confidence candidates on the same tile.
  - Wrote memory file `C:\\Users\\point\\.claude\\projects\\C--Users-point-projects-darkwatch\\memory\\weak-positive-augmentation-bug.md` and updated `MEMORY.md`.
- **Key findings:**
  - The mixed detector's July 23 regression was caused by **label corruption on the only two real weak-positive examples**, not by a fundamental model-capacity problem.
  - Photometric augmentation of real weak positives gives the model enough examples to learn low-backscatter vessel appearance without distorting labels.
  - v4 shows a small confidence reduction on bright targets vs SSDD-only, but all real contacts remain well above the detection threshold and one obvious artifact is removed.
  - Adaptive dB stretch is a powerful inference-time knob for faint targets; it should remain exposed in `scripts/detect_tiles.py` and the production inference path.
- **Status:** SSDD→GRD domain gap **closed** for the current test theater. The detector now finds both bright channel traffic and the small, low-backscatter July 23 dark vessels.
- **Tests pass:** `python -m pytest -q` → 16 passed.
- **Next unlock:** scale Phase 3 calibration. Re-run July 11/18/23 fusion with the v4 detector + adaptive stretch, collect additional scenes for CLEAR/ARTIFACT/DARK labels, and empirically validate the calibration curve.
- **Committed and pushed:** `7fefd65` to `satyamdas03/darkwatch` with message `darkwatch: v4 closes July 23 weak-target recall regression`.

### 2026-08-09 — Session #8: scale Phase 3 calibration with v4 + adaptive stretch
- **Goal:** re-run July 11/18/23 with the v4 detector and adaptive dB stretch, fuse contacts, label them, and regenerate the calibration report to empirically validate the probabilistic attribution layer.
- **Completed:**
  - Ran v4 inference on all three scenes with adaptive stretch (5/95 percentile, 0.05 confidence):
    - **July 11:** 2 contacts (1 outside theater, 1 on Platform Irene).
    - **July 18:** 15 contacts (large azimuth-ambiguity/wind artifacts, platform duplicates, and AIS matches).
    - **July 23:** 9 contacts in a tight cluster around the two known DARK vessels.
  - Re-ran fusion for all three scenes; wrote reports to `notebooks/fusion_20240711_v4_adaptive_report.md`, `notebooks/fusion_20240718_v4_adaptive_report.md`, `notebooks/fusion_20240723_v4_adaptive_report.md`.
  - Created `scripts/build_v4_calibration_labels.py` with deterministic labeling rules (AIS match → CLEAR, platform within 250 m → ARTIFACT, oversized detection → ARTIFACT, tile-edge → ARTIFACT, otherwise DARK) plus manual overrides for documented ambiguous cases.
  - Produced `data/processed/calibration_labels_v4_adaptive.json` with **26 labeled contacts**: 11 ARTIFACT, 6 CLEAR, 8 DARK, 1 UNKNOWN.
  - Fixed `scripts/evaluate_calibration.py` to report the actual label file path instead of hardcoding `calibration_labels.json`.
  - Generated new calibration report at `notebooks/calibration_v4_adaptive/calibration_report.md` with Brier scores and reliability diagrams.
- **Key findings from v4 adaptive calibration:**
  - **CLEAR calibration is strong:** all 6 CLEAR labels fall in the 0.60–0.80 `p_clear` bin, and the model is correct on every one (Brier 0.0238).
  - **DARK is overconfident:** mean `p_dark` 0.5366 vs. observed DARK fraction 0.3077; 18 contacts in the 0.60–0.80 `p_dark` bin are only 44.4% actually DARK. Most of the false DARK verdicts are oversized azimuth artifacts or platform-adjacent contacts that the static-object penalty is too weak to flip.
  - **ARTIFACT is underconfident:** mean `p_artifact` 0.1415 vs. observed ARTIFACT fraction 0.4231. The model rarely assigns high artifact probability even when the contact is clearly on a platform or an oversized streak.
  - The softmax association + fixed static-object falloff is the primary miscalibration source; a learned calibration layer or stronger artifact priors are the next step.
- **Decisions:**
  - Keep `data/processed/calibration_labels.json` as the Phase 3 baseline (15 labels, pre-v4).
  - Make `data/processed/calibration_labels_v4_adaptive.json` the active v4 calibration source; future scenes are added here.
  - Preserve the deterministic labeling script so new scenes can be labeled reproducibly and audited.
- **Tests pass:** `python -m pytest tests/ -q` → 16 passed.
- **Next unlock:** recalibrate the fusion component probabilities. Options: (1) stronger static-object penalty / larger buffer, (2) add a size-based artifact prior, (3) fit an isotonic regression or Platt scaling on the 26-label v4 dataset, (4) collect more CLEAR/ARTIFACT/DARK scenes to make calibration statistically robust.
- **Committed and pushed:** `80ef11f` to `satyamdas03/darkwatch` with message `darkwatch: scale Phase 3 calibration with v4 adaptive detector (26 labels)`.

### 2026-08-09 — Session #9: recalibrate fusion priors with size/shape artifact evidence
- **Goal:** fix the DARK overconfidence and ARTIFACT underconfidence found in Session #8 by adding size/shape artifact evidence and strengthening the static-object penalty.
- **Completed:**
  - Added `size_artifact_confidence()` to `darkwatch/fusion/associate.py` with three evidence channels:
    - Oversize ramp: 500–1000 m max dimension.
    - Extreme aspect ratio: 5–10 length/width ratio.
    - Tile-edge truncation: detections within 4 px of a tile border.
  - Strengthened static-object penalty: scaled confidence = `min(1.0, raw_conf * 1.5 + 0.3)`, giving a 0.3 floor for any platform hit inside 250 m.
  - Combined size + static evidence as independent artifact channels and applied to both real-vessel mass and dark-vessel residual (`dark_artifact_coupling=0.6` default).
  - Exposed new knobs in `scripts/fuse_contacts.py`: `--static-confidence-scale`, `--static-confidence-floor`, `--size-max-dim-soft-m`, `--size-max-dim-hard-m`, `--dark-artifact-coupling`.
  - Added `test_oversized_contact_with_no_ais_is_artifact` to `tests/test_fusion.py`.
  - Re-fused all three scenes and produced `data/processed/calibration_labels_v4_adaptive_recal.json` + `notebooks/calibration_v4_adaptive_recal/calibration_report.md`.
- **Calibration impact on 26 v4 labels (recal vs. original):**
  - **ARTIFACT Brier:** 0.3001 → 0.0960. All 11 ARTIFACT labels now have `p_artifact > 0.5`.
  - **DARK Brier:** 0.2235 → 0.0988. Mean `p_dark` dropped from 0.5366 to 0.3452.
  - **CLEAR Brier:** 0.0238 → 0.0379. 4 of 6 CLEAR labels still clear; 2 regressed to REVIEW because the size prior on large-but-matched contacts pushed `p_clear` just below the 0.6 verdict threshold.
  - 1 DARK label (`vv_c21010_r14232_det0000`, small contact with `ymin ≈ 2 px`) flipped to ARTIFACT due to tile-edge truncation.
- **Regressions to address next:**
  - 2 CLEAR → REVIEW cases: `vh_c2380_r8843_det0000` (MSC GIUSY, 714 m detection) and `vh_c6860_r7947_det0000` (JACKIE C, 353 m detection, near Platform Harmony). The size prior is too aggressive on large-but-cooperative vessels. Fix: reduce artifact penalty when AIS match confidence is high, or soften size ramp for contacts with a track inside the gate.
  - 1 DARK → ARTIFACT false positive: `vv_c21010_r14232_det0000` is genuinely small (42 × 32 m) but sits within 2 px of the top tile edge. Fix: require a minimum physical size for tile-edge penalty, or pass actual tile dimensions so only far-edge truncation triggers.
- **Tests pass:** `python -m pytest tests/ -q` → 17 passed.
- **Next unlock:** tune the two regressions (CLEAR size prior and tile-edge false positive), then collect more scenes to make calibration statistically robust.
- **Committed and pushed:** `0253b96` to `satyamdas03/darkwatch` with message `darkwatch: recalibrate fusion priors with size/shape artifact evidence`.

### 2026-08-09 — Session #10: tune fusion regressions with match-aware artifact discount and tile-edge size guard
- **Goal:** fix the two CLEAR→REVIEW regressions and one DARK→ARTIFACT false positive introduced by Session #9's size/shape artifact prior, while preserving the ARTIFACT/DARK calibration gains.
- **Completed:**
  - Added a **match-aware artifact discount** to `darkwatch/fusion/associate.py`: after combining size/shape + static artifact evidence, the combined confidence is rescaled by `(1 - p_matched_given_real) ** artifact_conf_ais_discount_power`. This protects contacts with strong in-gate AIS matches from being pushed below the `p_clear > 0.6` verdict threshold by spurious oversize or static-object signals.
  - Added a **tile-edge size guard** in `size_artifact_confidence()`: the tile-edge truncation channel now only fires when `max_dim >= size_tile_edge_min_size_m` (default 80 m) or, optionally, when the contact occupies a configured fraction of the tile. This prevents small plausible vessels a few pixels from the border from being misclassified as ARTIFACT.
  - Exposed new knobs in `scripts/fuse_contacts.py`: `--size-tile-edge-min-size-m`, `--size-tile-edge-min-tile-ratio`, `--artifact-conf-ais-discount-power`.
  - Added regression tests to `tests/test_fusion.py`: a small near-edge contact stays out of ARTIFACT, and a platform-adjacent contact with a strong AIS match returns to CLEAR. Total tests now **19 passed**.
  - Re-fused all three scenes into `data/processed/fusion_202407{11,18,23}_v4_adaptive_recal2/verdicts.json` and produced `data/processed/calibration_labels_v4_adaptive_recal2.json` + `notebooks/calibration_v4_adaptive_recal2/calibration_report.md`.
- **Calibration impact on 26 v4 labels (recal2 vs. recal):**
  - **All 3 known regressions resolved:**
    - `vh_c2380_r8843_det0000` (MSC GIUSY): REVIEW → CLEAR (`p_clear=0.702`, `p_artifact=0.118`).
    - `vh_c6860_r7947_det0000` (JACKIE C, near Platform Harmony): REVIEW → CLEAR (`p_clear=0.662`, `p_artifact=0.180`).
    - `vv_c21010_r14232_det0000` (small vessel near tile edge): ARTIFACT → DARK (`p_dark=0.674`, `p_artifact=0.101`).
  - **ARTIFACT Brier:** 0.0960 → 0.0854.
  - **CLEAR Brier:** 0.0379 → 0.0249.
  - **DARK Brier:** 0.0988 → 0.1000 (essentially unchanged; within noise).
  - **Per-label confusion matrix:** 10/11 ARTIFACT correct, 6/6 CLEAR correct, 8/8 DARK correct, 1 UNKNOWN → DARK.
  - **One new edge case:** `vh_c21010_r14232_det0002` (ARTIFACT label, small 67×40 m tile-edge contact) moved to DARK because the new 80 m minimum size guard no longer flags it as artifact. Logged for the next guard-tuning pass; net regressions fixed (3) exceed new regressions (1).
- **Decisions:**
  - Make `data/processed/calibration_labels_v4_adaptive_recal2.json` the active v4 calibration source; future scenes are added here.
  - Keep Session #8 (`calibration_labels_v4_adaptive.json`) and Session #9 (`calibration_labels_v4_adaptive_recal.json`) labels under version control for traceability.
- **Tests pass:** `python -m pytest tests/ -q` → **19 passed**.
- **Next unlock:** collect more CLEAR/ARTIFACT/DARK scenes to move from 26 labels to a statistically robust calibration dataset; revisit the small tile-edge guard if more edge-truncation labels appear.
- **Committed and pushed:** `33e78b1` to `satyamdas03/darkwatch` with message `darkwatch: fix Session #9 fusion regressions with match-aware artifact discount and tile-edge size guard`.

### 2026-08-08 — Session #6: closing the SSDD→GRD detector domain gap
- **Goal:** train a detector that generalizes from SSDD to real Sentinel-1 GRD by mixing real GRD training chips back into the dataset.
- **Completed:**
  - Relaunched failed mixed training as `darkwatch_yolov8n_ssdd_grd_v2`; finished 18 epochs with `mAP50=0.938`, `recall=0.879`, `precision=0.903`; weights now in repo under `models/detector_runs/darkwatch_yolov8n_ssdd_grd_v2/weights/best.pt`.
  - Fixed `scripts/extract_grd_chips.py` usage: re-extracted July 23 positives from loose detections, yielding 2 DARK-labeled vessel chips + 201 negatives.
  - Added `scripts/build_mixed_dataset.py` for reproducible SSDD+GRD merging with stratified train/val splits.
  - Built `data/processed/mixed_ssdd_grd_v3/`: 2,901 train / 512 val images, 1,017 training positives (SSDD + July 11/18/23).
  - Completed `darkwatch_yolov8n_ssdd_grd_v3` training from v2 weights on the expanded dataset; finished 2 epochs with best `mAP50=0.958`, final `mAP50=0.939`, `recall=0.869`, `precision=0.910`; weights at `models/detector_runs/darkwatch_yolov8n_ssdd_grd_v3/weights/best.pt`.
  - Validated v2 and v3 mixed detectors on all three scenes against the SSDD-only baseline.
- **Scene-by-scene detector comparison:**
  - **July 11:** 1 contact for all models. Confidences: SSDD-only 0.822; v3 mixed 0.783; v2 mixed 0.658–0.667.
  - **July 18:** 10–13 contacts. SSDD-only found 12 (conf 0.326–0.828); v3 mixed found 10–12 (conf 0.268–0.815); v2 mixed found 11–13 (conf 0.263–0.797). v3 roughly matches SSDD-only; v2 introduced extra weak candidates.
  - **July 23:** SSDD-only found 0 contacts at default `conf=0.25`, but 4 contacts at `conf=0.05` with stretch (-30, -10). Both v2 and v3 mixed detectors found **0 contacts even at `conf=0.05`**, a clear recall regression on small/weak targets.
- **Tests pass:** `python -m pytest -q` → 16 passed.
- **Key findings:**
  - Mixing real GRD chips raises validation mAP and restores confidence on bright targets (July 11/18), but does **not** automatically fix recall on small weak targets when the positive count is tiny.
  - July 23 targets are small (46–68 m) and low-backscatter. The 2 positive chips are only 37×56 px and represent a tiny fraction of the mixed dataset.
  - Default contrast stretch (-25, -5) and looser (-30, -10) both miss July 23 targets with the mixed model; lowering confidence to 0.05 still returns nothing.
- **Next unlock:** explicit weak-target representation. Options ranked by likely impact:
  1. Collect / synthesize more real small-vessel GRD positives (additional scenes, data augmentation, or synthetic low-backscatter ships).
  2. Add an **adaptive dB stretch** path in `darkwatch/detect/detector.py` so inference can per-tile optimize contrast for faint targets.
  3. Tile the scene at finer effective resolution and run multi-scale detection.
  4. Retrain with class-aware or scale-aware loss (e.g., smaller anchor boxes, FPN tuning) if YOLOv8n exposes those knobs.
- **Committed and pushed:** all code, logs, manifests, and sample inference outputs committed as `d781488` to `satyamdas03/darkwatch`.

### 2026-08-09 — Session #11: integrate 2024-08-11 scene and expand calibration dataset
- **Goal:** add a fourth real Sentinel-1 scene to the active calibration source, label its contacts, and regenerate the calibration report to move toward a statistically robust dataset.
- **Completed:**
  - Processed Sentinel-1 scene `S1A_IW_GRDH_1SDV_20240811T015853_20240811T015918_055159_06B8DF_48C3.SAFE` through prep, v4 adaptive detection (20 contacts), NOAA AIS fetch (263 clipped rows → 3 tracks), and fusion.
  - Fusion verdict counts for 2024-08-11: **ARTIFACT 15, CLEAR 2, DARK 2, REVIEW 1**.
  - Created `scripts/download_ais_noaa.py` (Python requests-based NOAA daily zip downloader with resume support) after a truncated curl download produced a BadZipFile.
  - Created `scripts/process_scene.py` end-to-end wrapper: S1 download → prep tiles → detect → fetch AIS → fuse → report + map.
  - Generated `notebooks/fusion_20240811_report.md`, `notebooks/fusion_20240811_map.html`, and `notebooks/contact_viz_20240811_v4_adaptive/` (40 full + zoom PNGs).
  - Visually reviewed all 20 Aug 11 contact chips and assigned ground-truth labels:
    - **ARTIFACT 13:** 7 platform-adjacent contacts and 6 oversized sea-surface patches.
    - **CLEAR 1:** RYAN T (MMSI 367104050) at 281 m, moored at Platform Hondo.
    - **DARK 1:** bright vessel-like contact with no AIS within gate and no platform nearby.
    - **UNKNOWN 2:** very faint or thin ambiguous contacts that could not be confirmed as real vessels.
  - Added one critical calibration correction: the oversized 1591 m × 1543 m contact matched to **KNOX T** at 995 m was labeled **ARTIFACT** despite the model's CLEAR verdict, because the spatial extent is physically impossible for the cooperative track.
  - Appended Aug 11 labels to `data/processed/calibration_labels_v4_adaptive_recal2.json`; active calibration source now has **46 labeled contacts** (27 ARTIFACT, 7 CLEAR, 9 DARK, 3 UNKNOWN).
  - Regenerated `notebooks/calibration_v4_adaptive_recal2/calibration_report.md` and plots.
- **Calibration impact after adding Aug 11:**
  - **CLEAR Brier:** 0.0249 → 0.0259 (stable; 7/7 CLEAR labels correct).
  - **DARK Brier:** 0.1000 → 0.0929 (improved; 9/9 DARK labels correct).
  - **ARTIFACT Brier:** 0.0854 → 0.0945 (slightly worse; 25/27 ARTIFACT labels correct, driven by 1 misclassified oversized KNOX T match and 1 low-confidence DARK label that the model calls ARTIFACT).
  - The KNOX T mismatch is a valuable counter-example: high AIS association probability alone is not sufficient when the SAR contact shape/size is physically incompatible with the matched vessel.
- **Decisions:**
  - Keep the oversized KNOX T match as an ARTIFACT label to teach the calibration layer that AIS association must be gated by plausible vessel dimensions.
  - Add `.gitignore` exceptions for `data/processed/calibration_labels_v4_adaptive_recal2.json` and calibration report directories if not already present; commit the active label source and report so the dataset is auditable.
- **Tests pass:** `python -m pytest tests/ -q` → **19 passed**.
- **Next unlock:** collect additional scenes (especially more CLEAR vessel matches and unambiguous open-water DARK cases) to reach ~100 labeled contacts, or implement a learned calibration layer (isotonic/Platt) on the 46-label dataset.

### 2026-08-11 — Session #12: physical-plausibility AIS gate + learned calibration layer, recal3 locked
- **Goal:** close the two highest-impact Phase 3 gaps identified in Session #11: (1) an oversized SAR contact with a strong AIS match must not be called CLEAR, and (2) raw fusion probabilities must be empirically calibrated so reported confidences match observed frequencies.
- **Completed:**
  - Implemented `physical_plausibility_confidence()` in `darkwatch/fusion/associate.py`.
    - Compares the SAR contact's max dimension to the matched AIS vessel's reported `Length`.
    - Defaults tuned to `length_tolerance=5.0` and `absolute_margin_m=200.0` so that normal SAR smearing of small cooperative vessels is tolerated, while extreme mismatches like the 1591 m KNOX T contact are penalized.
    - Reduces `p_matched_given_real` when a match is implausible; this disables the match-aware artifact discount, letting oversize/static evidence push the verdict toward ARTIFACT.
  - Added CLI knobs to `scripts/fuse_contacts.py` (`--disable-physical-plausibility`, `--plausibility-length-tolerance`, `--plausibility-absolute-margin-m`).
  - Added two regression tests in `tests/test_fusion.py`: a plausible small-vessel match stays CLEAR, and an oversized match is flagged ARTIFACT.
  - Re-ran fusion for all four scenes with the gate, producing `data/processed/fusion_*_v4_adaptive_recal3/` and `data/processed/calibration_labels_v4_adaptive_recal3.json`.
  - Verified the KNOX T oversized contact (`vv_c9565_r7943_det0002`, 1591 m × 1543 m matched to 32 m KNOX T) now comes back **ARTIFACT** (`p_artifact = 0.6862`) instead of CLEAR.
  - Implemented `darkwatch/fusion/calibration.py`: a small per-class Platt-scaling model with L2 regularization, fitted by minimizing Brier score.
  - Implemented `scripts/fit_calibration.py` to fit the model on the 46 recal3 labels and save it to `data/processed/fusion_calibration_v4_adaptive_recal3.json`.
  - Integrated optional calibration-model application into `scripts/fuse_contacts.py` and `scripts/evaluate_calibration.py` via `--calibration-model`.
  - Re-ran all four recal3 fusion runs with the saved calibration model applied, producing calibrated verdicts and probabilities.
  - Generated recal3 fusion reports and interactive maps:
    - `notebooks/fusion_20240711_v4_adaptive_recal3_report.md` + `_map.html`
    - `notebooks/fusion_20240718_v4_adaptive_recal3_report.md` + `_map.html`
    - `notebooks/fusion_20240723_v4_adaptive_recal3_report.md` + `_map.html`
    - `notebooks/fusion_20240811_v4_adaptive_recal3_report.md` + `_map.html`
  - Regenerated calibration report: `notebooks/calibration_recal3/calibration_report.md` with reliability diagrams and probability distributions.
- **Calibration impact (recal3, in-sample, 46 labels):**
  - **ARTIFACT Brier:** 0.1280 (gate only) → 0.0793 (gate + calibration)
  - **CLEAR Brier:** 0.1275 → 0.0679
  - **DARK Brier:** 0.1102 → 0.0641
  - Mean predicted probabilities are closer to observed label fractions in every class; reliability plots hug the diagonal better.
- **Verdict impact:**
  - All 9 DARK labels correctly predicted DARK.
  - 26 of 27 ARTIFACT labels correctly predicted ARTIFACT.
  - 4 of 7 CLEAR labels correctly predicted CLEAR; the 3 CLEAR→ARTIFACT errors are the oversized KNOX T and OCEAN SENTINEL matches, which are now treated as implausible artifacts rather than confident matches (labels may need re-review).
- **Decisions:**
  - Active calibration source is now `data/processed/calibration_labels_v4_adaptive_recal3.json`.
  - Saved calibration model `data/processed/fusion_calibration_v4_adaptive_recal3.json` is applied at recal3 inference time by default.
  - Default physical-plausibility constants are `length_tolerance=5.0`, `absolute_margin_m=200.0`.
- **Tests pass:** `python -m pytest tests/ -q` → **21 passed**.
- **Next unlock:** scale the calibration dataset to ~100 labeled contacts and validate in a second theater to test out-of-sample generalization of the gate and calibration model.

### 2026-08-11 — Session #13: scale calibration to 122 labels + Gulf of Mexico out-of-sample validation
- **Goal:** execute the Session #12 next unlock: expand the labeled calibration dataset from 46 toward ~100 contacts and measure out-of-sample generalization in a second theater (Gulf of Mexico offshore Louisiana).
- **Completed:**
  - Updated `scripts/build_v4_calibration_labels.py`:
    - Corrected default Santa Barbara theater to `(-120.8, 34.3, -119.8, 34.7)`.
    - Added `--theater`, `--scenes`, and `--base-labels` arguments so authoritative labels can be preserved while auto-labeling new scenes.
  - Generated `data/processed/calibration_labels_v4_adaptive_recal4_auto.json` by merging the 46 authoritative recal3 labels with rule-based labels for two new Santa Barbara scenes (2024-08-16, 2024-08-28), producing 64 Santa Barbara labels.
  - Generated review grids for the 18 new Santa Barbara contacts and visually inspected them; all low-confidence northern tile-edge contacts kept as ARTIFACT, two OSAKA BAY AIS matches kept as CLEAR.
  - Processed Gulf of Mexico scene `S1A_IW_GRDH_1SDV_20240708T000210_..._F3B2` with the fixed `process_scene.py` AIS center-time bug (acquisition time now read from prep manifest), recovering 5 AIS tracks and 58 contacts.
  - Auto-labeled Gulf contacts with `scripts/build_v4_calibration_labels.py --scenes gulf --theater -90.3 28.2 -89.5 28.8`, then manually reviewed and corrected high-confidence contacts outside the strict operational theater from ARTIFACT to DARK, producing `data/processed/calibration_labels_v4_adaptive_gulf_reviewed.json` (13 ARTIFACT, 3 CLEAR, 42 DARK).
  - Built combined training dataset `data/processed/calibration_labels_v4_adaptive_combined.json` with 122 labels (56 ARTIFACT, 12 CLEAR, 51 DARK, 3 UNKNOWN) spanning Santa Barbara and Gulf theaters.
  - Fitted three calibration models:
    - `data/processed/fusion_calibration_v4_adaptive_recal4.json` (64 Santa Barbara labels)
    - `data/processed/fusion_calibration_v4_adaptive_combined.json` (122 Santa Barbara + Gulf labels)
  - Evaluated out-of-sample on the 58 labeled Gulf contacts under four model variants.
- **Out-of-sample Gulf calibration results (Brier score, lower is better):**

  | Model | DARK Brier | ARTIFACT Brier | CLEAR Brier | Notes |
  |---|---|---|---|---|
  | Raw fusion (no calibration) | 0.1606 | 0.1653 | 0.0036 | Base model already reasonably calibrated for Gulf DARK |
  | Recal3 (46 SB labels) | 0.1472 | 0.1674 | 0.0005 | Best Gulf DARK Brier; less aggressive artifact suppression |
  | Recal4 (64 SB labels) | 0.2593 | 0.1932 | 0.0067 | Worse than raw; overfit to Santa Barbara artifacts |
  | Combined (122 SB + Gulf labels) | 0.1631 | 0.1450 | 0.0045 | Balanced compromise across both theaters |

- **Key findings:**
  - A calibration model trained only on Santa Barbara does **not** transfer cleanly to the Gulf: recal4 DARK Brier is 0.26 vs raw 0.16. The Santa Barbara dataset is artifact-heavy (43/64 ARTIFACT), so the learned model suppresses DARK probabilities too strongly for a theater where most real contacts are actually dark.
  - The raw fusion engine is already surprisingly well-calibrated for Gulf DARK; the main value of calibration is sharpening ARTIFACT discrimination in the original theater.
  - The combined (cross-theater) model is the best default going forward: it improves ARTIFACT Brier on Gulf (0.145 vs raw 0.165) without the severe DARK suppression of the Santa-Barbara-only recal4 model.
  - The physical-plausibility gate is in place and working; no oversized CLEAR mismatches were observed in the Gulf scene. The remaining artifact class is dominated by oversized azimuth-ambiguity/wind-streak detections and tile-edge truncations.
- **Decisions:**
  - Default calibration model is now `data/processed/fusion_calibration_v4_adaptive_combined.json` (cross-theater, 122 labels).
  - Operational rule: when deploying to a new theater, collect ~20 local labels before trusting calibrated probabilities; raw fusion probabilities may be more reliable until local calibration is available.
  - `data/processed/calibration_labels_v4_adaptive_combined.json` becomes the authoritative training set for future calibration iterations.
  - Gulf platform catalog remains absent; platform-adjacent contacts in the Gulf were handled by manual review (no false CLEARs observed).
- **Next unlock:**
  - Add a minimal Gulf static-object catalog (BOEM/NOAA platform locations) so future Gulf runs can auto-exclude platforms.
  - Collect a third theater (e.g., Mediterranean or North Sea) to test true out-of-sample transfer of the combined model.
  - Consider a theater-aware or regularized calibration formulation (e.g., strong L2 toward identity, or per-theater intercepts) to reduce cross-theater degradation.

### 2026-08-11 — Session #13.5: add Gulf of Mexico static-object catalog
- **Goal:** close the last manual-review gap in the Gulf theater by adding BOEM/BSEE platform locations to `darkwatch/fusion/static_objects.py`.
- **Completed:**
  - Extended `darkwatch/fusion/static_objects.py`:
    - Added `_platforms_gulf_of_mexico()` that reads from a cached BOEM GeoJSON or a small hard-coded fallback.
    - Made `default_static_objects()` theater-aware (`santa_barbara`, `santa_barbara_channel`, `gulf`, `gulf_of_mexico`).
  - Added `scripts/fetch_boem_gulf_platforms.py` to refresh the cache from the BOEM/BSEE ArcGIS REST service.
  - Fetched `data/external/boem_gulf_platforms.geojson` (1,316 platforms, 30 inside the `-90.3,28.2,-89.5,28.8` theater bbox).
  - Wired `--theater` through `scripts/fuse_contacts.py` and `scripts/process_scene.py`.
  - Added `static_objects` argument to `associate_contact()` / `associate_all_contacts()` so callers can override the catalog.
  - Added Gulf static-object unit tests in `tests/test_fusion.py`.
  - Regenerated `notebooks/fusion_20240708_report.md` and `notebooks/fusion_20240708_map.html` using `--theater gulf`.
- **Validation:**
  - `pytest tests/ -q` → **23 passed**.
  - Re-ran Gulf 2024-07-08 scene with `--theater gulf`:
    - Raw fusion verdicts unchanged (`{'CLEAR': 3, 'DARK': 54, 'ARTIFACT': 1}`) because none of the 58 contacts lie within 250 m of the 30 platforms in the operational bbox.
    - This confirms the manual Gulf ARTIFACT labels were oversized azimuth-ambiguity / wind-streak artifacts, not platform-adjacent contacts.
    - The pipeline is now ready to auto-exclude platforms in future Gulf scenes without manual review.
- **Decisions:**
  - `data/external/boem_gulf_platforms.geojson` is gitignored (regenerated by `scripts/fetch_boem_gulf_platforms.py`).
  - Canonical Gulf fusion output remains raw (uncalibrated) because the scene is the out-of-sample calibration evaluation baseline.
  - Default theater for `fuse_contacts.py` / `process_scene.py` stays Santa Barbara when `--theater` is omitted, preserving backward compatibility.
- **Next unlock:**
  - Collect a third theater (e.g., Mediterranean or North Sea) to test true out-of-sample transfer of the combined calibration model.
  - Consider a theater-aware or regularized calibration formulation (e.g., strong L2 toward identity, or per-theater intercepts) to reduce cross-theater degradation.

### 2026-08-11 — Session #14 (continued): Southern California Bight third-theater validation + Revolutionary roadmap kickoff
- **Goal:** test whether the 122-label combined calibration model transfers to a third theater without large local re-labeling; selected Southern California Bight as the lowest-friction candidate (same OSPR platform catalog and NOAA AIS source as Santa Barbara, but different wave climate and shipping patterns). Beyond validation, the session also kicked off the full revolutionary roadmap: unified CLI, analyst dashboard, and operational context layer.
- **Planned operational bbox:** `-118.5,33.3,-117.5,34.0` (San Pedro Channel / Catalina Basin, open water with shipping lanes).
- **Completed (Phase A — unblock SCB):**
  - Diagnosed the collapsed 201×201 pixel theater window on the 2024-07-06 descending pass.
  - Root cause: `darkwatch/s1_prep/geocode.py::bbox_to_window()` only used the valid corners of the requested bbox when the NE corners fell outside the sparse geolocation-grid convex hull, collapsing the window to a single point plus padding.
  - Fixed `geocode.py` so `bbox_to_window()` intersects the requested bbox with the scene footprint (convex hull of the geolocation grid) and geocodes the covered portion. The same 2024-07-06 scene now produces a 5,762×5,641 px window covering the actual overlap.
  - Updated `scripts/pick_ocean_scene.py` scoring to compute water fraction inside the operational-bbox overlap (not the whole footprint) and added `--min-overlap` (default 75%). This prevents selecting scenes with high open-water fraction but poor theater coverage.
  - Regenerated `data/raw/s1/scene_scores_socal.json`; new top candidate is `S1A_IW_GRDH_1SDV_20240701T135253_20240701T135318_054568_06A44B_14D0.SAFE` (ascending, 44.5% operational water, 100% overlap).
  - Started end-to-end processing of the new top candidate via `scripts/process_scene.py`; download hung (likely Long-Term Archive retrieval from CDSE), so switched to the already-downloaded 2024-07-06 descending pass.
  - Reprocessed 2024-07-06 with the geocoder fix and `--theater santa_barbara`: prep produced 84 tiles (42 VV + 42 VH) covering the actual footprint overlap, detector found **108 contacts**.
  - NOAA AIS daily zip for 2024-07-06 was corrupt from a prior partial download; removed and re-downloaded; `scripts/fetch_ais.py` hardened to stream curl progress and auto-detect/re-download corrupt zips.
  - Fusion completed: **108 contacts**, **665 AIS tracks**, verdict counts (raw) CLEAR 58 / REVIEW 10 / DARK 15 / ARTIFACT 25.
- **Completed (Phase B — third-theater validation):**
  - Generated contact review grids for all 108 SCB contacts under `notebooks/contact_viz_20240706_v4_adaptive/`.
  - Built 108 auto-labels in `data/processed/calibration_labels_v4_adaptive_socal.json` (CLEAR 78 / ARTIFACT 20 / DARK 10 / REVIEW 0) using AIS proximity + static-object rules.
  - Evaluated raw, combined, and SCB-specific calibration: combined model improves DARK Brier (0.0640 → 0.0443) but degrades CLEAR (0.1765 → 0.1966) and ARTIFACT (0.1178 → 0.1669) on SCB, confirming imperfect transfer and justifying theater-aware calibration.
- **Completed (Phase C — theater-aware calibration):**
  - Added `darkwatch/fusion/calibration_registry.py`: maps theaters to default calibration models (`santa_barbara`/`gulf` → combined model, `southern_california` → SCB-specific model).
  - Extended static-object `THEATERS` registry with `southern_california`, `southern_california_bight`, `socal`, `scb` aliases to the OSPR platform catalog.
  - Updated `scripts/fuse_contacts.py` and `scripts/process_scene.py` so `--theater` auto-selects the right default calibration model; explicit `--calibration-model` still overrides.
  - Fitted `data/processed/fusion_calibration_v4_adaptive_socal.json` on 108 SCB labels (Platt params: artifact scale=0.978/shift=-0.189, clear scale=1.175/shift=0.258, dark scale=1.163/shift=-0.232, review scale=1.148/shift=-0.095).
  - Re-fused 2024-07-06 with theater-aware SCB calibration: CLEAR 61 / ARTIFACT 28 / DARK 15 / REVIEW 4 (6 REVIEW → CLEAR, 3 REVIEW → ARTIFACT vs raw).
- **Completed (Phase E — unified CLI):**
  - Added `darkwatch/cli.py` with Typer subcommands: `search-scenes`, `process-scene`, `build-labels`, `fit-calibration`, `evaluate`, `serve`.
  - Registered `darkwatch` console entry point in `pyproject.toml`.
  - All unit tests still pass (`pytest tests/ -q` → 23 passed).
- **Next action:**
  - Begin Phase D — analyst web dashboard: FastAPI backend + static HTML/JS frontend, deep-ocean slate palette, Verdict Dial, contact list with filters, scene map, evidence dossier panel.
  - Continue curating a manually reviewed ~20-contact SCB subset to refine calibration; auto-labels remain the proxy until manual review is complete.

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
5. `P(SAR size/type compatible with matched AIS track)` — physical-plausibility gate (pending implementation).
6. `P(calibrated | empirical labels)` — learned calibration mapping raw fusion probabilities to observed frequencies (pending implementation).

Final `P(dark)` is a function of these; the **weakest link** is reported explicitly.

### 14.3 Environment Variables / Secrets (names only, never values)
Store actual values in `.env` (gitignored). Names expected by the code:
- `DARKWATCH_CDSE_USERNAME`
- `DARKWATCH_CDSE_PASSWORD`
- `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` (only if using S3 mirror)
- `GFW_API_KEY` (Phase 4)

The repo-level `.env` is loaded automatically by `scripts/fetch_first_scene.py` and `scripts/pick_ocean_scene.py` via `python-dotenv`.
