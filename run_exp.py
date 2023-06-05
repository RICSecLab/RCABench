#!/bin/python3
import argparse
import sys
import logging
import exp_manager


def parse_args(args):
    config = {}
    config["exp_name"] = args.exp_name
    config["target_id"] = args.target_id
    config["DA"] = {}
    config["DA"]["name"] = args.da
    if args.fe and args.fe_output:
        config["FE"] = {}
        config["FE"]["name"] = args.fe
    elif (args.fe and not args.fe_output) or \
            (not args.fe and args.fe_output):
        logging.error("Inconsistent arguments with FE")
        sys.exit(1)
    if not (args.fe or args.da):
        logging.error("Nothing to do?")
        sys.exit(1)
    config["time"] = list(map(int, args.time))
    config["seed"] = args.seed

    return config, args.da_output, args.fe_output


def run(config, build=True):
    exp_manager.run_single(config, build=build)


def do_exp(orig_config, da_output, fe_output, num):
    if num is None:
        config = orig_config
        if "DA" in config.keys():
            config["DA"]["output"] = da_output
        if "FE" in config.keys():
            config["FE"]["output"] = fe_output
        run(config)
    else:
        for i in range(num):
            config = orig_config
            if "DA" in config.keys():
                config["DA"]["output"] = da_output+"_{}".format(i)
            if "FE" in config.keys():
                config["FE"]["output"] = fe_output+"_{}".format(i)
            if i == 0:
                run(config, build=True)
            else:
                run(config, build=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--da", required=False)
    parser.add_argument("--fe", required=False)
    parser.add_argument("--da_output", required=True)
    parser.add_argument("--fe_output", required=False)
    parser.add_argument("--exp_name", required=True)
    parser.add_argument("--target_id", required=True)
    parser.add_argument("--time",  nargs='+', required=True)
    parser.add_argument("--seed", default="default", required=False)
    parser.add_argument("--num", type=int)
    args = parser.parse_args()

    do_exp(*parse_args(args), args.num)
