#!/bin/python3
import os
import json
import shutil

da_result = os.environ['DA_RESULT']
workdir = os.environ['WORKDIR']
timeout = int(os.environ['DA_TIMEOUT'])

crash_dir = workdir+"/inputs/crashes"
non_crash_dir = workdir+"/inputs/non_crashes"

with open(da_result+"/result.json","r") as f:
    data = json.load(f)

os.makedirs(crash_dir, exist_ok=True)
os.makedirs(non_crash_dir, exist_ok=True)

for inp in data["inputs"]:
    if inp["tag"] == "crash" and inp["time"] <= timeout:
        shutil.copy(da_result+"/inputs/"+inp["path"], crash_dir)

    elif inp["tag"] == "non_crash" and inp["time"] <= timeout:
        shutil.copy(da_result+"/inputs/"+inp["path"], non_crash_dir)
