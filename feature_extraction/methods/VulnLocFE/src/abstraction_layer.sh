#!/bin/bash
set -eu

echo "[start] Abstraction Layer"
cd ${WORKDIR}
mkdir ${WORKDIR}/output
python3 ${FE_ROOT}/src/gen_ini.py
python ${FE_ROOT}/scripts/convert.py --config_file "$WORKDIR/config.ini" --tag $TARGET_ID
echo "[done] Abstraction Layer"
