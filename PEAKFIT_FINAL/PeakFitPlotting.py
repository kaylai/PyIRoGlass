# %% -*- coding: utf-8 -*-
""" Created on August 1, 2021 // @author: Sarah Shi """

# %% Import packages

import os
import sys
import time
import glob
import warnings 
import mc3
import numpy as np
import pandas as pd

import scipy.signal as signal
import scipy.interpolate as interpolate

import matplotlib
from matplotlib import pyplot as plt
from matplotlib import rc, cm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.gridspec as gridspec

%matplotlib inline
%config InlineBackend.figure_format = 'retina'
rc('font',**{'family':'Avenir', 'size': 18})
plt.rcParams['pdf.fonttype'] = 42

plt.rcParams["xtick.major.size"] = 4 # Sets length of ticks
plt.rcParams["ytick.major.size"] = 4 # Sets length of ticks
plt.rcParams["xtick.labelsize"] = 18 # Sets size of numbers on tick marks
plt.rcParams["ytick.labelsize"] = 18 # Sets size of numbers on tick marks
plt.rcParams["axes.labelsize"] = 20 # Axes labels

# %% PCA Component Plotting

BaselinePCA = pd.read_csv('./InputData/Baseline_Avg+PCA.csv');
H2OPCA = pd.read_csv('./InputData/Water_Peak_1635_All.csv');

sz = 150
fig, ax = plt.subplots(1, 1, figsize = (8, 8))
ax.plot(BaselinePCA.Wavenumber, BaselinePCA.Average_Baseline, c = '#171008', lw = 2, label = 'Baseline')
ax.plot(BaselinePCA.Wavenumber, BaselinePCA.PCA_1, c = '#0C7BDC', lw = 2, label = 'PC1')
ax.plot(BaselinePCA.Wavenumber, BaselinePCA.PCA_2, c = '#E42211', lw = 2, label = 'PC2')
ax.plot(BaselinePCA.Wavenumber, BaselinePCA.PCA_3, c = '#5DB147', lw = 2, label = 'PC3')
ax.plot(BaselinePCA.Wavenumber, BaselinePCA.PCA_4, c = '#F9C300', lw = 2, label = 'PC4')
ax.legend(loc = 'upper left', labelspacing = 0.4, handletextpad = 0.5, handlelength = 1.50, prop={'size': 14}, frameon=False)
ax.set_xlim([1125, 2475])
ax.set_xlabel('Wavenumber (cm-1)')
ax.set_ylabel('Absorbance')
ax.tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax.tick_params(axis="y", direction='in', length=5, pad = 6.5)
ax.invert_xaxis()
plt.tight_layout()
plt.savefig('BL_PCVectors.pdf')

fig, ax = plt.subplots(1, 1, figsize = (8, 8))
ax.plot(H2OPCA.Wavenumber, H2OPCA.Average_1630_Peak, c = '#171008', lw = 2, label = 'H2Om, 1635')
ax.plot(H2OPCA.Wavenumber, H2OPCA['1630_Peak_PCA_1'], c = '#0C7BDC', lw = 2, label = 'PC1')
ax.plot(H2OPCA.Wavenumber, H2OPCA['1630_Peak_PCA_2'], c = '#E42211', lw = 2, label = 'PC2')
ax.legend(loc = 'upper left', labelspacing = 0.4, handletextpad = 0.5, handlelength = 1.50, prop={'size': 14}, frameon=False)
ax.set_xlim([1125, 2475])
ax.set_ylim([-0.4, 1.2])
ax.set_xlabel('Wavenumber (cm-1)')
ax.set_ylabel('Absorbance')
ax.tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax.tick_params(axis="y", direction='in', length=5, pad = 6.5)
ax.invert_xaxis()
plt.tight_layout()
# plt.savefig('H2Om1635_PCVectors.pdf')

# %% 

BaselinePCA = pd.read_csv('./InputData/Baseline_Avg+PCA.csv');
H2OPCA = pd.read_csv('./InputData/Water_Peak_1635_All.csv');

