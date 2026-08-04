# Darkwatch

A maritime surveillance system that detects vessels that have deliberately switched off their AIS transponders, by fusing free Sentinel-1 SAR imagery with AIS broadcasts and producing calibrated, auditable dark-vessel verdicts.

> **For the complete living project state, read [`DOSSIER.md`](DOSSIER.md) first.**

## Quick start

```bash
# Run tests
python -m pytest tests/ -q

# Search and download a Sentinel-1 scene over the Santa Barbara Channel
python scripts/fetch_first_scene.py --start 2024-07-01 --end 2024-07-12 --download

# Pick the pass with the most open ocean
python scripts/pick_ocean_scene.py --start 2024-07-01 --end 2024-07-31

# Prep a scene into analysis-ready tiles
python scripts/prep_s1.py "data/raw/s1/S1A_...SAFE" --output-dir data/processed/s1a_YYYYMMDD_channel --bbox "-120.8,34.3,-119.8,34.7"

# Convert SSDD to YOLO format and train the detector
python scripts/prepare_ssdd.py
python scripts/train_detector.py --epochs 30 --batch 4

# Detect vessels in tiles
python scripts/detect_tiles.py --manifest data/processed/s1a_YYYYMMDD_channel/manifest.json --output-dir data/processed/detections_YYYYMMDD
```

## Architecture

Five stages from raw radar to an auditable accusation:

1. **SAR Ingestion & Prep** — Sentinel-1 GRD → calibrated, land-masked, georeferenced tiles.
2. **Vessel Detection** — fine-tuned YOLO detector emits candidate contacts.
3. **Fusion & Attribution** — probabilistic match of SAR contacts to AIS tracks; calibrate `P(dark)`.
4. **Behavior & Intent** — zone overlays, persistence, rendezvous detection.
5. **Alert & Evidence** — ranked dossiers with imagery, reasoning, and confidence.

The visual reference is [`darkwatch-architecture.html`](darkwatch-architecture.html).

## License & data

Sentinel-1 SAR is fully open. NOAA Marine Cadastre AIS is public US-government data. Open SAR ship-detection training datasets (SSDD, HRSID, LS-SSDD) should be verified individually before training or redistribution.
