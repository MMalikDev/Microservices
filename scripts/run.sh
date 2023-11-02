#!/bin/bash

# Icons
icon_log="\xF0\x9F\x93\x91" # Bookmark Tabs (U+1F4D1)
icon_start="\xF0\x9F\x9B\xA0 " # Hammer and Wrench (U+1F6E0)

display_usage() {
    cat << EOF

Usage: $0 [OPTIONS]

Run Project in specified environment

    OPTIONS
     -e [SECRET]    Echo Secret in Base64
     -l             Run in Docker
     -p             Start Reverse Proxy (Docker)
     -m             Run Test for Microservices APIs (Docker)

     -g [OBJECTS]   Get Cluster Objects
     -c             Create Minikube Cluster
     -d             Delete Minikube Cluster
     -b             Build Local Docker Images for Minikube

     -v             Setup Volumes (Default Local)
     -i             Setup Ingress and Controller
     -r             Restart All Deployments
     -a             Setup All Microservices

     -x             Setup All Third Party Services
     -s             Setup Redis Stream Microservice Configs
     -q             Setup RabitQ Queue Microservice Configs

     -t             Tunnel to Ingress Controller Proxy
     -h             Display this help


    OBJECTS
        v* -> pv
        c* -> pvc
        p* -> pods
        h* -> nodes
        s* -> services
        d* -> deployment
        n* -> namespaces

Configure $0 defaults using .env file

    Keep Docker Logs:
        - KEEP_LOGS=True    ( 1 )

    Use Redis Streams (Docker):
        - USE_STREAMS=True  ( 1 )

EOF
    exit 1
}

# Generic
load_env(){
    set -a
    source .env
}
get_env(){
    echo $(grep -i "$@" .env | cut -d "=" -f 2)
}
get_bool(){
    local variable=$(get_env "$@" | tr '[A-Z]' '[a-z]')
    
    if [[ $variable =~ (1|true) ]]; then
        echo true
    else
        echo false
    fi
}

# Error Handlers
handle_errors(){
    if [[ $(get_bool KEEP_LOGS) == "true" ]]; then
        printf "\n$icon_log Keeping logs...\n\n"
        return
    fi
    if [[ $@ != 0 ]]; then
        printf "\n$icon_start Error encountered!\n\n"
        exit 1
    fi
    
    clear
    printf "\n$icon_log Cleared logs...\n\n"
}
log_error() {
    echo "$1" 2>&1;
    exit 1;
}

# Docker
reload_services(){
    local services=$@
    if [[ -n $services ]]; then
        printf "\n$icon_start Reloading the following service(s): "
        printf "$services\n\n"
    else
        printf "\n$icon_start Reloading all services\n\n"
    fi
    
    docker compose up -d
    echo "$services" | xargs docker compose kill
    echo "$services" | xargs docker compose up --force-recreate --build -d
}
follow_logs(){
    local services=$@
    if [[ -n $services ]]; then
        printf "\n$icon_log Getting logs from the following service(s): "
        printf "$services\n\n"
    else
        printf "\n$icon_log Getting logs from all services\n\n"
    fi
    
    echo "$services" | xargs docker compose logs -f
}
cp_docker(){
    local container=$1
    local source=$2
    local target=$3
    
    local containerID=$(docker-compose ps -qa $container)
    docker cp $containerID:$source $target
}

# Reverse Proxy
start_proxy(){
    cd proxy
    reload_services
    handle_errors $?
    
    docker image prune -f
    cd ..
}

# Python
use_venv(){
    local os=$(uname | tr '[A-Z]' '[a-z]')
    
    case ${os} in
        linux* | darwin*) source .venv/bin/activate ;;
        mingw* | cygwin*) source .venv/Scripts/activate ;;
        *) log_error "$icon_start Unsupported operating system: $os" ;;
    esac
}
run_pytest(){
    local command="python test"
    local containers=("$@")
    
    for container in "${containers[@]}"; do
        printf "\n$icon_start Running Tests for $container service...\n\n"
        docker exec -it "$container" $command
    done
}
run_python(){
    printf "\n$icon_start Running Python in local venv\n\n"
    use_venv
    cd $(get_env PYTHON_IMAGE)
    python main.py $@
    cd ..
}

# Javascript
run_javascript(){
    printf "\n$icon_start Running Javascript using Node\n\n"
    cd $(get_env JAVASCRIPT_IMAGE)
    npm install
    npm start
    cd ..
}
