from numpy import NaN
from wonambi import Data
from .surf import plot_surf


def plot_prf_results(result, param, channels, electrodes, surf, rsquared_threshold=0.05):
    val = result[param].copy()
    val[result['rsquared'] < rsquared_threshold] = NaN
    dat = Data(val, s_freq=1, chan=channels)

    return plot_surf(dat, electrodes, pial=surf, info='finger')
