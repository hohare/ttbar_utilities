import os
from argparse import ArgumentParser
import json
import glob
import numpy as np

prefix_dict = {
    "fnalEOS": "root://cmseos.fnal.gov/",
    "global": "root://cms-xrd-global.cern.ch/"
}

def getFileset(sample, startFile=0, nFiles=-1, verbose=False, ):
    f_ = sample.find("_")
    year = sample[:f_]
    detailKey = sample[(f_+1):]

    # find all json files for the sample or sample collection    
    fileset_all = {}
    #for sample in rD[dataset]:
    # temporary. eventually change to use environ
    #else: path = 'Inputs/'
    JSONDir = "/uscms/home/honor/private/ttbareft_broken/ttbareft/Inputs/" + year + "/"
    #JSONDir = environ['TTBAR_BASE'] + '/Inputs/' + year + "/"

    inputSamples = glob.glob(JSONDir+"*"+detailKey+"*.json")
    if len(inputSamples) == 0:
        raise Exception("Error: no json file like", detailKey, " found in:", JSONDir)
    
    # open all json files and dump them into the dictionary
    for s in inputSamples:
        if verbose:
            print('reading from', s)
        fileset_all.update(json.load(open(s ,'r')))
    
    # process a subset of a sample
    fileset = {}
    for n, rFiles in fileset_all.items():
        nf = nFiles
        fileset[n] = []

        if nf < 0:
            nf = len(rFiles)
        fn = startFile

        while fn < startFile+nf and fn < len(rFiles):
            if verbose: 
                print("Name of sample: %-40s" % (n), "start file number: " + str(fn), "Number of total files: " + str(len(rFiles)))
            fileset[n].append(rFiles[fn])
            fn+=1

    return fileset

def apply_prefix(fileset, prefix):
    """Add an xrootd prefix to all files in a fileset"""
    if not prefix.startswith("root:"):
        prefix = prefix_dict[prefix]
    newfileset = {}
    for subset in fileset:
        newlist = []
        for f in fileset[subset]:
            idx = f.find('/store')
            newlist.append(prefix+f[idx:])
        newfileset[subset] = newlist
    return newfileset

def search_save_filepaths(prefix, search_dir, datasetName):
    from search_eos import search_eos
    
    fdict = {datasetName: search_eos(prefix, search_dir)}
    fdict = apply_prefix(fdict, prefix)
    with open(f'Inputs/pretraining/{datasetName}.json', 'w') as f:
        json.dump(fdict, f, indent=4)

def construct_fileset(jsonFiles, prefix=None):
    fileset = {}
    for jsonFile in jsonFiles:
        fileset.update(json.load(open(jsonFile)))
    if prefix != "None":
        fileset = apply_prefix(fileset, prefix)
        
    return fileset

def make_skim_fileset(basepath, folders):
    """Constructs and renames fileset by searching for merged files."""
    filesets = {}
    for folder in folders:
        files = glob.glob(os.path.join(basepath,folder,"merged*.root"))
        for file in files:
            dataset = "_".join(file.split("/")[-1].split("_")[1:-2])
            if dataset in filesets: filesets[dataset].append(file)
            else: filesets[dataset] = [file]
    return filesets

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--search', '-s', action="store_true")
    parser.add_argument('--prefix', '-p', default="root://cmseos.fnal.gov/")
    parser.add_argument('--fpath',  '-f')
    parser.add_argument('--name',   '-n')
    args = parser.parse_args()

    if args.search:
        search_save_filepaths(args.prefix, args.fpath, args.name)
        