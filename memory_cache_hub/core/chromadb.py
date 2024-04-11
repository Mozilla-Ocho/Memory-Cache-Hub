from chromadb import PersistentClient, Documents, EmbeddingFunction, Embeddings
from typing import Dict, Any, cast

# This class is pulled from ChromaDB.
# The actual default embedding function from ChromaDB avoids the SentenceTransformer dependency, but we don't care about that here.
class SentenceTransformerEmbeddingFunction(EmbeddingFunction[Documents]):
    # Since we do dynamic imports we have to type this as Any
    models: Dict[str, Any] = {}

    # If you have a beefier machine, try "gtr-t5-large".
    # for a full list of options: https://huggingface.co/sentence-transformers, https://www.sbert.net/docs/pretrained_models.html
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        device: str = "cpu",
        normalize_embeddings: bool = False,
    ):
        if model_name not in self.models:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError:
                raise ValueError(
                    "The sentence_transformers python package is not installed. Please install it with `pip install sentence_transformers`"
                )
            self.models[model_name] = SentenceTransformer(model_name, device=device)
        self._model = self.models[model_name]
        self._normalize_embeddings = normalize_embeddings

    def __call__(self, input: Documents) -> Embeddings:
        return cast(
            Embeddings,
            self._model.encode(
                list(input),
                convert_to_numpy=True,
                normalize_embeddings=self._normalize_embeddings,
            ).tolist(),
        )

def chroma_client(persistence_path: str) -> PersistentClient:
    return PersistentClient(path=persistence_path)

def chroma_embedding_function(model_name: str, device: str, normalize_embeddings: bool):
    return SentenceTransformerEmbeddingFunction(
        model_name=model_name,
        device=device,
        normalize_embeddings=normalize_embeddings)

def chroma_collection_for_project(chroma_client: PersistentClient,
                                  embedding_function: Any,
                                  project_name: str):
    sanitized_project_name = project_name.replace(" ", "_").replace("/", "_")
    return chroma_client.get_or_create_collection(
        sanitized_project_name,
        metadata={"project_name": project_name},
        embedding_function=embedding_function)
