#!/bin/bash

# set -e

source ./scripts/reset.sh
# ---------------------------------------------------------------------- #
# Define Docker Variables
# ---------------------------------------------------------------------- #
declare -a images=(
    localhost/stream_svelte
    localhost/stream_api_inventory
    localhost/stream_api_payments
    localhost/queue_gateway
    localhost/queue_auth
    localhost/queue_converter
    localhost/queue_notification
)
declare -a volumes=(
    microservices_redis_data
    microservices_mongo_data
    microservices_mongo_config
    microservices_pgadmin_data
    microservices_postgres_data
    microservices_rabbitmq_data
)
declare -a bindings=(
    #
)

# ---------------------------------------------------------------------- #
# Main Function
# ---------------------------------------------------------------------- #
main(){
    # Shut down all containers
    docker compose down
    
    # End Reverse proxy for docker
    end_proxy
    
    # Clean up
    run folders remove_folders  ${bindings[*]}
    run volumes remove_volumes  ${volumes[*]}
    run images  remove_images   ${images[*]}
    prune_docker
}

main $@
