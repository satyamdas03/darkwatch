"""Copernicus Data Space Ecosystem adapter for Sentinel-1 queries and downloads.

This is a swappable SAR data adapter. It exposes a small, stable interface:
  - search()  -> list candidate products
  - download() -> fetch a product to local disk

Authentication uses environment variables:
  DARKWATCH_CDSE_USERNAME
  DARKWATCH_CDSE_PASSWORD
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import urlencode

import requests

CATALOGUE_URL = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
DOWNLOAD_URL = "https://download.dataspace.copernicus.eu/odata/v1/Products"
TOKEN_URL = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"

# Standard Sentinel-1 GRD product type for vessel detection.
_IW_GRDH = "IW_GRDH_1S"


@dataclass(frozen=True)
class S1Product:
    """Lightweight record for a Sentinel-1 product."""

    product_id: str
    name: str
    product_type: str
    footprint: dict  # GeoJSON geometry
    start_time: datetime
    end_time: datetime
    s3_path: str | None = None
    quicklook_url: str | None = None

    @property
    def download_url(self) -> str:
        return f"{DOWNLOAD_URL}({self.product_id})/$value"

    @property
    def native_zip_url(self) -> str:
        return f"{DOWNLOAD_URL}({self.product_id})/$zip"


class CopernicusAdapter:
    """Query and download Sentinel-1 scenes from CDSE."""

    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
        client_id: str = "cdse-public",
    ) -> None:
        self.username = username or os.environ.get("DARKWATCH_CDSE_USERNAME")
        self.password = password or os.environ.get("DARKWATCH_CDSE_PASSWORD")
        self.client_id = client_id
        self._token: str | None = None
        self._token_expiry: float = 0.0

        if not self.username or not self.password:
            raise ValueError(
                "Copernicus credentials required. Set DARKWATCH_CDSE_USERNAME "
                "and DARKWATCH_CDSE_PASSWORD environment variables."
            )

    def _get_token(self) -> str:
        """Refresh the bearer token if needed."""
        if self._token and time.time() < self._token_expiry - 60:
            return self._token

        resp = requests.post(
            TOKEN_URL,
            data={
                "client_id": self.client_id,
                "grant_type": "password",
                "username": self.username,
                "password": self.password,
            },
            timeout=30,
        )
        resp.raise_for_status()
        payload = resp.json()
        self._token = payload["access_token"]
        # Tokens are usually 10 minutes; keep a safety margin.
        self._token_expiry = time.time() + payload.get("expires_in", 600)
        return self._token

    @property
    def _session(self) -> requests.Session:
        session = requests.Session()
        session.headers["Authorization"] = f"Bearer {self._get_token()}"
        return session

    def search(
        self,
        bbox: tuple[float, float, float, float],
        start: datetime,
        end: datetime,
        product_type: str = _IW_GRDH,
        max_results: int = 20,
        orbit_direction: str | None = None,
        polarisation: str | None = None,
    ) -> list[S1Product]:
        """Search CDSE for Sentinel-1 products overlapping a bbox and time range.

        Args:
            bbox: (min_lon, min_lat, max_lon, max_lat) in WGS84.
            start, end: UTC datetime objects.
            product_type: Sentinel-1 product type, default IW_GRDH_1S.
            max_results: OData $top limit.
            orbit_direction: Optional filter 'ASCENDING' or 'DESCENDING'.
            polarisation: Optional filter, e.g. 'VV VH'.

        Returns:
            List of S1Product candidates, sorted by acquisition time ascending.
        """
        min_lon, min_lat, max_lon, max_lat = bbox
        polygon_wkt = (
            f"POLYGON(({min_lon} {min_lat}, {max_lon} {min_lat}, "
            f"{max_lon} {max_lat}, {min_lon} {max_lat}, {min_lon} {min_lat}))"
        )

        filters: list[str] = [
            "Collection/Name eq 'SENTINEL-1'",
            f"Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and "
            f"att/OData.CSC.StringAttribute/Value eq '{product_type}')",
            f"ContentDate/Start gt {start.isoformat(timespec='milliseconds').replace('+00:00', 'Z')}",
            f"ContentDate/Start lt {end.isoformat(timespec='milliseconds').replace('+00:00', 'Z')}",
            f"OData.CSC.Intersects(area=geography'SRID=4326;{polygon_wkt}')",
        ]
        if orbit_direction:
            filters.append(
                f"Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'orbitDirection' and "
                f"att/OData.CSC.StringAttribute/Value eq '{orbit_direction}')"
            )
        if polarisation:
            filters.append(
                f"Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'polarisationChannels' and "
                f"att/OData.CSC.StringAttribute/Value eq '{polarisation}')"
            )

        query = urlencode(
            {
                "$filter": " and ".join(filters),
                "$orderby": "ContentDate/Start asc",
                "$top": max_results,
                "$count": "true",
            },
            safe=":/,=()' ",
        )
        url = f"{CATALOGUE_URL}?{query}"

        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        payload = resp.json()

        products: list[S1Product] = []
        for value in payload.get("value", []):
            attrs = {a["Name"]: a.get("Value") for a in value.get("Attributes", [])}
            products.append(
                S1Product(
                    product_id=value["Id"],
                    name=value["Name"],
                    product_type=attrs.get("productType", product_type),
                    footprint=value.get("GeoFootprint", {}),
                    start_time=self._parse_iso(value["ContentDate"]["Start"]),
                    end_time=self._parse_iso(value["ContentDate"]["End"]),
                    s3_path=value.get("S3Path"),
                    quicklook_url=value.get("quicklook_url"),
                )
            )
        return products

    @staticmethod
    def _parse_iso(ts: str) -> datetime:
        # CDSE timestamps usually end in Z.
        ts = ts.replace("Z", "+00:00")
        return datetime.fromisoformat(ts)

    def download(
        self,
        product: S1Product,
        output_dir: Path | str,
        use_zip: bool = True,
        chunk_size: int = 8192,
        extract: bool = True,
    ) -> Path:
        """Download a product to output_dir. Returns the path to the saved file.

        Note:
            CDSE's `$value` endpoint streams a zip archive for both recent and
            archive products. The `$zip` endpoint is only valid for ~1 month after
            publication. We therefore always use `$value` and save/extract as zip.
            The `use_zip` parameter is kept for API compatibility but ignored.
        """
        del use_zip  # Always use `$value`; `$zip` is unreliable for archive products.

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Product names already end in `.SAFE`; avoid double extension.
        safe_name = product.name.removesuffix(".SAFE")
        zip_path = output_dir / f"{safe_name}.zip"

        # `$value` is the reliable endpoint for all products.
        url = product.download_url
        session = self._session
        with session.get(url, stream=True, timeout=600) as resp:
            resp.raise_for_status()
            with open(zip_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)

        if extract:
            import zipfile

            extract_dir = output_dir
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(extract_dir)
            return extract_dir / f"{safe_name}.SAFE"
        return zip_path

    def download_by_id(
        self,
        product_id: str,
        output_dir: Path | str,
        extract: bool = True,
    ) -> Path:
        """Download a product given only its CDSE UUID."""
        # Minimal product record for ID-only download.
        product = S1Product(
            product_id=product_id,
            name=product_id,
            product_type="",
            footprint={},
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc),
        )
        return self.download(product, output_dir, extract=extract)


def _bbox_to_wkt(bbox: Iterable[float]) -> str:
    """Helper to convert (min_lon, min_lat, max_lon, max_lat) to WKT."""
    min_lon, min_lat, max_lon, max_lat = bbox
    return (
        f"POLYGON(({min_lon} {min_lat}, {max_lon} {min_lat}, "
        f"{max_lon} {max_lat}, {min_lon} {max_lat}, {min_lon} {min_lat}))"
    )
