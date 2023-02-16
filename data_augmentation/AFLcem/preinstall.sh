#/bin/bash
set -eux

DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y build-essential wget
