#!/bin/bash
set -eu

cd ${FE_ROOT}/aurora/root_cause_analysis
cargo run --release --bin rca -- --eval-dir ${WORKDIR} --trace-dir ${WORKDIR} --monitor --rank-predicates
cargo run --release --bin addr2line -- --eval-dir ${WORKDIR}
