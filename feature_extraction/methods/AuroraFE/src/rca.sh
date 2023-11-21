#!/bin/bash
set -eu

RCA_LOAD_OFFSET=""
if [[ -v LOAD_OFFSET ]];
then
	RCA_LOAD_OFFSET="--load-offset ${LOAD_OFFSET}"
fi

cd ${FE_ROOT}/aurora/root_cause_analysis
cargo run --release --bin rca -- ${RCA_LOAD_OFFSET} --eval-dir ${WORKDIR} --trace-dir ${WORKDIR} --monitor --rank-predicates 
cargo run --release --bin addr2line -- ${RCA_LOAD_OFFSET} --eval-dir ${WORKDIR} 
