#!/usr/bin/env bash

set -e
set -x

pytest --cov-report=term --cov app/tests/
