#!/usr/bin/env bash

# CUSTOM IT
IMAGE_NAME="sample-fastapi-project"
TAG_NAME="1.0"
ENV_STATE="dev"

set -e # stop if error occurs
set -x # execute after print command

docker run -d --name=fastapi-container \
  -e ENV_STATE=${ENV_STATE} \
  -p 80:80 \
  ${IMAGE_NAME}:${TAG_NAME}
