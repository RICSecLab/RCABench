#!/bin/bash
. ${TARGET_ROOT}/config.sh


cd $TARGET_ROOT

git clone https://github.com/mruby/mruby.git aflcem_target
cd $TARGET_ROOT/aflcem_target
git checkout 88604e39ac9c25ffdad2e3f03be26516fe866038
CC=${DA_ROOT}/afl-fuzz/afl-gcc make -e -j$((`nproc`+1))
