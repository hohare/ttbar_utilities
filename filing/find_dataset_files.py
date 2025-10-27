"""
Based on Joseph Dulemba NanoAOD_Analyses make_dataset_txt_files.py

Honor Hare
Updated: October 2025 to have dataset argument
"""
import os, sys
#from pdb import set_trace
import subprocess as sub
#from site_mapping import site_name_to_xrootd
import json
from argparse import ArgumentParser

parser = ArgumentParser("Query DAS for file location strings")
parser.add_argument("sampleName", default="TTtoLNu2Q_0to700", help="valid sample key from pretraining/datasets.json")
parser.add_argument("year", default="2017")
parser.add_argument("-e", "--era", default=None, help="Build DAS path manually using sampleName/era/format")
parser.add_argument("-f", "--format", default="NANOAODSIM",help="Build DAS path manually using sampleName/era/format")
parser.add_argument('-l', "--location", default="fnal", help="Which xrootd prefix to use")
parser.add_argument('-v', "--verbose", action='store_true')
parser.add_argument('-d', "--dataset", default="Inputs/DAS_datasets.json", help="file where the dataset is defined")
args = parser.parse_args()

#interface through which to query the das system
def query(query_str, verbose=False):
    if verbose:
        print('Querying DAS for "%s"' %query_str)
    cmd = ['dasgoclient','--query=%s' %query_str, '--limit=0','--format=plain']
    p = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.PIPE)
    output, errors = p.communicate()
    if errors: raise RuntimeError('Query crashed with error: %s' %errors)
    output = output.decode()
    return output.split('\n')[:-1]

datasets = json.load(open(args.dataset))[args.year]
# if don't give an absolute path, assume is a provided DAS path
if args.sampleName[0]!="/" and args.sampleName in datasets:
    dataset = datasets[args.sampleName]
#if give an absolute path, then assume manual DAS path construction
elif args.sampleName[0]!="/" and args.era is not None:
    dataset = [os.path.join([args.sampleName, args.era, args.format])]
# otherwise print list of suggested samples
else:
    print('Need a valid dataset to search for.\nSee DAS_datasets.json for examples')
    exit()

if args.location=="cern": location="root://xrootd-cms.infn.it//store"
elif args.location=="global": location="root://cms-xrd-global.cern.ch//store"
else: location="root://cmsxrootd.fnal.gov//store"
    
    
# Retrieve file names of valid files for this dataset path
file_list = query("".join(["file status=VALID ","dataset=",dataset]),verbose=args.verbose)

if args.verbose: print('Parsing file names to locations')
# Convert file names to locations
out_list = []
for fname in file_list:
    out_list.append(fname.replace("/store", location))

# Write the information as jsons to the appropriate folders
d = {args.sampleName: out_list}
outpath = os.path.join("pretraining/Inputs/", "_".join([args.year, args.sampleName]))+".json"
with open(outpath,"w") as fout:
    json.dump(d, fout)
print(f'wrote {args.sampleName} to {outpath}\n')