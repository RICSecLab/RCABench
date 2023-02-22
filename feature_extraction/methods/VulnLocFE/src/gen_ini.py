#!/bin/bash
import os
import json

da_result = os.environ['DA_RESULT']

with open(da_result+"/result.json","r") as f:
    data = json.load(f)

def conv_args(args):
    return ";".join(args.replace("@@","***").split())

config = """\
[{TARGET_ID}]
trace_cmd=/target/origin_source/{RELPATH};{ARGS}
crash_cmd=/target/oracle_source/{RELPATH};{ARGS}
bin_path=/target/origin_source/{RELPATH}
poc={DA_RESULT}/inputs/{seed}
poc_fmt=bfile
mutate_range=default
folder=/workdir/output
""".format(TARGET_ID=os.environ['TARGET_ID'],
           RELPATH=os.environ['RELPATH'],
           ARGS=conv_args(os.environ['ARGS']),
           DA_RESULT=da_result,
           seed=data["seed"])

with open(os.environ['WORKDIR']+"/config.ini", "w") as f:
    f.write(config)
