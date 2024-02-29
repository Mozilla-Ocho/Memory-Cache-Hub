from dataclasses import dataclass
from memory_cache_hub.llamafile.types import LlamafileInfo
from typing import List
import json
import os
import sys

def llamafile_infos_from_json(llamafile_infos_dicts) -> List[LlamafileInfo]:
    return [LlamafileInfo(**info_dict) for info_dict in llamafile_infos_dicts]

def get_default_llamafile_infos() -> List[LlamafileInfo]:
    if getattr(sys, 'frozen', False):
        # The application is frozen
        base_path = sys._MEIPASS
    else:
        # The application is not frozen
        base_path = os.path.dirname(__file__)

    llamafile_infos_path = os.path.join(base_path, "llamafile_infos.json")
    llamafile_infos_dicts = None
    with open(llamafile_infos_path, "r") as f:
        llamafile_infos_dicts = json.load(f)

    return llamafile_infos_from_json(llamafile_infos_dicts)
