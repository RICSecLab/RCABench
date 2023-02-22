#!/bin/bash
set -eu

echo "[start] Abstraction Layer"
echo ${ARGS} > ${WORKDIR}/arguments.txt
python3 ${FE_ROOT}/src/convert.py
tracing.sh
echo "[done] Abstraction Layer"
