#!/bin/bash
set -eu

abs_start=`date +%s`
abstraction_layer.sh
abs_end=`date +%s`

fe_start=`date +%s`
fe.sh
fe_end=`date +%s`

check_start=`date +%s`
output.sh
check_end=`date +%s`

echo $((${abs_end} - ${abs_start})) > ${SHARED}/abs_time
echo $((${fe_end} - ${fe_start})) > ${SHARED}/fe_time
echo $((${check_end} - ${check_start})) > ${SHARED}/check_time
