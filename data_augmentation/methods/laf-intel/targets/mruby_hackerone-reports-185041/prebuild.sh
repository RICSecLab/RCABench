#!/bin/bash

. "${TARGET_ROOT}/config.sh"

cd "$TARGET_ROOT"

git clone https://github.com/mruby/mruby.git laf-intel_target
cd "${TARGET_ROOT}/laf-intel_target"
git checkout 88604e39ac9c25ffdad2e3f03be26516fe866038

AFL_LLVM_LAF_ALL=1 \
CC="${DA_ROOT}/AFLplusplus/afl-clang-fast" \
LD="${DA_ROOT}/AFLplusplus/afl-clang-fast" \
make -e "-j$(($(nproc) +1))"
