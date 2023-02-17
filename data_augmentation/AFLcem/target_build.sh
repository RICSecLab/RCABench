#/bin/bash
set -eu

. ${TARGET_ROOT}/config.sh

if [ $# -lt 1 ]; then
  echo "Usage: $0 /path/to/build.sh" 1>&2
  exit 1
fi

# TODO: Run a custom build script for a specific target, if it exists.
AFL_USE_ASAN=1 \
LDFLAGS="-fsanitize=address" \
CFLAGS="-fsanitize=address -static -ggdb -no-pie" \
CXXFLAGS="-fsanitize=address -static -ggdb -no-pie" \
CC=${DA_ROOT}/afl-fuzz/afl-gcc \
CXX=${DA_ROOT}/afl-fuzz/afl-g++ \
$1 aflcem_target

ORIG=${TARGET_ROOT}/aflcem_target/${RELPATH}
cp ${ORIG} ${WORKDIR}/`basename ${ORIG}`_fuzz
