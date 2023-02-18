#!/bin/python3
import yaml
import argparse
import os
import subprocess
import sys
import logging
import exp_manager

def parse_args(args):
    config = {}
    config["exp_name"] = args.exp_name
    config["target_id"] = args.target_id
    config["DA"] = {}
    config["DA"]["name"] = args.da
    config["FE"] = {}
    config["FE"]["name"] = args.fe
    config["time"] = list(map(int,args.time))
    config["seed"] = args.seed

    return config, args.da_output, args.fe_output

def run(config):
    exp_manager.run(config)

def do_exp(orig_config, da_output, fe_output, num):
    if num is None:
        config = orig_config
        config["DA"]["output"] = da_output
        config["FE"]["output"] = fe_output
        run(config)
    else:
        for i in range(num):
            config = orig_config
            config["DA"]["output"] = da_output+"_{}".format(i)
            config["FE"]["output"] = fe_output+"_{}".format(i)
            run(config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--da", required=True)
    parser.add_argument("--fe", required=True)
    parser.add_argument("--da_output", required=True)
    parser.add_argument("--fe_output", required=True)
    parser.add_argument("--exp_name", required=True)
    parser.add_argument("--target_id", required=True)
    parser.add_argument("--time",  nargs='+', required=True)
    parser.add_argument("--seed", default="default", required=False)
    parser.add_argument("--num", type=int)
    args = parser.parse_args()

    do_exp(*parse_args(args), args.num)
