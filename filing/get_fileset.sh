#!/bin/bash

YEAR=$1
LOCATION=$2

if [[ "$LOCATION" == "CERN" ]]; then
    XRDIR=root://eosuser.cern.ch/
    myEOSDIR=/eos/user/h/hohare/skims/${YEAR}/
fi

if [[ "$LOCATION" == "FNAL" ]]; then
    XRDIR=root://cmseos.fnal.gov/
    myEOSDIR=/store/user/honor/skims/${YEAR}/
fi

echo "Looking at $XRDIR in $myEOSDIR"

source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.36.08/x86_64-almalinux9.7-gcc115-opt/bin/thisroot.sh
cmd="xrdfs ${XRDIR} ls ${myEOSDIR}"
RESULT=$(eval $cmd)

for DIR in $RESULT; do 
    LEN=$((${#DIR}-23))
    dsNAME=${DIR:23:LEN}
    cmd="xrdfs ${XRDIR} ls -u ${DIR}"
    echo $cmd
    LS=$(eval $cmd)
    LEN=$((${#YEAR}+2))
    printf "%s\n" "${LS[@]}" > "/uscms/home/honor/private/ttbareft/Inputs/${YEAR}/skims/${dsNAME:LEN}-${LOCATION}.txt"
done
