import yaml

settings = {
    "mu": ['TOT', 'NonTRIG', 'IDtot', 'IDstat', 'IDsyst', 'RECOtot', 'RECOstat', 'RECOsyst', 'TRIGtot', 'TRIGstat', 'TRIGsyst', 'ISOtot', 'ISOstat', 'ISOsyst'],
    "el": ['TOT', 'NonTRIG', 'ID', 'RECO', 'TRIG'],
    "L1PreFiring" : ["ECAL", "Muon_Stat","Muon_Syst"],
    #"Pileup": ["Pileup"],
    #"jetPuId": ["jetPuId"],
    "Btag": ["bc", "light", 
         "bc_correlated","bc_uncorrelated",
         "light_correlated","light_uncorrelated"
        ],
    "FactRenorm": ["Factor","Renorm","Same","OppositeR"],
    "TTbar_FactRenorm": ["Factor","Renorm","Same","OppositeR"],
    "ST_FactRenorm": ["Factor","Renorm","Same","OppositeR"],
    "JEC": None,
}

def add_systematic(syst, data, debug=False):
    # No variation
    if not data[syst]:
        if debug: print('No variation', syst, data[syst])
        return []
    # Sub-variation
    elif syst in settings:
        if data[syst] in settings[syst]:#one specific subvariation
            if debug: print('one variation',syst, data[syst])
            if syst=='L1PreFiring': 
                [syst+data[syst]+"Up", syst+data[syst]+"Down"]
            else: 
                return [syst+"_"+data[syst]+"Up", syst+"_"+data[syst]+"Down"]
        elif data[syst]=='all':#all subvariations
            if debug: print('all variations',syst, data[syst])
            lst = []
            for key in settings[syst]:
                if syst=='FSR' or syst=='jetPuId' or syst=='Pileup':
                    lst += [syst+key+"Up", syst+key+"Down"]
                else:
                    lst += [syst+"_"+key+"Up", syst+"_"+key+"Down"]
            return lst
        else:# collective shift of multiple subvariations
            return [f'{syst}_TOTUp', f'{syst}_TOTDown']
    # Basic variation that only has up and down shifts
    elif syst:
        if debug: print('basic variation',syst, data[syst])
        return [syst+"Up", syst+"Down"] 
    else:
        print('Unknown variation procedure')
        return []

def parse_systematics(fname):
    with open(fname, "r") as f:
        data = yaml.safe_load(f)

    syst_list = []
    for key in data:
        if "JES" in key or "JER" in key: continue
        elif "hdamp" in key: continue
        elif "PDF" in key: continue
        elif "L1PreFiring" in key: continue #temporary until rerun 2016skims
        res = add_systematic(key, data)
        if key=="mu" or key=="el": res=["Lepton_"+k for k in res]
        syst_list += res
        
    return syst_list
