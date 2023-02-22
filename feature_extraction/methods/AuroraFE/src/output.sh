#!/bin/bash
set -eu

echo "[start] Result Check"
check.sh > ${SHARED}/fe_result.txt
mkdir ${SHARED}/data
cp -r ${WORKDIR}/. ${SHARED}/data
echo "[done] Result Check"
