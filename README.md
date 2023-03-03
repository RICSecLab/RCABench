# RCABench

RACBench is an end-to-end benchmarking platform for evaluating root cause analysis (RCA) techniques across various targeted programs.

## Overview

Several RCA techniques have been proposed to automatically analyse the causes of software crashes caused by bugs and vulnerabilities. However, the environment for comprehensive evaluation of existing RCA techniques is inadequate, making it difficult to analyse open challenges in the field of RCA. Therefore, we have developed RCABench, a benchmarking platform for automatic and comprehensive evaluation of different RCA techniques.

RCABench was developed as part of a paper accepted for NDSS BAR 2023. If you find our work interesting, please cite our paper.

```
@inproceedings{nishimura2023rcabench,
    title={{RCABench:} Open Benchmarking Platform for Root Cause Analysis},
    author={Keisuke Nishimura, Yuichi Sugiyama, Yuki Koike, Masaya Motoda, Tomoya Kitagawa, Toshiki Takatera, Yuma Kurogome},
    booktitle={NDSS Binary Analysis Research Workshop},
    year={2023}
}
```

## Getting started

### Prerequisites

This section explains how to set up your environment for RCABench.

#### Getting the code

Clone the RCABench repository to your machine by running the following commands:

```bash
git clone https://github.com/RICSecLab/RCABench
cd RCABench
```

#### Installing prerequisites

The following software must be installed to run RCABench.

- Docker
- Python3

RCABench basically runs in Docker containers. You will also need to run a simple Python script to set up the Docker environment.Their installation should be done according to the official documentation.

#### Environment

We only tested RCABench on x86_64 Ubuntu 20.04. Currently, it is not certain whether the experiment will work on other hardware or operating systems. It is recommended that you run RCABench in the same environment.

### Running an expriment

This section describes commands for running an RCA experiment. For clarity of explanation, this section specifically describes the commands for an experiment using [AFLcem](./data_augmentation/methods/AFLcem/), a data augmentation method, and [VulnLocFE ](./feature_extraction/methods/VulnLocFE/), a feature extraction method, for target [libtiff_cve-2016-10094](./targets/libtiff_cve-2016-10094/).

Of course, you can experiment with similar commands for other methods and targets. Please replace A, B and C in the commands below with your own experiments. You can see the targets and methods currently supported by RCABench at the following link.

- [List of targets](./targets/README.md#list-of-currently-available-methods)
- [List of data augmentation methods](./data_augmentation/README.md#list-of-currently-available-methods)
- [List of feature extraction methods](./feature_extraction/README.md#list-of-currently-available-methods)

The experiment consists of four main steps. Follow the instructions below and execute the commands in order.

#### 1. Create a directory

First, create a directory on the host machine to store the experiment results. RCABench runs RCA on the Docker container, but the artifacts of RCA (data augmentation results and final RCA results) are shared with the host machine.

For example, create a directory with the following command:

```bash
export RCABENCH_RESULTS="/tmp/rcabench_results"
mkdir -p ${RCABENCH_RESULTS}
```

By this command, a subdirectory `rcabench_results` is created under the `/tmp` directory, but this path can be changed for your environment. The path is also exported to the environment variable `RCABENCH_RESULTS` for easier access to the shared directory in later commands.

#### 2. Run a data augmentation method

Next, run AFLcem, a data augmentation method, with the following command:

```bash
python3 run_exp.py --da AFLcem --da_output ${RCABENCH_RESULTS}/da_output --exp_name test --target_id libtiff_cve-2016-10094 --time 10
```

This command specifies that the AFLcem is run for `10` seconds and that the results of the AFLcem are saved in `${RCABENCH_RESULTS}/da_output`. When this command is run, a docker image is created, a docker container is started, and AFLcem is run inside it.

When finished, the results are saved to the `${RCABENCH_RESULTS}/da_output` directory. In `{RCABENCH_RESULTS}/da_output/inputs` directory, the generated inputs are stored, and `${RCABENCH_RESULTS}/da_output/result.json` contains information about those inputs.

#### 3. Run a feature extraction

Next, using the results generated by the previous command, run VulnLocFE, a feature extraction method, with the following command:

```bash
python3 run_exp.py --fe VulnLocFE --da_output ${RCABENCH_RESULTS}/da_output --fe_output ${RCABENCH_RESULTS}/fe_output --exp_name test --target_id libtiff_cve-2016-10094 --time 10
```
This command specifies the `${RCABENCH_RESULTS}/da_output` directory as input and saves results in directory `{RCABENCH_RESULTS}/fe_output`. The option `--time 10` means that the feature extraction is performed using the input generated by data augmentation up to `10` seconds. You can use this option to run feature extraction for different data augmentation times using the results obtained from a single data augmentation run.

When this command is run, a docker image is created, a docker container is started, and AFLcem is run inside it. When finished, the results are saved to the `${RCABENCH_RESULTS}/fe_output` directory.

#### 4. Check results

Finally, check the RCA results with the following command:

```bash
cat {RCABENCH_RESULTS}/fe_output/10/fe_result.txt | grep loc_uniq | cut -d ":" -f2
```

RCABench automatically compares the results of feature extraction with a human-defined ground truth and outputs the number of candidates needed to estimate the correct root cause. A lower number indicates better results.

### Running an experiment with a config file

This section describes an easy way to run a experiment using a config file. The config file for an experiment on target A using AFLcem and VulnLocFE is as follows:

```yaml
exp_name: test
target_id: libtiff_cve-2016-10094
DA:
    name: AFLcem
    output: /tmp/rcabench_results/da_output
FE:
    name: VulnLocFE
    output: /tmp/rcabench_results/fe_output
time: [10, 100] # seconds
```

The config file is written in yaml format. The `output` key for DA and FE is the directory where the output results are stored. It can be changed according to your environment. In addition, the time key can control the time for data augmentation and feature extraction: data augmentation is performed up to the maximum value in the time list, and feature extraction is performed for all times in the time list, using only data generated up to that time.

After saving the above config file as `exp_config.yaml`, start the experiment with the following command:

```bash
python3 exp_manager.py exp_config.yaml
```

The final results are stored in the `/tmp/rcabench_results/fe_output` directory. See ["Check results"](#4-check-results) for how to read the results.

### Adding a new target and method

You can add new targets and methods to RCABench yourself. Please refer to the following document for instructions.

- [How to add a new target](./targets/README.md#how-to-add-a-new-target)
- [How to add a new data augmentation method](./data_augmentation/README.md#how-to-add-a-new-data-augmentation-method)
- [How to add a new feature extraction method](./feature_extraction/README.md#how-to-add-a-new-feature-extraction-method)

## Contributing

Please open GitHub Issues and Pull Requests.

## License

RCABench is released under the [Apache License, Version 2.0](https://opensource.org/licenses/Apache-2.0).

## Acknowledgements

This project has received funding from the Acquisition, Technology & Logistics Agency (ATLA) under the Innovative Science and Technology Initiative for Security 2020 (JPJ004596).
