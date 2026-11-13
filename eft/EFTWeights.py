import numpy as np
import awkward as ak
import time

# Ordering of WCs. Can be changed for your convention
wcs = [
    'cSM',
    'cQd1', 
    'ctj1', 
    'cQj31', 
    'ctj8', 
    'ctd1', 
    'ctd8', 
    'ctGRe', 
    'ctGIm', 
    'cQj11', 
    'cQj18', 
    'ctu8', 
    'cQd8', 
    'ctu1', 
    'cQu1', 
    'cQj38', 
    'cQu8'
]

def strnum2float(num: str):
    return float(num.replace("m", "-").replace("p", "."))
def float2strnum(num: float):
    """Rewrite decimal as str notation"""
    mystr = ""
    if num<0: 
        mystr += "m"
        num = abs(num)
    mystr += str(int(num)%10)
    mystr += "p"
    mystr += str(int(num%1 *1e4)).strip("0")
    return mystr
    
def vec(S):
    """Why do this?"""
    # Acquiring upper triangle of array
    j, i = np.tril_indices(S.shape[-1])
    # Replacing diagonal with 1, all others 2
    scale = np.where(i == j, 1.0, np.sqrt(2))
    return S[..., i, j] * scale

def mat(s, n=None):
    """Inverse of vec() operation"""
    if n is None:
        l = s.shape[-1]
        n = int(0.5 * (np.sqrt(1 + 8 * l) - 1))
    S = np.empty(s.shape[:-1] + (n, n))
    j, i = np.tril_indices(n)
    #scaled = np.where(i == j, 1.0, 0.5) * s
    scaled = np.where(i == j, 1.0, 1.0) * s
    S[..., i, j] = scaled
    S[..., j, i] = scaled
    return S

def get_points(lines):
    """Convert reweighting strings to array"""
    prefix = 'EFTrwgt'
    reweightpoints=[]
    reweightnumber=[]
    nweight = -2
    for wname in lines:
        nweight += 1
        if wname == "sm_point":
            #print(nweight)
            continue
            vector = np.zeros(len(wcs))
            vector[wcs.index("cSM")] = 1.0
            reweightpoints.append(vector)
        elif wname.startswith(prefix):
            i = wname.find("_")
            #num = wname[:i].replace(prefix,"")
            rwpoint = wname[i+1:]
            
            vector = np.zeros(len(wcs))
            vector[wcs.index("cSM")] = 1.0
    
            rwpoint = rwpoint.split("_")
            for name, value in zip(rwpoint[::2], rwpoint[1::2]):
                fval = strnum2float(value)
                vector[wcs.index(name)] = fval
            reweightpoints.append(vector)
            reweightnumber.append(nweight)
    reweightpoints_array = np.array(reweightpoints)
    reweightnumber_array = np.array(reweightnumber)
    return reweightpoints_array, reweightnumber_array

def parse_rwgt_card(cardpath, saveReweightNames=False):
    with open(cardpath, "r") as file:
        wholefile = file.read()
    
    lines = wholefile.split('\n')
    lines = [l.replace('launch --rwgt_name=','') for l in lines if l.startswith('launch')]
    pts, indexes = get_points(lines)
    if saveReweightNames:
        import json
        dct = {int(index): list(point) for index, point in zip(indexes, pts)}
        with open("rwgt_card.json", "w") as f:
            json.dump(dct, f, indent=4)
    
    return pts, indexes, dct

def get_structure_constant_mapping(wc_ordering):
    j,i = np.tril_indices(len(wc_ordering))
    J = list(map(lambda x: wc_ordering[x], j))
    I = list(map(lambda x: wc_ordering[x], i))
    return list(zip(I,J))
def get_pair(wc1, wc2, wc_ordering=wcs):
    pairs = get_structure_constant_mapping(wc_ordering)
    try:
        index = pairs.index((wc1, wc2))
    except:
        index = pairs.index((wc2, wc1))
    return index

def calculate_structure_constants(rwgt_point_mapping, weights):
    # Acquiring which weight indexes are valid for this and their corresponding WC settings
    reweight_names = np.array(list(rwgt_point_mapping.keys()), dtype=int)
    reweightpoints_array = np.array(list(rwgt_point_mapping.values()))
    # Acquiring a weighted lower triangle built from products of wc pairs
    reweightpoints_outer = vec(reweightpoints_array[:, :, None] * reweightpoints_array[:, None, :])
    # Filling an array with the weights
    weightsvector = np.empty((len(weights), len(reweightpoints_array)))
    for i, reweight_num in enumerate(reweight_names):
        weightsvector[:, i] = weights[:,reweight_num]
    # Solving the system
    x, residuals, rank, s = np.linalg.lstsq(reweightpoints_outer, weightsvector.T, rcond=None)
    
    return x, residuals