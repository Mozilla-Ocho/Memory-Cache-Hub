from dataclasses import dataclass
from memory_cache_hub.llamafile.types import LlamafileInfo
from typing import List
import json
import os

def llamafile_infos_from_json(json_file: str) -> List[LlamafileInfo]:
    llamafile_infos_path = os.path.join(os.path.dirname(__file__), json_file)
    with open(llamafile_infos_path, "r") as f:
        llamafile_infos_dicts = json.load(f)

    llamafile_infos = [LlamafileInfo(**info_dict) for info_dict in llamafile_infos_dicts]
    return llamafile_infos

def get_default_llamafile_infos() -> List[LlamafileInfo]:
    return llamafile_infos_from_json("llamafile_infos.json")

if __name__ == '__main__':
    llamafile_infos = llamafile_infos_from_json("llamafile_infos.json")
    for info in llamafile_infos:
        print(info)
