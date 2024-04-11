from memory_cache_hub.api.v1.depends import get_root_directory, get_chroma_client, get_embedding_function, get_completions_url, get_completions_model, get_db
from memory_cache_hub.api.v1.types import RagAskRequest, RagAskResponse
from memory_cache_hub.core.types import Message
from memory_cache_hub.core.files import get_project_uploads_directory, list_project_file_uploads
from memory_cache_hub.core.chromadb import chroma_collection_for_project
from memory_cache_hub.core.rag import fragments_from_files
from memory_cache_hub.core.llm import ollama_completions, openai_compatible_completions
from memory_cache_hub.db.projects import db_get_project

from fastapi import APIRouter, Depends
from dataclasses import asdict
import os

router = APIRouter()

@router.post("/rag_ask", status_code=200, tags=["rag"])
def rag_ask(
        body: RagAskRequest,
        root_directory: str = Depends(get_root_directory),
        complete_url: str = Depends(get_completions_url),
        complete_model: str = Depends(get_completions_model),
        chroma_client = Depends(get_chroma_client),
        chroma_embedding_function = Depends(get_embedding_function),
        db=Depends(get_db)
):
    prompt = body.prompt
    project = db_get_project(db, body.project_id)
    chroma_collection = chroma_collection_for_project(chroma_client, chroma_embedding_function, project.name)
    query_results = chroma_collection.query(query_texts=[prompt])

    big_content = ""
    big_content += f"Consider the following context:\n"
    for i, result in enumerate(query_results['metadatas'][0]):
        if i == 2:
            break
        file_path = result['source_file_path']
        big_content += f"----File: {file_path}\n"
        big_content += f"{query_results['documents'][0][i]}\n"

    big_content += f"Based on the context above, answer the following question:\n"
    big_content += f"{prompt}\n"

    messages = [
        Message(
            role="system",
            content="You are an AI assistant. The user will provide you fragments of documents to give you context to work with, and then ask you a question. First, read the document fragments. Then, answer the question at the end of the user's message. Minimize any other prose.",
        ),
        Message(
            role="user",
            content=big_content,
        ),
    ]

    #reply = ollama_completions(complete_url, complete_model, messages)
    print("\n--------\n")
    print(big_content)
    print("\n--------\n")
    reply = openai_compatible_completions(complete_url, complete_model, messages)
    print(reply)
    print("\n-------\n")

    return RagAskResponse(
        response=reply,
    )

@router.post("/vector_db_query", status_code=200, tags=["rag"])
def vector_db_query(
        body: RagAskRequest,
        root_directory: str = Depends(get_root_directory),
        chroma_client = Depends(get_chroma_client),
        chroma_embedding_function = Depends(get_embedding_function),
        db=Depends(get_db)
):
    prompt = body.prompt
    project = db_get_project(db, body.project_id)
    chroma_collection = chroma_collection_for_project(chroma_client, chroma_embedding_function, project.name)
    query_results = chroma_collection.query(query_texts=[prompt])
    response = []

    for i, result in enumerate(query_results['metadatas'][0]):
        file_path = result['source_file_path']
        file_content = f"{query_results['documents'][0][i]}"
        distance = query_results['distances'][0][i]

        response.append({
            'file_path': file_path,
            'file_content': file_content,
            'distance': distance,
        })

    return response
