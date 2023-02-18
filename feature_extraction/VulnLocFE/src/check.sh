#!/bin/bash
set -eu

RESDIR=`find ${WORKDIR}/output/ -maxdepth 1 -name 'output_*' -not -path '*/\.*' -type d | sed 's/^\.\///g'`
python3 ${FE_ROOT}/src/check.py ${RESDIR}/patchloc.log /target/root_causes
