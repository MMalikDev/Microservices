#!/bin/bash

# set -e

source ./scripts/run.sh
# ---------------------------------------------------------------------- #
# Define Docker Variables
# ---------------------------------------------------------------------- #
declare -A images=(
    ["localhost/stream_svelte"]="./apps/stream/web/"
    ["localhost/stream_api_inventory"]="./apps/stream/api/inventory/"
    ["localhost/stream_api_payments"]="./apps/stream/api/payments/"
    ["localhost/queue_gateway"]="./apps/queue/gateway/"
    ["localhost/queue_auth"]="./apps/queue/auth/"
    ["localhost/queue_converter"]="./apps/queue/converter/"
    ["localhost/queue_notification"]="./apps/queue/notification/"
)

declare -a reloads=(
    # rabbitqm
    # mongo
    # postgres
    # pgadmin4
    # redis
    auth
    gateway
    converter
    notification
    inventory
    payments
    web
)

declare -a logs=(
    # rabbitqm
    # mongo
    # postgres
    # pgadmin4
    # redis
    auth
    gateway
    converter
    notification
    inventory
    payments
    web
)

declare -a microservices=(
    inventory
    payments
)

# ---------------------------------------------------------------------- #
# Helper
# ---------------------------------------------------------------------- #
switch_namespace(){
    local namespace="$1"
    kubectl config set-context --current --namespace=$namespace
}

activate_streams(){
    if [[ $(get_bool USE_STREAMS) == "true"  ]]; then
        local containers=("$@")
        local command='python3 db/consumer.py'
        
        for container in "${containers[@]}"; do
            printf "\n$icon_start Activating Redis streams for $container microservice...\n\n"
            docker exec -d "$container" $command
        done
    fi
}

# ---------------------------------------------------------------------- #
# OPTIONS
# ---------------------------------------------------------------------- #
get_secret(){
    echo -n "$1" | base64
}

run_docker(){
    reload_services ${reloads[*]}
    handle_errors $?
    
    activate_streams ${microservices[*]}
    handle_errors $?
    
    docker image prune -f
    follow_logs ${logs[*]}
    exit 0
}

create_cluster(){
    minikube start;
}

delete_cluster(){
    minikube delete --all
}

build_images() {
    local -n mappings="$1"
    
    for name in "${!mappings[@]}"; do
        directory="${mappings[$name]}"
        minikube image build -t "$name"  "$directory" 
    done
    minikube image ls --format table
}

get_obj(){
    case ${1} in
        v*) kubectl get pv -A                 ;;
        c*) kubectl get pvc -A                ;;
        p*) kubectl get pods -A               ;;
        h*) kubectl get nodes -A              ;;
        s*) kubectl get services -A           ;;
        d*) kubectl get deployment -A         ;;
        n*) kubectl get namespaces -A         ;;
        *) log_error "Unsupported object: $1" ;;
    esac
}

tunnel_proxy(){
    minikube service proxy --url=true
}

start_ingress(){
    local repo=proxy
    
    kubectl apply -f "${repo}/controller.yaml"
    kubectl apply -f "${repo}/ingress.yaml"
}

setup_volumes(){
    local repo=data
    
    kubectl apply -f "${repo}/localClass.yaml"
    kubectl apply -f "${repo}/volumes.yaml"
}

setup_stream(){
    local repo=apps/stream
    
    kubectl apply -f "${repo}/namespace.yaml"

    kubectl apply -f "${repo}/redis/"

    kubectl apply -f "${repo}/api/inventory/manifests/"
    kubectl apply -f "${repo}/api/payments/manifests/"
    kubectl apply -f "${repo}/web/manifests/"

    kubectl apply -f "${repo}/ingress.yaml"
    
    switch_namespace stream
}

setup_queue(){
    local repo=apps/queue
    
    kubectl apply -f "${repo}/namespace.yaml"
    
    kubectl apply -f "${repo}/rabbitmq/"
    kubectl apply -f "${repo}/postgres/db/"
    kubectl apply -f "${repo}/postgres/web/"
    kubectl apply -f "${repo}/mongo/db/"
    kubectl apply -f "${repo}/mongo/web/"

    kubectl apply -f "${repo}/auth/manifests/"
    kubectl apply -f "${repo}/gateway/manifests/"    
    kubectl apply -f "${repo}/converter/manifests/"
    kubectl apply -f "${repo}/notification/manifests/"

    kubectl apply -f "${repo}/ingress.yaml"
    
    switch_namespace queue
}

setup_third_party(){
    local repo=apps/stream
    
    kubectl apply -f "${repo}/namespace.yaml"
    kubectl apply -f "${repo}/redis/"

    local repo=apps/queue
    
    kubectl apply -f "${repo}/namespace.yaml"
    kubectl apply -f "${repo}/rabbitmq/"
    kubectl apply -f "${repo}/postgres/db/"
    kubectl apply -f "${repo}/postgres/web/"
    kubectl apply -f "${repo}/mongo/db/"
    kubectl apply -f "${repo}/mongo/web/"
}
setup_all(){
    setup_volumes
    start_ingress
    setup_stream
    setup_queue
}

restart_all(){
    kubectl rollout restart deployment -n default
    kubectl rollout restart deployment -n stream
    kubectl rollout restart deployment -n queue
}

# ---------------------------------------------------------------------- #
# Main Function
# ---------------------------------------------------------------------- #
main(){
    while getopts "e:lpmg:cdbviraxsqth" OPTION; do
        case $OPTION in
            e) get_secret $OPTARG               ;;
            l) run_docker                       ;;
            p) start_proxy                      ;;
            m) run_pytest ${microservices[*]}   ;;

            g) get_obj $OPTARG                  ;;
            c) create_cluster                   ;;
            d) delete_cluster                   ;;
            b) build_images images              ;;
            
            v) setup_volumes                    ;;
            i) start_ingress                    ;;
            r) restart_all                      ;;
            a) setup_all                        ;;
            
            x) setup_third_party                ;;
            s) setup_stream                     ;;
            q) setup_queue                      ;;
            
            t) tunnel_proxy                     ;;
            h) display_usage                    ;;
            ?) display_usage                    ;;
        esac
    done
    shift $((OPTIND -1))
}

main $@
