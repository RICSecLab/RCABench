# Data Augmentation

Data augmentation is the process of generating new crashing and non-crashing inputs from a given crashing inputs and is the first step in RCA. The generated inputs are used as a dataset for feature extraction.

## List of currently available methods

Currently, RCABench supports two types of data augmentation methods as listed in the table below. If you want to add a new method, follow the instructions in ["How to add a new data augmentatio method"](#how-to-add-a-new-data-augmentatio-method).

| Method | Description |
| ---- | ---- |
| AFLcem | AFLCem is a data augmentation method in [Aurora [USENIX Security'20]](https://www.usenix.org/conference/usenixsecurity20/presentation/blazytko). Aurora uses the crash exploration mode provided by AFL, a typical coverage-guided fuzzer. For more information on crash exploration mode, read the blog post [afl-fuzz: crash exploration mode.](https://lcamtuf.blogspot.com/2014/11/afl-fuzz-crash-exploration-mode.html) |
| ConcFuzz | ConcFuzz is a data augmentation method in [VulnLoc [ASIA CCS'21]](https://dl.acm.org/doi/10.1145/3433210.3437528). VulnLoc proposed ConcFuzz, a directed fuzzer that efficiently generates inputs that exercise execution paths in the neighbourhood of the path taken by a given crash input. |

## How to add a new data augmentation method

To add a new data augmentation method to RCABench, follow the three steps below.

### 1. Create a directory

First, create a subdirectory under the `data_augmentation` directory. The name of this subdirectory will be treated by RCABench as the name of the newly added data augmentation method. It is recommended that this name contains only alphanumeric characters and underscores.

For example, the `AFLcem` directory is already under the `data_augmentation` directory for the AFL crash exploration mode. Prepare a new folder at the same level as this directory.

### 2. Create files

The next step is to create the necessary files to run the new data augmentation methods. These files are placed in the directory created in the first step. For a concrete example, look inside the [data_augmentation/AFLcem](./methods/AFLcem/) folder.

Follow the instructions below to create the necessary files.

#### `preinstall.sh`

This file specifies the commands to install the packages needed to build and run your data augmentation method. It needs to be written as a bash script. The script is also run as administrator privilege in the [Dockerfile](./Dockerfile).

Basically, you can use the following example to create this file. As shown in the example, you can use the `apt install` or `pip install` commands to install the packages you need. To use this example in practice, rewrite the `<PACKAGES>`.

```bash
#!/bin/bash
set -eux

# Install required packages by apt
apt install -y <PACKAGES>

# Install required packages by pip.
pip install <PACKAGES>
```

For more concrete examples, see [preinstall.sh](./methods/AFLcem/preinstall.sh) used in AFLcem and [preinstall.sh](./methods/ConcFuzz/preinstall.sh) used in ConcFuzz.

#### `build.sh`

This file specifies the command to download and build your data augmentation method. It needs to be written as a bash script. Also, because this script runs as non-root in the [Dockerfile](./Dockerfile), any work that requires administrative privileges must be done in the `preinstall.sh` explained in the previous step.

Basically, you can use the following example to create this file, which consists of three steps:

1. The working directory is changed to `$DA_ROOT`. `$DA_ROOT` is an environment variable that is set in the [Dockerfile](./Dockerfile). You can place the files needed for the data augmentation method in this directory.

2. Download the files needed to build your data augmentation method. If the new method is managed by GitHub or similar, you can use the `git clone` command as shown in the example, replacing the `<URL>` with the appropriate one. Alternatively, if the method is managed by another hosting service, you can download it using a command such as `wget`.

3. Build the data augmentation method. If the newly added method is written in a language that requires compilation, such as C/C++, replace `<BUILD_COMMAND>` with the appropriate command according to the project's build instructions. On the other hand, if the method is written in Python or other languages, this step may not be necessary.

```bash
#!/bin/bash
set -eux

# Move to the directory for data augmentation
cd "${DA_ROOT}"

# Download your data augmentation method
git clone <URL>

# Build your data augmentation method
<BUILD_COMMAND>
```

For more concrete examples, see [build.sh](./methods/AFLcem/build.sh) used in AFLcem and [build.sh](./methods/ConcFuzz/build.sh) used in ConcFuzz.

#### `config.sh`

This file specifies the initialisation process when the shell is started. It needs to be written as a bash script. This script is also set up in the [Dockerfile](./Dockerfile) to be called when the shell is initialised.

Basically, you can use the following example to create this file.

```bash
#!/bin/bash

export PATH="${DA_ROOT}/<PROGRAM_PATH>:${PATH}"
```

For more concrete examples, see [build.sh](./methods/AFLcem/build.sh) used in AFLcem and [build.sh](./methods/ConcFuzz/build.sh) used in ConcFuzz.

#### `target_build.sh`

This file specifies the compile options and other options for building the target for each method.

```bash
#!/bin/bash
set -eu

if [ $# -lt 1 ]; then
  echo "Usage: $0 /path/to/build.sh" 1>&2
  exit 1
fi

# Build the first binary
TARGET_DEF_LDFLAGS="-fsanitize=address -no-pie" \
TARGET_DEF_CFLAGS="-fsanitize=address -ggdb -no-pie" \
TARGET_DEF_CXXFLAGS="-fsanitize=address  -ggdb -no-pie" \
$1 <FIRST_BINARY_DIR>

# Build the second binary
TARGET_DEF_LDFLAGS="-no-pie" \
TARGET_DEF_CFLAGS="-ggdb -no-pie" \
TARGET_DEF_CXXFLAGS="-ggdb -no-pie" \
$1 <SECOND_BINARY_DIR>
```

For more concrete examples, see [target_build.sh](./methods/AFLcem/target_build.sh) used in AFLcem and [target_build.sh](./methods/ConcFuzz/target_build.sh) used in ConcFuzz.

#### `src/run.sh`

This file specifies the command to run your data augmentation method. It needs to be written as a bash script. Basically, you can use the following example to create this file. You must rewrite `<DA_COMMAND>` and `<DA_ARGS>` according to your data augmentation method. The following parameters are available at run time. See the variable definitions at the top of the script below to set `<DA_ARGS>`.


In addition, the output of the data augmentation must conform to the interface defined by RCABench. If your data augmentation is not compliant, you can add a script that converts the data for that interface, to the `src` directory and run it in `run.sh`. We have added such a conversion process for AFLcem and ConcFuzz.

Finally, copy the generated data to `$SHARED/data`. This data will later be shared with the feature extraction methods.

```bash
#!/bin/bash
set -eux

TIMEOUT=${DA_MAX_TIMEOUT}
TARGET_BIN=${TARGET_ROOT}/<FIRST_BINARY_DIR/SECOND_BINARY_DIR>/${RELPATH}
TARGET_BIN_ARGS=${ARGS}

mkdir -p ${WORKDIR}/seeds
cp ${TARGET_ROOT}/seeds/${DA_SEED} ${WORKDIR}/seeds

# Run your data augmentation method
<DA_COMMAND> <DA_ARGS>

# (Optional) Convert output
# <CONVERT_COMMAND>

# Copy data from $WORKDIR to $SHARED
mkdir ${SHARED}/data
cp -r ${WORKDIR}/. ${SHARED}/data
```

For more concrete examples, see [src/run.sh](./methods/AFLcem/src/run.sh) and [src/convert.py](./methods/AFLcem/src/convert.py) used in AFLcem, and [src/run.sh](./methods/ConcFuzz/src/run.sh) and [src/convert.py](./methods/ConcFuzz/src/convert.py) used in ConcFuzz.

### 3. Test your method
