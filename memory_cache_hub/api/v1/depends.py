from dataclasses import dataclass
from typing import List, Any
from memory_cache_hub.api.v1.types import ApiConfig
from memory_cache_hub.core.types import Chroma

api_config = ApiConfig(
    host="",
    port=80,
    chroma_db_path="",
    file_store_path="",
    llamafile_store_path="",
    completions_url="",
    completions_model="",
    embedding_device="",
    embedding_model="",
    normalize_embeddings=False,
)

def set_api_config(config: ApiConfig):
    global api_config
    api_config = config

def get_api_config():
    return api_config

def get_root_directory():
    return api_config.file_store_path

def get_completions_url():
    return api_config.completions_url

def get_completions_model():
    return api_config.completions_model

chroma = Chroma(
    client=None,
    embedding_function=None
)

def set_chroma(pc: Chroma):
    global chroma
    chroma = pc

def get_chroma_client():
    return chroma.client

def get_embedding_function():
    return chroma.embedding_function
