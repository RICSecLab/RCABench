#!/bin/bash
set -eux

cd "$DA_ROOT"

. ${DA_ROOT}/config.sh

git clone https://github.com/VulnLoc/VulnLoc ${CONCFUZZ_GIT_DIR}

cp ${CONCFUZZ_GIT_DIR}/code/fuzz.py ${DA_ROOT}/scripts
cp ${CONCFUZZ_GIT_DIR}/code/tracer.py ${DA_ROOT}/scripts
cp ${CONCFUZZ_GIT_DIR}/code/utils.py ${DA_ROOT}/scripts

patch ${DA_ROOT}/scripts/fuzz.py fuzz.patch

# for iftracer
export CMAKE_PREFIX_PATH="$DA_ROOT/deps/dynamorio/cmake"

# set up the tracer
cp -r ${CONCFUZZ_GIT_DIR}/code/iftracer.zip ${DA_ROOT}/scripts
cd "$DA_ROOT/scripts"
unzip iftracer.zip
cd "$DA_ROOT/scripts/iftracer"
sed -i 's/<path_to_dynamorio>\/build/\"\{$DA_ROOT\/deps\/dynamorio\/build\}\"/g' iftracer/CMakeLists.txt
sed -i 's/<path_to_dynamorio>\/build/\"\{$DA_ROOT\/deps\/dynamorio\/build\}\"/g' ifLineTracer/CMakeLists.txt
cd "$DA_ROOT/scripts/iftracer/iftracer"
cmake CMakeLists.txt
make
cd ../ifLineTracer
cmake CMakeLists.txt
make
