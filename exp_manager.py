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

    if not "exp_name" in config.keys():
        logging.error("No exp_name in {}".format(fname))
        sys.exit(1)
    if not "seed" in config.keys():
        config["seed"] = "default"
    if not "name" in config["DA"].keys():
        config["DA"]["name"] = None

    return config

def exec_DA(exp_name, DA, target, max_timeout, res_path, seed):
    if os.path.exists(res_path):
        logging.error("DA: Result already exists.")
        sys.exit(1)

    env = os.environ.copy()
    env["DA"] = DA
    env["TARGET_ID"] = target
    res = subprocess.run("data_augmentation/container_build.sh", env=env)
    if res.returncode != 0:
        logging.error("DA container_build.sh failed")
        sys.exit(1)

    os.makedirs(res_path)
    env["DA_MAX_TIMEOUT"] = str(max_timeout)
    env["DA_SEED"] = seed
    env["DA_OUTPUT"] = res_path
    res = subprocess.run("data_augmentation/container_run.sh", env=env)
    if res.returncode != 0:
        logging.error("DA container_run.sh failed")
        sys.exit(1)

def exec_FE(exp_name, FE, target, da_timeout, da_path, base_path):
    fe_path = base_path + "/" + str(da_timeout)

    if not os.path.exists(da_path):
        logging.error("FE: Not Found: DA Result ")
        sys.exit(1)

    os.makedirs(base_path, exist_ok=True)
    os.makedirs(fe_path)
    env = os.environ.copy()
    env["FE"] = FE
    env["TARGET_ID"] = target
    env["DA_TIMEOUT"] = str(da_timeout)
    env["DA_RESULT"] = da_path
    env["FE_OUTPUT"] = fe_path
    res = subprocess.run("feature_extraction/container_build.sh", env=env)
    if res.returncode != 0:
        logging.error("FE: container_build.sh failed")
        sys.exit(1)

    res = subprocess.run("feature_extraction/container_run.sh", env=env)
    if res.returncode != 0:
        logging.error("FE: container_run.sh failed")
        sys.exit(1)

def run(config):

    if config["DA"]["name"] is not None:
        exec_DA(config["exp_name"],
                config["DA"]["name"],
                config["target_id"],
                max(config["time"]),
                config["DA"]["output"],
                config["seed"])

    if not "FE" in config.keys():
        sys.exit(0)

    for da_timeout in config["time"]:
        exec_FE(config["exp_name"],
                config["FE"]["name"],
                config["target_id"],
                da_timeout,
                config["DA"]["output"],
                config["FE"]["output"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    args = parser.parse_args()

    run(parse_config(args.config))
