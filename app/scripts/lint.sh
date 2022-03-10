#!/usr/bin/env bash

set -x

black app
isort app
flake8
mypy app --no-warn-return-any --ignore-missing-imports
