#/bin/bash
set -eux

# Dependencies
## XXX: this section should be in preinstall.sh?
## But installing rust and pin with root makes some troubles...
mkdir -p "${FE_ROOT}/deps"
cd "${FE_ROOT}/deps"

## GDB Enhanced Features
## https://github.com/RUB-SysSec/aurora/blob/master/docker/Dockerfile#L24
wget -O ~/.gdbinit-gef.py -q https://gef.blah.cat/sh \
  && echo source ~/.gdbinit-gef.py >> ~/.gdbinit

## Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain nightly
export PATH="$HOME/.cargo/bin:$PATH"

## Intel Pin
wget -U "" -c http://software.intel.com/sites/landingpage/pintool/downloads/pin-3.15-98253-gb56e429b1-gcc-linux.tar.gz
tar -xzf pin*.tar.gz

# Aurora Setup
AURORA_GIT_DIR="${FE_ROOT}/aurora"
git clone https://github.com/RUB-SysSec/aurora.git ${AURORA_GIT_DIR}

# Build aurora_tracer.so
export PIN_ROOT="${FE_ROOT}/deps/pin-3.15-98253-gb56e429b1-gcc-linux"
mkdir -p "${PIN_ROOT}/source/tools/AuroraTracer"
cp -r ${AURORA_GIT_DIR}/tracing/* ${PIN_ROOT}/source/tools/AuroraTracer
cd ${PIN_ROOT}/source/tools/AuroraTracer
make obj-intel64/aurora_tracer.so

# Build RCA tools
cd ${AURORA_GIT_DIR}/root_cause_analysis
cargo build -j 1 --release --bin monitor
cargo build -j 1 --release --bin rca
