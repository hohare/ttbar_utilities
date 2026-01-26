import uproot
import json
import numpy as np
from tqdm import tqdm

def combine_metadata_files(path):
    import glob
    from coffea.util import load, save
    from coffea.processor import defaultdict_accumulator
    files = glob.glob('/uscms_data/d3/honor/ttbareft/Outputs/2017_ST_tchannel_top/summary*.coffea')
    totals = defaultdict_accumulator(float)
    for f in tqdm(files):
        meta = load(f)
        totals += meta['cutflow']
        print(meta['cutflow']['InputEventCount'])
        #TODO add call to merge all the meta['outfiles']

    return totals

def get_wcs():
    """NOT COMPLETED YET"""
    print(f"Opening with uproot: {fname}")
    with uproot.open(fname) as f:
        # Check if all the EFTrwgt points use the same set of wcs
        rwgt_names = [name for name in tree.keys() if name.startswith("LHEWeight_EFTrwgt")]
        print(rwgt_names)
        coeffs = [f.split('_')[2::2] for f in rwgt_names]
        all_same_wcs = all(np.all(np.unique(x) == np.unique(coeffs[0])) for x in coeffs)
        print(coeffs)
        if all_same_wcs:
            wc_names = coeffs[0]
        else:
            wc_names = []
    return wc_names

# Extracts event information from a root file
def get_info(fname, tree_name = "Events", verbose=False):
    # The info we want to get
    raw_events = 0  # The raw number of entries as reported by TTree.num_entries
    gen_events = 0  # Number of gen events according to 'genEventCount' or set to raw_events if not found
    sow_events = 0  # Sum of weights
    sow_lhe_wgts = 0 # Sum of LHE weights
    is_data = False
    if verbose: print(f"Opening with uproot: {fname}")
    with uproot.open(fname) as f:
        tree = f[tree_name]
        is_data = not "genWeight" in tree

        raw_events = int(tree.num_entries)
        if is_data:
            # Data doesn't have gen or weighted events!
            gen_events = raw_events
            sow_events = raw_events
        else:
            gen_events = raw_events
            if 'LHEWeight_sm_point' in tree:
                sow_events = np.sum(tree['LHEWeight_sm_point'])
            else:
                sow_events = np.sum(tree["genWeight"])
                if "Runs" in f:
                    # Instead get event from the "Runs" tree
                    runs = f["Runs"]
                    gen_key = "genEventCount" if "genEventCount" in runs else "genEventCount_"
                    sow_key = "genEventSumw"  if "genEventSumw"  in runs else "genEventSumw_"
                    gen_events = sum(runs[gen_key].array())
                    sow_events = sum(runs[sow_key].array())
    
                    # Get the LHE weights array (note it's stored as a ratio, so multiply by sow before summing)
                    sow_arr = runs[sow_key].array()
                    LHEScaleSumw_arr = runs["LHEScaleSumw"].array()
                    sow_lhe_wgts = sum(sow_arr*LHEScaleSumw_arr)

    return [raw_events, gen_events, sow_events, sow_lhe_wgts, is_data]

def get_infos(fileset, fpath=None, verbose=False):
    sample_dict = {}
    for dataset in fileset:
        nevents = 0
        n_gen_events = 0
        n_sum_of_weights = 0
        sow_lhe_wgts = 0
        is_data_lst = []
        for f in tqdm(fileset[dataset]):
            i_events, i_gen_events, i_sum_of_weights, sow_lhe_wgts, is_data = get_info(f, "Events", verbose=verbose)
            nevents += i_events
            n_gen_events += i_gen_events
            n_sum_of_weights += i_sum_of_weights
            is_data_lst.append(is_data)

        if len(set(is_data_lst)) != 1:
            raise Exception("ERROR: There are a mix of files that are data and mc")
        else:
            is_data = is_data_lst[0]
        
        sample_dict[dataset] = {
            'nEvts': nevents,
            'nGenEvts': int(n_gen_events),
            'sumOfWeights': float(n_sum_of_weights),
            'isData': is_data,
            #'wcNames': utils.get_list_of_wc_names(fileset[dataset][0])
        }

    if fpath:
        with open(fpath,'w') as fout:
            json.dump(sample_dict, fout, indent=4)
        
    return sample_dict
        # save sampdic in json file
        #with open(outputFile, "w") as outfile:
            #json.dump(sample_dict, outfile, indent=4)
            #print(f"\n New json file: {outputFile}") 

        #print("If this is an EFT sample, the sow is incorrect and needs to be replaced with the sum of event weights at the SM")


    