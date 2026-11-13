import os
from argparse import ArgumentParser
import json
import glob
import numpy as np

prefix_dict = {
    "fnalEOS": "root://cmseos.fnal.gov/",
    "global": "root://cms-xrd-global.cern.ch/"
}

def getFileset(sample, startFile=0, nFiles=-1, verbose=False, 
               JSONDir="/uscms/home/honor/private/ttbareft/Inputs/"
              ):
    f_ = sample.find("_")
    year = sample[:f_]
    JSONDir = JSONDir + year + "/"
    
    if "skims" in sample:
        detailKey = sample.replace(year+"_skims_","")
        JSONDir = os.path.join(JSONDir, "skims/")
    else:
        detailKey = sample[(f_+1):]
    
    # find all json files for the sample or sample collection    
    fileset_all = {}

    inputSamples = glob.glob(JSONDir+"*"+detailKey+"*.json")
    if "ext" not in detailKey:
        # central EFT sample has datasets with -extX on the end
        # don't want to accidentally pick up those unless specified
        inputSamples = [key for key in inputSamples if "ext" not in key]
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

def save_skimlist2jsons(year):
    import subprocess
    import glob
    import json

    #***** RETRIEVE LIST OF FILES PER DATASET AND STORE IN .TXT *****#
    #FNAL
    cmd = ["./get_fileset.sh", year, "FNAL"]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    proc.communicate()
    #CERN
    cmd = ["./get_fileset.sh", year, "CERN"]
    #proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    #proc.communicate()

    #basepath = f"~/private/ttbar/Inputs/{year}/skims/"
    basepath = f"/uscms/home/honor/private/ttbareft/Inputs/{year}/skims/"
    #***** PUT LISTS INTO JSONS *****#
    full_fileset = {}
    filelist = glob.glob(basepath+"*.txt")
    for fpath in filelist:
        with open(fpath, "r") as f:
            fset = f.readlines()
        fset = [f[:-1] for f in fset]#remove newline
        dataset = fpath.split("/")[-1][:-9]#remove -LOCATION.root
        full_fileset.update({dataset:fset})
        
        with open(basepath+f"{dataset}.json", "w") as f:
            json.dump({dataset: fset}, f, indent=4)

    with open(basepath+"fileset.json","w") as f:
        json.dump(full_fileset, f, indent=4)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--skims', '-k', action="store_true")
    parser.add_argument('--year', '-y')
    parser.add_argument('--search', '-s', action="store_true")
    parser.add_argument('--prefix', '-p', default="root://cmseos.fnal.gov/")
    parser.add_argument('--fpath',  '-f')
    parser.add_argument('--name',   '-n')
    args = parser.parse_args()

    if args.skims:
        if "year" not in args:
            print("Must specify year for skims with --year")
        else:
            save_skimlist2jsons(args.year)
    elif args.search:
        search_save_filepaths(args.prefix, args.fpath, args.name)
        