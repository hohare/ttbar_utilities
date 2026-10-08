#!/bin/bash

YEAR=$1
DATASET=$2

source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.36.08/x86_64-almalinux9.7-gcc115-opt/bin/thisroot.sh
xrdfsls -u /store/user/honor/skims/$YEAR/$DATASET > filelst.txt
