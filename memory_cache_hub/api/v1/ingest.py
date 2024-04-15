from fastapi import APIRouter, Depends
from memory_cache_hub.api.v1.depends import get_root_directory, get_chroma_client, get_embedding_function, get_db
from memory_cache_hub.api.v1.types import IngestProjectFilesRequest, IngestProjectFilesResponse
from memory_cache_hub.core.files import get_project_uploads_directory, list_project_file_uploads
from memory_cache_hub.core.chromadb import chroma_collection_for_project
from memory_cache_hub.core.rag import fragments_from_files
from memory_cache_hub.db.projects import db_get_project
from dataclasses import asdict
import os

router = APIRouter()

@router.post("/ingest_project_files", status_code=200, tags=["ingest"])
def ingest_project_files(
        project_id: int,
        root_directory: str = Depends(get_root_directory),
        chroma_client = Depends(get_chroma_client),
        chroma_embedding_function = Depends(get_embedding_function),
        db = Depends(get_db)
):
    project = db_get_project(db, project_id)
    project_files = list_project_file_uploads(root_directory, project.name)
    chroma_collection = chroma_collection_for_project(chroma_client, chroma_embedding_function, project.name)
    # Delete the collection because we are going to re-ingest all the files
    # chroma_client.delete_collection(chroma_collection.name)
    chroma_collection = chroma_collection_for_project(chroma_client, chroma_embedding_function, project.name)
    # Prepend root_direct to each project_files path
    file_paths = [os.path.join(root_directory, project_file) for project_file in project_files]
    # Filter the file_paths such that only the files that have not been ingested are included
    filtered_file_paths = []
    for file_path in file_paths:
        query_results = chroma_collection.query(query_texts=[""], where={"source_file_path": file_path})
        if len(query_results["ids"][0]) == 0:
            print(f"ADDING FILE {file_path}")
            filtered_file_paths.append(file_path)

    
    file_paths = filtered_file_paths

    fragments = fragments_from_files(file_paths, 1000, 200, chroma_embedding_function)
    if len(fragments) == 0:
        return {"status": "ok", "message": "No fragments found in the project files"}

    # If we had multiple fragments with the same ID, remove the duplicates
    fragments = list({fragment.fragment_id: fragment for fragment in fragments}.values())

    try:
        chroma_collection.add(
            ids=[fragment.fragment_id for fragment in fragments],
            embeddings=[fragment.fragment_embedding for fragment in fragments],
            metadatas=[asdict(fragment.fragment_metadata) for fragment in fragments],
            documents=[fragment.fragment_text for fragment in fragments],
        )
        return IngestProjectFilesResponse(
            num_files=len(file_paths),
            num_fragments=len(fragments),
        )
    except Exception as e:
        return {"status": "error", "message": str(e)}
