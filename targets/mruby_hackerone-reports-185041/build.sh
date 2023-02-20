#!/bin/bash
set -eu

. ${TARGET_ROOT}/config.sh

if [ $# -lt 1 ]; then
  echo "Usage: $0 <build dir name>" 1>&2
  exit 1
fi

cd $TARGET_ROOT

git clone https://github.com/mruby/mruby.git $1
cd ${TARGET_ROOT}/$1
git checkout 88604e39ac9c25ffdad2e3f03be26516fe866038

for var in "${!TARGET_DEF_@}"; do
  eval export "${var#TARGET_DEF_}"="$(printf "%q" "${!var}")"
done

make -e -j$((`nproc`+1))