sz = 150
fig, ax = plt.subplots(1, 1, figsize = (8, 8))
ax.plot(BaselinePCA.Wavenumber, BaselinePCA.Average_Baseline, c = '#171008', lw = 2, label = 'Baseline')
ax.plot(BaselinePCA.Wavenumber, BaselinePCA.Average_Baseline + BaselinePCA.PCA_1, c = '#0C7BDC', lw = 2, label = 'Baseline \N{PLUS-MINUS SIGN} PC1', zorder = 20)
ax.plot(BaselinePCA.Wavenumber, BaselinePCA.Average_Baseline - BaselinePCA.PCA_1, c = '#0C7BDC', lw = 2)
ax.plot(BaselinePCA.Wavenumber, BaselinePCA.Average_Baseline + BaselinePCA.PCA_2, c = '#E42211', lw = 2, label = 'Baseline \N{PLUS-MINUS SIGN} PC2', zorder = 15)
ax.plot(BaselinePCA.Wavenumber, BaselinePCA.Average_Baseline - BaselinePCA.PCA_2, c = '#E42211', lw = 2)
ax.plot(BaselinePCA.Wavenumber, BaselinePCA.Average_Baseline + BaselinePCA.PCA_3, c = '#5DB147', lw = 2, label = 'Baseline \N{PLUS-MINUS SIGN} PC3', zorder = 10)
ax.plot(BaselinePCA.Wavenumber, BaselinePCA.Average_Baseline - BaselinePCA.PCA_3, c = '#5DB147', lw = 2)
ax.plot(BaselinePCA.Wavenumber, BaselinePCA.Average_Baseline + BaselinePCA.PCA_4, c = '#F9C300', lw = 2, label = 'Baseline \N{PLUS-MINUS SIGN} PC4', zorder = 5)
ax.plot(BaselinePCA.Wavenumber, BaselinePCA.Average_Baseline - BaselinePCA.PCA_4, c = '#F9C300', lw = 2)
ax.legend(loc = 'upper left', labelspacing = 0.4, handletextpad = 0.5, handlelength = 1.50, prop={'size': 14}, frameon=False)
ax.set_xlim([1125, 2475])
ax.set_xlabel('Wavenumber (cm-1)')
ax.set_ylabel('Absorbance')
ax.tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax.tick_params(axis="y", direction='in', length=5, pad = 6.5)
ax.invert_xaxis()
plt.tight_layout()
plt.savefig('BL+PCVectors.pdf')

# %%

fig, ax = plt.subplots(1, 1, figsize = (8, 8))
ax.plot(H2OPCA.Wavenumber, H2OPCA.Average_1630_Peak, c = '#171008', lw = 2, label = 'H2Om, 1635')
ax.plot(H2OPCA.Wavenumber, H2OPCA.Average_1630_Peak + H2OPCA['1630_Peak_PCA_1'], c = '#0C7BDC', lw = 2, label = 'H2Om, 1635 \N{PLUS-MINUS SIGN} PC1', zorder = 20)
ax.plot(H2OPCA.Wavenumber, H2OPCA.Average_1630_Peak - H2OPCA['1630_Peak_PCA_1'], c = '#0C7BDC', lw = 2, zorder = 20)
ax.plot(H2OPCA.Wavenumber, H2OPCA.Average_1630_Peak + H2OPCA['1630_Peak_PCA_2'], c = '#E42211', lw = 2, label = 'H2Om, 1635 \N{PLUS-MINUS SIGN} PC2', zorder = 10)
ax.plot(H2OPCA.Wavenumber, H2OPCA.Average_1630_Peak - H2OPCA['1630_Peak_PCA_2'], c = '#E42211', lw = 2, zorder = 10)
ax.legend(loc = 'upper left', labelspacing = 0.4, handletextpad = 0.5, handlelength = 1.50, prop={'size': 14}, frameon=False)
ax.set_xlim([1125, 2475])
ax.set_ylim([-0.4, 1.2])
ax.set_xlabel('Wavenumber (cm-1)')
ax.set_ylabel('Absorbance')
ax.tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax.tick_params(axis="y", direction='in', length=5, pad = 6.5)
ax.invert_xaxis()
plt.tight_layout()
plt.savefig('H2Om1635+PCVectors.pdf')


# %%
# %% 

spec = pd.read_csv('./InputData/AC4_OL49_021920_30x30_H2O_a.csv')
x = pd.read_csv('./InputData/x.csv') 

