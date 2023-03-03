# Targets

## List of currently available methods

Currently, RCABench supports the seven targets listed in the table below.Each target is a program that contains a bug or vulnerability. If you want to add a new method, follow the instructions in [How to add a new target](#how-to-add-a-new-target).

| | Program | ID | Root Cause | Crash Cause |
| ---- | ---- | ---- | ---- | ---- |
| [libtiff_cve-2016-10094](./libtiff_cve-2016-10094) | LibTIFF | CVE-2016-10094 | off-by-one error | heap buffer overflow |
| [libtiff_cve-2018-19664](./libjpeg_cve-2018-19664/) | Libjpeg | CVE-2018-19664 | incomplete check | heap buffer overflow |
| [libjpeg_cve-2017-15232](./libjpeg_cve-2017-15232/) | Libjpeg | CVE-2017-15232 | missing check | null pointer dereference |
| [libxml2_cve-2017-5969](./libxml2_cve-2017-5969/) | Libxml2 | CVE-2017-5969 | incomplete check | null pointer dereference |
| [mruby_hackerone-reports-185041](./mruby_hackerone-reports-185041/) | mruby | HackerOne 185041 | missing check | type confusion |
| [readelf_cve-2019-9077](./readelf_cve-2019-9077/) | readelf | CVE-2019-9077 | missing check | heap buffer overflow |
| [lua_cve-2019-6706/](./lua_cve-2019-6706/) | Lua | CVE-2019-6706 | missing check | use-after-free |

## How to add a new target

To add a new target to RCABench, follow the four steps below.

### 1. Create a directory

First, create a subdirectory under the `targets` directory. The name of this subdirectory will be treated by RCABench as the name of the newly added target. Its name should follow format `<PROGRAM>_<ID>`, with `<PROGRAM>` and `<ID>` changing for each target. Typically, `<PROGRAM>` represents the program name of the target, while `<ID>` is an identifier, such as a CVE ID, representing a bug or vulnerability of the target. They should consist of lowercase letters, numbers or hyphens.

For example, the directory for CVE-2016-10094 in LibTIFF is in the `targets` directory. The name of this directory is `libtiff_cve-2016-10094`.

### 2. Create files for executing a target

The next step is to create the necessary files to run the newly added target. These files are placed in the directory created in the first step. For a concrete example, look inside the [targets/libtiff_cve-2016-10094](./libtiff_cve-2016-10094/) folder.

Follow the instructions to create three files.

#### `preinstall.sh`

This file specifies the commands to install the packages needed to build and run the target. It needs to be written as a bash script. The script is also run as administrator privilege in the [Dockerfile](../data_augmentation/Dockerfile) of data augumentation and the [Dockerfile](../feature_extraction/Dockerfile) for feature extraction.

Basically, you can use the following example to create this file. As shown in the example, you can use the `apt install` commands to install the packages you need. To use this example in practice, rewrite the `<PACKAGES>`. You can also use commands other than `apt install`.

```bash
#!/bin/bash
set -eux

apt install -y <PACKAGES>
```

For more concrete examples, see [preinstall.sh](./libtiff_cve-2016-10094/preinstall.sh) used in [libtiff_cve-2016-10094](./libtiff_cve-2016-10094).

#### `build.sh`

This file specifies the commands to download and build the newly added target program. It must be written as a bash script. Also, this script runs as non-root in the [Dockerfile](../data_augmentation/Dockerfile) for data augmentation and the [Dockerfile](../feature_extraction/Dockerfile) for feature extraction, so any work that requires administrative privileges must be done in `preinstall.sh` as described in the previous step.

Basically, you can use the following example to create this file, which consists of three steps:

1. The working directory is changed to `$TARGET_ROOT`. `$TARGET_ROOT` is an environment variable that is set in the the [Dockerfile](../data_augmentation/Dockerfile) for data augmentation and the [Dockerfile](../feature_extraction/Dockerfile) for feature extraction. You can place the files needed for the target in this directory.

2. Download the files needed to build the target. If the target is managed by GitHub or similar, you can use the `git clone` command as shown in the example, replacing the `<URL>` with the appropriate one. Alternatively, if the method is managed by another hosting service, you can download it using a command such as `wget`. You can place the files needed to build the target in `$TARGET_ROOT/$1`, a subdirectory of `$TARGET_ROOT`. Some methods require the use of binaries built with several different options. To prepare for this, the name of the subdirectory is passed as the first argument when build.sh is called. In addition, it is recommended to fix the target with a specific commit hash for reproducibility of the experiment; for git-managed targets, rewrite `<COMMIT_HASH>` to a specific value.

3. Receives variables `TARGET_DEF_CFLAGS` and `TARGET_DEF_CXXFLAGS` with the options used to build the target. These variables are defined in the `target_build.sh` script for each of the data augmentation or feature extraction methods. This basically does not need to be changed by the target.

4. Build the target. You need to write a script that generates the build options, `ARGS`, from variables `TARGET_DEF_CFLAGS` and `TARGET_DEF_CXXFLAGS` according to the build method of each target. Also, `<BUILD_COMMAND>` should be rewritten to match the target.

```bash
#!/bin/bash

if [ $# -lt 1 ]; then
  echo "Usage: $0 <build dir name>" 1>&2
  exit 1
fi

# 1. Move to the directory for target
cd ${TARGET_ROOT}

# 2. Download target
git clone <URL> $1
cd ${TARGET_ROOT}/$1
git checkout <COMMIT_HASH>

# 3. Receive compile options required by each method
TARGET_DEF_CFLAGS="${TARGET_DEF_CFLAGS-} -static"
TARGET_DEF_CXXFLAGS="${TARGET_DEF_CXXFLAGS-} -static"

# 4. Build target
ARGS=""
for var in "${!TARGET_DEF_@}"; do
  ARGS="${ARGS} ${var#TARGET_DEF_}=\"$(echo ${!var})\""
done
eval <BUILD_COMMAND> ${ARGS}
```

For more concrete examples, see [build.sh](./libtiff_cve-2016-10094/build.sh) used in [libtiff_cve-2016-10094](./libtiff_cve-2016-10094).

#### `config.sh`

This file specifies the environment variables to be exported in the environment in which each data augmentation or feature extraction method is run. It sets the path to the program binary built in the previous step and the arguments to be used when executing the binary. This file allows each method to know how to execute targets.

You can use the following example to create this file. As shown in the example, the environment variables `RELPATH` and `ARGS` are defined. To use this example, you must rewrite `<TARGET_BIN_PATH>` to the path to the binary you created in the previous step. You also need to rewrite `<TARGET_BIT_ARGS>` to the arguments for executing the binary. If the argument contains the name of the input file, replace it with `@@`. This is the same as for AFL.

```bash
#!/bin/bash
set -eux

export RELPATH="<TARGET_BIN_PATH>"
export ARGS="<TARGET_BIT_ARGS>"
```

For more concrete examples, see [config.sh](./libtiff_cve-2016-10094/config.sh) used in [libtiff_cve-2016-10094](./libtiff_cve-2016-10094) and [config.sh](./libjpeg_cve-2017-15232/config.sh) used in [libjpeg_cve-2017-15232](./libjpeg_cve-2017-15232/). In the first example, only the input file is set as an execution argument to the target; in the second example, the input file and multiple arguments are set.

### 3. Prepare an crashing input

RCA uses a crashing input as an initial seed and analyzes the root cause. Therefore, you must prepare one or more crashing inputs in advance.

First, you should create a directory named `seeds` under the directory you created in the [first step](#1-create-a-directory). Next, place a crashing input in this directory with the file name `default`. The crashing input will be used as the default initial seed for each target. For more details, see the [default](./libtiff_cve-2016-10094/seeds/default) file in [libtiff_cve-2016-10094](./libtiff_cve-2016-10094).

Optionally, you can place several different crashing inputs other than the `default` file in the `seeds` directory. This is used to measure the difference in performance of the RCA tool due to different initial seeds.

### 4. Define root causes

RCABench evaluates the results inferred by each feature extraction method based on the ground truth of the root cause, which is predefined by humans. Currently, RCABench supports the definition of the root cause at the line level of the source code. It is also possible to register multiple ground truths.

Basically, you can use the following example to create this file. Multiple ground truths are defined using the format shown below. Each line represents one ground truth, where `<FILE_*>` and `<LINE_*>` indicate the file name of each ground truth and the line number of that file.

```text
<FILE_1>:<LINE_1>
<FILE_2>:<LINE_2>
...
<FILE_N>:<LINE_N>
```

For more concrete examples, see [locations](./libtiff_cve-2016-10094/root_causes/locations) used in [libtiff_cve-2016-10094](./libtiff_cve-2016-10094) and [locations](./libxml2_cve-2017-5969/root_causes/locations) used in [libxml2_cve-2017-5969](./libxml2_cve-2017-5969/). The first example defines a single location as the root cause, while the second example defines multiple locations as the root cause.
