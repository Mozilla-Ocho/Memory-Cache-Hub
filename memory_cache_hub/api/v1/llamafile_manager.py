from fastapi import APIRouter, Depends
from memory_cache_hub.api.v1.depends import get_llamafile_manager
from memory_cache_hub.api.v1.types import DownloadLlamafileByNameRequest, DownloadLlamafileByNameResponse, LlamafileDownloadStatusResponse, StartLlamafileResponse, StopLlamafileResponse
from memory_cache_hub.llamafile.llamafile_manager import get_llamafile_info_by_filename, download_llamafile, start_llamafile, stop_llamafile, has_llamafile, delete_llamafile
import os
import shutil

router = APIRouter()

@router.post("/download_llamafile_by_name", status_code=200, tags=["llamafile"])
async def download_llamafile_by_name(
        llamafile_filename: str,
        llamafile_manager = Depends(get_llamafile_manager)):
    llamafile_info = get_llamafile_info_by_filename(llamafile_manager, llamafile_filename)
    if llamafile_info is None:
        return {"status": "error", "message": "Llamafile not found"}
    download_handle = download_llamafile(llamafile_manager, llamafile_info)
    return DownloadLlamafileByNameResponse(status="success", message="Llamafile download started")

@router.post("/check_llamafile_status", status_code=200, tags=["llamafile"])
async def check_llamafile_status(
        llamafile_filename: str,
        llamafile_manager = Depends(get_llamafile_manager)):
    llamafile_info = get_llamafile_info_by_filename(llamafile_manager, llamafile_filename)
    if llamafile_info is None:
        return LlamafileDownloadStatusResponse(status="error", message="Llamafile not found")

    for run_handle in llamafile_manager.run_handles:
        if run_handle.llamafile_info.filename == llamafile_info.filename:
            return LlamafileDownloadStatusResponse(status="running", message="Llamafile is running")

    for download_handle in llamafile_manager.download_handles:
        if download_handle.filename == llamafile_info.filename:
            return LlamafileDownloadStatusResponse(status="downloading", message="Llamafile is downloading", progress=download_handle.progress(), content_length=download_handle.content_length, written=download_handle.written)

    if has_llamafile(llamafile_manager, llamafile_info):
        return LlamafileDownloadStatusResponse(status="idle", message="Llamafile is downloaded")
    return LlamafileDownloadStatusResponse(status="absent", message="Llamafile not downloaded")

@router.post("/start_llamafile", status_code=200, tags=["llamafile"])
async def api_start_llamafile(
        llamafile_filename: str,
        llamafile_manager = Depends(get_llamafile_manager)):
    llamafile_info = get_llamafile_info_by_filename(llamafile_manager, llamafile_filename)
    if llamafile_info is None:
        return StartLlamafileResponse(status="error", message="Llamafile not found")
    if start_llamafile(llamafile_manager, llamafile_info):
        return StartLlamafileResponse(status="success", message="Llamafile started")
    else:
        return StartLlamafileResponse(status="error", message="Llamafile not found")

@router.post("/stop_llamafile", status_code=200, tags=["llamafile"])
async def api_stop_llamafile(
        llamafile_filename: str,
        llamafile_manager = Depends(get_llamafile_manager)):
    llamafile_info = get_llamafile_info_by_filename(llamafile_manager, llamafile_filename)
    if llamafile_info is None:
        return StopLlamafileResponse(status="error", message="Llamafile not found")
    if await stop_llamafile(llamafile_manager, llamafile_info):
        return StopLlamafileResponse(status="success", message="Llamafile stopped")
    else:
        return StopLlamafileResponse(status="error", message="Llamafile not found")

@router.get("/list_llamafiles", status_code=200, tags=["llamafile"])
async def list_llamafiles(llamafile_manager = Depends(get_llamafile_manager)):
    return llamafile_manager.llamafiles

@router.delete("/delete_llamafile", status_code=200, tags=["llamafile"])
async def api_delete_llamafile(
        llamafile_filename: str,
        llamafile_manager = Depends(get_llamafile_manager)):
    llamafile_info = get_llamafile_info_by_filename(llamafile_manager, llamafile_filename)
    if llamafile_info is None:
        return {"status": "error", "message": "Llamafile not found"}
    if delete_llamafile(llamafile_manager, llamafile_info):
        return {"status": "success", "message": "Llamafile deleted"}
    else:
        return {"status": "error", "message": "Llamafile not found"}