data_H2O5200_1 = pd.read_csv('./InputData/data_H2O5200_1.csv')
data_H2O5200_2 = pd.read_csv('./InputData/data_H2O5200_2.csv')
data_H2O5200_3 = pd.read_csv('./InputData/data_H2O5200_3.csv')

data_H2O4500_1 = pd.read_csv('./InputData/data_H2O4500_1.csv')
data_H2O4500_2 = pd.read_csv('./InputData/data_H2O4500_2.csv')
data_H2O4500_3 = pd.read_csv('./InputData/data_H2O4500_3.csv')

krige_output_5200_1 = pd.read_csv('./InputData/krige_output_5200_1.csv')
krige_output_5200_2 = pd.read_csv('./InputData/krige_output_5200_2.csv')
krige_output_5200_3 = pd.read_csv('./InputData/krige_output_5200_3.csv')

krige_output_4500_1 = pd.read_csv('./InputData/krige_output_4500_1.csv')
krige_output_4500_2 = pd.read_csv('./InputData/krige_output_4500_2.csv')
krige_output_4500_3 = pd.read_csv('./InputData/krige_output_4500_3.csv')

plot_output_3550_1 = pd.read_csv('./InputData/plot_output_3550_1.csv') 
plot_output_3550_2 = pd.read_csv('./InputData/plot_output_3550_2.csv') 
plot_output_3550_3 = pd.read_csv('./InputData/plot_output_3550_3.csv') 

data_H2O3550_1 = pd.read_csv('./InputData/data_H2O3550_1.csv') 
data_H2O3550_2 = pd.read_csv('./InputData/data_H2O3550_2.csv') 
data_H2O3550_3 = pd.read_csv('./InputData/data_H2O3550_3.csv') 

Baseline_Solve_BP = pd.read_csv('./InputData/Baseline_Solve_BP.csv') 
Baseline_Array_Plot = pd.read_csv('./InputData/Baseline_Array_Plot.csv').to_numpy()
linearray = pd.read_csv('./InputData/linearray.csv') 

H1635_BP = pd.read_csv('./InputData/H1635_BP.csv') 
CO2P1515_BP = pd.read_csv('./InputData/CO2P1515_BP.csv') 
CO2P1430_BP = pd.read_csv('./InputData/CO2P1430_BP.csv') 
carbonate = pd.read_csv('./InputData/carbonate.csv') 

# %% NIR Peak Plotting

sz = 150
fig, ax = plt.subplots(2, 1, figsize = (8, 8))
ax = ax.flatten()
ax[0].plot(spec.Wavenumber, spec.Absorbance, c = 'k', lw = 2, label = 'FTIR Spectrum')
ax[0].plot(data_H2O5200_1.Wavenumber, data_H2O5200_1.Absorbance_Hat, c = '#0C7BDC', lw = 1, label = 'Median Filtered Peak')
ax[0].plot(data_H2O5200_2.Wavenumber, data_H2O5200_2.Absorbance_Hat, c = '#0C7BDC', lw = 1)
ax[0].plot(data_H2O5200_3.Wavenumber, data_H2O5200_3.Absorbance_Hat, c = '#0C7BDC', lw = 1)
ax[0].plot(data_H2O5200_1.Wavenumber, data_H2O5200_1.BL_NIR_H2O, linestyle = '--', dashes = (4, 8), c = '#5E5E5E', lw = 1, label = 'ALS Baselines')
ax[0].plot(data_H2O5200_2.Wavenumber, data_H2O5200_2.BL_NIR_H2O, linestyle = '--', dashes = (4, 8), c = '#5E5E5E', lw = 1)
ax[0].plot(data_H2O5200_3.Wavenumber, data_H2O5200_3.BL_NIR_H2O, linestyle = '--', dashes = (4, 8), c = '#5E5E5E', lw = 1)

