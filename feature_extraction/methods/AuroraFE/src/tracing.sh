#!/bin/bash
set -eu

ORIG=${TARGET_ROOT}/aflcem_target/${RELPATH}

mkdir -p ${WORKDIR}/traces
cd ${FE_ROOT}/aurora/tracing/scripts
python3 tracing.py "${WORKDIR}/`basename ${ORIG}`_trace ${ARGS}" ${WORKDIR}/inputs ${WORKDIR}/traces
python3 addr_ranges.py --eval_dir ${WORKDIR} ${WORKDIR}/traces
