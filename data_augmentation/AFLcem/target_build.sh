#/bin/bash
set -eu

. ${TARGET_ROOT}/config.sh

if [ $# -lt 1 ]; then
  echo "Usage: $0 /path/to/build.sh" 1>&2
  exit 1
fi

# TODO: Run a custom build script for a specific target, if it exists.
AFL_USE_ASAN=1 \
TARGET_DEF_LDFLAGS="-fsanitize=address" \
TARGET_DEF_CFLAGS="-fsanitize=address -static -ggdb -no-pie" \
TARGET_DEF_CXXFLAGS="-fsanitize=address -static -ggdb -no-pie" \
TARGET_DEF_CC=${DA_ROOT}/afl-fuzz/afl-gcc \
TARGET_DEF_CXX=${DA_ROOT}/afl-fuzz/afl-g++ \
$1 aflcem_target

ORIG=${TARGET_ROOT}/aflcem_target/${RELPATH}
cp ${ORIG} ${WORKDIR}/`basename ${ORIG}`_fuzz