ax[0].plot(data_H2O4500_1.Wavenumber, data_H2O4500_1.Absorbance_Hat, c = '#5DB147', lw = 1)
ax[0].plot(data_H2O4500_2.Wavenumber, data_H2O4500_2.Absorbance_Hat, c = '#5DB147', lw = 1)
ax[0].plot(data_H2O4500_3.Wavenumber, data_H2O4500_3.Absorbance_Hat, c = '#5DB147', lw = 1)
ax[0].plot(data_H2O4500_1.Wavenumber, data_H2O4500_1.BL_NIR_H2O, linestyle = '--', dashes = (4, 8), c = '#5E5E5E', lw = 1)
ax[0].plot(data_H2O4500_2.Wavenumber, data_H2O4500_2.BL_NIR_H2O, linestyle = '--', dashes = (4, 8), c = '#5E5E5E', lw = 1)
ax[0].plot(data_H2O4500_3.Wavenumber, data_H2O4500_3.BL_NIR_H2O, linestyle = '--', dashes = (4, 8), c = '#5E5E5E', lw = 1)
ax[0].text(5150, 0.6625, 'H2Om, 5200', ha = 'center', fontsize = 16)
ax[0].text(4485, 0.5225, 'OH-4500', ha = 'center', fontsize = 16)

ax[0].legend(loc = 'lower left', labelspacing = 0.4, handletextpad = 0.5, handlelength = 1.50, prop={'size': 14}, frameon=False)
ax[0].set_xlim([4200, 5400])
ax[0].set_ylim([0.4, 0.7])
ax[0].tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax[0].tick_params(axis="y", direction='in', length=5, pad = 6.5)
ax[0].axes.xaxis.set_ticklabels([])
ax[0].invert_xaxis()

ax[1].plot(data_H2O5200_1.Wavenumber, data_H2O5200_1['Subtracted_Peak'] - np.min(krige_output_5200_1.Absorbance), c = 'k', lw = 1, label = 'Baseline Subtracted Peak')
ax[1].plot(data_H2O5200_2.Wavenumber, data_H2O5200_2['Subtracted_Peak'] - np.min(krige_output_5200_2.Absorbance), c = 'k', lw = 1)
ax[1].plot(data_H2O5200_3.Wavenumber, data_H2O5200_3['Subtracted_Peak'] - np.min(krige_output_5200_3.Absorbance), c = 'k', lw = 1)
ax[1].plot(krige_output_5200_1.Wavenumber, krige_output_5200_1.Absorbance - np.min(krige_output_5200_1.Absorbance), c = '#0C7BDC', lw = 2, label = 'Gaussian Kriged Peak')
ax[1].plot(krige_output_5200_2.Wavenumber, krige_output_5200_2.Absorbance - np.min(krige_output_5200_2.Absorbance), c = '#074984', lw = 2)
ax[1].plot(krige_output_5200_3.Wavenumber, krige_output_5200_3.Absorbance - np.min(krige_output_5200_3.Absorbance), c = '#6DAFEA', lw = 2)

ax[1].plot(data_H2O4500_1.Wavenumber, data_H2O4500_1['Subtracted_Peak'] - np.min(krige_output_4500_1.Absorbance), c = 'k', lw = 1)
ax[1].plot(data_H2O4500_2.Wavenumber, data_H2O4500_2['Subtracted_Peak'] - np.min(krige_output_4500_2.Absorbance), c = 'k', lw = 1)
ax[1].plot(data_H2O4500_3.Wavenumber, data_H2O4500_3['Subtracted_Peak'] - np.min(krige_output_4500_3.Absorbance), c = 'k', lw = 1)
ax[1].plot(krige_output_4500_1.Wavenumber, krige_output_4500_1.Absorbance - np.min(krige_output_4500_1.Absorbance), c = '#417B31', lw = 2)
ax[1].plot(krige_output_4500_2.Wavenumber, krige_output_4500_2.Absorbance - np.min(krige_output_4500_2.Absorbance), c = '#5DB147', lw = 2) 
ax[1].plot(krige_output_4500_3.Wavenumber, krige_output_4500_3.Absorbance - np.min(krige_output_4500_3.Absorbance), c = '#8DC87E', lw = 2)
ax[1].text(5150, 0.0015, 'H2Om, 5200', ha = 'center', fontsize = 16) # 02775
ax[1].text(4485, 0.0015, 'OH-4500', ha = 'center', fontsize = 16) # 0165

