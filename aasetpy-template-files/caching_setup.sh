#!/bin/bash

## credits: aadarshlalchandani/aasetpy

data_dirname=data
logs_dirname=logs
virtual_env_name=env
dotenv_filename=.env
cache_dirname=__pycache__
requirements_filename=requirements.txt

mkdir_if_not() {
    if [ "$2" = "dir" ]; then
        if [ ! -e "$1" ]; then
            mkdir -p "$1"
        fi
    elif [ "$2" = "file" ]; then
        if [ ! -f "$1" ]; then
            touch "$1"
        fi
    fi
}

remover() {
    if [ -d "$1" ]; then
        rm -rf "$1" >/dev/null 2>&1
    elif [ -f "$1" ]; then
        rm "$1" >/dev/null 2>&1
    fi
}

add_to_file() {
    local content="$1"
    local file="$2"
    local bypass="${3:-false}"

    if [ "$bypass" = true ] || ! grep -qF -- "$content" "$file"; then
        echo $content >>$file
    fi
}

reset_arg=reset
caching_arg=caching

if [[ "$@" =~ "$reset_arg" ]]; then
    remover "$dotenv_filename"
fi

## create fresh virtual environment
remover "$virtual_env_name"
python -m venv $virtual_env_name
. $virtual_env_name/bin/activate
remover "$(python -m pip cache dir)/selfcheck"

mkdir_if_not "$data_dirname" "dir"
mkdir_if_not "$logs_dirname" "dir"
mkdir_if_not "$dotenv_filename" "file"

for arg in "$@"; do
    if [[ "$arg" != "$reset_arg" ]]; then
        if [[ "$arg" == "$caching_arg" ]]; then
            add_to_file "" "$dotenv_filename" true
            add_to_file "## SERVER CACHE" "$dotenv_filename"
            add_to_file "CACHE_HOST=localhost" "$dotenv_filename"
            add_to_file "CACHE_PORT=6379" "$dotenv_filename"
            add_to_file "CACHE_DB=0" "$dotenv_filename"
            add_to_file "CACHE_MAX_CONNECTIONS=10" "$dotenv_filename"
            add_to_file "CACHE_MAXSIZE=500" "$dotenv_filename"
            add_to_file "DEFAULT_CACHE_EXPIRE_SECONDS=86400" "$dotenv_filename"
        fi
    fi
done

## update pip tools
update_libs="pip wheel setuptools"
python -m pip install -U -q $update_libs

## install uv for blazing fast python library installation
pip install uv -q

## install dependencies
uv pip install -r "$requirements_filename" -q

if [ ! -f "$dotenv_filename" ]; then
    echo "writing environment variables to .env"
    add_to_file "AUTH_TOKEN=token" "$dotenv_filename"
else
    :
fi

## Remove cache directories from codebase
find . -type d -name $cache_dirname -exec rm -rf {} \; >/dev/null 2>&1

echo
echo "Setup Complete."
