#!/bin/bash

SCRIPT_PATH=$(dirname `readlink -f ${BASH_SOURCE[0]}`)
python $SCRIPT_PATH/run.py $@