ax[1].legend(loc = 'upper right', labelspacing = 0.4, handletextpad = 0.5, handlelength = 1.50, prop={'size': 14}, frameon=False)
ax[1].set_xlim([4200, 5400])
ax[1].set_ylim([0, 0.03])
ax[1].tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax[1].tick_params(axis="y", direction='in', length=5, pad = 6.5)
ax[1].invert_xaxis()

fig.supxlabel('Wavenumber (cm-1)', y = 0.06)
fig.supylabel('Absorbance', x = 0.06)
plt.tight_layout()
# plt.savefig('NIRPeaks.pdf')

# %% H2Ot, 3550 Peak Plotting

sz = 150
fig, ax = plt.subplots(1, 1, figsize = (8, 8))
ax.plot(spec.Wavenumber, spec.Absorbance, c = 'k', lw = 2, label = 'FTIR Spectrum')
ax.plot(data_H2O3550_1.Wavenumber, data_H2O3550_1.BL_MIR_3550, linestyle = '--', dashes = (3, 4), c = '#5E5E5E', lw = 1.5, label = 'ALS Baseline')
# ax.plot(data_H2O3550_2.Wavenumber, data_H2O3550_2.BL_MIR_3550, linestyle = '--', dashes = (2, 8), c = '#5E5E5E', lw = 1.5)
# ax.plot(data_H2O3550_3.Wavenumber, data_H2O3550_3.BL_MIR_3550, linestyle = '--', dashes = (2, 8), c = '#5E5E5E', lw = 1.5)
ax.plot(plot_output_3550_1.Wavenumber, plot_output_3550_1['Subtracted_Peak_Hat']+plot_output_3550_1['BL_MIR_3550'], c = '#E42211', lw = 2.5, label = 'Median Filtered Peak')
ax.plot(plot_output_3550_2.Wavenumber, plot_output_3550_2['Subtracted_Peak_Hat']+plot_output_3550_1['BL_MIR_3550'], c = '#E42211', lw = 2.5)
ax.plot(plot_output_3550_3.Wavenumber, plot_output_3550_3['Subtracted_Peak_Hat']+plot_output_3550_1['BL_MIR_3550'], c = '#E42211', lw = 2.5)
ax.text(3250, 0.55, 'H2Ot, 3550', ha = 'center', fontsize = 16)
ax.text(1645, 1.5, 'H2Om, 1635', ha = 'center', fontsize = 16)
ax.text(1470, 0.95, 'CO32-', ha = 'center', fontsize = 16)

ax.legend(loc = 'upper right', labelspacing = 0.4, handletextpad = 0.5, handlelength = 1.50, prop={'size': 14}, frameon=False)
ax.set_xlim([1275, 4000])
ax.set_ylim([0, 3])
ax.set_xlabel('Wavenumber (cm-1)')
ax.set_ylabel('Absorbance')
ax.tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax.tick_params(axis="y", direction='in', length=5, pad = 6.5)
ax.invert_xaxis()
plt.tight_layout()
# plt.savefig('3550Peak.pdf')


# %% Carbonate Peak Plotting

fig, ax = plt.subplots(1, 1, figsize = (8, 8))
ax.plot(spec.Wavenumber, spec.Absorbance, c = 'k', lw = 2, label = 'FTIR Spectrum')
ax.plot(x.Wavenumber, Baseline_Array_Plot[1, :], c = '#5E5E5E', lw = 0.25, label = 'MC3 Sampled Baselines')
for i in range(0, 302, 2):
    plt.plot(x.Wavenumber, Baseline_Array_Plot[i, :], c = '#5E5E5E', lw = 0.1)
ax.plot(x.Wavenumber, H1635_BP['Wavenumber']+Baseline_Solve_BP['Wavenumber'], c = '#E69F00', lw = 2, label = 'H2Om, 1635')
ax.plot(x.Wavenumber, CO2P1515_BP['Wavenumber']+Baseline_Solve_BP['Wavenumber'], c = '#E42211', lw = 2, label = 'CO32-1515')
ax.plot(x.Wavenumber, CO2P1430_BP['Wavenumber']+Baseline_Solve_BP['Wavenumber'], c = '#009E73', lw = 2, label = 'CO32-1430')
ax.plot(x.Wavenumber, carbonate['Wavenumber'], c = '#9A5ABD', lw = 2, label = 'MC3 Best-Fit Spectrum')
ax.plot(x.Wavenumber, Baseline_Solve_BP['Wavenumber'], linestyle = '--', dashes = (2, 2), c = 'k', lw = 2, label = 'MC3 Best-Fit Baseline')
ax.text(1645, 1.44, 'H2Om, 1635', ha = 'center', fontsize = 14)
ax.text(1470, 0.92, 'CO32-1515 and 1430', ha = 'center', fontsize = 14)

