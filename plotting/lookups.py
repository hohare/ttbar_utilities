import hist
import numpy as np
import mplhep as hep
import matplotlib.pyplot as plt

def plotLookup(lookup, **kwargs):
    """Plot a coffea lookup table for 1 or 2 dimensions"""
    axes = lookup._axes
    vals = lookup._values

    fig, ax = plt.subplots(figsize=(4,4))
    if vals.ndim==1:
        print("plotting 1-D histogram with mplhep")
        hep.histplot(vals[:-1], axes)
    elif vals.ndim==2:
        print("plotting 2-D histogram with mplhep")
        hep.hist2dplot(vals, xbins=axes[0], ybins=axes[1], flow=None)
    else:
        print("histogram has more than 2 dimensions")
        del fig, axes
        return None, vals
    
    if "xlabel" in kwargs.keys(): ax.set_xlabel(kwargs["xlabel"])
    if "ylabel" in kwargs.keys(): ax.set_ylabel(kwargs["ylabel"])
    if "xlim" in kwargs.keys(): ax.set_xlim(kwargs["xlim"])
    if "ylim" in kwargs.keys(): ax.set_ylim(kwargs["ylim"])

    return axes, vals

def printCorrSet(cset):
    for corr in cset.values():
        print(f"Correction {corr.name} has {len(corr.inputs)} inputs")
        for ix in corr.inputs:
            print(f"   Input {ix.name} ({ix.type}): {ix.description}")
def printCorr(corr):
    print(f"Correction {corr.name} has {len(corr.inputs)} inputs")
    for ix in corr.inputs:
        print(f"   Input {ix.name} ({ix.type}): {ix.description}")

def plotCorr(corr, obj, x_lim, y_lim, WP='T', setting='nom', vlim=None):
    """Plot a 2-D correctionlib correction"""
    xs  = np.linspace(x_lim[0],  x_lim[1],  x_lim[2],  endpoint=False)
    ys = np.linspace(y_lim[0], y_lim[1], y_lim[2], endpoint=False)

    x,y = np.meshgrid(xs, ys)
    if obj=='jet': res = corr.evaluate(np.ravel(y), np.ravel(x), setting, WP)
    elif obj=='mu': res = corr.evaluate(abs(np.ravel(y)), np.ravel(x), syst)
    elif obj=='jetveto': res = corr.evaluate(setting, x, y)# etas and phis
    unflat = np.reshape(res, x.shape)

    fig, ax = plt.subplots()
    res = ax.pcolormesh(x,y,unflat, vmin=0.8, vmax=1.2)
    fig.colorbar(res)
    ax.set_title(setting)

    return fig, ax
