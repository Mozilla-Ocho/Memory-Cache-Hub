from fastapi import APIRouter, Depends
from memory_cache_hub.api.v1.depends import get_llamafile_manager
from memory_cache_hub.api.v1.types import DownloadLlamafileByNameRequest, DownloadLlamafileByNameResponse, LlamafileDownloadStatusResponse
from memory_cache_hub.llamafile.llamafile_manager import get_llamafile_info_by_filename, download_llamafile
import os
import shutil

router = APIRouter()

@router.post("/download_llamafile_by_name", status_code=200, tags=["llamafile"])
async def download_llamafile_by_name(
        request: DownloadLlamafileByNameRequest,
        llamafile_manager = Depends(get_llamafile_manager)):
    llamafile_info = get_llamafile_info_by_filename(llamafile_manager, request.llamafile_filename)
    if llamafile_info is None:
        return {"status": "error", "message": "Llamafile not found"}
    download_handle = download_llamafile(llamafile_manager, llamafile_info)
    return DownloadLlamafileByNameResponse(status="success", message="Llamafile download started")

@router.post("/llamafile_download_status", status_code=200, tags=["llamafile"])
async def llamafile_download_status(
        request: DownloadLlamafileByNameRequest,
        llamafile_manager = Depends(get_llamafile_manager)):
    llamafile_info = get_llamafile_info_by_filename(llamafile_manager, request.llamafile_filename)
    if llamafile_info is None:
        return LlamafileDownloadStatusResponse(status="error", message="Llamafile not found")
    for download_handle in llamafile_manager.download_handles:
        if download_handle.filename == llamafile_info.filename:
            return LlamafileDownloadStatusResponse(status="downloading", message="Llamafile is downloading", progress=download_handle.progress(), content_length=download_handle.content_length, written=download_handle.written)
    return LlamafileDownloadStatusResponse(status="error", message="Llamafile not found")
