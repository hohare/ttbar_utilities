"""
Based on Joseph Dulemba NanoAOD_Analyses make_dataset_txt_files.py
"""
import os, sys
import subprocess as sub
#from site_mapping import site_name_to_xrootd
import json
from argparse import ArgumentParser

eras={
    #"2016": "RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v*",
    "2016postVFP": "RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v*",
    #"2016APV": "RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v*",
    "2016preVFP": "RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v*",
    "2017": "RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v*",
    "2018": "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v*"
}

def query(query_str, verbose=False):
    if verbose:
        print('Querying DAS for "%s"' %query_str)
    cmd = ['dasgoclient','--query=%s' %query_str, '--limit=0','--format=plain']
    print(" ".join(cmd))
    p = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.PIPE)
    output, errors = p.communicate()
    if errors: raise RuntimeError('Query crashed with error: %s' %errors)
    output = output.decode()
    return output.split('\n')[:-1]

def run_only_files(args, datasets):
    #if don't give an absolute path, assume is a key to provided DAS path dict
    if args.sampleName[0]!="/" and args.sampleName in datasets:
        dataset = datasets[args.sampleName]
    #if given an era, then assume manual DAS path construction
    elif args.era is not None:
        dataset="/"+"/".join([args.sampleName, args.era, args.format])
    #otherwise print list of suggested samples
    else:
        print('Need a valid dataset to search for.\nSee DAS_datasets.json for examples')
        exit()

    # Retrieve file names of valid files for this dataset path
    file_list = query("".join(["file status=VALID ","dataset=",dataset]),verbose=args.verbose)
    # Convert file names to locations
    if args.verbose: print('Parsing file names to locations')
    if args.location=="cern": location="root://xrootd-cms.infn.it//store"
    elif args.location=="global": location="root://cms-xrd-global.cern.ch//store"
    else: args.location="root://cmsxrootd.fnal.gov//store"
    out_list = []
    for fname in file_list:
        out_list.append(fname.replace("/store", args.location))
    if args.verbose: print(f'Found {len(out_list)} files')
    # Write the information as jsons to the appropriate folders
    if "APV" in args.year: replace="_APV"
    else: replace=""

    loc = args.sampleName.find('_13TeV')
    if loc<0: loc = len(args.sampleName)
    outname = args.sampleName[:loc]+replace
    d = {outname: out_list}
    outpath = os.path.join(args.sample_path, args.year, outname)+".json"
    with open(outpath,"w") as fout:
        json.dump(d, fout, indent=4)
    print(f'Wrote {outname} to {outpath}\n')

def run_intermediary(args):
    datasets = json.load(open(args.sample_path+f'samples_{args.year}.json'))
    if args.sampleName=="all":
        print(f"To run all samples in year {args.year}")
        for ds in datasets:
            args.sampleName=ds
            result = run_only_files(args, datasets)
    else:
        result = run_only_files(args, datasets)

if __name__=="__main__":
    parser = ArgumentParser("Query DAS for file location strings")
    parser.add_argument("sampleName", help="valid sample key from Inputs/samples_201X.json")
    parser.add_argument("year", choices=["2016preVFP","2016postVFP","2017","2018"], help='self explanatory')
    parser.add_argument("-s", "--searchPath", action='store_true', help='Construct the DAS path')
    parser.add_argument("-e", "--era", default=None, help="Build DAS path manually using sampleName/era/format")
    parser.add_argument("-f", "--format", default="NANOAODSIM",help="Build DAS path manually using sampleName/era/format")
    parser.add_argument('-l', "--location", default="fnal", help="Which xrootd prefix to use")
    parser.add_argument('-v', "--verbose", action='store_true')
    parser.add_argument('-p', "--sample_path", default="/uscms/home/honor/private/ttbareft_broken/ttbareft/Inputs/", help="path to the necessary inputs and outputs")
    args = parser.parse_args()

    if args.searchPath:
        if "pre" in args.year: isAPV=True
        else: isAPV=False
        
        datasearch = args.sampleName+eras[args.year]+"/"+args.format
        
        print('Querying for datasets...')
        datasets = query("".join(["dataset status=VALID ","dataset=",datasearch]))
        print(f'Found {len(datasets)} datasets!\n')
    
        sample_path = f'{args.sample_path}/samples_{args.year}.json'
        samples = json.load(open(sample_path))
        for ds in datasets:
            _s = ds.split("/")
            name = _s[1].replace("_13TeV-madgraphMLM-pythia8",'')
            # And adding the dataset to the sample json
            if isAPV: name="_".join([name, 'APV'])
            samples[name] = ds
            # Retrieving the file list for each dataset
            args.sampleName=_s[1]
            args.era=_s[2]
            args.format=_s[3]
            run_intermediary(args)
        with open(sample_path,"w") as fout:
            json.dump(samples, fout, indent=4)
        print(f'Wrote updated sample dict to {sample_path}')
    else:
        run_intermediary(args)
            
