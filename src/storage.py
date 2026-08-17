"""GCS access for the lego-service.

Reads module template .ldr files from the private assets bucket by their stable object key.
Credentials come from GOOGLE_APPLICATION_CREDENTIALS (a mounted service-account key), which the
google-cloud-storage client picks up automatically.
"""

import os
from functools import lru_cache

from google.cloud import storage

_ASSETS_BUCKET = os.environ.get("GCS_ASSETS_BUCKET", "")

_client: storage.Client | None = None


def _get_client() -> storage.Client:
    global _client
    if _client is None:
        _client = storage.Client()
    return _client


@lru_cache(maxsize=256)
def read_ldr(key: str) -> str:
    """Fetch an .ldr object's text from the assets bucket.

    Cached in-process: templates are effectively immutable per deploy, so repeated reads across
    generations avoid re-fetching. Restart the service to pick up edited templates.
    """
    if not _ASSETS_BUCKET:
        raise RuntimeError("GCS_ASSETS_BUCKET is not configured")
    blob = _get_client().bucket(_ASSETS_BUCKET).blob(key)
    return blob.download_as_text()
