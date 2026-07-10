import os, sys
import subprocess as sub
from argparse import ArgumentParser

def run_cmd(cmd):
    print(" ".join(cmd))
    p = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.PIPE)
    output, errors = p.communicate()
    if errors: raise RuntimeError('hadd crashed with error: %s' %errors)
    output = output.decode()
    return output.split('\n')[:-1]

def merge_prep(fname, eosdir, 
               summaryPath = '/uscms_data/d3/honor/Outputs/'
              ):
    summary = util.load(os.path.join(summaryPath, fname))
    # Get root release for hadd
    cmd = ['source', '/cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.36.08/x86_64-almalinux9.7-gcc115-opt/bin/thisroot.sh']
    print(cmd)
    #result = run_cmd(cmd)
    # Run hadd for each systematic
    all_systematics = [f[:f.find("2026")-1] for f in summary['outfiles'].value ] 
    unique_systematics = np.unique(lst)
    for syst in unique_systematics:
        outname = f'{summaryPath}merged_{syst}_{eosdir}.root'
        eos_filesearch = f"`xrdfsls -u /store/user/honor/skims/{eosdir} | grep \'{syst}.*\.root\'`"
        cmd = ['hadd', newname, eos_filesearch]
        print(cmd)
        #res = merge(cmd)
        # if failed bc too much to merge, divide filelist into multiple

if __name__=="__main__":
    parser = ArgumentParser("Merge skim .root files from EOS into nobackup")
    parser.add_argument("summaryFile", help="location of the summary .coffea file")
    parser.add_argument("eosdir", help='name of the directory on EOS containing the skims')
    args = parser.parse_args()

    merge_prep(args.summaryFile, args.eosdir)