#!/bin/bash
set -eux

#
# clone AFL++
#
cd "$DA_ROOT"
git clone https://github.com/AFLplusplus/AFLplusplus.git
cd AFLplusplus
git checkout 4.07c

#
# apply the Aurora patch (TODO)
#
patch -p1 < "${DA_ROOT}/aflppcem.patch"

#
# build AFL++
#
cd "${DA_ROOT}/AFLplusplus"
make all
