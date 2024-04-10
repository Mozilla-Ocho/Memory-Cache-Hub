from fastapi import APIRouter, Depends
from memory_cache_hub.api.v1.depends import get_chroma_client, get_root_directory, get_db
from memory_cache_hub.api.v1.types import ListProjectsResponse, OkResponse, ErrorResponse
from memory_cache_hub.core.files import delete_project_directory, create_empty_project_directory
from memory_cache_hub.db.projects import db_create_project, db_list_projects, db_delete_project, db_create_project_directory, db_list_project_directories, db_delete_project_directory, db_get_project, db_update_project
from memory_cache_hub.core.files import remove_directory_from_project
from memory_cache_hub.db.types import Project

router = APIRouter()

@router.get("/list_projects", response_model=ListProjectsResponse, tags=["projects"])
async def list_projects(db=Depends(get_db)):
    projects = db_list_projects(db)
    return ListProjectsResponse(projects=projects)

@router.post("/create_project", response_model=ListProjectsResponse, tags=["projects"])
async def create_project(project_name: str,
                         chroma_client=Depends(get_chroma_client),
                         root_directory=Depends(get_root_directory),
                         db=Depends(get_db)):
    project = db_create_project(db, project_name or "New Project")
    collection = chroma_client.create_collection(f"project_id_{project.id}")
    create_empty_project_directory(root_directory, f"project_id_{project.id}")
    return ListProjectsResponse(projects=[project])

@router.post("/update_project", response_model=Project, tags=["projects"])
async def update_project(project_id: int, project_name: str, db=Depends(get_db)):
    project = db_update_project(db, project_id, project_name)
    return project

@router.delete("/delete_project", tags=["projects"])
async def delete_project(project_id: int,
                         chroma_client=Depends(get_chroma_client),
                         root_directory=Depends(get_root_directory),
                         db=Depends(get_db)):
    try:
        db_delete_project(db, project_id)
        collection = chroma_client.delete_collection(f"project_id_{project_id}")
        delete_project_directory(root_directory, f"project_id_{project_id}")
        return OkResponse()
    except ValueError:
        return ErrorResponse(message="Project not found")

@router.post("/create_project_directory", tags=["projects"])
async def create_project_directory(project_id: int, path: str, db=Depends(get_db)):
    if path == "":
        return ErrorResponse(message="Path cannot be empty")
    project_directory = db_create_project_directory(db, project_id, path)
    return project_directory

@router.get("/list_project_directories", tags=["projects"])
async def list_project_directories(project_id: int, db=Depends(get_db)):
    project_directories = db_list_project_directories(db, project_id)
    return project_directories

@router.delete("/delete_project_directory", tags=["projects"])
async def api_delete_project_directory(directory_id: int, db=Depends(get_db), root_directory=Depends(get_root_directory)):
    project_directory = db_delete_project_directory(db, directory_id)
    project = db_get_project(db, project_directory.project_id)
    remove_directory_from_project(root_directory, project.name, project_directory.path)
    return project_directory
