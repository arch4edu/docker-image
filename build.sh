#!/bin/sh
set -e

#python packages.py
packages=$(grep -v '^#' packages.txt)
packages=$(echo $packages)
sed "s/PACKAGES/$packages/" Dockerfile.template > Dockerfile

DOCKER_BUILDKIT=1 docker build \
	--no-cache \
	--pull \
	--squash \
	-t arch4edu/base:latest .
