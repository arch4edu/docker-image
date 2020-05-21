#!/bin/sh
set -e

#python packages.py
packages=$(grep -v '^#' packages.txt)
packages=$(echo $packages)
sed "s/PACKAGES/$packages/" Dockerfile.template | DOCKER_BUILDKIT=1 docker build -f - \
	--no-cache \
	--pull \
	--compress \
	--squash \
	-t arch4edu/base:latest .

#docker save arch4edu/base | zstd -c -T32 --ultra -21 - > arch4edu.tar.zst
#docker push arch4edu/base:latest
