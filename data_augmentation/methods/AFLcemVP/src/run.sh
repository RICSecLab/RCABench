#!/bin/bash
set -eux

AFLCEMVP_TIMEOUT="${DA_MAX_TIMEOUT}"
ORIG="${TARGET_ROOT}/aflcemvp_target/${RELPATH}"

mkdir -p "${WORKDIR}/default/seeds"
cp "${TARGET_ROOT}/seeds/${DA_SEED}" "${WORKDIR}/default/seeds"

T="$(date --iso-8601=seconds)"
timeout --preserve-status --foreground "${AFLCEMVP_TIMEOUT}" \
    "${DA_ROOT}/AFLplusplus/afl-fuzz" \
    -C \
    -m none \
    -i "${WORKDIR}/default/seeds" \
    -o "${WORKDIR}" \
    -- "${WORKDIR}/default/$(basename "$ORIG")_fuzz" ${ARGS}

python3 "${DA_ROOT}/src/convert.py" "$T"
mkdir "${SHARED}/data"
cp -r "${WORKDIR}/default/." "${SHARED}/data"
