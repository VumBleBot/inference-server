#!/usr/bin/env bash

# CUSTOM IT
IMAGE_NAME="sample-fastapi-project"
TAG_NAME="1.0"


set -e # stop if error occurs
set -x # execute after print command

docker build . --tag=${IMAGE_NAME}:${TAG_NAME} \
