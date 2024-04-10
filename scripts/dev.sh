PROJECT_ROOT=$(realpath $0 | xargs dirname | xargs dirname)
cd $PROJECT_ROOT
source venv/bin/activate
pkill -f "python -m memory_cache_hub.server.main" -9
python -m memory_cache_hub.server.main
