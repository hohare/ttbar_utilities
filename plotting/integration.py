import hist
    
# Integration dictionaries to plot key0_key1 from histo[key0] with axis Object=key1
default_mapping = {
    "leptype": sum,
    "systematic": "nominal",
    "WC": "allWC_0"
}
# Potential groups of datasets to plot
ttbar_datasets = ['Correct','Unmatchable','Wrong','merged','tau']
processes = {
    "datadriven": ttbar_datasets+['tt DL','Single Top','EW+QCD (Data-Driven)'],
    "process": ['tt SL','tt DL','Single Top','W+jets', 'Misc', 'QCD (sim)'],
    "process_ttSL": ttbar_datasets+['tt DL','Single Top','W+jets','Misc', 'QCD (sim)'],
    "process_EW": ['tt SL','tt DL','Single Top','EW (sim)', 'QCD (sim)'],
    "simple": ['TTbar','Single Top', 'EW (sim)', 'QCD (sim)'],
    "EWQCD_estimation": ['TTbar','Single Top', 'EW+QCD (Data-Driven)'],
    "preEWQCD_estimation": ['TTbar','Single Top', 'W+jets','Misc', 'QCD (sim)']
}

def complete_integration(histograms, distribution, **kwargs):
    """Integrate histogram based on input distribution key and object from the Object axis
    Inputs:
    - histograms: dictionary of hist histograms
    - distribution: 
        - which distribution to use of all available histograms
        - or which combination of [distribution]_[object_type]
    - object_type: which choice to use from within the Object axis
    Outputs:
    - a hist histogram that only has the "variable", "Sideband", and "dataset" axes
    """
    _split = distribution.split("_")
    histoname = _split[0]
    if "object_type" not in kwargs: kwargs['object_type'] = "_".join(_split[1:])
    # get axes set manually
    integ_dict = {k: kwargs[k] for k in kwargs if k in default_mapping}
    # default axes in every histo
    for key in default_mapping:
        if (key in histograms[_split[0]].axes.name) and (key not in kwargs):
            integ_dict.update({key: default_mapping[key]})
    # axes specific to this histogram
    integ_dict.update({"Object": kwargs['object_type']})
    # perform integration
    result_histo = histograms[histoname][integ_dict]
    return result_histo

def get_histo_list(histograms):
    """Returns list of (distribution, object) available from input dictionary"""
    lst = []
    for key in histograms:
        if key=='addtl_wgt': continue
        try:
            if "Object" in histograms[key].axes.name:
                for obj in histograms[key].axes['Object']:
                    lst.append((key, obj))
            else:
                print(key, 'HAS NO OBJECT')
        except:
            print(f"Can't check {key}")
    return lst
    
def GroupBy(h, oldname, newname, grouping):
    """Convert histo with new axis name and groupings"""
    # add new group axis and copy the old histogram axes and storage type
    hnew = hist.Hist(
        hist.axis.StrCategory(grouping, name=newname),
        *(ax for ax in h.axes if ax.name != oldname),
        storage=h.storage_type(),
    )
    # integrate each group and save under new name
    oldContents = h.axes[oldname]
    for name, indices in enumerate(grouping.values()):
        newContents = [dataset for dataset in indices if dataset in oldContents]
        hnew.view(flow=True)[name] = h[{oldname: newContents}][{oldname: sum}].view(flow=True)
    return hnew