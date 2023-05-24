#!/bin/python3
import yaml
import argparse
import os
import subprocess
import sys
import logging
import time

#TODO: use schema for more readbable and safer validation...
def parse_and_validate_config_single(config):
    if not "name" in config["DA"].keys():
        config["DA"]["name"] = None

    return config

def parse_and_validate_config_multiple(config):
    # DA/FE.name must contain at least one DA/FE technique.

    def validation(key):
        if not key in config.keys():
            logging.error("No {} (multiple-mode)".format(key))
            return False
        if not isinstance(config[key],list):
            config[key] = [config[key]]
        if len(config[key]) == 0:
            logging.error("{k} must include at least one available {k} (multiple-mode)".format(k=key))
            return False
        return True

    def validation_w_name(key):
        if not "name" in config[key].keys():
            logging.error("No name key in {} (multiple-mode)".format(key))
            return False
        if not isinstance(config[key]["name"],list):
            config[key]["name"] = [config[key]["name"]]
        if len(config[key]["name"]) == 0:
            logging.error("name in {k} must include at least one available {k} (multiple-mode)".format(k=key))
            return False
        return True

    if not ( validation("target_id") ):
        sys.exit(1)

    if not ( validation_w_name("DA") and validation_w_name("FE") ):
        sys.exit(1)

    if not "repeat" in config.keys() or not int(config["repeat"]) >= 1:
        logging.error("repeat must be > 1 (multiple-mode)")
        sys.exit(1)

    config["repeat"] = int(config["repeat"])

    return config

def parse_and_validate_config(fname):
    with open(fname) as file:
        config = yaml.safe_load(file)

    if not "exp_name" in config.keys():
        logging.error("No exp_name key in {}".format(fname))
        sys.exit(1)
    if not "DA" in config.keys():
        logging.error("No DA key in {}".format(fname))
        sys.exit(1)
    if not "seed" in config.keys():
        config["seed"] = "default"

    if not "mode" in config.keys():
        config["mode"] = "single"

    if config["mode"] == "single":
        return parse_and_validate_config_single(config)
    elif config["mode"] == "multiple":
        return parse_and_validate_config_multiple(config)

    logging.error("Invalid mode: {}".format(config["mode"]))
    sys.exit(1)

def exec_DA(exp_name, DA, target, max_timeout, res_path, seed, build=True):
    if os.path.exists(res_path):
        logging.error("DA: Result already exists.")
        sys.exit(1)

    env = os.environ.copy()
    env["DA"] = DA
    env["TARGET_ID"] = target
    if build:
        res = subprocess.run("data_augmentation/container_build.sh", env=env)
        if res.returncode != 0:
            logging.error("DA container_build.sh failed")
            sys.exit(1)

    os.makedirs(res_path)
    env["DA_MAX_TIMEOUT"] = str(max_timeout)
    env["DA_SEED"] = seed
    env["DA_OUTPUT"] = res_path
    da_start_time = time.time()
    res = subprocess.run("data_augmentation/container_run.sh", env=env)
    da_end_time = time.time()
    with open(res_path+"/da_time_external.txt", "w") as f:
        f.write(str(int(da_end_time - da_start_time))+"\n")
    if res.returncode != 0:
        logging.error("DA container_run.sh failed")
        sys.exit(1)

def exec_FE(exp_name, FE, target, da_timeout, da_path, base_path, build=True):
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
    if build:
        res = subprocess.run("feature_extraction/container_build.sh", env=env)
        if res.returncode != 0:
            logging.error("FE: container_build.sh failed")
            sys.exit(1)

    res = subprocess.run("feature_extraction/container_run.sh", env=env)
    if res.returncode != 0:
        logging.error("FE: container_run.sh failed")
        sys.exit(1)

def run_single(config, build=True):

    if config["DA"]["name"] is not None:
        exec_DA(config["exp_name"],
                config["DA"]["name"],
                config["target_id"],
                max(config["time"]),
                config["DA"]["output"],
                config["seed"],
                build=build)

    if not "FE" in config.keys():
        sys.exit(0)

    for da_timeout in config["time"]:
        exec_FE(config["exp_name"],
                config["FE"]["name"],
                config["target_id"],
                da_timeout,
                config["DA"]["output"],
                config["FE"]["output"],
                build=build)

def run_multiple(config):
    opath = config["output"]
    os.makedirs(opath, exist_ok=True)

    da_path = opath + "/DA/"
    os.makedirs(da_path, exist_ok=True)

    fe_path = opath + "/FE/"
    os.makedirs(fe_path, exist_ok=True)

    for da in config["DA"]["name"]:
        for target in config["target_id"]:
            for r in range(config["repeat"]):
                da_res = da_path + "/" + da + "/" + target + "/" + str(r) + "/"
                exec_DA(config["exp_name"],
                        da,
                        target,
                        max(config["time"]),
                        da_res,
                        config["seed"],
                        build= (True if r == 0 else False))

    for fe in config["FE"]["name"]:
        for da in config["DA"]["name"]:
            for target in config["target_id"]:
                for r in range(config["repeat"]):
                    d = da + "/" + target + "/" + str(r) + "/"
                    da_res = da_path + "/" + d
                    fe_res = fe_path + "/" + fe + "/" + d

                    for i, da_timeout in enumerate(config["time"]):
                        exec_FE(config["exp_name"],
                                fe,
                                target,
                                da_timeout,
                                da_res,
                                fe_res,
                                build=(True if r == 0 and i == 0 else False))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    args = parser.parse_args()

    config = parse_and_validate_config(args.config)

    assert(config["mode"] in ["single", "multiple"])

    if config["mode"] == "single":
        run_single(config)
    elif config["mode"] == "multiple":
        run_multiple(config)
