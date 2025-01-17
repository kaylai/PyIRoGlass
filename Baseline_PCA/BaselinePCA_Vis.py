# %% -*- coding: utf-8 -*-

""" Created on January 20, 2023 // @author: Sarah Shi for figures"""
import numpy as np
import pandas as pd 

import os
import glob 
from pathlib import Path
from scipy import signal

from matplotlib import pyplot as plt
from matplotlib import rc, cm

%matplotlib inline
%config InlineBackend.figure_format = 'retina'
rc('font',**{'family':'Avenir', 'size': 20})
plt.rcParams['pdf.fonttype'] = 42

plt.rcParams["xtick.major.size"] = 4 # Sets length of ticks
plt.rcParams["ytick.major.size"] = 4 # Sets length of ticks
plt.rcParams["xtick.labelsize"] = 20 # Sets size of numbers on tick marks
plt.rcParams["ytick.labelsize"] = 20 # Sets size of numbers on tick marks
plt.rcParams["axes.titlesize"] = 22
plt.rcParams["axes.labelsize"] = 22 # Axes labels


# %% 

wn_low = 1250
wn_high = 2400

parent_dir = os.path.split(os.getcwd())[0]

bl_i = pd.read_csv('BLi.csv', index_col = 'Wavenumber')
bl_i = bl_i[wn_low:wn_high]

h2o_free = pd.read_csv('H2O_Free.csv', index_col = 'Wavenumber')
h2o_free = h2o_free[wn_low:wn_high]

devol = pd.read_csv('Devolatilized.csv', index_col = 'Wavenumber')
devol = devol[wn_low:wn_high]

dan = pd.read_csv('Dan_Cleaned.csv', index_col = 'Wavenumber')
dan = dan[wn_low:wn_high]

peak1635 = pd.read_csv('1635_PeakBLRemoved.csv', index_col = 'Wavenumber')
peak1635 = peak1635[wn_low:wn_high]

BaselinePCA = pd.read_csv(parent_dir + '/Peak_Fit/InputData/Baseline_Avg+PCA.csv', index_col = 'Wavenumber')
BaselinePCA = BaselinePCA[wn_low:wn_high]

H2OPCA = pd.read_csv(parent_dir + '/Peak_Fit/InputData/Water_Peak_1635_All.csv', index_col = 'Wavenumber')
H2OPCA = H2OPCA[wn_low:wn_high]

def rescale(abs, range): 
    abs_m = abs * (range / np.abs(abs.iloc[0] - abs.iloc[-1]))
    abs_mb = abs_m - abs_m.iloc[-1]
    return abs_mb

def rescale_peak(abs, range): 
    abs_m = abs * (range / np.max(abs))
    abs_mb = abs_m - abs_m.iloc[-1]
    return abs_mb

# %% 

BaselinePCA = pd.read_csv(parent_dir + '/Peak_Fit/InputData/Baseline_Avg+PCA.csv', index_col = 'Wavenumber')
BaselinePCA = BaselinePCA[wn_low:wn_high]

h2o_free_scale = h2o_free.apply(lambda x: rescale(x, 2))

fig, ax = plt.subplots(3, 2, figsize = (13, 16)) 
ax = ax.flatten()
ax[0].plot(np.nan, np.nan, lw = 0, c = None, label = '')
ax[0].plot(h2o_free.index, rescale(bl_i, 2), c = '#171008', lw = 3, label = '$\mathregular{\overline{Baseline_i}}$')
ax[0].plot(h2o_free.index, h2o_free_scale, alpha = 0.5)
ax[0].plot(h2o_free.index, h2o_free_scale.iloc[:, -1], alpha = 0.5, label = 'Devolatilized Spectra, n='+str(np.shape(h2o_free)[1]))
ax[0].plot(h2o_free.index, rescale(bl_i, 2), c = '#171008', lw = 3)
ax[0].annotate("A.", xy=(0.0425, 0.925), xycoords="axes fraction", fontsize=20, weight='bold')
ax[0].legend(loc = (0.03, 0.77), labelspacing = 0.05, handletextpad = 0.5, handlelength = 0.6, prop={'size': 16}, frameon=False)
ax[0].set_xlim([1200, 2450])
ax[0].set_ylim([-0.25, 2.25])
ax[0].tick_params(axis="x", direction='in', length=5, pad = 6.5, labelbottom=False)
ax[0].tick_params(axis="y", direction='in', length=5, pad = 6.5)
ax[0].invert_xaxis()

