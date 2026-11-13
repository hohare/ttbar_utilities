import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplhep as mh
from ttbar_utilities.plotting.conventions import get_colors, sideband_map, dataset2label
from ttbar_utilities.inputs.xsecs import lumis

plt.rcParams.update({
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
    "axes.labelsize": 16,
    "legend.title_fontsize": 16
})

# plot mc and data for already integrated histograms
def plot_histogram_list(histograms, mc_datasets, sideband, year, era, blinded=True):
    """
    Plots already integrated histograms as specified by process and sideband region
    Inputs:
    - histograms: a Hist object with axes variable, dataset, sideband
    - mc_datasets: list of which datasets (aka process groups) to plot
    - sideband: which sideband to plot
    - blinded: whether to be blind data in the signal region
    Returns:
    - fig: matplotlib Figure
    - axes: list of matplotlib axes with structure [main axis, ratio axis]
    """
    luminosity = lumis[year][era]
    mc_list = []
    mc_labels = []
    for ds in mc_datasets:
        mc_list.append(histograms[{'dataset':ds}])
        if ds in dataset2label:
            mc_labels.append(dataset2label[ds])
        else:
            mc_labels.append(ds)
    
    fig, axes = plt.subplots(2, 1, figsize=(7,5), sharex=False, gridspec_kw={"height_ratios": (3, 1), "wspace":0})
    if blinded:
        mh.histplot(mc_list, histtype='fill',label=mc_labels, stack=True, ax=axes[0],
                    color=get_colors(mc_datasets))
        mh.cms.label("Preliminary", fontsize=16, lumi=round(luminosity,1), ax=axes[0], loc=0, data=False)
    else:
        #if not blinded, can plot data
        data = histograms[{'dataset': 'data'}]
        try:
            fig, ax_main, ax_comp = mh.comp.data_model(data, 
                                                       stacked_components=mc_list,
                                                       stacked_labels=mc_labels,
                                                       stacked_colors=get_colors(mc_datasets),
                                                       fig=fig, ax_main=axes[0], ax_comparison=axes[1],
                                                       )
            axes = [ax_main, ax_comp]
        except:
            print("Failed data-model comparison for ?", )
        #axes[0].set_ylim(0, data.values().max())
        mh.cms.label("Preliminary", fontsize=12, lumi=round(luminosity,1), ax=axes[0], loc=0, data=True)

    axes[0].set_xlabel('')
    #axes[1].tick_params(axis='x', labelbottom=True)
    axes[1].set_ylabel('Data/MC')#, fontsize=16)
    axes[1].tick_params(axis="both", which="minor",labelbottom=True)


    axes[0].legend(title=f'CR: {sideband_map[str(sideband)]}', 
                   ncols=round(len(mc_labels)/4), frameon=True)


    return fig, axes, mc_labels