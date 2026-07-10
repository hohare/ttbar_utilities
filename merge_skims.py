import os
import subprocess
import json
import time
import glob
from argparse import ArgumentParser

def merge_skims(path, fname):
    injson = json.loads(open(path+fname).read())
    # one json holds multiple jobs
    # per summary file
    #mergedFiles = []
    for key in injson:
        flist = injson[key]
        # skims have been divided into groups
        for group in range(len(flist)):
            # each group needs to be merge into one root file
            outname = "_".join(["merged", key, str(group)])+".root"
            #mergedFiles.append(outname)
            cmd = ["hadd",  path+outname] + flist[group][:5]
            #"-f",

            tstart=time.time()
            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
            proc.communicate()
            elapsed = time.time()-tstart
            print("Total time: %.1f seconds"%elapsed)


inplace = "Outputs/sideband_tests/"
nobackup = "/uscms_data/d3/honor/Outputs/"
def merge_skims_v2(path, fname):
    injson = json.loads(open(path+fname).read())
    # one json holds multiple jobs
    # per summary file
    #cmds = []
    for key in injson:
        flist = injson[key]
        # skims have been divided into groups
        for group in range(len(flist)):
            thislist = [f.replace(inplace, nobackup) for f in flist[group]]
            # each group needs to be merge into one root file
            outname = "_".join(["merged", key, str(group)])+".root"
            cmd = ["hadd", "-fk",  path+outname] + thislist#[:20]
            #cmds.append(cmd)
            print(cmd)

            #tstart=time.time()
            #proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
            #proc.communicate()
            #elapsed = time.time()-tstart
            #print("Total time: %.1f seconds"%elapsed)

#xrdfsls -u /store/user/honor/ttbareft/skims/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8 > filelst.txt
#xrdfsls -u /store/user/honor/ttbareft/skims/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8 > filelist.txt

def merge_eos_skims(dataset_name,
                    year,
                    chunksize=300,
                    syst_shift='nominal',
                    eospath='/store/user/honor/skims/',
                    outpath=''
                    ):
    #before this point have confirmed that all files in the summary outfiles list is unique
    #should probably also do a check that nfiles in summary matches nfiles in eos dir
    eosfolder = os.path.join(eospath,year,dataset_name)
    # Acquire file list
    #cmd = ['xrdfsls','-u', eosfolder,  "> filelst.txt"]#f"| grep \'{sy"ST_shift}.*\.root\'",
    #idk why couldnt run the xrdfsls command from here (wasnt a recognized command)
    cmd = ['./get_flist.sh', year, dataset_name]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    proc.communicate()
    
    # Divide file list
    with open('filelst.txt') as f:
        lst = [line.rstrip() for line in f if syst_shift in line]
    chunks = [lst[x:x+chunksize] for x in range(0, len(lst), chunksize)]
    # Merge each division
    for i,chunk in enumerate(chunks):
        merged_name = os.path.join(nobackup,outpath,"_".join(['merged', dataset_name, syst_shift, str(i)])+".root")
        cmd = ["hadd", merged_name] + chunk
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        proc.communicate()

run_dict = {
    "2016preVFP_SingleElectron": [
        "Data_2016_RunBver2himp_SingleElectron",
        "Data_2016_RunChimp_SingleElectron",
        "Data_2016_RunDhimp_SingleElectron",
        "Data_2016_RunEhimp_SingleElectron",
        "Data_2016_RunFhimp_SingleElectron"
    ],
    "2016preVFP_SingleMuon" :[
        "Data_2016_RunBver2himp_SingleMuon",
        "Data_2016_RunChimp_SingleMuon",
        "Data_2016_RunDhimp_SingleMuon",
        "Data_2016_RunEhimp_SingleMuon",
        "Data_2016_RunFhimp_SingleMuon"
    ],
    "2016postVFP_SingleElectron":[
        "Data_2016_RunF_SingleElectron",
        "Data_2016_RunG_SingleElectron",
        "Data_2016_RunH_SingleElectron",
    ],
    "2016postVFP_SingleMuon":[
        "Data_2016_RunF_SingleMuon",
        "Data_2016_RunG_SingleMuon",
        "Data_2016_RunH_SingleMuon"
    ],
    "QCD_MuEnrichedPt5": [
        "QCD_Pt-1000_MuEnrichedPt5_TuneCP5_APV",
        "QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_APV",
        "QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_APV",
        "QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_APV",
        "QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_APV",
        "QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_APV",
        "QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_APV",
        "QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_APV",
        "QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_APV",
    ],
    "QCD_EMEnriched": [
        "QCD_Pt-120to170_EMEnriched_TuneCP5_APV",
        "QCD_Pt-170to300_EMEnriched_TuneCP5_APV",
        "QCD_Pt-300toInf_EMEnriched_TuneCP5_APV",
        "QCD_Pt-30to50_EMEnriched_TuneCP5_APV",
        "QCD_Pt-50to80_EMEnriched_TuneCP5_APV",
        "QCD_Pt-80to120_EMEnriched_TuneCP5_APV",
    ],
    "ST":[
        "ST_s-channel_4f_leptonDecays_TuneCP5",
        "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5",
        "ST_t-channel_top_4f_InclusiveDecays_TuneCP5",
        "ST_tW_antitop_5f_NoFullyHadronicDecays",
        "ST_tW_top_5f_NoFullyHadronicDecays",
    ],
    "WJetsToLNu": [
        "WJetsToLNu_HT-70To100_TuneCP5",
        "WJetsToLNu_HT-100To200_TuneCP5",
        "WJetsToLNu_HT-200To400_TuneCP5",
        "WJetsToLNu_HT-400To600_TuneCP5",
        "WJetsToLNu_HT-600To800_TuneCP5",
        "WJetsToLNu_HT-800To1200_TuneCP5",
        "WJetsToLNu_HT-1200To2500_TuneCP5",
        "WJetsToLNu_HT-2500ToInf_TuneCP5"
    ],
    "miscBkgnd": [
        "WW_TuneCP5",
        "WZ_TuneCP5",
        "ZZ_TuneCP5",
        "TTWJetsToLNu_TuneCP5",
        "TTWJetsToQQ_TuneCP5",
        "TTZToLLNuNu_M-10_TuneCP5",
        "TTZToQQ_TuneCP5"
    ],
    "DY": ["DYJetsToLL_M-50_TuneCP5"],
    "TTToSemiLeptonic": ["TTToSemiLeptonic_TuneCP5"],
    "TTTo2L2Nu": ["TTTo2L2Nu_TuneCP5"],
    "TTToHadronic": ["TTToHadronic_TuneCP5"]
}

if __name__=="__main__":
    parser = ArgumentParser("Merging skims given groups of files to merge")
    parser.add_argument("year")
    parser.add_argument("name",help="Name dataset")
    parser.add_argument("-p", "--outpath", default='/uscms_data/d3/honor/Outputs/', help="")
    parser.add_argument("-s", "--syst", default='nominal', help='Which systematic shift to apply')
    parser.add_argument("-e", "--eos", action='store_true')
    args = parser.parse_args()
    
    if not args.eos:
        #merge_skims_v2(args.path,args.name)
        print('Not rewritten for new organizational scheme')
    else:
         if args.name in run_dict:
             torun=run_dict[args.name]
         else:
             torun=[args.name]
                 
         for dataset in torun:
             merge_eos_skims(dataset, args.year, outpath=args.outpath)