dan_scale = dan.apply(lambda x: rescale(x, 2))
ax[1].plot(np.nan, np.nan, lw = 0, c = None, label = '')
ax[1].plot(bl_i.index, rescale(bl_i, 2), c = '#171008', lw = 3, label = '$\mathregular{\overline{Baseline_i}}$')
ax[1].plot(dan.index, dan_scale, alpha = 0.5)
ax[1].plot(dan.index, dan_scale.iloc[:, -1], alpha = 0.5, label = '$\mathregular{CO_{3}^{2-}}$ Below Detection Spectra, n='+str(np.shape(dan_scale)[1]))
ax[1].plot(h2o_free.index, rescale(bl_i, 2), c = '#171008', lw = 3)
ax[1].annotate("B.", xy=(0.0425, 0.925), xycoords="axes fraction", fontsize=20, weight='bold')
ax[1].legend(loc = (0.03, 0.77), labelspacing = 0.05, handletextpad = 0.5, handlelength = 0.6, prop={'size': 16}, frameon=False)
ax[1].set_xlim([1200, 2450])
ax[1].set_ylim([-0.25, 2.25])
ax[1].tick_params(axis="x", direction='in', length=5, pad = 6.5, labelbottom=False)
ax[1].tick_params(axis="y", direction='in', length=5, pad = 6.5)
ax[1].invert_xaxis()

peak1635_scale = peak1635.apply(lambda x: rescale_peak(x, 2))
ax[2].plot(np.nan, np.nan, lw = 0, c = None, label = '')
ax[2].plot(H2OPCA.index, rescale_peak(H2OPCA.Average_1630_Peak, 2), c = '#171008', lw = 3, label = '$\overline{\mathregular{H_2O_{m, 1635}}}$')
ax[2].plot(peak1635_scale.index, peak1635_scale, alpha = 0.5)
ax[2].plot(peak1635_scale.index, peak1635_scale.iloc[:, -1], alpha = 0.5, label = '$\mathregular{H_2O_{m, 1635}}$ Spectra, n='+str(np.shape(peak1635)[1]))
ax[2].plot(H2OPCA.index, rescale_peak(H2OPCA.Average_1630_Peak, 2), c = '#171008', lw = 3)
ax[2].annotate("C.", xy=(0.0425, 0.925), xycoords="axes fraction", fontsize=20, weight='bold')
ax[2].legend(loc = (0.03, 0.77), labelspacing = 0.05, handletextpad = 0.5, handlelength = 0.6, prop={'size': 16}, frameon=False)
ax[2].set_xlim([1200, 2450])
ax[2].set_ylim([-0.25, 2.25])
ax[2].tick_params(axis="x", direction='in', length=5, pad = 6.5, labelbottom=False)
ax[2].tick_params(axis="y", direction='in', length=5, pad = 6.5)
ax[2].invert_xaxis()

devol_scale = devol.apply(lambda x: rescale(x, 2))
ax[3].plot(np.nan, np.nan, lw = 0, c = None, label = '')
ax[3].plot(BaselinePCA.index, rescale(BaselinePCA.Average_Baseline, 2), c = '#171008', lw = 3, label = '$\mathregular{\overline{Baseline}}$')
ax[3].plot(devol_scale.index, devol_scale, alpha = 0.5)
ax[3].plot(devol_scale.index, devol_scale.iloc[:, -1], alpha = 0.5, label = 'Peak Stripped Spectra, n='+str(np.shape(devol)[1]))
ax[3].plot(BaselinePCA.index, rescale(BaselinePCA.Average_Baseline, 2), c = '#171008', lw = 3)
ax[3].annotate("D.", xy=(0.0425, 0.925), xycoords="axes fraction", fontsize=20, weight='bold')
ax[3].legend(loc = (0.03, 0.77), labelspacing = 0.05, handletextpad = 0.5, handlelength = 0.6, prop={'size': 16}, frameon=False)
ax[3].set_xlim([1200, 2450])
ax[3].set_ylim([-0.25, 2.25])
ax[3].tick_params(axis="x", direction='in', length=5, pad = 6.5, labelbottom = False)
ax[3].tick_params(axis="y", direction='in', length=5, pad = 6.5)
ax[3].invert_xaxis()

