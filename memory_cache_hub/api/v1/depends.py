from dataclasses import dataclass
from typing import List, Any
from memory_cache_hub.api.v1.types import ApiConfig
from memory_cache_hub.core.types import Chroma
from memory_cache_hub.llamafile.llamafile_infos import get_default_llamafile_infos
from memory_cache_hub.llamafile.types import LlamafileManager


# TODO: John: This way of storing state feels wrong,
#       but I don't know a better way. I don't care that it's
#       global or mutable -- in fact that's the point. But
#       maybe there's a common python pattern for making
#       singletons / global values

api_config = None
chroma = None
llamafile_manager = None
db = None

get_api_config = lambda: api_config
get_chroma = lambda: chroma
get_llamafile_manager = lambda: llamafile_manager
get_db = lambda: db

def set_api_config(config: ApiConfig):
    global api_config
    api_config = config

def set_chroma(c: Chroma):
    global chroma
    chroma = c

def set_llamafile_manager(manager: LlamafileManager):
    global llamafile_manager
    llamafile_manager = manager

def set_db(_db):
    global db
    db = _db

def get_root_directory():
    return api_config.file_store_path

def get_completions_url():
    return api_config.completions_url

def get_completions_model():
    return api_config.completions_model

def get_chroma_client():
    return chroma.client

def get_embedding_function():
    return chroma.embedding_function
