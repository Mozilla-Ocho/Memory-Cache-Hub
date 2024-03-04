from fastapi import APIRouter, Depends
from memory_cache_hub.api.v1.depends import get_chroma_client, get_root_directory
from memory_cache_hub.api.v1.types import ListProjectsResponse, GetOrCreateProjectRequest, DeleteProjectRequest
from memory_cache_hub.core.files import delete_project_directory, create_empty_project_directory

router = APIRouter()



@router.get("/list_projects", response_model=ListProjectsResponse, tags=["projects"])
async def list_projects(chroma_client=Depends(get_chroma_client)):
    collections = chroma_client.list_collections()
    collection_names = [collection.name for collection in collections]
    # Use the collection name as both the project name and project id
    projects = [{"project_name": collection_name, "project_id": collection_name} for collection_name in collection_names]
    return {"projects": projects}


@router.post("/get_or_create_project", response_model=ListProjectsResponse, tags=["projects"])
async def get_or_create_project(request: GetOrCreateProjectRequest, chroma_client=Depends(get_chroma_client), root_directory=Depends(get_root_directory)):
    project_name = request.project_name
    collection = chroma_client.get_or_create_collection(project_name)
    create_empty_project_directory(root_directory, project_name)
    collection_names = [collection.name]
    # Use the collection name as both the project name and project id
    projects = [{"project_name": collection_name, "project_id": collection_name} for collection_name in collection_names]

@router.delete("/delete_project", tags=["projects"])
async def delete_project(request: DeleteProjectRequest, chroma_client=Depends(get_chroma_client), root_directory=Depends(get_root_directory)):
    project_name = request.project_name
    try:
        delete_project_directory(root_directory, project_name)
        chroma_client.delete_collection(project_name)
        return {"status": "ok"}
    except ValueError:
        return {"status": "error", "reason": f"Project {project_name} does not exist"}
