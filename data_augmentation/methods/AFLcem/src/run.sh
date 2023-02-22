#!/bin/bash
set -eux

AFLCEM_TIMEOUT=${DA_MAX_TIMEOUT}
ORIG=${TARGET_ROOT}/aflcem_target/${RELPATH}

mkdir -p ${WORKDIR}/seeds
cp ${TARGET_ROOT}/seeds/${DA_SEED} ${WORKDIR}/seeds

T=`date --iso-8601=seconds`
timeout --preserve-status --foreground ${AFLCEM_TIMEOUT} ${DA_ROOT}/afl-fuzz/afl-fuzz -C -d -m none \
  -i ${WORKDIR}/seeds -o ${WORKDIR} -- ${WORKDIR}/`basename ${ORIG}`_fuzz ${ARGS}

python3 ${DA_ROOT}/src/convert.py $T
mkdir ${SHARED}/data
cp -r ${WORKDIR}/. ${SHARED}/data
