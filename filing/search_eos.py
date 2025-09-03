import os
import subprocess as sub
import argparse

def run_cmd(cmd):
    p = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.PIPE)
    output, errors = p.communicate()
    if errors: raise RuntimeError('find crashed with error: %s' %errors)
    output = output.decode()
    return output

def search_eos(prefix, search_dir):
    """Searches for files in search_dir at EOS location"""
    if "fnal" in prefix: search_dir="/eos/uscms"+search_dir
    cmd = ['eos', prefix, 'find', search_dir]
    #print("Running cmd:"," ".join(cmd))
    output = run_cmd(cmd)
    
    flist = output.split('\n')[:-1]
    root_flist = [f.replace('/eos/uscms','') for f in flist if f.endswith(".root")]
    return root_flist

def move_eos(src_dir, dest_dir, prefix='root://cmseos.fnal.gov/'):
    """Move files from fnal EOS to EOS"""
    # getting file list
    flist = search_eos(prefix, src_dir)
    # making destination directory
    tmp = src_dir[::-1]
    find = tmp.find("/")
    newend = tmp[:find][::-1]+"/0000/"
    dest_dir = os.path.join(dest_dir, newend)
    cmd = ['eos', prefix, 'mkdir -p', dest_dir]
    #print("Running cmd:"," ".join(cmd))
    output = run_cmd(cmd)
    # moving files
    for f in flist:
        cmd = ['eos', prefix, 'mv', f, dest_dir]
        #print("Running cmd:"," ".join(cmd))
        output = run_cmd(cmd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='You can customize your run')
    parser.add_argument("src_dir")
    parser.add_argument('-p', '--prefix', default='root://cmseos.fnal.gov/')
    parser.add_argument('-s','--search', default=False, action='store_true')
    parser.add_argument('-m','--move', default=False, action='store_true')
    parser.add_argument('-d','--dest_dir')
    args = parser.parse_args()

    if args.search:
        flist = search_eos(args.prefix, args.src_dir)
    elif args.move:
        move_eos(args.src_dir, args.dest_dir, args.prefix)