handles, labels = plt.gca().get_legend_handles_labels()
order = [0,2,3,4,1,6,5]
ax.legend([handles[idx] for idx in order],[labels[idx] for idx in order], loc = 'upper left', labelspacing = 0.4, handletextpad = 0.5, handlelength = 1.50, prop={'size': 14}, frameon=False)
ax.set_xlim([1275, 2200])
ax.set_ylim([0.4, 1.6])

ax.set_xlabel('Wavenumber (cm-1)')
ax.set_ylabel('Absorbance')
ax.tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax.tick_params(axis="y", direction='in', length=5, pad = 6.5)
ax.invert_xaxis()
plt.tight_layout()
# plt.savefig('CarbonatePeak.pdf')

# %% 

fig = plt.figure(figsize = (15, 15))
gs = fig.add_gridspec(ncols = 4, nrows = 5)

ax0 = plt.subplot(gs[0, :])
ax1 = plt.subplot(gs[1, 0:2])
ax2 = plt.subplot(gs[2, 0:2])
ax3 = plt.subplot(gs[1:3, 2:4])
ax4 = plt.subplot(gs[3:5, 0:2])


ax0.plot(spec.Wavenumber, spec.Absorbance, c = 'k', lw = 2, label = 'FTIR Spectrum')
ax0.set_xlim([1275, 5400])
ax0.set_ylim([0, 3])
ax0.invert_xaxis()

ax1.plot(spec.Wavenumber, spec.Absorbance, c = 'k', lw = 2, label = 'FTIR Spectrum')
ax1.plot(data_H2O5200_1.Wavenumber, data_H2O5200_1.Absorbance_Hat, c = '#0C7BDC', lw = 1, label = 'Median Filtered Peak')
ax1.plot(data_H2O5200_2.Wavenumber, data_H2O5200_2.Absorbance_Hat, c = '#0C7BDC', lw = 1)
ax1.plot(data_H2O5200_3.Wavenumber, data_H2O5200_3.Absorbance_Hat, c = '#0C7BDC', lw = 1)
ax1.plot(data_H2O5200_1.Wavenumber, data_H2O5200_1.BL_NIR_H2O, linestyle = '--', dashes = (4, 8), c = '#5E5E5E', lw = 1, label = 'ALS Baselines')
ax1.plot(data_H2O5200_2.Wavenumber, data_H2O5200_2.BL_NIR_H2O, linestyle = '--', dashes = (4, 8), c = '#5E5E5E', lw = 1)
ax1.plot(data_H2O5200_3.Wavenumber, data_H2O5200_3.BL_NIR_H2O, linestyle = '--', dashes = (4, 8), c = '#5E5E5E', lw = 1)

ax1.plot(data_H2O4500_1.Wavenumber, data_H2O4500_1.Absorbance_Hat, c = '#5DB147', lw = 1)
ax1.plot(data_H2O4500_2.Wavenumber, data_H2O4500_2.Absorbance_Hat, c = '#5DB147', lw = 1)
ax1.plot(data_H2O4500_3.Wavenumber, data_H2O4500_3.Absorbance_Hat, c = '#5DB147', lw = 1)
ax1.plot(data_H2O4500_1.Wavenumber, data_H2O4500_1.BL_NIR_H2O, linestyle = '--', dashes = (4, 8), c = '#5E5E5E', lw = 1)
ax1.plot(data_H2O4500_2.Wavenumber, data_H2O4500_2.BL_NIR_H2O, linestyle = '--', dashes = (4, 8), c = '#5E5E5E', lw = 1)
ax1.plot(data_H2O4500_3.Wavenumber, data_H2O4500_3.BL_NIR_H2O, linestyle = '--', dashes = (4, 8), c = '#5E5E5E', lw = 1)
ax1.text(5150, 0.6625, 'H2Om, 5200', ha = 'center', fontsize = 16)
ax1.text(4485, 0.5225, 'OH-4500', ha = 'center', fontsize = 16)

