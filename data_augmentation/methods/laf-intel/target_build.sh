#!/bin/bash
set -eu

. "${TARGET_ROOT}/config.sh"

if [ $# -lt 1 ]; then
    echo "Usage: $0 /path/to/build.sh" 1>&2
    exit 1
fi

#
# run a custom build script for a specific target, it it exists.
#
if [ -d "${DA_ROOT}/targets/${TARGET_ID}" ]; then
    if [[ $(tr -d ' ' < "${DA_ROOT}/targets/${TARGET_ID}/target.yaml" | grep 'run_build_sh:' | cut -d ':' -f2) =~ "true" ]]; then
        TARGET_BUILD_FLAG=true
    else
        TARGET_BUILD_FLAG=false
    fi
    "${DA_ROOT}/targets/${TARGET_ID}/prebuild.sh"
else
    TARGET_BUILD_FLAG=true
fi

if $TARGET_BUILD_FLAG; then
    AFL_LLVM_LAF_ALL=1 \
    AFL_USE_ASAN=1 \
    TARGET_DEF_LDFLAGS="-fsanitize=address -no-pie" \
    TARGET_DEF_CFLAGS="-fsanitize=address -ggdb" \
    TARGET_DEF_CXXFLAGS="-fsanitize=address -ggdb" \
    TARGET_DEF_CC="${DA_ROOT}/AFLplusplus/afl-clang-fast" \
    TARGET_DEF_CXX="${DA_ROOT}/AFLplusplus/afl-clang-fast++" \
    $1 laf-intel_target
fi

ORIG="${TARGET_ROOT}/laf-intel_target/${RELPATH}"
mkdir -p "${WORKDIR}/default/"
cp "$ORIG" "${WORKDIR}/default/$(basename "$ORIG")_fuzz"
