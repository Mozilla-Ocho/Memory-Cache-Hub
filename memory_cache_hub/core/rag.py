from sentence_transformers import SentenceTransformer
from dataclasses import dataclass, asdict
from chromadb import Documents, EmbeddingFunction, EphemeralClient
from typing import List, cast
from argparse import ArgumentParser
from hashlib import md5
from typing import List
from memory_cache_hub.core.chromadb import SentenceTransformerEmbeddingFunction
from memory_cache_hub.core.types import FragmentMetadata, Fragment
import os
import sys

def split_text(text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
    """Split text into chunks of the specified size with the specified overlap."""
    chunks = []
    for i in range(0, len(text), chunk_size - chunk_overlap):
        chunks.append(text[i : i + chunk_size])
    return chunks

def md5_hash(text: str) -> str:
    """Return the MD5 hash of the input text."""
    return md5(text.encode("utf-8")).hexdigest()

def fragments_from_files(file_paths: List[str],
                         chunk_size: int,
                         chunk_overlap: int,
                         embedding_function: EmbeddingFunction[Documents]):
    """Generate document fragments for the given file_paths."""
    fragments = []
    for file_path in file_paths:
        try:
            file_content = open(file_path, encoding="utf-8").read()
        except UnicodeDecodeError:
            print(f"Skipping file {file_path} due to UnicodeDecodeError")
            continue

        chunks = split_text(file_content, chunk_size, chunk_overlap)
        for i, chunk in enumerate(chunks):
            fragment = Fragment(
                fragment_id=md5_hash(chunk),
                fragment_text=chunk,
                fragment_embedding=embedding_function(cast(Documents, [chunk]))[0],
                fragment_metadata=FragmentMetadata(
                    fragment_index=i,
                    fragment_count=len(chunks),
                    fragment_chunk_size=chunk_size,
                    fragment_chunk_overlap=chunk_overlap,
                    source_file_path=file_path
                )
            )
            fragments.append(fragment)
    return fragments
