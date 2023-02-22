#!/bin/bash
set -eu

. ${TARGET_ROOT}/config.sh

if [ $# -lt 1 ]; then
  echo "Usage: $0 /path/to/build.sh" 1>&2
  exit 1
fi

# TODO: Run a custom build script for a specific target, if it exists.
TARGET_DEF_CFLAGS="-ggdb -O0" \
TARGET_DEF_CXXFLAGS="-ggdb -O0" \
$1 aurorafe_target

ORIG=${TARGET_ROOT}/aurorafe_target/${RELPATH}
cp ${ORIG} ${WORKDIR}/`basename ${ORIG}`_trace
