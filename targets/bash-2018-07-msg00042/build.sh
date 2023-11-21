#!/bin/bash

. ${TARGET_ROOT}/config.sh

if [ $# -lt 1 ]; then
  echo "Usage: $0 <build dir name>" 1>&2
  exit 1
fi

cd $TARGET_ROOT
# Since there is no tag named 'bash-4.4.23' in git repo, follow from 'bash-5.0' tag.
git clone --branch bash-5.0 --depth 2 https://git.savannah.gnu.org/git/bash.git  $1
cd ${TARGET_ROOT}/$1
git checkout 64447609994bfddeef1061948022c074093e9a9f

TARGET_DEF_CFLAGS="${TARGET_DEF_CFLAGS-}"
TARGET_DEF_CXXFLAGS="${TARGET_DEF_CXXFLAGS-}"

ARGS=""
for var in "${!TARGET_DEF_@}"; do
  ARGS="${ARGS} ${var#TARGET_DEF_}=\"$(echo ${!var})\""
done
set -o xtrace
echo ${ARGS}
eval ./configure ${ARGS} --with-static-link --without-bash-malloc 
eval make -j$(nproc)

#set +e
#./bash < ../poc1
#./bash < ../poc2
