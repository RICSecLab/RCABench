#!/bin/bash
set -eu

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
  TARGET_DEF_LDFLAGS="-fsanitize=address -no-pie" \
  TARGET_DEF_CFLAGS="-fsanitize=address -ggdb -no-pie" \
  TARGET_DEF_CXXFLAGS="-fsanitize=address  -ggdb -no-pie" \
  $1 oracle_source

  TARGET_DEF_LDFLAGS="-no-pie" \
  TARGET_DEF_CFLAGS="-ggdb -no-pie" \
  TARGET_DEF_CXXFLAGS="-ggdb -no-pie" \
  $1 origin_source
fi
