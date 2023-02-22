#!/bin/bash
set -eux

cd `dirname $0`/../

IMAGE_NAME=`echo rcabench/${FE}/${TARGET_ID} | tr '[:upper:]' '[:lower:]'`

docker run --rm -it \
                --privileged \
                --env DA_TIMEOUT=${DA_TIMEOUT} \
                -v ${DA_RESULT}:/da_result:ro \
                -v ${FE_OUTPUT}:/shared \
                ${IMAGE_NAME} bash -i fe_run.sh
