import numpy as np
import hist

def get_ratio_from_np(denom, numer, density=False):
    """If plotted both using plt.hist"""
    bins = denom[1]
    if density:
        nHistEft = (denom[0]/(sum(denom[0])*np.diff(bins)))
        ratio = np.ones(nHistEft.shape)
        ratio[nHistEft != 0] = numer[0][nHistEft != 0]/nHistEft[nHistEft != 0]
    else: 
        nHistEft = denom[0]
        mask = (nHistEft != 0) 
        ratio = np.ones(nHistEft.shape)
        ratio[mask] = numer[0][mask]/nHistEft[mask]

    return ratio

def get_ratio_from_histEFT():
    """If plotted denom using histEFT"""
    return 0