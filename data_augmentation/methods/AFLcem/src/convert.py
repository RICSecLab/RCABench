#!/bin/python3
import glob
import datetime
import sys
import pathlib
import shutil
import hashlib
import os
import json

OUTPUT = os.environ["SHARED"]

seed_path = "/workdir/seeds/" + os.environ["DA_SEED"]

result = dict()
result["inputs"] = list()
result["max_timeout"] = os.environ["DA_MAX_TIMEOUT"]

offset = datetime.datetime.fromisoformat(sys.argv[1])

os.makedirs(OUTPUT+"/inputs")

def gen_name(fname, prefix=""):
    sha1 = hashlib.sha1()
    with open(fname, 'rb') as f:
        data = f.read()
        sha1.update(data)
    return prefix + sha1.hexdigest()

# seed
shutil.copy(seed_path, OUTPUT + "/inputs/" + "seed")
result["seed"] = "seed"

# crashes
for f in glob.glob("/workdir/queue/id*"):
    if "orig" in f:
        # seed
        t = 0
    else:
        p = pathlib.Path(f)
        t = (datetime.datetime.fromtimestamp(p.stat().st_mtime).astimezone() - offset).total_seconds()
    n = gen_name(f, prefix="q")
    shutil.copy(f, OUTPUT + "/inputs/" + n)
    result["inputs"].append({"tag": "crash", "path":n, "time": t, "info": []})

# non crashes
for f in glob.glob("/workdir/non_crashes/id*"):
    p = pathlib.Path(f)
    t = (datetime.datetime.fromtimestamp(p.stat().st_mtime).astimezone() - offset).total_seconds()
    n = gen_name(f, prefix="n")
    shutil.copy(f, OUTPUT + "/inputs/" + n)
    result["inputs"].append({"tag": "non_crash", "path":n, "time": t, "info": []})

with open(OUTPUT+'/result.json', 'w') as f:
    json.dump(result, f)