ax1.legend(loc = 'lower left', labelspacing = 0.4, handletextpad = 0.5, handlelength = 1.50, prop={'size': 14}, frameon=False)
ax1.set_xlim([4200, 5400])
ax1.set_ylim([0.4, 0.7])
ax1.tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax1.tick_params(axis="y", direction='in', length=5, pad = 6.5)
ax1.axes.xaxis.set_ticklabels([])
ax1.invert_xaxis()


ax2.plot(data_H2O5200_1.Wavenumber, data_H2O5200_1['Subtracted_Peak'] - np.min(krige_output_5200_1.Absorbance), c = 'k', lw = 1, label = 'Baseline Subtracted Peak')
ax2.plot(data_H2O5200_2.Wavenumber, data_H2O5200_2['Subtracted_Peak'] - np.min(krige_output_5200_2.Absorbance), c = 'k', lw = 1)
ax2.plot(data_H2O5200_3.Wavenumber, data_H2O5200_3['Subtracted_Peak'] - np.min(krige_output_5200_3.Absorbance), c = 'k', lw = 1)
ax2.plot(krige_output_5200_1.Wavenumber, krige_output_5200_1.Absorbance - np.min(krige_output_5200_1.Absorbance), c = '#0C7BDC', lw = 2, label = 'Gaussian Kriged Peak')
ax2.plot(krige_output_5200_2.Wavenumber, krige_output_5200_2.Absorbance - np.min(krige_output_5200_2.Absorbance), c = '#074984', lw = 2)
ax2.plot(krige_output_5200_3.Wavenumber, krige_output_5200_3.Absorbance - np.min(krige_output_5200_3.Absorbance), c = '#6DAFEA', lw = 2)

ax2.plot(data_H2O4500_1.Wavenumber, data_H2O4500_1['Subtracted_Peak'] - np.min(krige_output_4500_1.Absorbance), c = 'k', lw = 1)
ax2.plot(data_H2O4500_2.Wavenumber, data_H2O4500_2['Subtracted_Peak'] - np.min(krige_output_4500_2.Absorbance), c = 'k', lw = 1)
ax2.plot(data_H2O4500_3.Wavenumber, data_H2O4500_3['Subtracted_Peak'] - np.min(krige_output_4500_3.Absorbance), c = 'k', lw = 1)
ax2.plot(krige_output_4500_1.Wavenumber, krige_output_4500_1.Absorbance - np.min(krige_output_4500_1.Absorbance), c = '#417B31', lw = 2)
ax2.plot(krige_output_4500_2.Wavenumber, krige_output_4500_2.Absorbance - np.min(krige_output_4500_2.Absorbance), c = '#5DB147', lw = 2) 
ax2.plot(krige_output_4500_3.Wavenumber, krige_output_4500_3.Absorbance - np.min(krige_output_4500_3.Absorbance), c = '#8DC87E', lw = 2)
ax2.text(5150, 0.0015, 'H2Om, 5200', ha = 'center', fontsize = 16) # 02775
ax2.text(4485, 0.0015, 'OH-4500', ha = 'center', fontsize = 16) # 0165

ax2.legend(loc = 'upper right', labelspacing = 0.4, handletextpad = 0.5, handlelength = 1.50, prop={'size': 14}, frameon=False)
ax2.set_xlim([4200, 5400])
ax2.set_ylim([0, 0.03])
ax2.tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax2.tick_params(axis="y", direction='in', length=5, pad = 6.5)
ax2.invert_xaxis()


