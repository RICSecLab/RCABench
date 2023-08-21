#!/bin/bash
set -eux

#
# install dependencies for AFL++
#
apt-get update
apt-get install -y \
    build-essential \
    python3-dev \
    automake \
    cmake \
    git \
    flex \
    bison \
    libglib2.0-dev \
    libpixman-1-dev \
    python3-setuptools \
    cargo \
    libgtk-3-dev
# try to install llvm 14 and install the distro default if that fails
apt-get install -y lld-14 llvm-14 llvm-14-dev clang-14 || apt-get install -y lld llvm llvm-dev clang
apt-get install -y \
    "gcc-$(gcc --version|head -n1|sed 's/\..*//'|sed 's/.* //')-plugin-dev" \
    "libstdc++-$(gcc --version|head -n1|sed 's/\..*//'|sed 's/.* //')-dev"
