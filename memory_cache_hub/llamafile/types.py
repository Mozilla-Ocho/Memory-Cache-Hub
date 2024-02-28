from dataclasses import dataclass
from typing import Any

@dataclass
class DownloadHandle:
    llamafile_name: str
    download_url: str
    content_length: int
    written: int
    coroutine: Any

@dataclass
class LlamafileInfo:
    model: str
    size: str
    license: str
    license_url: str
    filename: str
    url: str
