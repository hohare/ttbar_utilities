import json
import matplotlib.pyplot as plt
import mplhep as mh
from ttbar_utilities.plotting.conventions import get_colors, sideband_map

luminosity = json.load(open('ttbar_utilities/inputs/luminosity_in_fb.json'))

# plot mc and data for already integrated histograms
def plot_histogram_list(histograms, mc_datasets, sideband, year, blinded=True):
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
    mc_list = []
    mc_labels = []
    for ds in mc_datasets:
        mc_list.append(histograms[{'dataset':ds}])
        mc_labels.append(ds)
    
    fig, axes = plt.subplots(2, 1, figsize=(7,5), sharex=True, gridspec_kw={"height_ratios": (3, 1), "wspace":0})
    if blinded:
        mh.histplot(mc_list, histtype='fill',label=mc_labels, stack=True, ax=axes[0],
                    color=get_colors(mc_datasets))
        axes[1].set_ylabel('Data/MC')
        mh.cms.label("Preliminary", fontsize=16, lumi=round(luminosity[year],1), ax=axes[0], loc=0, data=False)
    else:
        #if not blinded, can plot data in the signal region (sideband=0)
        data = histograms[{'dataset': 'data'}]
        fig, ax_main, ax_comp = mh.comp.data_model(data, 
                                                   stacked_components=mc_list,
                                                   stacked_labels=mc_labels,
                                                   stacked_colors=get_colors(mc_datasets),
                                                   fig=fig, ax_main=axes[0], ax_comparison=axes[1],
                                                  )
        axes = [ax_main, ax_comp]
        mh.cms.label("Preliminary", fontsize=16, lumi=round(luminosity[year],1), ax=axes[0], loc=0, data=True)

    axes[0].set_xlabel('')

    axes[0].legend(title=f'CR: {sideband_map[str(sideband)]}', title_fontsize=16, 
                   fontsize=10, ncols=round(len(mc_labels)/4), frameon=True)

    return fig, axes