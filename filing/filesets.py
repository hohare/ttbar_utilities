from argparse import ArgumentParser
import json
import numpy as np

prefix_dict = {
    "fnalEOS": "root://cmseos.fnal.gov/",
    "global": "root://cms-xrd-global.cern.ch/"
}

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
    
    flist = search_eos(prefix, search_dir)
    dict_with_prefix = apply_prefix({"modCentral": flist}, prefix)
    with open(f'Inputs/pretraining/{datasetName}.json', 'w') as f:
        json.dump(dict_with_prefix, f, indent=4)

def construct_fileset(jsonFiles, prefix=None):
    fileset = {}
    for jsonFile in jsonFiles:
        fileset.update(json.load(open(jsonFile)))
    if prefix is not None:
        fileset = apply_prefix(fileset, prefix)
        
    return fileset

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--search', '-s', action="store_true")
    parser.add_argument('--prefix', '-p', default="root://cmseos.fnal.gov/")
    parser.add_argument('--fpath',  '-f')
    parser.add_argument('--name',   '-n')
    args = parser.parse_args()

    if args.search:
        search_save_filepaths(args.prefix, args.fpath, args.name)
        