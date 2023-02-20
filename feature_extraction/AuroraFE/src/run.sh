#!/bin/bash
set -eu

echo "[start] Abstraction Layer"
echo ${ARGS} > ${WORKDIR}/arguments.txt
python3 ${FE_ROOT}/src/convert.py
tracing.sh
echo "[done] Abstraction Layer"

echo "[start] FE"
rca.sh
echo "[done] FE"

echo "[start] Result Check"
check.sh > ${SHARED}/fe_result.txt
mkdir ${SHARED}/data
cp -r ${WORKDIR}/. ${SHARED}/data
echo "[done] Result Check"
