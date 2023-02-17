#/bin/bash
set -eu

if [ $# -lt 1 ]; then
  echo "Usage: $0 /path/to/build.sh" 1>&2
  exit 1
fi

# TODO: Run a custom build script for a specific target, if it exists.
TARGET_DEF_LDFLAGS="-fsanitize=address" \
TARGET_DEF_CFLAGS="-fsanitize=address -ggdb -no-pie" \
TARGET_DEF_CXXFLAGS="-fsanitize=address  -ggdb -no-pie" \
$1 oracle_source

TARGET_DEF_CFLAGS="-ggdb -no-pie" \
TARGET_DEF_CXXFLAGS="-ggdb -no-pie" \
$1 origin_source
