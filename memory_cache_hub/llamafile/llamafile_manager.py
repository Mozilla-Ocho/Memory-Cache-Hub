from memory_cache_hub.llamafile.types import LlamafileManager, LlamafileInfo, DownloadHandle
from memory_cache_hub.llamafile.llamafile_infos import get_default_llamafile_infos
from memory_cache_hub.llamafile.run_handle import RunHandle
import os

def get_llamafile_info_by_filename(llamafile_manager: LlamafileManager, filename: str):
    for llamafile_info in llamafile_manager.llamafiles:
        if llamafile_info.filename == filename:
            return llamafile_info
    return None

def download_llamafile(llamafile_manager: LlamafileManager, llamafile_info: LlamafileInfo):
    def on_complete(download_handle):
        llamafile_manager.download_handles.remove(download_handle)

    download_handle = DownloadHandle(
        url=llamafile_info.url,
        filename=llamafile_info.filename,
        file_path=os.path.join(llamafile_manager.llamafile_store_path, llamafile_info.filename),
        on_complete=on_complete
    )
    llamafile_manager.download_handles.append(download_handle)
    return download_handle

def start_llamafile(llamafile_manager: LlamafileManager, llamafile_info: LlamafileInfo):
    run_handle = RunHandle(
        llamafile_info=llamafile_info,
        llamafile_store_path=llamafile_manager.llamafile_store_path,
    )
    llamafile_manager.run_handles.append(run_handle)
    # TODO: A run_handle does not automatically start, but a download_handle does.
    #       Maybe both should have the same behavior.
    run_handle.start()
    return run_handle

async def stop_llamafile(llamafile_manager: LlamafileManager, llamafile_info: LlamafileInfo):
    for run_handle in llamafile_manager.run_handles:
        if run_handle.llamafile_info.filename == llamafile_info.filename:
            print(f"Stopping llamafile {llamafile_info.filename}...")
            await run_handle.stop()
            llamafile_manager.run_handles.remove(run_handle)
            return True
    print(f"No running llamafile found for {llamafile_info.filename}.")
    return False

def has_llamafile(llamafile_manager: LlamafileManager, llamafile_info: LlamafileInfo):
    # Check if the file is already downloaded
    file_path = os.path.join(llamafile_manager.llamafile_store_path, llamafile_info.filename)
    return os.path.exists(file_path)

def delete_llamafile(llamafile_manager: LlamafileManager, llamafile_info: LlamafileInfo):
    file_path = os.path.join(llamafile_manager.llamafile_store_path, llamafile_info.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False
