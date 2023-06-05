#!/bin/bash
import os
import random
import yaml

random.seed()


def conv_args(args):
    return ";".join(args.replace("@@", "***").split())


with open(os.environ["DA_ROOT"]+"/crash_tags.yaml", "r") as f:
    ctags = yaml.safe_load(f)

config = """\
[{TARGET_ID}]
trace_cmd={TARGET_ROOT}/origin_source/{RELPATH};{ARGS}
crash_cmd={TARGET_ROOT}/oracle_source/{RELPATH};{ARGS}
bin_path={TARGET_ROOT}/origin_source/{RELPATH}
poc={TARGET_ROOT}/seeds/{SEED}
poc_fmt=bfile
mutate_range=default
folder=/workdir/output
rand_seed={RAND}
crash_tag={CTAG}
""".format(TARGET_ROOT=os.environ['TARGET_ROOT'],
           TARGET_ID=os.environ['TARGET_ID'],
           RELPATH=os.environ['RELPATH'],
           ARGS=conv_args(os.environ['ARGS']),
           RAND=random.randint(1, 1000),
           SEED=os.environ["DA_SEED"],
           CTAG=ctags[os.environ['TARGET_ID']])

with open(os.environ['WORKDIR']+"/config.ini", "w") as f:
    f.write(config)
