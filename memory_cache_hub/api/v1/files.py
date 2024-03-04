from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Form
from typing import List
from memory_cache_hub.api.v1.depends import get_root_directory
from memory_cache_hub.core.files import write_file_upload, create_empty_project_directory, get_project_uploads_directory, get_project_summaries_directory, list_project_file_uploads, list_project_file_summaries
from memory_cache_hub.core.files import delete_file as _delete_file
from memory_cache_hub.api.v1.types import FileUpload, DeleteFileRequest
import os
import shutil

router = APIRouter()

@router.post("/upload_file", status_code=200, tags=["files"])
async def upload_file(
        project_name: str = Form(...),
        file_path: str = Form(...),
        file: UploadFile = File(...),
        root_directory = Depends(get_root_directory)):
    write_file_upload(root_directory, project_name, file_path, file)
    return {"status": "ok"}

@router.delete("/delete_file", status_code=200, tags=["files"])
async def delete_file(request: DeleteFileRequest, root_directory = Depends(get_root_directory)):
    project_name = request.project_name
    file_path = request.file_path
    if _delete_file(root_directory, project_name, file_path):
        return {"status": "ok"}
    else:
        raise HTTPException(status_code=404, detail="File not found")

@router.get("/list_files/{project_name}", response_model=List[str], tags=["files"])
async def list_files(project_name: str, root_directory = Depends(get_root_directory)):
    files_list = []
    files_list.extend(list_project_file_uploads(root_directory, project_name))
    files_list.extend(list_project_file_summaries(root_directory, project_name))
    return files_list
