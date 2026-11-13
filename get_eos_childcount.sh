#!/bin/bash

YEAR=$1
DATASET=$2

eos root://cmseos.fnal.gov find --childcount /eos/uscms/store/user/honor/skims/$YEAR/$DATASET

