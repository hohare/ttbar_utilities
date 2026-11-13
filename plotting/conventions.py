ttbar = r't\bar{t}'
HadT = r't_{h}'
LepT = r't_{\mathscr{l}}'
HadW = r'W_{h}'
LepW = r'W_{\mathscr{l}}'
HadB = r'b_{h}'
LepB = r'b_{\mathscr{l}}'
Wup = r'W_{up}'
Wdn = r'W_{down}'
Lepton = r'\mathscr{l}'
Nu = r'\nu'


import matplotlib.pyplot as plt
plt.rcParams.update({
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
    "axes.labelsize": 16,
    "legend.title_fontsize": 16
})

###############
# PLOT COLORS #
###############
# Recommended colors by CMS
colors = ["#5790fc", "#f89c20", "#e42536", "#964a8b", "#9c9ca1", "#7a21dd"]
colors10 = ["#3f90da","#ffa90e", "#bd1f01", "#94a4a2", "#832db6", "#a96b59", "#e76300", "#b9ac70","#717581","#92dadd"]
# Mapping dataset groupings to a color in order to be consistent
dataset2color = {
    "TTbar": colors[0],
    "tt SL": colors[0],
    "tt DL": colors[5],
    "Single Top": colors[1],
    "EW (sim)": colors[2], 
    "QCD (sim)": colors[3],
    # longer format
    "Correct": colors10[0],
    "Wrong": colors10[7],
    "Unmatchable": colors10[9],
    "merged": colors10[3],
    "tau": colors10[8],
    # slightly broken down categories
    "W+jets": colors[2],
    "EW+QCD (Data-Driven)": colors[3],
    "Misc": colors10[5],
    "tt Had": colors10[6]
}

def get_colors(dataset_list):
    """Retrieve colors corresponding to input list of datasets"""
    return[dataset2color[ds] for ds in dataset_list]


####################
# DATASET TO LABEL #
####################

dataset2label = {
    "TTbar": r'$'+ttbar+'$',
    "Single Top": "Single top quark",
}


#############
# SIDEBANDS #
#############

sideband_map = {
    "signal": 0,
    "central": 2,
    "up": 1,
    "down": 3,
    "0": "signal",
    "1": 'B (up)',
    "2": 'C (nominal)',
    "3": 'D (down)'
}

##############
# AXES NAMES #
##############
variables = {
    'pt': 'p_T',
    'ptlow': 'p_T',
    'pthigh': 'p_T',
    'mass': r'm',
    'eta': r'\eta',
    'phi': r'\phi',
    'rapidity': 'y',
    'rapidity_abs': '|y|',
    'rapidityAbs': '|y|',
    'deltaR': r'\Delta r',
    'deltay_abs': r'\lvert y_1-y_2\rvert',
    'delta_yabs': r'\lvert y_1\rvert -\lvert y_2| \rvert',
    'deltaphi': r'\Delta\phi',
    'discrim': r'\lambda',
    'ctstar': r'\cos(\theta^{*})'
}

units = {
    'pt': r'[GeV]',
    'ptlow': r'[GeV]',
    'pthigh': r'[GeV]',
    'eta': '',
    'phi': '',
    'mass': r'[GeV]',
    'rapidity':'',
    'rapidity_abs':'',
    'ctstar': ''
}

objects = {
    'joint': '',
    'mass': r'_{m}',
    'nu': r'_{\nu}',
    'ttbar': ttbar,
    'hadt' : HadT,
    'lept' : LepT,
    'HadT' : HadT,
    'LepT' : LepT,
    'hadW' : HadW,
    'lepW' : LepW,
    'HadW' : HadW,
    'LepW' : LepW,
    'HadB': HadB,
    'LepB': LepB,
    'Wup': Wup,
    'Wdn': Wdn,
    'Lepton' : Lepton,
    'Nu': Nu,
    'MET' : r'MET',
    'leadingJet': r'\mathrm{leading \: jet}',
    'subleadingJet': r'\mathrm{subleading \: jet}',
    'HT': r'H_T',
    'ST': r'S_T',
    # break point
    'lep_HadB': r'\mathscr{l},b_h',
    'lep_LepB': r'\mathscr{l},b_\mathscr{l}',
    'lep_Wdn': r'\mathscr{l},W_{dn}',
    'lep_Wup': r'\mathscr{l},W_{up}',
    'hadt_lept': r't_{h},t_{\mathscr{l}}',
    'lepWdn': r'\mathscr{l,W_{down}',
    'lephadB': r'\mathscr{l},t_{h}',
    'leplepB': r'\mathscr{l},t_{\mathscr{l}}',
    'hadTlepT': r't_{h},t_{\mathscr{l}}',
    'hadBlepB': r'b_{h},b_{\mathscr{l}}',
    'lepTlepB': r't_{h},b_{\mathscr{l}}',
    'lepThadB': r't_{h},b_{h}',
}

def get_axisname(var, obj):
    if obj=='phi':  return 'phi MET'
    #index = list(objects.keys()).index(obj)
    if var.startswith('delta'):
        return r'$'+variables[var]+'('+objects[obj]+')$ '
    elif var == 'discrim':
        return r'$'+variables[var]+objects[obj]+'$ '
    else:
        return r'$'+variables[var]+'^{('+objects[obj]+')}$ ' + units[var]


########
# XLIM #
########
