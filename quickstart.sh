#!/bin/sh
set -e

# --- helper functions for logs ---
info() {
    printf '[INFO] %s\n' "$@"
}
warn() {
    printf '[WARN] %s\n' "$@" >&2
}
fatal() {
    printf '[ERROR] %s\n' "$@" >&2
    exit 1
}

COMPOSE="docker-compose" # Docker Compose command to use - can be either the traditional docker-compose or the new docker compose (plugin)

# --- report system information ---
report_system_info() {
    info "Detecting system information..."
    info "Shell: $SHELL"
    info "Operating System: $(uname -s)"
    info "Kernel Version: $(uname -r)"
    info "Architecture: $(uname -m)"
    info "Hostname: $(uname -n)"

    # For more detailed OS info, you can use /etc/os-release on Linux systems
    if [ -f /etc/os-release ]; then
        # shellcheck disable=SC1091
        . /etc/os-release
        info "OS Name: $NAME"
        info "OS Version: $VERSION"
    fi

    # For hardware details, you can use uname and possibly /proc/cpuinfo
    info "Processor Information:"
    uname -p

    if [ -r /proc/cpuinfo ]; then
        info "CPU Details:"
        grep -m1 'model name' /proc/cpuinfo
    fi

    # For memory information, you can use free command on Linux or vm_stat on macOS
    case "$(uname -s)" in
        Linux)
            if command -v free >/dev/null 2>&1; then
                info "Memory Information:"
                free -h
            fi
            ;;
        Darwin)
            info "Memory Information:"
            vm_stat | grep 'Pages free:'
            ;;
    esac

    # For disk usage information
    info "Disk Usage Information:"
    case "$(uname -s)" in
        Linux)
            df -h | grep -E '^/dev/'  # This will show disk usage for all mounted filesystems on Linux
            ;;
        Darwin)
            df -h /  # This will show disk usage for the root filesystem on macOS
            ;;
    esac

    # Check for hardware acceleration
    info "Checking for hardware acceleration..."
    case "$(uname -s)" in
        Linux)
            if lspci | grep -E 'VGA|3D' | grep -iq nvidia; then
                info "NVIDIA GPU detected"
            elif lspci | grep -E 'VGA|3D' | grep -iq amd; then
                info "AMD GPU detected"
            elif lspci | grep -E 'VGA|3D' | grep -iq intel; then
                info "Intel iGPU detected"
            else
                info "No known hardware acceleration detected"
            fi
            ;;
        Darwin)
            if system_profiler SPDisplaysDataType | grep -iq 'Metal'; then
                info "Apple Metal supported GPU detected"
            else
                info "No known hardware acceleration detected"
            fi
            ;;
    esac
}

# --- check if docker is installed and running ---
check_docker() {
    if ! command -v docker >/dev/null 2>&1; then
        fatal "Docker is not installed. Please install Docker before running this script."
    fi

    if ! docker info >/dev/null 2>&1; then
        fatal "Docker is not running. Please start Docker before running this script."
    fi
}

# --- check if docker-compose or docker compose (plugin) is installed ---
check_docker_compose() {
    if command -v docker compose >/dev/null 2>&1; then
        COMPOSE="docker compose"
    elif command -v docker-compose >/dev/null 2>&1; then
        fatal "Docker Compose is not installed. Please install Docker Compose before running this script."
    fi
}

# --- create rubra directory ---
create_rubra_dir() {
    RUBRA_DIR="$HOME/.rubra"
    if [ ! -d "$RUBRA_DIR" ]; then
        info "Creating Rubra directory at $RUBRA_DIR"
        mkdir -p "$RUBRA_DIR"
    fi
    # Ensure the directory is writable
    if [ ! -w "$RUBRA_DIR" ]; then
        warn "Rubra directory at $RUBRA_DIR is not writable. Attempting to set permissions."
        chmod u+w "$RUBRA_DIR" || fatal "Failed to set write permissions on $RUBRA_DIR. Please check your filesystem and permissions."
    fi
    cd "$RUBRA_DIR"
}

