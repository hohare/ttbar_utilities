import os
import subprocess
import json
import time
import glob
import uuid
from argparse import ArgumentParser

nobackup = "/uscms_data/d3/honor/Outputs/"
cerneos = "root://eosuser.cern.ch//eos/user/h/hohare/skims"
fnaleos = "root://cmseos.fnal.gov//store/user/honor/skims"


def merge_eos_skims(dataset_name,
                    args,
                    #syst_shift='nominal',
                    eospath='/store/user/honor/skims/',
                    outpath='',
                    suppression_level='-f505',
                    starter = 'root://cmseosmgm01.fnal.gov:1094/'
                    ):
    #before this point have confirmed that all files in the summary outfiles list is unique
    #should probably also do a check that nfiles in summary matches nfiles in eos dir
    eosfolder = os.path.join(eospath,args.year,dataset_name)
    # Acquire file list
    #cmd = ['xrdfsls','-u', eosfolder,  "> filelst.txt"]#f"| grep \'{sy"ST_shift}.*\.root\'",
    #idk why couldnt run the xrdfsls command from here (wasnt a recognized command)
    cmd = ['./get_flist.sh', args.year, dataset_name]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    proc.communicate()
    
    # Divide file list
    with open('filelst.txt') as f:
        lst = [line.rstrip() for line in f if "merged" not in line]
    chunks = [lst[x:x+args.chunksize] for x in range(0, len(lst), args.chunksize)]
    print(f'merging {len(lst)} files in chunks of {args.chunksize} totaling {len(chunks)} chunks')
    
    if args.run_merge:
        cp_list = []
        # Merge each division
        for i,chunk in enumerate(chunks):
            t0 = time.time()
            fname = "merged_{dataset_name}_{i}_{uid}.root".format(dataset_name=dataset_name, i=i, uid=uuid.uuid4())
    
            merged_name = os.path.join(nobackup,outpath,fname)
            cmd = ["hadd", suppression_level, merged_name] + chunk
            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
            proc.communicate()
    
            timestamp = time.strftime('%Y%m%d_%H%M%S',time.localtime())
            print(time.time()-t0)
    
            with open(f'../Outputs/toremove/torm_{i}_{timestamp}.sh', 'w') as f:
                for c in chunk:
                    f.write('eosrm '+c.replace(starter,'')+"\n")
            cp_list.append(f'xrdcp {merged_name} {fnaleos}/2018/{dataset_name}/{fname}\n')
            
            if i==30: break
        
        with open(f'{os.path.join(nobackup,outpath)}/tocp_{dataset_name}.sh', 'w') as f:
            f.writelines(cp_list)
    
            

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

#source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.36.08/x86_64-almalinux9.7-gcc115-opt/bin/thisroot.sh

if __name__=="__main__":
    parser = ArgumentParser("Merging skims given groups of files to merge")
    parser.add_argument("year")
    parser.add_argument("name",help="Name dataset")
    parser.add_argument("-p", "--outpath", default='/uscms_data/d3/honor/Outputs/', help="")
    parser.add_argument("-s", "--syst", default='nominal', help='Which systematic shift to apply')
    parser.add_argument("-e", "--eos", action='store_true')
    parser.add_argument("-r", "--run_merge", action='store_true')
    parser.add_argument("-c", "--chunksize", type=int, default=150)
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
             merge_eos_skims(dataset, args, outpath=args.outpath)