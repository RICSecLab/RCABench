#ref: https://github.com/VulnLoc/VulnLoc/blob/e1f607abea71db0eb57b41684f3dfae0ecee4321/code/fuzz.py
import argparse
import ConfigParser
import logging
import os
import utils
import numpy as np
from time import time
import string
from copy import deepcopy as dc
import hashlib
import shutil
import tracer
import itertools
from multiprocessing import Pool
import glob
import json

DefaultItems = ['trace_cmd', 'crash_cmd', 'poc', 'poc_fmt', 'folder', 'mutate_range']
OutFolder = ''
TmpFolder = ''
TraceFolder = ''

SeedPool = [] # Each element is in the fmt of [<process_tag>, <seed_content>]. <process_tag>: True (selected) / False (not selected)
SeedTraceHashList = []
ReportCollection = [] # Each element if in the fmt of [<trace_hash>, <tag>]. <tag>: m - malicious / b - benign
TraceHashCollection = []

def parse_args():
    parser = argparse.ArgumentParser(description="ConcFuzz")
    parser.add_argument('--config_file', dest='config_file', type=str, required=True,
                        help="The path of config file")
    parser.add_argument('--tag', dest='tag', type=str, required=True,
                        help="The corresponding CVE id")
    parser.add_argument('--verbose', dest='verbose', type=str, default='True',
                        help="Whether print out the debugging info")
    args = parser.parse_args()

    # check the validity of args
    config = ConfigParser.ConfigParser()
    config.read(args.config_file)
    if args.tag not in config.sections():
        raise Exception("ERROR: Please provide the configuration file for %s" % args.tag)
    # read & processing config file
    detailed_config = {}
    detailed_config['results_path'] = os.environ['DA_RESULT']
    detailed_config['da_timeout'] = os.environ['DA_TIMEOUT']
    for item in config.items(args.tag):
        if item[0] == 'folder':
            if not os.path.exists(item[1]):
                raise Exception("ERROR: The folder does not exist -> %s" % item[1])
            detailed_config[item[0]] = item[1]
        else:
            detailed_config[item[0]] = item[1].split(';')
    # check whether it contains all the required attributes
    if len(set(detailed_config.keys()) & set(DefaultItems)) != len(DefaultItems):
        raise Exception("ERROR: Missing required attributes in config.ini -> Required attributes: %s" % str(DefaultItems))
    # check poc & poc_fmt & mutate_range
    arg_num = len(detailed_config['poc'])
    if arg_num != len(detailed_config['poc_fmt']) and arg_num != len(detailed_config['mutate_range']):
        raise Exception("ERROR: Your defined poc is not matched with poc_fmt/mutate_range")
    processed_arg = []
    processed_fmt = [] # each element is in the fmt of [<type>, <start_idx>, <size>, <mutate_range>]
    for arg_no in range(arg_num):
        if detailed_config['poc_fmt'][arg_no] == 'bfile':
            if not os.path.exists(detailed_config['poc'][arg_no]):
                raise Exception("ERROR: Exploit file does not exist -> %s" % detailed_config['poc'][arg_no])
            content = utils.read_bin(detailed_config['poc'][arg_no])

            processed_fmt.append(['bfile', len(processed_arg), len(content), range(256)])
            processed_arg += content
        elif detailed_config['poc_fmt'][arg_no] == 'int':
            try:
                tmp = detailed_config['mutate_range'][arg_no].split('~')
                mutate_range = range(int(tmp[0]), int(tmp[1]))
            except:
                raise Exception('ERROR: Please check the value of mutate_range in your config file.')
            processed_fmt.append(['int', len(processed_arg), 1, mutate_range])
            processed_arg.append(int(detailed_config['poc'][arg_no]))
        elif detailed_config['poc_fmt'][arg_no] == 'float':
            try:
                tmp = detailed_config['mutate_range'][arg_no].split('~')
                mutate_range = list(np.arange(float(tmp[0]), float(tmp[1]), float(tmp[2])))
            except:
                raise Exception('ERROR: Please check the value of mutate_range in your config file.')
            processed_fmt.append(['float', len(processed_arg), 1, mutate_range])
            processed_arg.append(float(detailed_config['poc'][arg_no]))
        elif detailed_config['poc_fmt'][arg_no] == 'str':
            processed_fmt.append(['str', len(processed_arg), len(detailed_config['poc'][arg_no]), list(string.printable)])
            processed_arg += list(detailed_config['poc'][arg_no])
        else:
            raise Exception("ERROR: Unknown type of arguments -> %s" % detailed_config['poc_fmt'][arg_no])
    detailed_config['poc'] = processed_arg
    detailed_config['poc_fmt'] = processed_fmt
    detailed_config.pop('mutate_range')
    # process the optional args
    if 'tmp_filename_len' in detailed_config: # read the length of temperol filename
        utils.FileNameLen = int(detailed_config['tmp_filename_len'][0])
    # get all the replace idx in the cmd
    tmp = ';'.join(detailed_config['trace_cmd']).split('***')
    detailed_config['trace_cmd'] = []
    detailed_config['trace_replace_idx'] = []
    for id in range(len(tmp)):
        detailed_config['trace_cmd'].append(tmp[id])
        detailed_config['trace_cmd'].append('')
        detailed_config['trace_replace_idx'].append(2*id + 1)
    detailed_config['trace_cmd'] = detailed_config['trace_cmd'][:-1]
    detailed_config['trace_replace_idx'] = detailed_config['trace_replace_idx'][:-1]

    return args.tag, detailed_config, args.verbose

