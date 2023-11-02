#!/bin/bash
set -eux

. ${TARGET_ROOT}/config.sh


cd "${TARGET_ROOT}"

git clone https://github.com/mruby/mruby.git aflcemvp_target
cd "${TARGET_ROOT}/aflcemvp_target"
git checkout 88604e39ac9c25ffdad2e3f03be26516fe866038

AFL_LLVM_INSTRUMENT=NATIVE \
CC="${DA_ROOT}/AFLplusplus/afl-clang-fast" \
LD="${DA_ROOT}/AFLplusplus/afl-clang-fast" \
make -e -j$((`nproc`+1))
