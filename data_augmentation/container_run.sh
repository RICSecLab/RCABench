#!/bin/bash
set -eux

cd `dirname $0`/../

IMAGE_NAME=`echo rcabench/${DA}/${TARGET_ID} | tr '[:upper:]' '[:lower:]'`

DA_ENV_LIST_INTERNAL=""
if [ -n "${DA_ENV_LIST:-}" ]; then
  DA_ENV_LIST_INTERNAL="--env-file $DA_ENV_LIST"
fi

docker run --rm -it \
                --privileged \
                --env DA_SEED=${DA_SEED} \
                --env DA_MAX_TIMEOUT=${DA_MAX_TIMEOUT} \
                -v ${DA_OUTPUT}:/shared \
                ${DA_ENV_LIST_INTERNAL} \
                ${IMAGE_NAME} bash -i run.sh
