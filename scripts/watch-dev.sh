PROJECT_ROOT=$(realpath $0 | xargs dirname | xargs dirname)
cd $PROJECT_ROOT
source venv/bin/activate
pip install -r requirements.txt
trap "exit" INT
while :
do
    fd . $PROJECT_ROOT/memory_cache_hub | entr -d -r $PROJECT_ROOT/scripts/dev.sh
done