ax3.plot(spec.Wavenumber, spec.Absorbance, c = 'k', lw = 2, label = 'FTIR Spectrum')
ax3.plot(data_H2O3550_1.Wavenumber, data_H2O3550_1.BL_MIR_3550, linestyle = '--', dashes = (3, 4), c = '#5E5E5E', lw = 1.5, label = 'ALS Baseline')
# ax3.plot(data_H2O3550_2.Wavenumber, data_H2O3550_2.BL_MIR_3550, linestyle = '--', dashes = (2, 8), c = '#5E5E5E', lw = 1.5)
# ax3.plot(data_H2O3550_3.Wavenumber, data_H2O3550_3.BL_MIR_3550, linestyle = '--', dashes = (2, 8), c = '#5E5E5E', lw = 1.5)
ax3.plot(plot_output_3550_1.Wavenumber, plot_output_3550_1['Subtracted_Peak_Hat']+plot_output_3550_1['BL_MIR_3550'], c = '#E42211', lw = 2.5, label = 'Median Filtered Peak')
ax3.plot(plot_output_3550_2.Wavenumber, plot_output_3550_2['Subtracted_Peak_Hat']+plot_output_3550_1['BL_MIR_3550'], c = '#E42211', lw = 2.5)
ax3.plot(plot_output_3550_3.Wavenumber, plot_output_3550_3['Subtracted_Peak_Hat']+plot_output_3550_1['BL_MIR_3550'], c = '#E42211', lw = 2.5)
ax3.text(3250, 0.55, 'H2Ot, 3550', ha = 'center', fontsize = 16)
ax3.text(1645, 1.5, 'H2Om, 1635', ha = 'center', fontsize = 16)
ax3.text(1470, 0.95, 'CO32-', ha = 'center', fontsize = 16)

ax3.legend(loc = 'upper right', labelspacing = 0.4, handletextpad = 0.5, handlelength = 1.50, prop={'size': 14}, frameon=False)
ax3.set_xlim([1275, 4000])
ax3.set_ylim([0, 3])
ax3.tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax3.tick_params(axis="y", direction='in', length=5, pad = 6.5)
ax3.invert_xaxis()

ax4.plot(spec.Wavenumber, spec.Absorbance, c = 'k', lw = 2, label = 'FTIR Spectrum')
ax4.plot(x.Wavenumber, Baseline_Array_Plot[1, :], c = '#5E5E5E', lw = 0.25, label = 'MC3 Sampled Baselines')
for i in range(0, 302, 2):
    ax4.plot(x.Wavenumber, Baseline_Array_Plot[i, :], c = '#5E5E5E', lw = 0.1)
ax4.plot(x.Wavenumber, H1635_BP['Wavenumber']+Baseline_Solve_BP['Wavenumber'], c = '#E69F00', lw = 2, label = 'H2Om, 1635')
ax4.plot(x.Wavenumber, CO2P1515_BP['Wavenumber']+Baseline_Solve_BP['Wavenumber'], c = '#E42211', lw = 2, label = 'CO32-1515')
ax4.plot(x.Wavenumber, CO2P1430_BP['Wavenumber']+Baseline_Solve_BP['Wavenumber'], c = '#009E73', lw = 2, label = 'CO32-1430')
ax4.plot(x.Wavenumber, carbonate['Wavenumber'], c = '#9A5ABD', lw = 2, label = 'MC3 Best-Fit Spectrum')
ax4.plot(x.Wavenumber, Baseline_Solve_BP['Wavenumber'], linestyle = '--', dashes = (2, 2), c = 'k', lw = 2, label = 'MC3 Best-Fit Baseline')
ax4.text(1645, 1.44, 'H2Om, 1635', ha = 'center', fontsize = 14)
ax4.text(1470, 0.92, 'CO32-1515 and 1430', ha = 'center', fontsize = 14)

handles, labels = ax4.get_legend_handles_labels()
order = [0,2,3,4,1,6,5]
ax4.legend([handles[idx] for idx in order],[labels[idx] for idx in order], loc = 'upper left', labelspacing = 0.4, handletextpad = 0.5, handlelength = 1.50, prop={'size': 14}, frameon=False)
ax4.set_xlim([1275, 2200])
ax4.set_ylim([0.4, 1.6])

ax4.tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax4.tick_params(axis="y", direction='in', length=5, pad = 6.5)
ax4.invert_xaxis()

fig.supxlabel('Wavenumber (cm-1)', y = 0.03)
fig.supylabel('Absorbance', x = 0.03)

plt.tight_layout()
# plt.savefig('AllPeaks.pdf')

# %%
# %%
