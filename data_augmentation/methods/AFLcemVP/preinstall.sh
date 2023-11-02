#!/bin/bash
set -eux

# setup apt repository for llvm-14
apt-get update
apt-get install -y \
    apt-utils \
    ca-certificates \
    wget
mkdir -p /etc/apt/keyrings
echo "deb [signed-by=/etc/apt/keyrings/llvm-snapshot.gpg.key] http://apt.llvm.org/focal/ llvm-toolchain-focal-14 main" > /etc/apt/sources.list.d/llvm.list
wget -qO /etc/apt/keyrings/llvm-snapshot.gpg.key https://apt.llvm.org/llvm-snapshot.gpg.key


# install dependencies for AFL++
# cf. https://github.com/AFLplusplus/AFLplusplus/blob/4.07c/docs/INSTALL.md
apt-get update
apt-get install -y \
    automake \
    build-essential \
    bison \
    cargo \
    cmake \
    flex \
    git \
    libglib2.0-dev \
    libgtk-3-dev \
    libpixman-1-dev \
    python3-dev \
    python3-setuptools
apt-get install -y lld-14 llvm-14 llvm-14-dev clang-14
apt-get install -y "gcc-$(gcc --version|head -n1|sed 's/\..*//'|sed 's/.* //')-plugin-dev" "libstdc++-$(gcc --version|head -n1|sed 's/\..*//'|sed 's/.* //')-dev"
apt-get install -y ninja-build

# for ASan
apt-get install -y libclang-rt-14-dev
