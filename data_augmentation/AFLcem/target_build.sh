#/bin/bash
set -eu

. ${TARGET_ROOT}/config.sh

if [ $# -lt 1 ]; then
  echo "Usage: $0 /path/to/build.sh" 1>&2
  exit 1
fi

# TODO: Run a custom build script for a specific target, if it exists.
AFL_USE_ASAN=1 \
TMP_LDFLAGS="-fsanitize=address" \
TMP_CFLAGS="-fsanitize=address -static -ggdb -no-pie" \
TMP_CXXFLAGS="-fsanitize=address -static -ggdb -no-pie" \
TMP_CC=${DA_ROOT}/afl-fuzz/afl-gcc \
TMP_CXX=${DA_ROOT}/afl-fuzz/afl-g++ \
$1 aflcem_target

ORIG=${TARGET_ROOT}/aflcem_target/${RELPATH}
cp ${ORIG} ${WORKDIR}/`basename ${ORIG}`_fuzz
