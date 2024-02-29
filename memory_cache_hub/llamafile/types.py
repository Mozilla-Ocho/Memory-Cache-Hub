from dataclasses import dataclass
from typing import Any, List
from pydantic import BaseModel
from memory_cache_hub.llamafile.download_handle import DownloadHandle
from memory_cache_hub.llamafile.run_handle import RunHandle

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
    run_handles: List[RunHandle]
    llamafile_store_path: str
