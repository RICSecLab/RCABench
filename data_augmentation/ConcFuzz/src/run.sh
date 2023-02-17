#!/bin/bash
set -eux

cd ${WORKDIR}

#  make vunloc ouput dir
mkdir -p "${WORKDIR}/output"

python3 ${DA_ROOT}/src/gen_ini.py

T=`date --iso-8601=seconds`
TIMEOUT=${DA_MAX_TIMEOUT} python ${DA_ROOT}/scripts/fuzz.py --config_file "$WORKDIR/config.ini" --tag $TARGET_ID

RES_DIR=`find ${WORKDIR}/output/ -maxdepth 1 -name 'output_*' -not -path '*/\.*' -type d | sed 's/^\.\///g'`
python3 ${DA_ROOT}/src/convert.py $T $RES_DIR/inputs
