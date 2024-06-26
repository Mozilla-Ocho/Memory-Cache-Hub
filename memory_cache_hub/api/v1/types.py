from pydantic import BaseModel
from typing import List, Optional
from dataclasses import dataclass
from memory_cache_hub.core.types import Chroma
from memory_cache_hub.db.types import Project

class OkResponse(BaseModel):
    status: str = "ok"

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str

@dataclass
class ApiConfig:
    host: str
    port: int
    chroma_db_path: str
    file_store_path: str
    llamafile_store_path: str
    completions_url: str
    completions_model: str
    embedding_device: str
    embedding_model: str
    normalize_embeddings: bool

class ListProjectsResponse(BaseModel):
    projects: List[Project]

class SummarizeFileRequest(BaseModel):
    project_id: int
    file_path: str

# For SummarizeFileResponse, there are two types of responses:
#  - success has status, project_name, summary_file_path, and summary
#  - failure has status and message
class SummarizeFileResponse(BaseModel):
    status: str
    project_name: Optional[str] = None
    summary_file_path: Optional[str] = None
    summary: Optional[str] = None
    message: Optional[str] = None

class IngestProjectFilesRequest(BaseModel):
    project_name: str

class IngestProjectFilesResponse(BaseModel):
    num_files: int
    num_fragments: int

class RagAskRequest(BaseModel):
    project_id: int
    prompt: str

class RagAskResponse(BaseModel):
    status: str
    message: Optional[str] = None
    response: Optional[str] = None

class DownloadLlamafileByNameRequest(BaseModel):
    llamafile_filename: str

class DownloadLlamafileByNameResponse(BaseModel):
    status: str
    message: Optional[str] = None

class LlamafileDownloadStatusResponse(BaseModel):
    status: str
    message: Optional[str] = None
    progress: Optional[int] = None
    content_length: Optional[int] = None
    written: Optional[int] = None

class StartLlamafileResponse(BaseModel):
    status: str
    message: Optional[str] = None

class StopLlamafileResponse(BaseModel):
    status: str
    message: Optional[str] = None
