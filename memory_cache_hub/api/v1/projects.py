from fastapi import APIRouter, Depends
from memory_cache_hub.api.v1.depends import get_chroma_client, get_root_directory, get_db
from memory_cache_hub.api.v1.types import ListProjectsResponse, DeleteProjectRequest, CreateProjectRequest, OkResponse, ErrorResponse
from memory_cache_hub.core.files import delete_project_directory, create_empty_project_directory
from memory_cache_hub.db.projects import db_create_project, db_list_projects, db_delete_project

router = APIRouter()

@router.get("/list_projects", response_model=ListProjectsResponse, tags=["projects"])
async def list_projects(db=Depends(get_db)):
    projects = db_list_projects(db)
    return ListProjectsResponse(projects=projects)

@router.post("/create_project", response_model=ListProjectsResponse, tags=["projects"])
async def create_project(request: CreateProjectRequest,
                         chroma_client=Depends(get_chroma_client),
                         root_directory=Depends(get_root_directory),
                         db=Depends(get_db)):
    project = db_create_project(db, request.project_name or "New Project")
    collection = chroma_client.create_collection(f"project_id_{project.id}")
    create_empty_project_directory(root_directory, f"project_id_{project.id}")
    return ListProjectsResponse(projects=[project])

@router.delete("/delete_project", tags=["projects"])
async def delete_project(request: DeleteProjectRequest,
                         chroma_client=Depends(get_chroma_client),
                         root_directory=Depends(get_root_directory),
                         db=Depends(get_db)):
    try:
        project_id = request.project_id
        project = db_delete_project(db, project_id)
        collection = chroma_client.delete_collection(f"project_id_{project.id}")
        delete_project_directory(root_directory, f"project_id_{project.id}")
        return OkResponse()
    except ValueError:
        return ErrorResponse(message="Project not found")
