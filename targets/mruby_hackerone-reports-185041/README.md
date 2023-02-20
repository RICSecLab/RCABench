# Type confusion in mrb_exc_set leading to memory corruption

## description

Macro E_NOTIMP_ERROR is not a constant value and there is no type check so it can be overwritten to any value in ruby source code.

## references

https://hackerone.com/reports/185041

## patch commit

first patch https://github.com/mruby/mruby/commit/36fc1f1431d9aa85c167f91ef30abe0953c56400

second patch https://github.com/mruby/mruby/commit/fb1dad82aae8c98949be7e5ad7440675c67265bb

## fixed files

first: https://github.com/mruby/mruby/commit/36fc1f1431d9aa85c167f91ef30abe0953c56400#diff-0785f4cf8a2cc06d90d511879d9b43ff9f69858fceb83bc13a5f78bd8b3a9187

second: https://github.com/mruby/mruby/commit/fb1dad82aae8c98949be7e5ad7440675c67265bb#diff-0785f4cf8a2cc06d90d511879d9b43ff9f69858fceb83bc13a5f78bd8b3a9187

## Source of PoC

https://hackerone.com/reports/185041
