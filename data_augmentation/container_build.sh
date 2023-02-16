#!/bin/bash
set -eux

cd `dirname $0`/../

IMAGE_NAME=`echo rcabench/${DA}/${TARGET_ID} | tr '[:upper:]' '[:lower:]'`

docker build -t ${IMAGE_NAME} \
                --build-arg USER_UID=`id -u` \
                --build-arg USER_GID=`id -g` \
                --build-arg DA=${DA} \
                --build-arg TARGET_ID=${TARGET_ID} \
                -f data_augmentation/Dockerfile .

