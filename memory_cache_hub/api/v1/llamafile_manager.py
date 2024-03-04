from fastapi import APIRouter, Depends
from memory_cache_hub.api.v1.depends import get_llamafile_manager
from memory_cache_hub.api.v1.types import DownloadLlamafileByNameRequest, DownloadLlamafileByNameResponse, LlamafileDownloadStatusResponse, StartLlamafileResponse, StopLlamafileResponse
from memory_cache_hub.llamafile.llamafile_manager import get_llamafile_info_by_filename, download_llamafile, start_llamafile, stop_llamafile
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

@router.post("/check_llamafile_download_progress", status_code=200, tags=["llamafile"])
async def check_llamafile_download_progress(
        request: DownloadLlamafileByNameRequest,
        llamafile_manager = Depends(get_llamafile_manager)):
    llamafile_info = get_llamafile_info_by_filename(llamafile_manager, request.llamafile_filename)
    if llamafile_info is None:
        return LlamafileDownloadStatusResponse(status="error", message="Llamafile not found")
    for download_handle in llamafile_manager.download_handles:
        if download_handle.filename == llamafile_info.filename:
            return LlamafileDownloadStatusResponse(status="downloading", message="Llamafile is downloading", progress=download_handle.progress(), content_length=download_handle.content_length, written=download_handle.written)
    return LlamafileDownloadStatusResponse(status="error", message="Llamafile not found")

@router.post("/start_llamafile", status_code=200, tags=["llamafile"])
async def api_start_llamafile(
        request: DownloadLlamafileByNameRequest,
        llamafile_manager = Depends(get_llamafile_manager)):
    llamafile_info = get_llamafile_info_by_filename(llamafile_manager, request.llamafile_filename)
    if llamafile_info is None:
        return StartLlamafileResponse(status="error", message="Llamafile not found")
    if start_llamafile(llamafile_manager, llamafile_info):
        return StartLlamafileResponse(status="success", message="Llamafile started")
    else:
        return StartLlamafileResponse(status="error", message="Llamafile not found")

@router.post("/stop_llamafile", status_code=200, tags=["llamafile"])
async def api_stop_llamafile(
        request: DownloadLlamafileByNameRequest,
        llamafile_manager = Depends(get_llamafile_manager)):
    llamafile_info = get_llamafile_info_by_filename(llamafile_manager, request.llamafile_filename)
    if llamafile_info is None:
        return StopLlamafileResponse(status="error", message="Llamafile not found")
    if await stop_llamafile(llamafile_manager, llamafile_info):
        return StopLlamafileResponse(status="success", message="Llamafile stopped")
    else:
        return StopLlamafileResponse(status="error", message="Llamafile not found")
