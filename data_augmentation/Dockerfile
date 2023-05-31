FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV GIT_SSL_NO_VERIFY 1

ENV SHARED  /shared
ENV WORKDIR /workdir
ENV TARGET_ROOT /target

RUN apt-get update && apt-get install -y git vim python3

SHELL ["/bin/bash", "-c"]

# Create an user
ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd -o --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

RUN mkdir -p ${SHARED} ${WORKDIR} \
    && chown user:user ${SHARED} ${WORKDIR} \
    && chmod 744 ${SHARED} ${WORKDIR}

# Setup Data Augmenatation
ARG DA
ENV DA ${DA}
ENV DA_ROOT /data_augmentation
USER root:root
RUN mkdir -p ${DA_ROOT} \
    && chown user:user ${DA_ROOT}
COPY --chown=user:user data_augmentation/methods/${DA}/ ${DA_ROOT}
RUN ${DA_ROOT}/preinstall.sh
USER user:user
RUN ${DA_ROOT}/build.sh
RUN echo '. ${DA_ROOT}/config.sh' >> ~/.bash_profile

# Setup a target
ARG TARGET_ID
ENV TARGET_ID ${TARGET_ID}
USER root:root
RUN mkdir -p ${TARGET_ROOT} \
    && chown user:user ${TARGET_ROOT}
COPY --chown=user:user targets/${TARGET_ID} ${TARGET_ROOT}
RUN ${TARGET_ROOT}/preinstall.sh
USER user:user
RUN source ~/.bash_profile && ${DA_ROOT}/target_build.sh ${TARGET_ROOT}/build.sh
RUN echo '. ${TARGET_ROOT}/config.sh' >> ~/.bash_profile

RUN echo '. ~/.bash_profile' >> ~/.bashrc
