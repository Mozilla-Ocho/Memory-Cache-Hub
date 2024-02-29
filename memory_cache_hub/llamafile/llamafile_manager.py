from memory_cache_hub.llamafile.types import LlamafileManager, LlamafileInfo, DownloadHandle
from memory_cache_hub.llamafile.llamafile_infos import get_default_llamafile_infos
import os

def get_llamafile_info_by_filename(llamafile_manager: LlamafileManager, filename: str):
    for llamafile_info in llamafile_manager.llamafiles:
        if llamafile_info.filename == filename:
            return llamafile_info
    return None

def download_llamafile(llamafile_manager: LlamafileManager, llamafile_info: LlamafileInfo):
    download_handle = DownloadHandle(
        url=llamafile_info.url,
        filename=llamafile_info.filename,
        file_path=os.path.join(llamafile_manager.llamafile_store_path, llamafile_info.filename),
    )
    llamafile_manager.download_handles.append(download_handle)
    return download_handle
