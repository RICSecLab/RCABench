#!/bin/bash
set -eux

apt-get update -y
# for python2
apt-get install -y software-properties-common
add-apt-repository universe
apt-get update -y
apt-get install -y build-essential git vim unzip python-dev python2 wget libssl-dev g++-multilib doxygen transfig imagemagick ghostscript zlib1g-dev curl python3-pip

mkdir -p "$DA_ROOT/deps"
cd "$DA_ROOT/deps"

# pip2 install
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
python get-pip.py
rm ./get-pip.py

# install ipython, setuptools, pyelftools
pip install ipython
pip install setuptools
pip install pyelftools
pip install numpy==1.16.6

cd "$DA_ROOT/deps"
# install cmake for dynamorio
wget https://github.com/Kitware/CMake/releases/download/v3.16.2/cmake-3.16.2.tar.gz
tar -xvzf cmake-3.16.2.tar.gz
rm cmake-3.16.2.tar.gz
mv cmake-3.16.2 cmake
cd ./cmake
./bootstrap
make
make install
cd "$DA_ROOT/deps"

# install dynamorio
wget https://github.com/DynamoRIO/dynamorio/releases/download/release_9.0.0/DynamoRIO-Linux-9.0.0.tar.gz
tar -xvzf DynamoRIO-Linux-9.0.0.tar.gz
rm ./DynamoRIO-Linux-9.0.0.tar.gz
mv DynamoRIO-Linux-9.0.0 dynamorio


pip3 install pyyaml
