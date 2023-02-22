#!/bin/bash
set -eu

python3 ${FE_ROOT}/src/check.py ${WORKDIR}/ranked_predicates_verbose.txt /target/root_causes
