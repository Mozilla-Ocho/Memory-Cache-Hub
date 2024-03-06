from fastapi import APIRouter, Depends
from memory_cache_hub.api.v1.depends import get_root_directory, get_completions_url, get_completions_model, get_db
from memory_cache_hub.api.v1.types import SummarizeFileRequest, SummarizeFileResponse
from memory_cache_hub.core.types import Message
from memory_cache_hub.core.summaries import summarize_file
from memory_cache_hub.core.files import get_file_summary_path, get_file_summary

router = APIRouter()

@router.post("/summarize_file", status_code=200, tags=["summaries"])
async def api_summarize_file(request: SummarizeFileRequest,
                             completions_url = Depends(get_completions_url),
                             completions_model = Depends(get_completions_model),
                             root_directory = Depends(get_root_directory),
                             db = Depends(get_db)):

    project = db_get_project(db, request.project_id)

    if summarize_file(completions_url, completions_model, root_directory, project.name, request.file_path):
        return SummarizeFileResponse(
            status="ok",
            project_name=project.name,
            summary_file_path=get_file_summary_path(root_directory, project.name, request.file_path),
            summary=get_file_summary(root_directory, project.name, request.file_path))
    else:
        return SummarizeFileResponse(
            status="error",
            message="Failed to summarize file. Check if the file exists and the LLM server is running. Check the server logs for more information."
        )
