import json
lumis = json.load(open('ttbar_utilities/inputs/luminosity_in_fb.json'))

# Trusting Joseph's AN Appendix A
# in pb
xsecs = {
    "dim6top": 366.3580,
    "TTbar_SL": 366.3580,
    "TTToSemiLeptonic": 366.3580,
    "TTTo2L2Nu": 88.5193,
    "TTToSemiLeptonic_TuneCP5": 366.3580,
    "TTTo2L2Nu_TuneCP5": 88.5193,
    "TTToHadronic_TuneCP5": 379.0647,
    "WJetsToLNu_HT-70To100": 1443.6560,
    "WJetsToLNu_HT-100To200": 1434.5189,
    "WJetsToLNu_HT-200To400": 383.1856,
    "WJetsToLNu_HT-400To600": 51.6815,
    "WJetsToLNu_HT-600To800": 12.5292,
    "WJetsToLNu_HT-800To1200": 5.6341,
    "WJetsToLNu_HT-1200To2500": 1.3249,
    "WJetsToLNu_HT-2500ToInf": 0.0093,
    
    "WJetsToLNu70": 1443.6560,
    "WJetsToLNu100": 1434.5189,
    "WJetsToLNu200": 383.1856,

    "DYJetsToLL": 6077.22,
    "ST_s-channel": 3.45,
    "ST_s-channel_4f_leptonDecays": 3.45,
    "ST_t-channel_top_4f_InclusiveDecays": 136.02,
    "ST_t-channel_antitop_4f_InclusiveDecays": 80.95,
    "ST_tW_antitop_5f_NoFullyHadronicDecays": 19.466,
    "ST_tW_top_5f_NoFullyHadronicDecays": 19.466,
    "ST_t-channel_top_4f": 136.02,
    "ST_t-channel_antitop_4f": 80.95,
    "ST_t-channel_top": 136.02,
    "ST_t-channel_antitop": 80.95,
    "ST_tW_antitop_5f": 19.466,
    "ST_tW_top_5f": 19.466,

    "QCD_Pt-30to50_EMEnriched": 6396000.,
    "QCD_Pt-50to80_EMEnriched": 1989000.,
    "QCD_Pt-80to120_EMEnriched": 376500.,
    "QCD_Pt-120to170_EMEnriched": 666490.,
    "QCD_Pt-170to300_EMEnriched": 16480.,
    "QCD_Pt-300toInf_EMEnriched": 1099.,

    "QCD_Pt-20To30_MuEnrichedPt5": 2526000.0,
    "QCD_Pt-30To50_MuEnrichedPt5": 1362000.0,
    "QCD_Pt-50To80_MuEnrichedPt5": 376600.0,
    "QCD_Pt-80To120_MuEnrichedPt5": 88930.0,
    "QCD_Pt-120To170_MuEnrichedPt5": 21230.0,
    "QCD_Pt-170To300_MuEnrichedPt5": 7055.0,
    "QCD_Pt-300To470_MuEnrichedPt5": 619.3,
    "QCD_Pt-470To600_MuEnrichedPt5": 759.24,
    "QCD_Pt-600To800_MuEnrichedPt5": 18.21,
    "QCD_Pt-800To1000_MuEnrichedPt5": 3.275,
    "QCD_Pt-1000_MuEnrichedPt5": 1.078,

    "WZ": 27.6,
    "WW": 118.7,
    "ZZ": 12.14,
    "TTWJetsToLNu": 0.2149,
    "TTWJetsToQQ": 0.4316,
    "TTZToLLNuNu_M-10": 0.2432,
    "TTZToQQ": 0.5104
}

def lumixsec_scaling(year, sample, sum_of_weights, isEFT):
    """Find scaling of histogram by luminosity and event type cross-section"""
    for x in xsecs.keys():
        if sample.startswith(x): 
            xsec = xsecs[x]
            break
    return 1e3*lumis[year][year]*xsec / sum_of_weights

def xsec_scaling(sample, sum_of_weights, isEFT):
    for x in xsecs.keys():
        if sample.startswith(x): 
            xsec = xsecs[x]
            break
    return xsec / sum_of_weights
    