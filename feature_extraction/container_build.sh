#!/bin/bash
set -eux

cd `dirname $0`/../
pwd
IMAGE_NAME=`echo rcabench/${FE}/${TARGET_ID} | tr '[:upper:]' '[:lower:]'`

docker build -t ${IMAGE_NAME} --no-cache \
                --build-arg USER_UID=`id -u` \
                --build-arg USER_GID=`id -g` \
                --build-arg FE=${FE} \
                --build-arg TARGET_ID=${TARGET_ID} \
                -f feature_extraction/Dockerfile .

