#!/bin/bash
# Source Global
# export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
source /opt/ros/humble/setup.bash

# Check venv
if [ ! -d "./.venv" ]; then
  python -m venv .venv
fi
# source local build
source ./install/setup.bash
# install addition reqs
source ./.venv/bin/activate
pip install -r ./requirements.txt
