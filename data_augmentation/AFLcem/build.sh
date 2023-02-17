#!/bin/bash
set -eux

# Clone AFL
cd "${DA_ROOT}"
wget -q -c https://lcamtuf.coredump.cx/afl/releases/afl-latest.tgz
tar xf afl-latest.tgz
mv afl-2.52b afl-fuzz

# Apply patch
cd afl-fuzz
wget -O "${DA_ROOT}"/crash_exploration.patch https://raw.githubusercontent.com/RUB-SysSec/aurora/master/crash_exploration/crash_exploration.patch
patch -p1 < "${DA_ROOT}"/crash_exploration.patch

# Build AFL
make -j$(nproc)
