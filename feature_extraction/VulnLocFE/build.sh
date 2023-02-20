#!/bin/bash
set -eux

cd "${FE_ROOT}"

. ${FE_ROOT}/config.sh

git clone https://github.com/VulnLoc/VulnLoc ${VULNLOC_GIT_DIR}

cp ${VULNLOC_GIT_DIR}/code/patchloc.py ${FE_ROOT}/scripts
cp ${VULNLOC_GIT_DIR}/code/tracer.py ${FE_ROOT}/scripts
cp ${VULNLOC_GIT_DIR}/code/utils.py ${FE_ROOT}/scripts
cp ${VULNLOC_GIT_DIR}/code/parse_dwarf.py ${FE_ROOT}/scripts

export CMAKE_PREFIX_PATH="$FE_ROOT/deps/dynamorio/cmake"

cp -r ${VULNLOC_GIT_DIR}/code/iftracer.zip ${FE_ROOT}/scripts
cd "$FE_ROOT/scripts"
unzip iftracer.zip
cd "$FE_ROOT/scripts/iftracer"
sed -i 's/<path_to_dynamorio>\/build/\"\{$FE_ROOT\/deps\/dynamorio\/build\}\"/g' iftracer/CMakeLists.txt
sed -i 's/<path_to_dynamorio>\/build/\"\{$FE_ROOT\/deps\/dynamorio\/build\}\"/g' ifLineTracer/CMakeLists.txt
cd "$FE_ROOT/scripts/iftracer/iftracer"
cmake CMakeLists.txt
make
cd ../ifLineTracer
cmake CMakeLists.txt
make