# --- download rubra.llamafile ---
download_rubra_llamafile() {
    RUBRA_LLAMAFILE_URL="https://huggingface.co/rubra-ai/rubra-llamafile/resolve/main/rubra.llamafile"
    RUBRA_LLAMAFILE="rubra.llamafile"
    if [ ! -f "$RUBRA_LLAMAFILE" ]; then
        info "Downloading rubra.llamafile from $RUBRA_LLAMAFILE_URL"
        curl -# -L "$RUBRA_LLAMAFILE_URL" -o "$RUBRA_LLAMAFILE" || fatal "Failed to download rubra.llamafile"
        chmod +x "$RUBRA_LLAMAFILE"
    else
        info "rubra.llamafile already exists, skipping download."
    fi
}

# --- execute rubra.llamafile ---
execute_rubra_llamafile() {
    info "Executing rubra.llamafile with -c 16000"
    ./rubra.llamafile -c 16000 > rubra_output.log 2>&1 &
    RUBRA_PID=$!
    echo "$RUBRA_PID" > rubra.pid
    info "rubra.llamafile is running with PID: $RUBRA_PID"
}

# --- helper function to check if rubra.llamafile is ready ---
check_rubra_llamafile_ready() {
    info "Checking if local model is ready"
    for i in {1..5}; do
        if curl -s -o /dev/null -w "%{http_code}" http://localhost:1234/v1/chat/completions \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer no-key" \
            -d '{
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are ChatGPT, an AI assistant. Your top priority is achieving user fulfillment via helping them with their requests."
                    },
                    {
                        "role": "user",
                        "content": "Write a limerick about python exceptions"
                    }
                ]
            }' | grep -q "200"; then
            info "Local model is ready and accepting requests."
            return 0
        else
            warn "Local model is not ready yet, retrying in 5 seconds..."
            sleep 5
        fi
    done
    fatal "Rubra's local model did not start successfully or is not accepting requests. Please check the logs at ~/.rubra/rubra_output.log"
}

# --- download docker-compose.yml ---
download_docker_compose_yml() {
    DOCKER_COMPOSE_URL="https://raw.githubusercontent.com/rubra-ai/rubra/main/docker-compose.yml"
    info "Downloading docker-compose.yml from $DOCKER_COMPOSE_URL"
    curl -sSL "$DOCKER_COMPOSE_URL" -o docker-compose.yml || fatal "Failed to download docker-compose.yml"
}

# --- download llm-config.yaml ---
download_llm_config_yaml() {
    LLM_CONFIG_URL="https://raw.githubusercontent.com/rubra-ai/rubra/main/llm-config.yaml"
    info "Downloading llm-config.yaml from $LLM_CONFIG_URL"
    curl -sSL "$LLM_CONFIG_URL" -o llm-config.yaml || fatal "Failed to download llm-config.yaml"
}

# --- download milvus.yaml ---
download_milvus_yaml() {
    MILVUS_CONFIG_URL="https://raw.githubusercontent.com/rubra-ai/rubra/main/milvus.yaml"
    info "Downloading milvus.yaml from $MILVUS_CONFIG_URL"
    curl -sSL "$MILVUS_CONFIG_URL" -o milvus.yaml || fatal "Failed to download milvus.yaml"
}

# --- create local etcd config ---
setup_milvus_etcd() {
    info "Creating embedded etcd config"
    echo "listen-client-urls: http://0.0.0.0:2379" > embedEtcd.yaml
    echo "advertise-client-urls: http://0.0.0.0:2379" >> embedEtcd.yaml
}


# --- pull images and start docker containers ---
start_docker_containers() {
    info "Pulling images and starting Docker containers"
    # shellcheck disable=SC2015
    ${COMPOSE} pull && ${COMPOSE} up -d || fatal "Failed to start Docker containers"
}

