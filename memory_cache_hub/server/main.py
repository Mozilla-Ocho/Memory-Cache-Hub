from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from memory_cache_hub.core.chromadb import chroma_client, chroma_embedding_function
from memory_cache_hub.api.v1.depends import set_api_config, set_chroma, set_llamafile_manager
from memory_cache_hub.api.v1.projects import router as projects_router
from memory_cache_hub.api.v1.files import router as files_router
from memory_cache_hub.api.v1.summaries import router as summaries_router
from memory_cache_hub.api.v1.ingest import router as ingest_router
from memory_cache_hub.api.v1.rag import router as rag_router
from memory_cache_hub.api.v1.llamafile_manager import router as llamafile_manager_router
from memory_cache_hub.api.v1.types import ApiConfig
from memory_cache_hub.core.types import Chroma
from memory_cache_hub.llamafile.types import LlamafileManager
from memory_cache_hub.core.llm import ollama_completions, Message
from memory_cache_hub.llamafile.llamafile_infos import get_default_llamafile_infos
import os
import sys

def create_app(args):
    set_api_config(ApiConfig(
        host=args.host,
        port=args.port,
        chroma_db_path=args.chroma_db_path,
        file_store_path=args.file_store_path,
        llamafile_store_path=args.llamafile_store_path,
        completions_url=args.completions_url,
        completions_model=args.completions_model,
        embedding_device=args.embedding_device,
        embedding_model=args.embedding_model,
        normalize_embeddings=args.normalize_embeddings

    ))
    set_chroma(Chroma(
        client=chroma_client(args.chroma_db_path),
        embedding_function=chroma_embedding_function(args.embedding_model, args.embedding_device, args.normalize_embeddings)
    ))
    set_llamafile_manager(LlamafileManager(
        llamafiles=get_default_llamafile_infos(),
        download_handles=[],
        run_handles=[],
        # Get the FULL path for llamafile_store_path
        llamafile_store_path=os.path.abspath(args.llamafile_store_path)
    ))

    app = FastAPI(
        title="Memory Cache Hub",
        description="A backend server for Memory Cache.",
        version="0.1.0",
       )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
       )

    app.include_router(projects_router, prefix="/api/v1")
    app.include_router(files_router, prefix="/api/v1")
    app.include_router(summaries_router, prefix="/api/v1")
    app.include_router(ingest_router, prefix="/api/v1")
    app.include_router(rag_router, prefix="/api/v1")
    app.include_router(llamafile_manager_router, prefix="/api/v1")

    if not os.path.exists(args.file_store_path):
        print(f"File store path {args.file_store_path} does not exist. Creating it.")
        os.makedirs(args.file_store_path)

    app.mount("/files", app=StaticFiles(directory=args.file_store_path), name="files")

    if args.client_path:
        app.mount("/", StaticFiles(directory=args.client_path, html=True ), name="static")
    elif getattr(sys, 'frozen', False) and os.path.exists(os.path.join(sys._MEIPASS, "client")):
        app.mount("/", StaticFiles(directory=os.path.join(sys._MEIPASS, "client"), html=True), name="static")

    return app


def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser(description="Memory Cache Hub")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to run the server on. (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=4444, help="Port to run the server on. (default: 4444)")
    parser.add_argument("--chroma-db-path", type=str, default="chroma.db", help="Path to the chroma database. (default: chroma.db)")
    parser.add_argument("--file-store-path", type=str, default="file_store", help="Path to the file store directory. (default: file_store)")
    parser.add_argument("--llamafile-store-path", type=str, default="llamafile_store", help="Path where llamafiles should be stored. (default: llamafile_store)")
    parser.add_argument("--completions-url", type=str, default="http://localhost:8888/v1/chat/completions", help="Path to an OpenAI-compatible LLM completions endpoint. (default: localhost:8888/v1/chat/completions)")
    parser.add_argument("--completions-model", type=str, default="mixtral:8x7b-instruct-v0.1-fp16", help="Model to use for completions. (default: mixtral:8x7b-instruct-v0.1-fp16). This argument is ignored when running local llamafiles.")
    parser.add_argument('--embedding-device', help='Device to use for embedding (cpu or cuda)', default='cpu', choices=['cpu', 'cuda'])
    parser.add_argument('--embedding-model', help='Model to use for embedding (default "all-MiniLM-L6-v2")', default='all-MiniLM-L6-v2')
    parser.add_argument('--normalize-embeddings', help='Normalize embeddings', action='store_true')
    parser.add_argument("--client-path", type=str, help="Path to the build directory of the client.")
    return parser.parse_args()

def main():
    import uvicorn
#    from multiprocessing import freeze_support
#    freeze_support() # See https://pyinstaller.org/en/stable/common-issues-and-pitfalls.html#multi-processing
    args = parse_arguments()
    app = create_app(args)
    uvicorn.run(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()
