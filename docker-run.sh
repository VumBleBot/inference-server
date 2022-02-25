#!/usr/bin/env bash

# CUSTOM IT
IMAGE_NAME="vumblebot"
TAG_NAME="0.1"
ENV_STATE="dev"

set -e # stop if error occurs
set -x # execute after print command

docker run -d --name=inference-server \
  -e ENV_STATE=${ENV_STATE} \
  -p 80:80 \
  ${IMAGE_NAME}:${TAG_NAME}
