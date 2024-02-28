from dataclasses import dataclass
from typing import Union, Sequence, Any

@dataclass
class Chroma:
    client: Any
    embedding_function: Any

# chromadb does not export Vector, so we define it here
Vector = Union[Sequence[float], Sequence[int]]
# chromadb does not export Document, so we define it here
Document = str

@dataclass
class Message:
    """A message to send to the LLM server."""
    role: str
    content: str

@dataclass
class FragmentMetadata:
    """Metadata for a document fragment."""
    fragment_index: int
    fragment_count: int
    fragment_chunk_size: int
    fragment_chunk_overlap: int
    source_file_path: str

@dataclass
class Fragment:
    """A fragment of a document."""
    fragment_id: str
    fragment_text: Document
    fragment_embedding: Vector
    fragment_metadata: FragmentMetadata
