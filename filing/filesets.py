import json
import numpy as np
from utils.search_eos import search_eos

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
    flist = search_eos(prefix, search_dir)
    dict_with_prefix = apply_prefix({"modCentral": flist}, prefix)
    with open(f'Inputs/pretraining/{datasetName}.json', 'w') as f:
        json.dump(dict_with_prefix, f, indent=4)


def construct_fileset(jsonFiles, prefix="fnalEOS", save=False):
    fileset = {}
    for jsonFile in jsonFiles:
        fileset.update(json.load(open("Inputs/pretraining/"+jsonFile)))
    if prefix is not None:
        fileset = apply_prefix(fileset, prefix)
        
    return fileset

