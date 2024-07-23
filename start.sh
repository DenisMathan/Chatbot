
export ROOT_PATH=$(pwd)
cd src
# export PYTHONPATH=$(pwd)
gunicorn --timeout 600 --bind 0.0.0.0:3333 wsgi:app