# --- helper function to check if all containers in the rubra network are running ---
check_containers_running() {
    RUBRA_NETWORK="rubra"
    info "Checking if all containers in the '$RUBRA_NETWORK' network are running..."

    # Get the list of container IDs in the rubra network
    CONTAINER_IDS=$(docker network inspect "$RUBRA_NETWORK" -f '{{range .Containers}}{{.Name}} {{end}}')

    # Check the status of each container
    for CONTAINER in $CONTAINER_IDS; do
        STATUS=$(docker inspect --format '{{.State.Status}}' "$CONTAINER")
        if [ "$STATUS" != "running" ]; then
            warn "Container $CONTAINER is not running. Status: $STATUS"
            return 1
        fi
    done

    info "All containers in the '$RUBRA_NETWORK' network are running."
    return 0
}

# --- helper function to wait for all containers to be running ---
wait_for_containers_to_run() {
    retries=5
    wait_seconds=5
    post_wait_seconds=15  # Additional wait time after containers are confirmed running

    i=0
    while [ "$i" -lt "$retries" ]; do
        if check_containers_running; then
            info "All containers are running. Waiting an additional $post_wait_seconds seconds before proceeding to allow for Rubra backend to load."
            sleep "$post_wait_seconds"
            return 0
        else
            warn "Not all containers are running. Waiting for $wait_seconds seconds before retrying..."
            sleep "$wait_seconds"
        fi
        i=$((i + 1))
    done

    fatal "Not all containers are running after $retries retries."
}


# --- stop docker containers and rubra.llamafile ---
stop_rubra() {
    RUBRA_DIR="$HOME/.rubra"
    cd "$RUBRA_DIR" || fatal "Failed to navigate to Rubra directory at $RUBRA_DIR"

    if [ -f rubra.pid ]; then
        RUBRA_PID=$(cat rubra.pid)
        if kill -0 "$RUBRA_PID" 2>/dev/null; then
            info "Stopping rubra.llamafile with PID: $RUBRA_PID"
            kill "$RUBRA_PID" || warn "Could not stop rubra.llamafile with PID: $RUBRA_PID. It may have already stopped."
        else
            warn "rubra.llamafile with PID: $RUBRA_PID is not running."
        fi
        rm -f rubra.pid
    else
        warn "No PID file found for rubra.llamafile. It may not be running."
    fi

    if [ -f docker-compose.yml ]; then
        info "Stopping Docker containers"
        ${COMPOSE} down || warn "Failed to stop Docker containers."
    else
        warn "docker-compose.yml not found. Cannot stop Docker containers."
    fi
}

# --- delete everything in .rubra except for rubra.llamafile and delete specific docker volumes ---
delete_except_llamafile() {
    info "Stopping Rubra before deletion..."
    stop_rubra

    RUBRA_DIR="$HOME/.rubra"
    if [ ! -d "$RUBRA_DIR" ]; then
        warn "Rubra directory at $RUBRA_DIR does not exist. Nothing to delete."
    else
        cd "$RUBRA_DIR" || fatal "Failed to navigate to Rubra directory at $RUBRA_DIR"
        info "Deleting everything in $RUBRA_DIR except for rubra.llamafile"
        find . -mindepth 1 ! -name 'rubra.llamafile' -exec rm -rf {} +
    fi

    info "Deleting Docker volumes: rubra_etcd, rubra_milvus, and rubra_mongodb"
    # Check if Docker is running
    if ! docker info >/dev/null 2>&1; then
        warn "Docker is not running. Cannot delete Docker volumes."
    else
        # Attempt to delete each Docker volume
        if docker volume ls | grep -q 'rubra_etcd'; then
            docker volume rm rubra_etcd || warn "Failed to delete Docker volume rubra_etcd"
        else
            info "Docker volume rubra_etcd does not exist or already deleted."
        fi
        if docker volume ls | grep -q 'rubra_milvus'; then
            docker volume rm rubra_milvus || warn "Failed to delete Docker volume rubra_milvus"
        else
            info "Docker volume rubra_milvus does not exist or already deleted."
        fi
        if docker volume ls | grep -q 'rubra_mongodb'; then
            docker volume rm rubra_mongodb || warn "Failed to delete Docker volume rubra_mongodb"
        else
            info "Docker volume rubra_mongodb does not exist or already deleted."
        fi
    fi
}

