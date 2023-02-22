# targets
You can place a custom script file for a specific target in this directory.

## How to add a custom script
1. In this directory, create a new directory with the same name as `TARGET_ID`.
2. Create the files `prebuild.sh` and `target.yaml` as described below.

### prebuild.sh
Write a bash script you want to run before `targets/$TARGET_ID/build.sh` runs.

### target.yaml
Place a configuration yaml file as defined below.

<dl>
  <dt>target</dt>
  <dd>Specify the target name.</dd>
  <dt>run_build_sh</dt>
  <dd>Specify `true` to run `targets/$TARGET_ID/build.sh` after running `prebuild.sh`, `false` otherwise.</dd>
</dl>

Here is a typical example of `target.yaml`.

```
target: program_CVE-XXXX-XXXX
run_build_sh: true
```