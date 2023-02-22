#!/bin/bash
set -eu

echo "[start] Check Result"
check.sh > ${SHARED}/fe_result.txt
mkdir ${SHARED}/data
cp -r ${WORKDIR}/. ${SHARED}/data
echo "[done] Check Result"
