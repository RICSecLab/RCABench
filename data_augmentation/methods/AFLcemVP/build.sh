#!/bin/bash
set -eux

# clone AFL++
cd "${DA_ROOT}"
git clone https://github.com/AFLplusplus/AFLplusplus.git
cd AFLplusplus
git checkout 4.07c

# apply patches
patch -p1 < "${DA_ROOT}/aurora.aflpp.patch"
patch -p1 < "${DA_ROOT}/value_profile.patch"

# build AFL++
cd "${DA_ROOT}/AFLplusplus"
LLVM_CONFIG=llvm-config-14 make all
