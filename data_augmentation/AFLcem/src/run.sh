#!/bin/bash
set -eux

AFLCEM_TIMEOUT=${DA_MAX_TIMEOUT}

mkdir -p ${WORKDIR}/seeds
cp ${TARGET_ROOT}/seeds/${DA_SEED} ${WORKDIR}/seeds

T=`date --iso-8601=seconds`
timeout --preserve-status --foreground ${AFLCEM_TIMEOUT} ${DA_ROOT}/afl-fuzz/afl-fuzz -C -d -m none \
  -i ${WORKDIR}/seeds -o ${WORKDIR} -- ${WORKDIR}/${AFLCEM_DA_TARGET} ${AFLCEM_DA_ARGS}

python3 ${DA_ROOT}/src/convert.py $T
