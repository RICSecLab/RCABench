#!/bin/bash
set -eux

cd ${WORKDIR}

cve_out_folder=`find ${WORKDIR}/output/ -maxdepth 1 -name 'output_*' -not -path '*/\.*' -type d | sed 's/^\.\///g'`
echo "Output Folder: $cve_out_folder"
# get the hash of the poc
target_fuzz_path="$cve_out_folder/fuzz.log"
echo $target_fuzz_path
poc_hash=`grep "PoC Hash" $target_fuzz_path | awk '{print $NF}'`

python ${FE_ROOT}/scripts/patchloc.py --config_file "$WORKDIR/config.ini" --tag $TARGET_ID --func calc --out_folder $cve_out_folder --poc_trace_hash $poc_hash --process_num 10 --show_num 10000

crash_result="./crash_result.log"
if [ -f $crash_result ]; then
    mv $crash_result $cve_out_folder
else
    echo "$crash_result not Found"
fi
