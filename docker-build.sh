#!/usr/bin/env bash

# CUSTOM IT
IMAGE_NAME="vumblebot"
TAG_NAME="0.1"


set -e # stop if error occurs
set -x # execute after print command

docker build . --tag=${IMAGE_NAME}:${TAG_NAME}
