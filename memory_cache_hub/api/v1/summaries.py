from fastapi import APIRouter, Depends
from memory_cache_hub.api.v1.depends import get_root_directory, get_completions_url, get_completions_model
from memory_cache_hub.api.v1.types import SummarizeFileRequest, SummarizeFileResponse
from memory_cache_hub.core.types import Message
from memory_cache_hub.core.summaries import summarize_file as _summarize_file
from memory_cache_hub.core.files import get_file_summary_path, get_file_summary

router = APIRouter()

@router.post("/summarize_file", status_code=200, tags=["summaries"])
async def summarize_file(request: SummarizeFileRequest,
                         completions_url = Depends(get_completions_url),
                         completions_model = Depends(get_completions_model),
                         root_directory = Depends(get_root_directory)):
    _summarize_file(
        completions_url,
        completions_model,
        root_directory,
        request.project_name,
        request.file_path);
    print("Summarized file")
    return SummarizeFileResponse(
        project_name=request.project_name,
        summary_file_path=get_file_summary_path(root_directory, request.project_name, request.file_path),
        summary=get_file_summary(root_directory, request.project_name, request.file_path)
    )