def init_log(tag, verbose, folder):
	global OutFolder, TmpFolder, TraceFolder
	OutFolder = os.path.join(folder, 'output_%d' % int(time()))
	if os.path.exists(OutFolder):
		raise Exception("ERROR: Output folder already exists! -> %s" % OutFolder)
	else:
		os.mkdir(OutFolder)
	TmpFolder = os.path.join(OutFolder, 'tmp')
	if not os.path.exists(TmpFolder):
		os.mkdir(TmpFolder)
	TraceFolder = os.path.join(OutFolder, 'traces')
	if not os.path.exists(TraceFolder):
		os.mkdir(TraceFolder)
	log_path = os.path.join(OutFolder, 'fuzz.log')
	if verbose == 'True':
		logging.basicConfig(filename=log_path, filemode='a+', level=logging.DEBUG,
							format="[%(asctime)s-%(funcName)s-%(levelname)s]: %(message)s",
							datefmt="%d-%b-%y %H:%M:%S")
	else:
		pass
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	console_fmt = logging.Formatter(fmt="[%(asctime)s-%(funcName)s-%(levelname)s]: %(message)s", datefmt="%d-%b-%y %H:%M:%S")
	console.setFormatter(console_fmt)
	logging.getLogger().addHandler(console)
	logging.info('Output Folder: %s' % OutFolder)
	logging.debug("CVE: %s" % tag)
	logging.debug("Config Info: \n%s" % '\n'.join(['\t%s : %s' % (key, config_info[key]) for key in config_info]))

def prepare_args(input_no, poc, poc_fmt):
	global TmpFolder
	# prepare the arguments
	arg_num = len(poc_fmt)
	arg_list = []
	for arg_no in range(arg_num):
		if poc_fmt[arg_no][0] == 'bfile': # write the list into binary file
			content = np.asarray(poc[poc_fmt[arg_no][1]: poc_fmt[arg_no][1]+poc_fmt[arg_no][2]]).astype(np.int)
			tmp_filepath = os.path.join(TmpFolder, 'tmp_%d' % input_no)
			utils.write_bin(tmp_filepath, content)
			arg_list.append(tmp_filepath)
		elif poc_fmt[arg_no][0] == 'int':
			arg_list.append(int(poc[poc_fmt[arg_no][1]]))
		elif poc_fmt[arg_no][0] == 'float':
			arg_list.append(float(poc[poc_fmt[arg_no][1]]))
		elif poc_fmt[arg_no][0] == 'str': # concatenate all the chars together
			arg_list.append(''.join(poc[poc_fmt[arg_no][1]: poc_fmt[arg_no][1]+poc_fmt[arg_no][2]]))
		else:
			raise Exception("ERROR: Unknown poc_fmt -> %s" % poc_fmt[arg_no][0])
	return arg_list

def prepare_cmd(cmd_list, replace_idx, arg_list):
	replaced_cmd = dc(cmd_list)
	arg_num = len(replace_idx)
	for arg_no in range(arg_num):
		replaced_cmd[replace_idx[arg_no]] = str(arg_list[arg_no])
	replaced_cmd = ''.join(replaced_cmd)
	replaced_cmd = replaced_cmd.split(';')
	return replaced_cmd

def calc_trace_hash(trace):
	trace_str = '\n'.join(trace)
	return hashlib.sha256(trace_str).hexdigest()

