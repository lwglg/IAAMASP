#!/bin/sh -e
set -x

ruff check src --fix --unsafe-fixes
ruff format src
