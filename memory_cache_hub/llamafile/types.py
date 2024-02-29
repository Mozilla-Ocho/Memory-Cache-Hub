from dataclasses import dataclass
from typing import Any, List
from pydantic import BaseModel
from memory_cache_hub.llamafile.download_handle import DownloadHandle

@dataclass
class LlamafileInfo:
    model: str
    size: str
    license: str
    license_url: str
    filename: str
    url: str

@dataclass
class LlamafileManager:
    llamafiles: List[LlamafileInfo]
    download_handles: List[DownloadHandle]
    llamafile_store_path: str
