#!/bin/python3
import yaml
import argparse
import os
import subprocess
import sys
import logging

def parse_config(fname):
    with open(fname) as file:
        config = yaml.safe_load(file)

    if not "seed" in config.keys():
        config["seed"] = "default"

    return config

def exec_DA(DA, target, max_timeout, res_path, seed):
    os.makedirs(res_path, exist_ok=True)
    env = os.environ.copy()
    env["DA"] = DA
    env["TARGET_ID"] = target
    env["DA_MAX_TIMEOUT"] = str(max_timeout)
    env["DA_SEED"] = seed
    env["DA_OUTPUT"] = res_path
    res = subprocess.run("data_augmentation/container_build.sh", env=env)
    if res.returncode != 0:
        logging.error("DA build.sh failed")
        sys.exit(1)

    res = subprocess.run("data_augmentation/container_run.sh", env=env)
    if res.returncode != 0:
        logging.error("DA run.sh failed")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    args = parser.parse_args()

    config = parse_config(args.config)

    exec_DA(config["DA"]["name"],
            config["target_id"],
            max(config["time"]),
            config["DA"]["output"],
            config["seed"])