BaselinePCA = pd.read_csv(parent_dir + '/Peak_Fit/InputData/Baseline_Avg+PCA.csv', index_col = 'Wavenumber')
ax[4].plot(np.nan, np.nan, lw = 0, c = None, label = '')
ax[4].plot(BaselinePCA.index, BaselinePCA.Average_Baseline, c = '#171008', lw = 3, label = '$\mathregular{\overline{Baseline}}$')
ax[4].plot(BaselinePCA.index, BaselinePCA.PCA_1, c = '#0C7BDC', lw = 2, label = '$\mathregular{\overline{Baseline}_{PC1,}}$79% exp var')
ax[4].plot(BaselinePCA.index, BaselinePCA.PCA_2, c = '#E42211', lw = 2, label = '$\mathregular{\overline{Baseline}_{PC2,}}$15% exp var')
ax[4].plot(BaselinePCA.index, BaselinePCA.PCA_3, c = '#5DB147', lw = 2, label = '$\mathregular{\overline{Baseline}_{PC3,}}$ 4% exp var')
ax[4].plot(BaselinePCA.index, BaselinePCA.PCA_4, c = '#F9C300', lw = 2, label = '$\mathregular{\overline{Baseline}_{PC4,}}$ 1% exp var')
ax[4].annotate("E.", xy=(0.0425, 0.925), xycoords="axes fraction", fontsize=20, weight='bold')
ax[4].legend(loc = (0.03, 0.55), labelspacing = 0.05, handletextpad = 0.5, handlelength = 0.6, prop={'size': 16}, frameon=False)
ax[4].set_xlim([1200, 2450])
ax[4].tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax[4].tick_params(axis="y", direction='in', length=5, pad = 6.5)
ax[4].invert_xaxis()

ax[5].plot(np.nan, np.nan, lw = 0, c = None, label = '')
ax[5].plot(H2OPCA.index, H2OPCA.Average_1630_Peak, c = '#171008', lw = 3, label = '$\mathregular{\overline{H_2O_{m, 1635}}}$')
ax[5].plot(H2OPCA.index, H2OPCA['1630_Peak_PCA_1'], c = '#0C7BDC', lw = 2, label = '$\mathregular{\overline{H_2O_{m, 1635}}_{PC1,}}$65% exp var')
ax[5].plot(H2OPCA.index, H2OPCA['1630_Peak_PCA_2'], c = '#E42211', lw = 2, label = '$\mathregular{\overline{H_2O_{m, 1635}}_{PC2,}}$16% exp var')
ax[5].annotate("F.", xy=(0.0425, 0.925), xycoords="axes fraction", fontsize=20, weight='bold')
ax[5].legend(loc = (0.03, 0.7), labelspacing = 0.05, handletextpad = 0.5, handlelength = 0.6, prop={'size': 16}, frameon=False)
ax[5].set_xlim([1200, 2450])
ax[5].tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax[5].tick_params(axis="y", direction='in', length=5, pad = 6.5)
ax[5].invert_xaxis()

fig.supxlabel('Wavenumber ($\mathregular{cm^{-1}}$)', y = 0.03)
fig.supylabel('Absorbance', x = 0.05)

# fig.subplots_adjust(hspace=0.05, wspace=0.1)
plt.tight_layout()
# plt.savefig('AllBaselines.pdf', bbox_inches='tight', pad_inches = 0.025)

# %%
