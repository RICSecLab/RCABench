#!/bin/bash
set -eux

DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y curl wget cmake python3 psmisc build-essential