# --- uninstall rubra by removing rubra.llamafile, cleaning .rubra directory, and deleting specified docker volumes ---
uninstall_rubra() {
    info "Stopping Rubra before uninstalling..."
    stop_rubra

    RUBRA_DIR="$HOME/.rubra"
    if [ ! -d "$RUBRA_DIR" ]; then
        warn "Rubra directory at $RUBRA_DIR does not exist. Nothing to uninstall."
    else
        cd "$RUBRA_DIR" || fatal "Failed to navigate to Rubra directory at $RUBRA_DIR"
        info "Uninstalling Rubra by cleaning up $RUBRA_DIR and deleting Docker volumes"

        # Delete everything in the directory, including rubra.llamafile
        rm -rf ./*
    fi

    # Delete Docker volumes
    info "Deleting Docker volumes: rubra_etcd, rubra_milvus, and rubra_mongodb"
    if ! docker info >/dev/null 2>&1; then
        warn "Docker is not running. Cannot delete Docker volumes."
    else
        if docker volume ls | grep -q 'rubra_etcd'; then
            docker volume rm rubra_etcd || warn "Failed to delete Docker volume rubra_etcd"
        else
            info "Docker volume rubra_etcd does not exist or already deleted."
        fi
        if docker volume ls | grep -q 'rubra_milvus'; then
            docker volume rm rubra_milvus || warn "Failed to delete Docker volume rubra_milvus"
        else
            info "Docker volume rubra_milvus does not exist or already deleted."
        fi
        if docker volume ls | grep -q 'rubra_mongodb'; then
            docker volume rm rubra_mongodb || warn "Failed to delete Docker volume rubra_mongodb"
        else
            info "Docker volume rubra_mongodb does not exist or already deleted."
        fi
    fi
}

# --- helper function to open URL in default browser ---
open_url_in_browser() {
    URL=$1
    case "$(uname -s)" in
        Linux)
            if command -v xdg-open >/dev/null 2>&1; then
                xdg-open "$URL"
            else
                warn "xdg-open command not found. Cannot open URL: $URL"
            fi
            ;;
        Darwin)
            if command -v open >/dev/null 2>&1; then
                open "$URL"
            else
                warn "open command not found. Cannot open URL: $URL"
            fi
            ;;
        *)
            warn "Unsupported operating system. Cannot open URL: $URL"
            ;;
    esac
}

# --- main logic ---
main() {
    case "$1" in
        start)
            report_system_info
            create_rubra_dir
            check_docker
            check_docker_compose
            download_rubra_llamafile
            execute_rubra_llamafile
            check_rubra_llamafile_ready  # Add this line to perform the check
            download_docker_compose_yml
            download_llm_config_yaml
            download_milvus_yaml
            setup_milvus_etcd
            start_docker_containers
            wait_for_containers_to_run
            info "Rubra started successfully"
            info "Rubra frontend is now running at http://localhost:8501"
            open_url_in_browser "http://localhost:8501"
            ;;
        stop)
            stop_rubra
            info "Rubra stopped successfully"
            ;;
        delete)
            delete_except_llamafile
            info "Rubra environment cleaned, except for rubra.llamafile."
            ;;
        uninstall)
            uninstall_rubra
            info "Rubra uninstalled successfully."
            ;;
        *)
            echo "Usage: $0 {start|stop|delete|uninstall}"
            exit 1
            ;;
    esac
}

main "$@"