def just_trace(input_no, raw_args, poc_fmt, trace_cmd, trace_replace_idx):
	processed_args = prepare_args(input_no, raw_args, poc_fmt)
	cmd = prepare_cmd(trace_cmd, trace_replace_idx, processed_args)
	trace = tracer.ifTracer(cmd)
	trace_hash = calc_trace_hash(trace)
	return trace, trace_hash

def gen_report(input_no, raw_args, poc_fmt, trace_cmd, trace_replace_idx, crash_result):
	processed_args = prepare_args(input_no, raw_args, poc_fmt)
	trace_cmd = prepare_cmd(trace_cmd, trace_replace_idx, processed_args)
	trace = tracer.ifTracer(trace_cmd)
	trace_hash = calc_trace_hash(trace)
	return [input_no, trace, trace_hash, crash_result]

def read_da_results(res_path, da_timeout):
    with open(res_path+"/result.json","r") as f:
        data = json.load(f)

    cres = []
    nres = []
    for inp in data["inputs"]:
        if inp["tag"] == "crash" and inp["time"] <= da_timeout:
            cres.append(utils.read_bin(res_path+"/inputs/"+inp["path"]))
        elif inp["tag"] == "non_crash" and inp["time"] <= da_timeout:
            nres.append(utils.read_bin(res_path+"/inputs/"+inp["path"]))

    seed = utils.read_bin(res_path+"/inputs/"+data["seed"])
    return cres, nres, seed

def gen_concfuzz_output(config_info):
    global TraceHashCollection, ReportCollection, SeedPool, SeedTraceHashList, TraceFolder, TmpFolder

    pool = Pool(utils.ProcessNum)
    result_collection = [] # each element is in the fmt of [id, trace, trace_hash, crash_result, trace_diff_id]

    crash_inputs, non_crash_inputs,seed = read_da_results(config_info["results_path"], config_info["da_timeout"])

    trace, trace_hash = just_trace(0, seed, config_info['poc_fmt'], config_info['trace_cmd'], config_info['trace_replace_idx'])
    logging.debug('PoC Hash: %s' % trace_hash)
    seed_len = len(seed)
    # save the trace
    TraceHashCollection.append(trace_hash)
    path = os.path.join(TraceFolder, trace_hash)
    np.savez(path, trace=trace)
    # add the report
    ReportCollection.append([trace_hash, 'm'])
    # add into seed pool
    SeedPool.append([False, seed])
    SeedTraceHashList.append(trace_hash)
    logging.info('Finish processing the poc!')

    c_num = len(crash_inputs)
    for i,crash_input in enumerate(crash_inputs):
            pool.apply_async(
                    gen_report,
                    args = (i, crash_input, config_info['poc_fmt'], config_info['trace_cmd'], config_info['trace_replace_idx'], "m" ),
                    callback = result_collection.append
            )

    for i,non_crash_input in enumerate(non_crash_inputs):
            pool.apply_async(
                    gen_report,
                    args = (i+c_num, non_crash_input, config_info['poc_fmt'], config_info['trace_cmd'], config_info['trace_replace_idx'], "b"),
                    callback = result_collection.append
            )
    pool.close()
    pool.join()

    # Delete all the tmp files
    shutil.rmtree(TmpFolder)
    os.mkdir(TmpFolder)

    inputs = crash_inputs + non_crash_inputs
    for item in result_collection:
        # save the trace
        if item[2] not in TraceHashCollection:
                TraceHashCollection.append(item[2])
                trace_path = os.path.join(TraceFolder, item[2])
                np.savez(trace_path, trace=item[1])
        # check whether to add it into the seed pool
        if item[3] == 'm' and item[2] not in SeedTraceHashList:
                SeedPool.append([False, inputs[item[0]]])
                SeedTraceHashList.append(item[2])
        # Update reports
        if [item[2], item[3]] not in ReportCollection:
                ReportCollection.append([item[2], item[3]])

    # save all the remaining info
    report_filepath = os.path.join(OutFolder, 'reports.pkl')
    utils.write_pkl(report_filepath, ReportCollection)
    logging.debug("Finish writing all the reports!")

    seed_filepath = os.path.join(OutFolder, 'seeds.pkl')
    utils.write_pkl(seed_filepath, SeedPool)
    logging.debug("Finish writing all the seeds!")

    seed_hash_filepath = os.path.join(OutFolder, 'seed_hashes.pkl')
    utils.write_pkl(seed_hash_filepath, SeedTraceHashList)
    logging.debug("Finish writing all the hash of seeds!")
    logging.debug('Done!')

if __name__ == '__main__':
	tag, config_info, verbose = parse_args()
	init_log(tag, verbose, config_info['folder'])
	gen_concfuzz_output(config_info)
