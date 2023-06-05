FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV GIT_SSL_NO_VERIFY 1

ENV SHARED  /shared
ENV WORKDIR /workdir
ENV TARGET_ROOT /target
ENV DA_RESULT /da_result

RUN apt-get update && apt-get install -y git vim python3

SHELL ["/bin/bash", "-c"]

# Create an user
ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd -o --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

RUN mkdir -p ${SHARED} ${WORKDIR} ${DA_RESULT} \
    && chown user:user ${SHARED} ${WORKDIR} ${DA_RESULT} \
    && chmod 744 ${SHARED} ${WORKDIR} ${DA_RESULT}


# Setup Feature Extraction
ARG FE
ENV FE ${FE}
ENV FE_ROOT /feature_extraction
USER root:root
RUN mkdir -p ${FE_ROOT} \
    && chown user:user ${FE_ROOT}
COPY --chown=user:user feature_extraction/methods/${FE} ${FE_ROOT}
COPY --chown=user:user feature_extraction/scripts_inside_container ${FE_ROOT}/scripts_inside_container
RUN ${FE_ROOT}/preinstall.sh
USER user:user
RUN ${FE_ROOT}/build.sh \
    && echo '. ${FE_ROOT}/config.sh' >> ~/.bash_profile \
    && echo '. ${FE_ROOT}/scripts_inside_container/config.sh' >> ~/.bash_profile

# Setup a target
ARG TARGET_ID
ENV TARGET_ID ${TARGET_ID}
USER root:root
RUN mkdir -p ${TARGET_ROOT} \
    && chown user:user ${TARGET_ROOT}
COPY --chown=user:user targets/${TARGET_ID} ${TARGET_ROOT}
RUN ${TARGET_ROOT}/preinstall.sh
USER user:user
RUN source ~/.bash_profile && ${FE_ROOT}/target_build.sh ${TARGET_ROOT}/build.sh
RUN echo '. ${TARGET_ROOT}/config.sh' >> ~/.bash_profile

RUN echo '. ~/.bash_profile' >> ~/.bashrc
