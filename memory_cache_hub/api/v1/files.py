from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Form
from typing import List
from memory_cache_hub.api.v1.depends import get_root_directory, get_db
from memory_cache_hub.core.files import write_file_upload, list_project_file_uploads, list_project_file_summaries
# from memory_cache_hub.core.files import delete_file as _delete_file
from memory_cache_hub.core.files import sync_project_files
# from memory_cache_hub.api.v1.types import DeleteFileRequest
from memory_cache_hub.api.v1.types import ErrorResponse, OkResponse
from memory_cache_hub.db.projects import db_get_project
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

# TODO: Remove?
# @router.delete("/delete_file", status_code=200, tags=["files"])
# async def delete_file(request: DeleteFileRequest, root_directory = Depends(get_root_directory)):
#     project_name = request.project_name
#     file_path = request.file_path
#     if _delete_file(root_directory, project_name, file_path):
#         return {"status": "ok"}
#     else:
#         raise HTTPException(status_code=404, detail="File not found")

@router.get("/list_project_files/{project_id}", response_model=List[str], tags=["files"])
async def list_project_files(project_id: int, root_directory = Depends(get_root_directory), db=Depends(get_db)):
    files_list = []
    project = db_get_project(db, project_id)
    project_name = project.name
    files_list.extend(list_project_file_uploads(root_directory, project_name))
    files_list.extend(list_project_file_summaries(root_directory, project_name))
    return files_list

@router.post("/sync_project_files", status_code=200, tags=["files"])
async def api_sync_project_files(project_id: int,
                                 root_directory = Depends(get_root_directory),
                                 db=Depends(get_db)
                                 ):
    result = sync_project_files(db, root_directory, project_id)
    if result["status"] == "ok":
        return OkResponse()
    else:
        return ErrorResponse(message=result["message"])
