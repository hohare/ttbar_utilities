
data = {
    "2018": [
        ""
    ],
    "2017": {
        "2017": [
                "data_Run2017B_SingleMuon","data_Run2017B_SingleElectron",
                "data_Run2017C_SingleMuon","data_Run2017C_SingleElectron",
                "data_Run2017D_SingleMuon","data_Run2017D_SingleElectron",
                "data_Run2017E_SingleMuon","data_Run2017E_SingleElectron",
                "data_Run2017F_SingleMuon","data_Run2017F_SingleElectron",
            ],
        "B": ["data_Run2017B_SingleMuon","data_Run2017B_SingleElectron"],
        "C": ["data_Run2017C_SingleMuon","data_Run2017C_SingleElectron"],
        "D": ["data_Run2017D_SingleMuon","data_Run2017D_SingleElectron"],
        "E": ["data_Run2017E_SingleMuon","data_Run2017E_SingleElectron"],
        "EF": ["data_Run2017E_SingleMuon","data_Run2017E_SingleElectron", "data_Run2017F_SingleMuon","data_Run2017F_SingleElectron"],
        "F": ["data_Run2017F_SingleMuon","data_Run2017F_SingleElectron"],
    },
    "2016preVFP": [
        "Data_2016_RunFhimp_SingleElectron",
        "Data_2016_RunEhimp_SingleElectron",
        "Data_2016_RunDhimp_SingleElectron",
        "Data_2016_RunChimp_SingleElectron",
        "Data_2016_RunBver2himp_SingleElectron",
        "Data_2016_RunFhimp_SingleMuon",
        "Data_2016_RunEhimp_SingleMuon",
        "Data_2016_RunDhimp_SingleMuon",
        "Data_2016_RunChimp_SingleMuon",
        "Data_2016_RunBver2himp_SingleMuon"
    ],
    "2016postVFP": [
        "Data_2016_RunF_SingleElectron",
        "Data_2016_RunG_SingleElectron",
        "Data_2016_RunH_SingleElectron",
        "Data_2016_RunF_SingleMuon",
        "Data_2016_RunG_SingleMuon",
        "Data_2016_RunH_SingleMuon",
    ]
}

ttbar_sl = ["Correct","Wrong","Unmatchable","merged","tau"]#["TTToSemiLeptonic"]
ttbar_dilep = ['TTTo2L2Nu', 'TTTo2L2Nu_TuneCP5']
ttbar = ttbar_sl+ttbar_dilep
ST = [
    "ST_t-channel_top_4f_InclusiveDecays",
    "ST_t-channel_antitop_4f_InclusiveDecays",
    "ST_s-channel_4f_leptonDecays"
]
tW = [
    "ST_tW_top_5f_NoFullyHadronicDecays",
    "ST_tW_antitop_5f_NoFullyHadronicDecays"
]
WJets = [
    "WJetsToLNu_HT-70To100",
    "WJetsToLNu_HT-100To200",
    "WJetsToLNu_HT-200To400",
    "WJetsToLNu_HT-400To600",
    "WJetsToLNu_HT-600To800",
    "WJetsToLNu_HT-800To1200",
    "WJetsToLNu_HT-1200To2500",
    "WJetsToLNu_HT-2500ToInf"
]
DY = ["DYJetsToLL"]
MISC = ["WW", "WZ", "ZZ", "TZToQQ"]
TTX = ["TTZToLLNuNu_M-10", "TTWJetsToLNu", "TTWJetsToQQ"]
QCD = [
    "QCD_Pt-30to50_EMEnriched",    #spikes 
    "QCD_Pt-50to80_EMEnriched",    #spikes
    "QCD_Pt-80to120_EMEnriched",
    "QCD_Pt-120to170_EMEnriched", #problematic central?
    "QCD_Pt-170to300_EMEnriched",  
    "QCD_Pt-20To30_MuEnrichedPt5", #no events from this so not in axis
    "QCD_Pt-30To50_MuEnrichedPt5", #spikes
    "QCD_Pt-50To80_MuEnrichedPt5",
    "QCD_Pt-80To120_MuEnrichedPt5",
    "QCD_Pt-120To170_MuEnrichedPt5",
    "QCD_Pt-170To300_MuEnrichedPt5",
    "QCD_Pt-300To470_MuEnrichedPt5",
    "QCD_Pt-470To600_MuEnrichedPt5",
    "QCD_Pt-600To800_MuEnrichedPt5",
    "QCD_Pt-800To1000_MuEnrichedPt5",
    "QCD_Pt-1000_MuEnrichedPt5"
]
EW = WJets+DY+MISC+TTX

def get_grouping(year, era):
    grouping = {
        "data": data[year][era],
        "Correct": ["Correct"],
        "Wrong": ["Wrong"],
        "Unmatchable": ["Unmatchable"],
        "merged": ["merged"],
        "tau": ["tau"],
        "tt SL": ttbar_sl,
        "tt DL": ttbar_dilep,
        "TTbar": ttbar_sl+ttbar_dilep,
        "Single Top": ST+tW,
        "tW": tW,
        "W+jets": WJets,
        "DY": DY,
        "Misc": MISC + TTX + DY,
        "non-EW/QCD": ttbar+ST,
        "EW (sim)": EW,
        "QCD (sim)": QCD,
        "EW+QCD (Data-Driven)": [],
        "EW+QCD (sim)": EW+QCD,
    }
    print(grouping['data'])
    return grouping