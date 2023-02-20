#!/bin/bash
set -eu

. ${TARGET_ROOT}/config.sh

if [ $# -lt 1 ]; then
  echo "Usage: $0 /path/to/build.sh" 1>&2
  exit 1
fi

# Run a custom build script for a specific target, if it exists.
if [ -d ${DA_ROOT}/targets/${TARGET_ID} ]; then
  if [[ "`cat ${DA_ROOT}/targets/${TARGET_ID}/target.yaml | tr -d ' ' | grep 'run_build_sh:' | cut -d ':' -f2 `" =~ "true" ]]; then
    TARGET_BUILD_FLAG=true
  else
    TARGET_BUILD_FLAG=false
  fi
  ${DA_ROOT}/targets/${TARGET_ID}/prebuild.sh
else
  TARGET_BUILD_FLAG=true
fi

if $TARGET_BUILD_FLAG; then
  AFL_USE_ASAN=1 \
  TARGET_DEF_LDFLAGS="-fsanitize=address" \
  TARGET_DEF_CFLAGS="-fsanitize=address -ggdb -no-pie" \
  TARGET_DEF_CXXFLAGS="-fsanitize=address -ggdb -no-pie" \
  TARGET_DEF_CC=${DA_ROOT}/afl-fuzz/afl-gcc \
  TARGET_DEF_CXX=${DA_ROOT}/afl-fuzz/afl-g++ \
  $1 aflcem_target
fi

ORIG=${TARGET_ROOT}/aflcem_target/${RELPATH}
cp ${ORIG} ${WORKDIR}/`basename ${ORIG}`_fuzz
