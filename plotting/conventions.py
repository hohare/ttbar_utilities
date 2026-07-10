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
    "Unmatchable": colors10[9],
    "Wrong": colors10[7],
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
    'deltaR': r'\Delta r',
    'deltay_abs': r'|y_1-y_2}',
    'delta_yabs': r'|y_1|-|y_2|',
    'deltaphi': r'\Delta\phi',
}

units = {
    'pt': r'[GeV]',
    'ptlow': r'[GeV]',
    'pthigh': r'[GeV]',
    'eta': '',
    'phi': '',
    'mass': r'[GeV]',
    'rapidity':'',
    'rapidity_abs':''
}

objects = {
    'ttbar': r't\bar{t}',
    'hadt' : 't_{h}',
    'lept' : r't_{\mathscr{l}}',
    'hadW' : r'W_{h}',
    'lepW' : r'W_{\mathscr{l}}',
    'HadB': r'b_{h}',
    'LepB': r'b_{\mathscr{l}}',
    'Wup': r'W_{up}',
    'Wdn': r'W_{down}',
    'Lepton' : r'\mathscr{l}',
    'Nu': '\nu',
    'MET' : r'MET',
    'leadingJet': r'\mathrm{leading \: jet}',
    'subleadingJet': r'\mathrm{subleading \: jet}',
    'H_T': r'H_T',
    'S_T': r'S_T',
    # break point
    'lep_HadB': '\mathscr{l},b_h',
    'lep_LepB': '\mathscr{l},b_\mathscr{l}',
    'lep_Wdn': '\mathscr{l},W_{dn}',
    'lep_Wup': '\mathscr{l},W_{up}',
    'hadt_lept': 't_{h},t_{\mathscr{l}}',
    'lepWdn': '\mathscr{l},W_{down}',
    'lephadB': '\mathscr{l},t_{h}',
    'leplepB': '\mathscr{l},t_{\mathscr{l}}',
    'hadTlepT': 't_{h},t_{\mathscr{l}}',
    'hadBlepB': 'b_{h},b_{\mathscr{l}}',
    'lepTlepB': 't_{h},b_{\mathscr{l}}',
    'lepThadB': 't_{h},b_{h}',
}

def get_axisname(var, obj):
    if obj=='phi':  return 'phi MET'
    index = list(objects.keys()).index(obj)
    if var.startswith('delta'):
        return r'$'+variables[var]+'('+objects[obj]+')$ '
    else:
        return r'$'+variables[var]+'^{('+objects[obj]+')}$ ' + units[var]