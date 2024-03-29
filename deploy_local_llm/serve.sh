#!/bin/bash
# Before start, make sure you are using python 3.9+ and wget is installed

# Function to compare versions
version_gt() { test "$(printf '%s\n' "$@" | sort -V | head -n 1)" != "$1"; }

# Check for Python 3.9+
required_python_version="3.9"
current_python_version=$(python3 --version 2>&1 | awk '{print $2}')
if version_gt "$required_python_version" "$current_python_version"; then
    echo "Error: Python 3.9 or later is required."
    exit 1
fi

# Create virtual environment
venv_dir=".rubra_serve_env"
if [ ! -d "$venv_dir" ]; then
    python3 -m venv "$venv_dir"
fi

# Activate virtual environment
source "$venv_dir/bin/activate"

# Install dependencies
python3 -m pip install cmake scikit-build setuptools fastapi uvicorn sse-starlette pydantic-settings starlette-context

# Install llama-cpp-python from source
if [ -d "llama-cpp-python" ]; then
    cd llama-cpp-python
    git pull
    cd ..
else
    git clone --recurse-submodules https://github.com/tybalex/llama-cpp-python.git
fi
# python3 -m pip install --no-cache -e ./llama-cpp-python
python3 -m pip install -e ./llama-cpp-python

# (Optional) export grammar file path as environment variable
export GRAMMAR_FILE=grammar/json_grammar.gbnf

# Create model directory if it doesn't exist
model_dir="./model"
if [ ! -d "$model_dir" ]; then
    mkdir "$model_dir"
fi
model_name="openhermes-2.5-neural-chat-v3-3-slerp.Q6_K.gguf"
llm_file="${model_dir}/${model_name}"
model_url="https://huggingface.co/TheBloke/OpenHermes-2.5-neural-chat-v3-3-Slerp-GGUF/resolve/main/${model_name}"

# Download the LLM
if [ ! -f "$llm_file" ]; then
    curl -L -o "$llm_file" "$model_url"
fi

# Start server
python3 -m llama_cpp.server --model "$llm_file" --port 1234 --chat_format chatml --n_ctx 30000 --n_gpu_layers 1

# Deactivate virtual environment
deactivate
