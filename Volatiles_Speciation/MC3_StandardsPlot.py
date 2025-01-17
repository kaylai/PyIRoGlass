# %% -*- coding: utf-8 -*-
""" Created on June 12, 2021 // @author: Sarah Shi """

# Import packages

import os
import sys
import time
import glob
import warnings 
import mc3
import numpy as np
import pandas as pd
import scipy 

import scipy.signal as signal
import scipy.interpolate as interpolate
from sklearn.metrics import mean_squared_error

import matplotlib
from matplotlib import pyplot as plt
from matplotlib import rc, cm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

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

# %% Load PC components. 

path_parent = os.path.dirname(os.getcwd())
path_beg =  path_parent + '/'
path_input = path_parent + '/Inputs/'

output_dir = ["FIGURES", "PLOTFILES", "NPZTXTFILES", "LOGFILES", "FINALDATA"] # NPZFILES

# Change paths to direct to folder with SampleSpectra -- last bit should be whatever your folder with spectra is called. 
PATHS = [path_input + string for string in ['TransmissionSpectra/Fuego/', 'TransmissionSpectra/Standards/', 'TransmissionSpectra/Fuego1974RH/', 'TransmissionSpectra/ND70/', 'TransmissionSpectra/HJYM/', 'TransmissionSpectra/YM/']]

# Put ChemThick file in Inputs. Direct to what your ChemThick file is called. 
CHEMTHICK_PATH = [path_input + string for string in ['FuegoChemThick.csv', 'StandardChemThick.csv', 'DanRHChemThick.csv', 'ND70ChemThick.csv', 'HJYMChemThick.csv', 'YMChemThick.csv']]

# Change last value in list to be what you want your output directory to be called. 
INPUT_PATHS = ['FUEGO', 'STD', 'FRH']

# Change to be what you want the prefix of your output files to be. 
OUTPUT_PATH = ['FUEGO', 'STD', 'FRH']

stdno = 1
MEGA_SPREADSHEET = pd.read_csv(path_parent + '/' + output_dir[-1] + '/' + OUTPUT_PATH[stdno] + '_H2OCO2_FwSTD.csv', index_col = 0)

# %% 

INSOL = MEGA_SPREADSHEET[MEGA_SPREADSHEET.index.str.contains('INSOL')]
ALV1846 = MEGA_SPREADSHEET[MEGA_SPREADSHEET.index.str.contains('21ALV1846')]
WOK5_4 = MEGA_SPREADSHEET[MEGA_SPREADSHEET.index.str.contains('23WOK5-4')]
ALV1833_11 = MEGA_SPREADSHEET[MEGA_SPREADSHEET.index.str.contains('ALV1833-11')]
CD33_12_2_2 = MEGA_SPREADSHEET[MEGA_SPREADSHEET.index.str.contains('CD33_12-2-2')]
CD33_22_1_1 = MEGA_SPREADSHEET[MEGA_SPREADSHEET.index.str.contains('CD33_22-1-1')]
ETFSR_Ol8 = MEGA_SPREADSHEET[MEGA_SPREADSHEET.index.str.contains('ETFSR_Ol8')]
Fiege63 = MEGA_SPREADSHEET[MEGA_SPREADSHEET.index.str.contains('Fiege63')]
Fiege73 = MEGA_SPREADSHEET[MEGA_SPREADSHEET.index.str.contains('Fiege73')]
STD_C1 = MEGA_SPREADSHEET[MEGA_SPREADSHEET.index.str.contains('C1')]
STD_CN92C_OL2 = MEGA_SPREADSHEET[MEGA_SPREADSHEET.index.str.contains('CN92C_OL2')]
STD_D1010 = MEGA_SPREADSHEET[MEGA_SPREADSHEET.index.str.contains('D1010')]
STD_D1010 = STD_D1010.dropna()
STD_ETF46 = MEGA_SPREADSHEET[MEGA_SPREADSHEET.index.str.contains('ETF46')]
VF74_127_7 = MEGA_SPREADSHEET[MEGA_SPREADSHEET.index.str.contains('VF74_127-7')]
VF74_132_2 = MEGA_SPREADSHEET[MEGA_SPREADSHEET.index.str.contains('VF74_132-2')]
NS1 = MEGA_SPREADSHEET[MEGA_SPREADSHEET.index.str.contains('NS1')]
M35 = MEGA_SPREADSHEET[MEGA_SPREADSHEET.index.str.contains('M35')]
M43 = MEGA_SPREADSHEET[MEGA_SPREADSHEET.index.str.contains('M43')]
BF73 = MEGA_SPREADSHEET[MEGA_SPREADSHEET.index.str.contains('BF73_100x100')]
BF76 = MEGA_SPREADSHEET[MEGA_SPREADSHEET.index.str.contains('BF76_100x')]
BF77 = MEGA_SPREADSHEET[MEGA_SPREADSHEET.index.str.contains('BF77_50x50')]



def H2O_mean(DF): 
    return DF['H2OT_MEAN'].mean()
def H2O_std(DF): 
    return np.sqrt(np.sum(np.square(DF['H2OT_STD']), axis=0)) / len(DF)
def CO2_mean(DF): 
    return DF['CO2_MEAN'].mean()
def CO2_std(DF): 
    return np.sqrt(np.sum(np.square(DF['CO2_STD']), axis=0)) / len(DF)
def H2O_expmean(DF): 
    return DF['H2O_EXP'][0]
def H2O_expstd(DF): 
    return DF['H2O_EXP_STD'][0]
def CO2_expmean(DF): 
    return DF['CO2_EXP'][0]
def CO2_expstd(DF): 
    return DF['CO2_EXP_STD'][0]
def H2O_rsd(DF): 
    return np.mean(DF['H2OT_STD'] / DF['H2OT_MEAN'])
def CO2_rsd(DF): 
    return np.mean(DF['CO2_STD'] / DF['CO2_MEAN'])



def concordance_correlation_coefficient(y_true, y_pred):
    """Concordance correlation coefficient."""
    # Remove NaNs
    df = pd.DataFrame({
        'y_true': y_true,
        'y_pred': y_pred
    })
    df = df.dropna()
    y_true = df['y_true']
    y_pred = df['y_pred']
    # Pearson product-moment correlation coefficients
    cor = np.corrcoef(y_true, y_pred)[0][1] 
    # Mean
    mean_true = np.mean(y_true)
    mean_pred = np.mean(y_pred)
    # Variance
    var_true = np.var(y_true)
    var_pred = np.var(y_pred)
    # Standard deviation
    sd_true = np.std(y_true)
    sd_pred = np.std(y_pred)
    # Calculate CCC
    numerator = 2 * cor * sd_true * sd_pred
    denominator = var_true + var_pred + (mean_true - mean_pred)**2
    return numerator / denominator


# %% sims calibration 


c_si_si_calib = np.array([0.00352726, 0.00364888, 0.39991483, 0.35405633, 0.25057402, 0.25527224, 0.77261763, 0.69592738, 0.01366744, 0.01466238, 15.21391320, 15.75483819])
co2_calib = np.array([0, 0, 165, 165, 90, 90, 243, 243, 0, 0, 7754, 7754])

bf73_csisi = np.array([4.98502480, 4.83861929])
bf76_csisi = np.array([5.33802805, 4.88439129])
bf77_csisi = np.array([1.77990001, 1.66122648])
ns1_csisi = np.array([10.30641893, 9.29042104, 9.59020493])

bf73_co2 = np.array([2321, 2321])
bf76_co2 = np.array([1769, 1769])
bf77_co2 = np.array([679, 679])
ns1_co2 = np.array([4125, 4125, 4125])


arr = np.array([0, 10, 17])
slope0, intercept0, r_value0, p_value0, std_err0 = scipy.stats.linregress(c_si_si_calib, co2_calib)
line = slope0*arr+intercept0

sz = 150
fig, ax = plt.subplots(1, 1, figsize = (8, 8))
ax.plot(arr, line, 'k--')
ax.scatter(c_si_si_calib, co2_calib, s = sz-25, c = '#9D9D9D', edgecolors='black', linewidth = 0.5, zorder = 15, label='Calibration Standards')
ax.scatter(bf73_csisi, bf73_co2, marker='s', s = sz, c = '#F4A582', edgecolors='black', linewidth = 0.5, zorder = 15, label='BF73')
ax.scatter(bf76_csisi, bf76_co2, marker='s', s = sz, c = '#FDDBC7', edgecolors='black', linewidth = 0.5, zorder = 15, label='BF76')
ax.scatter(bf77_csisi, bf77_co2, marker='s', s = sz, c = '#F7F7F7', edgecolors='black', linewidth = 0.5, zorder = 15, label='BF77')
ax.scatter(ns1_csisi, ns1_co2, marker='s', s = sz, c = '#4393C3', edgecolors='black', linewidth = 0.5, zorder = 15, label='NS-1')
ax.annotate('y=502.8225x-38.1266', xy=(0.55, 0.8), xycoords="axes fraction", horizontalalignment='center', fontsize=16)
ax.annotate('$\mathregular{R^2}$=0.9994', xy=(0.55, 0.765), xycoords="axes fraction", horizontalalignment='center', fontsize=16)
ax.set_xlabel(r'$\mathregular{^{12}C/^{30}Si \cdot SiO_2}$')
ax.set_ylabel('$\mathregular{CO_2}$ (ppm)')
ax.legend(labelspacing = 0.3, handletextpad = 0.25, handlelength = 1.00, prop={'size': 13}, frameon=False)
ax.set_xlim([-0.5, 18])
ax.set_ylim([-250, 8250])
ax.tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax.tick_params(axis="y", direction='in', length=5, pad = 6.5)
plt.tight_layout()
# plt.savefig('SIMS_Calibration.pdf', bbox_inches='tight', pad_inches = 0.025)

# %% 


# %% no citations

def relative_root_mean_squared_error(true, pred):
    num = np.sum(np.square(true - pred))
    den = np.sum(np.square(pred))
    squared_error = num/den
    rrmse_loss = np.sqrt(squared_error)
    return rrmse_loss

h2o_line = np.array([0, 6])
co2_line = np.array([0, 6000])
sz_sm = 80
sz = 150

fig, ax = plt.subplots(1, 2, figsize = (14, 7))

ax = ax.flatten()
ax[0].plot(h2o_line, h2o_line, 'k', lw = 0.5, zorder = 0)
ax[0].scatter(H2O_expmean(Fiege63), H2O_mean(Fiege63), s = sz, c = '#fff7bc', ec = '#171008', lw = 0.5, zorder = 15, label = 'ABWCl-F0x')
ax[0].scatter(H2O_expmean(Fiege63)+0.01, H2O_mean(Fiege63), s = sz_sm, marker = '>', c = '#FFFFFF', ec = '#171008', lw = 0.5, zorder = 20)
ax[0].errorbar(H2O_expmean(Fiege63), H2O_mean(Fiege63), xerr = H2O_expstd(Fiege63), yerr = H2O_mean(Fiege63) * H2O_rsd(Fiege63), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(Fiege73), H2O_mean(Fiege73), s = 120, marker = 'D', c = '#fee392', ec = '#171008', lw = 0.5, zorder = 15, label = 'ABWB-0x')
ax[0].scatter(H2O_expmean(Fiege73)+0.01, H2O_mean(Fiege73), s = sz_sm, marker = '>', c = '#FFFFFF', ec = '#171008', lw = 0.5, zorder = 20)
ax[0].errorbar(H2O_expmean(Fiege73), H2O_mean(Fiege73), xerr = H2O_expstd(Fiege73), yerr = H2O_mean(Fiege73) * H2O_rsd(Fiege73), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(BF73), H2O_mean(BF73), s = 120, marker = 'D', c = '#fec44f', ec = '#171008', lw = 0.5, zorder = 20, label = 'BF73')
ax[0].errorbar(H2O_expmean(BF73), H2O_mean(BF73), xerr = H2O_expstd(BF73), yerr = H2O_mean(BF73) * H2O_rsd(BF73), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(BF76), H2O_mean(BF76), s = 120, marker = 'D', c = '#fb9a29', ec = '#171008', lw = 0.5, zorder = 20, label = 'BF76')
ax[0].errorbar(H2O_expmean(BF76), H2O_mean(BF76), xerr = H2O_expstd(BF76), yerr = H2O_mean(BF76) * H2O_rsd(BF76), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(BF77), H2O_mean(BF77), s = 120, marker = 'D', c = '#ec7014', ec = '#171008', lw = 0.5, zorder = 20, label = 'BF77')
ax[0].errorbar(H2O_expmean(BF77), H2O_mean(BF77), xerr = H2O_expstd(BF77), yerr = H2O_mean(BF77) * H2O_rsd(BF77), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(NS1), H2O_mean(NS1), s = sz, c = '#cc4c02', ec = '#171008', lw = 0.5, zorder = 20, label = 'NS-1')
ax[0].errorbar(H2O_expmean(NS1), H2O_mean(NS1), xerr = H2O_expstd(NS1), yerr = H2O_mean(NS1) * H2O_rsd(NS1), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(M35), H2O_mean(M35), s = 120, marker = 'D', c = '#983404', ec = '#171008', lw = 0.5, zorder = 20, label = 'M35')
ax[0].errorbar(H2O_expmean(M35), H2O_mean(M35), xerr = H2O_expstd(M35), yerr = H2O_mean(M35) * H2O_rsd(M35), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(M43), H2O_mean(M43), s = 120, marker = 'D', c = '#662506', ec = '#171008', lw = 0.5, zorder = 20, label = 'M43')
ax[0].errorbar(H2O_expmean(M43), H2O_mean(M43), xerr = H2O_expstd(M43), yerr = H2O_mean(M43) * H2O_rsd(M43), lw = 0.5, c = 'k', zorder = 10)


ax[0].scatter(H2O_expmean(ETFSR_Ol8), H2O_mean(ETFSR_Ol8), s = sz, marker = 's', facecolors='white', ec = '#FEE391', lw = 2.5, zorder = 20, label = 'ETFSR-OL8') #c = '#f2821d',
ax[0].errorbar(H2O_expmean(ETFSR_Ol8), H2O_mean(ETFSR_Ol8), xerr = H2O_expstd(ETFSR_Ol8), yerr = H2O_mean(ETFSR_Ol8) * H2O_rsd(ETFSR_Ol8), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(CD33_12_2_2), H2O_mean(CD33_12_2_2), s = sz, marker='s', facecolors='white',  ec = '#FEC44F', lw = 2.5, zorder = 20, label = 'CD33-12-2-2') #c = '#e76b11',
ax[0].errorbar(H2O_expmean(CD33_12_2_2), H2O_mean(CD33_12_2_2), xerr = H2O_expstd(CD33_12_2_2), yerr = H2O_mean(CD33_12_2_2) * H2O_rsd(CD33_12_2_2), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(CD33_22_1_1), H2O_mean(CD33_22_1_1), s = sz, marker='s',facecolors='white', ec = '#FB9A29', lw = 2.5, zorder = 20, label = 'CD33-22-1-1') #c = '#d55607',
ax[0].errorbar(H2O_expmean(CD33_22_1_1), H2O_mean(CD33_22_1_1), xerr = H2O_expstd(CD33_22_1_1), yerr = H2O_mean(CD33_22_1_1) * H2O_rsd(CD33_22_1_1), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(STD_D1010), H2O_mean(STD_D1010), s = sz, facecolors='white', ec = '#EC7014', lw = 2.5, zorder = 20, label = 'D1010') #c = '#bc4503', 
ax[0].errorbar(H2O_expmean(STD_D1010), H2O_mean(STD_D1010), xerr = H2O_expstd(STD_D1010), yerr = H2O_mean(STD_D1010) * H2O_rsd(STD_D1010), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(ALV1833_11), H2O_mean(ALV1833_11), s = sz, facecolors='white', ec = '#CC4C02', lw = 2.5, zorder = 20, label = 'ALV1833-11') #c = '#a03704', 
ax[0].errorbar(H2O_expmean(ALV1833_11), H2O_mean(ALV1833_11), xerr = H2O_expstd(ALV1833_11), yerr = H2O_mean(ALV1833_11) * H2O_rsd(ALV1833_11), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(WOK5_4), H2O_mean(WOK5_4), s = sz, facecolors='white', ec = '#993404', lw = 2.5, zorder = 20, label = '23WOK5-4') #c = '#832d05',
ax[0].errorbar(H2O_expmean(WOK5_4), H2O_mean(WOK5_4), xerr = H2O_expstd(WOK5_4), yerr = H2O_mean(WOK5_4) * H2O_rsd(WOK5_4), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(ALV1846), H2O_mean(ALV1846), s = sz, facecolors='white', ec = '#662506', lw = 2.5, zorder = 20, label = '21ALV1846-9') #c = '#662506',
ax[0].errorbar(H2O_expmean(ALV1846), H2O_mean(ALV1846), xerr = H2O_expstd(ALV1846), yerr = H2O_mean(ALV1846) * H2O_rsd(ALV1846), lw = 0.5, c = 'k', zorder = 10)

ax[0].set_xlim([0, 5])
ax[0].set_ylim([0, 5])
ax[0].set_xlabel('$\mathregular{H_2O}$ Expected (wt.%)')
ax[0].set_ylabel('LDEO FTIR $\mathregular{H_2O_t}$ with PyIRoGlass (wt.%)')
l1 = ax[0].legend(loc = 'lower right', labelspacing = 0.2, handletextpad = 0.25, handlelength = 1.00, prop={'size': 13}, frameon=False)
ax[0].tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax[0].tick_params(axis="y", direction='in', length=5, pad = 6.5)

ftir_sym = ax[0].scatter(np.nan, np.nan, s = sz, ec = '#171008', facecolors='white', lw = 0.5, zorder = 20, label = 'FTIR')
sims_sym = ax[0].scatter(np.nan, np.nan, s = 100, marker = 's', ec = '#171008', facecolors='white', lw = 0.5, zorder = 20, label = 'SIMS')
kft_sym = ax[0].scatter(np.nan, np.nan, s = 100, marker = 'D', ec = '#171008', facecolors='white', lw = 0.5, zorder = 20, label = 'KFT')
ea_sym = ax[0].scatter(np.nan, np.nan, s = sz+10, marker = 'p', ec = '#171008', facecolors='white', lw = 0.5, zorder = 20, label = 'KFT')
sat_symb = ax[0].scatter(np.nan, np.nan, s = sz_sm, marker = '>', ec = '#171008', facecolors='white', lw = 0.5, zorder = 20, label = '$\mathregular{H_2O_{t, 3550}}$ Saturated')
ax[0].legend([ftir_sym, sims_sym, kft_sym, ea_sym, sat_symb], ['FTIR', 'SIMS', 'KFT', 'EA', '$\mathregular{H_2O_{t, 3550}}$ Saturated'], loc = (0.0025, 0.50), labelspacing = 0.3, handletextpad = 0.25, handlelength = 1.00, prop={'size': 12.5}, frameon=True)
ax[0].add_artist(l1)
ax[0].annotate("A.", xy=(0.02, 0.95), xycoords="axes fraction", fontsize=20, weight='bold')

h2o_exp = np.array([H2O_expmean(Fiege63), H2O_expmean(Fiege73), H2O_expmean(BF73), H2O_expmean(BF76), H2O_expmean(BF77), H2O_expmean(M35), H2O_expmean(M43), H2O_expmean(NS1), H2O_expmean(ETFSR_Ol8), 
                    H2O_expmean(CD33_12_2_2), H2O_expmean(CD33_22_1_1), H2O_expmean(STD_D1010), H2O_expmean(ALV1833_11), H2O_expmean(WOK5_4), H2O_expmean(ALV1846)]) # 
h2o_py = np.array([H2O_mean(Fiege63), H2O_mean(Fiege73), H2O_mean(BF73), H2O_mean(BF76), H2O_mean(BF77), H2O_mean(M35), H2O_mean(M43), H2O_mean(NS1), H2O_mean(ETFSR_Ol8), 
                    H2O_mean(CD33_12_2_2), H2O_mean(CD33_22_1_1), H2O_mean(STD_D1010), H2O_mean(ALV1833_11), H2O_mean(WOK5_4), H2O_mean(ALV1846)]) 
slope0, intercept0, r_value0, p_value0, std_err0 = scipy.stats.linregress(h2o_exp, h2o_py)
ccc0 = concordance_correlation_coefficient(h2o_exp, h2o_py)
rmse0 = mean_squared_error(h2o_exp, h2o_py, squared=False)

ax[0].annotate("$\mathregular{R^{2}}$="+str(np.round(r_value0**2, 2)), xy=(0.02, 0.8275), xycoords="axes fraction", fontsize=16)
ax[0].annotate("CCC="+str(np.round(ccc0, 2)), xy=(0.02, 0.91), xycoords="axes fraction", fontsize=16)
ax[0].annotate("RMSE="+str(np.round(rmse0, 2))+"; RRMSE="+str(np.round(relative_root_mean_squared_error(h2o_exp, h2o_py)*100, 2))+'%', xy=(0.02, 0.87), xycoords="axes fraction", fontsize=16)
ax[0].annotate("m="+str(np.round(slope0, 2)), xy=(0.02, 0.79), xycoords="axes fraction", fontsize=16)
ax[0].annotate("b="+str(np.round(intercept0, 2)), xy=(0.02, 0.75), xycoords="axes fraction", fontsize=16)



ax[1].plot(co2_line, co2_line, 'k', lw = 0.5, zorder = 0)
ax[1].scatter(CO2_expmean(BF73), CO2_mean(BF73)*338.6880953/265, s = sz+10, marker = 'p', c = '#fec44f', ec = '#171008', lw = 0.5, zorder = 20, label = 'BF73')
ax[1].errorbar(CO2_expmean(BF73), CO2_mean(BF73)*338.6880953/265, xerr = CO2_expstd(BF73), yerr = CO2_mean(BF73) * CO2_rsd(BF73) * 2 *338.6880953/265, lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(BF76), CO2_mean(BF76)*338.6880953/265, s = sz+10, marker = 'p', c = '#fb9a29', ec = '#171008', lw = 0.5, zorder = 20, label = 'BF76')
ax[1].errorbar(CO2_expmean(BF76), CO2_mean(BF76)*338.6880953/265, xerr = CO2_expstd(BF76), yerr = CO2_mean(BF76) * CO2_rsd(BF76) * 2 *338.6880953/265, lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(BF77), CO2_mean(BF77)*338.6880953/265, s = sz+10, marker = 'p', c = '#ec7014', ec = '#171008', lw = 0.5, zorder = 20, label = 'BF77')
ax[1].errorbar(CO2_expmean(BF77), CO2_mean(BF77)*338.6880953/265, xerr = CO2_expstd(BF77), yerr = CO2_mean(BF77) * CO2_rsd(BF77) * 2*338.6880953/265, lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(NS1), CO2_mean(NS1)*315.2724799/375, s = sz, marker='s', c = '#cc4c02', ec = '#171008', lw = 0.5, zorder = 20, label = 'NS-1')
ax[1].errorbar(CO2_expmean(NS1), CO2_mean(NS1)*315.2724799/375, xerr = CO2_expstd(NS1), yerr = CO2_mean(NS1) * CO2_rsd(NS1) * 2/315.2724799*375, lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(M35), CO2_mean(M35)*329.7316656/317, s = sz, c = '#983404', ec = '#171008', lw = 0.5, zorder = 20, label = 'M35')
ax[1].errorbar(CO2_expmean(M35), CO2_mean(M35)*329.7316656/317, xerr = CO2_expstd(M35), yerr = CO2_mean(M35) * CO2_rsd(M35)* 2*329.7316656/317, lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(M43), CO2_mean(M43)*336.1936113/317, s = sz, c = '#662506', ec = '#171008', lw = 0.5, zorder = 20, label = 'M43')
ax[1].errorbar(CO2_expmean(M43), CO2_mean(M43)*336.1936113/317, xerr = CO2_expstd(M43), yerr = CO2_mean(M43) * CO2_rsd(M43) * 2*336.1936113/317, lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(CD33_12_2_2), CO2_mean(CD33_12_2_2), s = sz, marker = 's', facecolors='white', ec = '#FEC44F', lw = 2.5, zorder = 20, label = 'CD33-12-2-2')
ax[1].errorbar(CO2_expmean(CD33_12_2_2), CO2_mean(CD33_12_2_2), xerr = CO2_expstd(CD33_12_2_2), yerr = CO2_mean(CD33_12_2_2) * CO2_rsd(CD33_12_2_2) * 2, lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(CD33_22_1_1), CO2_mean(CD33_22_1_1), s = sz, marker = 's', facecolors='white', ec = '#FB9A29', lw = 2.5, zorder = 20, label = 'CD33-22-1-1')
ax[1].errorbar(CO2_expmean(CD33_22_1_1), CO2_mean(CD33_22_1_1), xerr = CO2_expstd(CD33_22_1_1), yerr = CO2_mean(CD33_22_1_1) * CO2_rsd(CD33_22_1_1) * 2, lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(STD_D1010), CO2_mean(STD_D1010)*315.7646212/375, s = sz, facecolors='white', ec = '#EC7014', lw = 2.5, zorder = 20, label = 'D1010')
ax[1].errorbar(CO2_expmean(STD_D1010), CO2_mean(STD_D1010)*315.7646212/375, xerr = CO2_expstd(STD_D1010), yerr = CO2_mean(STD_D1010) * CO2_rsd(STD_D1010) * 2*315.7646212/375, lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(ALV1833_11), CO2_mean(ALV1833_11)*353.8503071/375, s = sz, facecolors='white', ec = '#CC4C02', lw = 2.5, zorder = 20, label = 'ALV1833-11')
ax[1].errorbar(CO2_expmean(ALV1833_11), CO2_mean(ALV1833_11)*353.8503071/375, xerr = CO2_expstd(ALV1833_11), yerr = CO2_mean(ALV1833_11) * CO2_rsd(ALV1833_11) * 2*353.8503071/375, lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(WOK5_4), CO2_mean(WOK5_4)*310.7007261/375, s = sz, facecolors='white', ec = '#993404', lw = 2.5, zorder = 20, label = '23WOK5-4')
ax[1].errorbar(CO2_expmean(WOK5_4), CO2_mean(WOK5_4)*310.7007261/375, xerr = CO2_expstd(WOK5_4), yerr = CO2_mean(WOK5_4) * CO2_rsd(WOK5_4) * 2*310.7007261/375, lw = 0.5, c = 'k', zorder = 10)

ax[1].set_xlim([0, 4000]) # 4250
ax[1].set_ylim([0, 4000])
ax[1].set_xlabel('$\mathregular{CO_2}$ Expected (ppm)')
ax[1].set_ylabel('LDEO FTIR $\mathregular{CO_2}$ with PyIRoGlass (ppm)')
ax[1].tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax[1].tick_params(axis="y", direction='in', length=5, pad = 6.5)
ax[1].legend(loc = 'lower right', labelspacing = 0.2, handletextpad = 0.25, handlelength = 1.00, prop={'size': 13}, frameon=False)
ax[1].annotate("B.", xy=(0.02, 0.95), xycoords="axes fraction", fontsize=20, weight='bold')

co2_exp = np.array([CO2_expmean(BF73), CO2_expmean(BF76), CO2_expmean(BF77), CO2_expmean(M35), CO2_expmean(M43), CO2_expmean(NS1),
                    CO2_expmean(CD33_12_2_2), CO2_expmean(CD33_22_1_1), CO2_expmean(STD_D1010), CO2_expmean(ALV1833_11), CO2_expmean(WOK5_4)])
co2_py = np.array([CO2_mean(BF73)*338.6880953/265, CO2_mean(BF76)*338.6880953/265, CO2_mean(BF77)*338.6880953/265, CO2_mean(M35)*329.7316656/317, CO2_mean(M43)*336.1936113/317, CO2_mean(NS1)*315.2724799/375,
                    CO2_mean(CD33_12_2_2), CO2_mean(CD33_22_1_1), CO2_mean(STD_D1010)*315.7646212/375, CO2_mean(ALV1833_11)*353.8503071/375, CO2_mean(WOK5_4)*310.7007261/375])
slope1, intercept1, r_value1, p_value1, std_err1 = scipy.stats.linregress(co2_exp, co2_py)
ccc1 = concordance_correlation_coefficient(co2_exp, co2_py)
rmse1 = mean_squared_error(co2_exp, co2_py, squared=False)

ax[1].annotate("$\mathregular{R^{2}}$="+str(np.round(r_value1**2, 2)), xy=(0.02, 0.8275), xycoords="axes fraction", fontsize=16)
ax[1].annotate("CCC="+str(np.round(ccc1, 2)), xy=(0.02, 0.91), xycoords="axes fraction", fontsize=16)
ax[1].annotate("RMSE="+str(np.round(rmse1, 2))+"; RRMSE="+str(np.round(relative_root_mean_squared_error(co2_exp, co2_py)*100, 2))+'%', xy=(0.02, 0.87), xycoords="axes fraction", fontsize=16)
ax[1].annotate("m="+str(np.round(slope1, 2)), xy=(0.02, 0.79), xycoords="axes fraction", fontsize=16)
ax[1].annotate("b="+str(np.round(intercept1, 2)), xy=(0.02, 0.75), xycoords="axes fraction", fontsize=16)

plt.tight_layout()
# plt.savefig('FTIRSIMS_Comparison.pdf', bbox_inches='tight', pad_inches = 0.025)
plt.show()


# %% 

# %% old values for non brounce


h2o_line = np.array([0, 6])
co2_line = np.array([0, 6000])
sz_sm = 80
sz = 150

fig, ax = plt.subplots(1, 2, figsize = (14, 7))

ax = ax.flatten()
ax[0].plot(h2o_line, h2o_line, 'k', lw = 0.5, zorder = 0)
ax[0].scatter(H2O_expmean(Fiege63), H2O_mean(Fiege63), s = sz, c = '#fff7bc', ec = '#171008', lw = 0.5, zorder = 15, label = 'ABWCl-F0x')
ax[0].scatter(H2O_expmean(Fiege63)+0.01, H2O_mean(Fiege63), s = sz_sm, marker = '>', c = '#FFFFFF', ec = '#171008', lw = 0.5, zorder = 20)
ax[0].errorbar(H2O_expmean(Fiege63), H2O_mean(Fiege63), xerr = H2O_expstd(Fiege63), yerr = H2O_mean(Fiege63) * H2O_rsd(Fiege63), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(Fiege73), H2O_mean(Fiege73), s = 120, marker = 'D', c = '#fee392', ec = '#171008', lw = 0.5, zorder = 15, label = 'ABWB-0x')
ax[0].scatter(H2O_expmean(Fiege73)+0.01, H2O_mean(Fiege73), s = sz_sm, marker = '>', c = '#FFFFFF', ec = '#171008', lw = 0.5, zorder = 20)
ax[0].errorbar(H2O_expmean(Fiege73), H2O_mean(Fiege73), xerr = H2O_expstd(Fiege73), yerr = H2O_mean(Fiege73) * H2O_rsd(Fiege73), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(BF73), H2O_mean(BF73), s = 120, marker = 'D', c = '#fec44f', ec = '#171008', lw = 0.5, zorder = 20, label = 'BF73')
ax[0].errorbar(H2O_expmean(BF73), H2O_mean(BF73), xerr = H2O_expstd(BF73), yerr = H2O_mean(BF73) * H2O_rsd(BF73), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(BF76), H2O_mean(BF76), s = 120, marker = 'D', c = '#fb9a29', ec = '#171008', lw = 0.5, zorder = 20, label = 'BF76')
ax[0].errorbar(H2O_expmean(BF76), H2O_mean(BF76), xerr = H2O_expstd(BF76), yerr = H2O_mean(BF76) * H2O_rsd(BF76), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(BF77), H2O_mean(BF77), s = 120, marker = 'D', c = '#ec7014', ec = '#171008', lw = 0.5, zorder = 20, label = 'BF77')
ax[0].errorbar(H2O_expmean(BF77), H2O_mean(BF77), xerr = H2O_expstd(BF77), yerr = H2O_mean(BF77) * H2O_rsd(BF77), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(M35), H2O_mean(M35), s = 120, marker = 'D', c = '#cc4c02', ec = '#171008', lw = 0.5, zorder = 20, label = 'M35')
ax[0].errorbar(H2O_expmean(M35), H2O_mean(M35), xerr = H2O_expstd(M35), yerr = H2O_mean(M35) * H2O_rsd(M35), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(M43), H2O_mean(M43), s = 120, marker = 'D', c = '#983404', ec = '#171008', lw = 0.5, zorder = 20, label = 'M43')
ax[0].errorbar(H2O_expmean(M43), H2O_mean(M43), xerr = H2O_expstd(M43), yerr = H2O_mean(M43) * H2O_rsd(M43), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(NS1), H2O_mean(NS1), s = sz, c = '#fb9929', ec = '#662506', lw = 0.5, zorder = 20, label = 'NS-1')
ax[0].errorbar(H2O_expmean(NS1), H2O_mean(NS1), xerr = H2O_expstd(NS1), yerr = H2O_mean(NS1) * H2O_rsd(NS1), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(ETFSR_Ol8), H2O_mean(ETFSR_Ol8), s = sz, marker = 's', facecolors='white', ec = '#FEE391', lw = 2.5, zorder = 20, label = 'ETFSR-OL8') #c = '#f2821d',
ax[0].errorbar(H2O_expmean(ETFSR_Ol8), H2O_mean(ETFSR_Ol8), xerr = H2O_expstd(ETFSR_Ol8), yerr = H2O_mean(ETFSR_Ol8) * H2O_rsd(ETFSR_Ol8), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(CD33_12_2_2), H2O_mean(CD33_12_2_2), s = sz, marker='s', facecolors='white',  ec = '#FEC44F', lw = 2.5, zorder = 20, label = 'CD33-12-2-2') #c = '#e76b11',
ax[0].errorbar(H2O_expmean(CD33_12_2_2), H2O_mean(CD33_12_2_2), xerr = H2O_expstd(CD33_12_2_2), yerr = H2O_mean(CD33_12_2_2) * H2O_rsd(CD33_12_2_2), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(CD33_22_1_1), H2O_mean(CD33_22_1_1), s = sz, marker='s',facecolors='white', ec = '#FB9A29', lw = 2.5, zorder = 20, label = 'CD33-22-1-1') #c = '#d55607',
ax[0].errorbar(H2O_expmean(CD33_22_1_1), H2O_mean(CD33_22_1_1), xerr = H2O_expstd(CD33_22_1_1), yerr = H2O_mean(CD33_22_1_1) * H2O_rsd(CD33_22_1_1), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(STD_D1010), H2O_mean(STD_D1010), s = sz, facecolors='white', ec = '#EC7014', lw = 2.5, zorder = 20, label = 'D1010') #c = '#bc4503', 
ax[0].errorbar(H2O_expmean(STD_D1010), H2O_mean(STD_D1010), xerr = H2O_expstd(STD_D1010), yerr = H2O_mean(STD_D1010) * H2O_rsd(STD_D1010), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(ALV1833_11), H2O_mean(ALV1833_11), s = sz, facecolors='white', ec = '#CC4C02', lw = 2.5, zorder = 20, label = 'ALV1833-11') #c = '#a03704', 
ax[0].errorbar(H2O_expmean(ALV1833_11), H2O_mean(ALV1833_11), xerr = H2O_expstd(ALV1833_11), yerr = H2O_mean(ALV1833_11) * H2O_rsd(ALV1833_11), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(WOK5_4), H2O_mean(WOK5_4), s = sz, facecolors='white', ec = '#993404', lw = 2.5, zorder = 20, label = '23WOK5-4') #c = '#832d05',
ax[0].errorbar(H2O_expmean(WOK5_4), H2O_mean(WOK5_4), xerr = H2O_expstd(WOK5_4), yerr = H2O_mean(WOK5_4) * H2O_rsd(WOK5_4), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(ALV1846), H2O_mean(ALV1846), s = sz, facecolors='white', ec = '#662506', lw = 2.5, zorder = 20, label = '21ALV1846-9') #c = '#662506',
ax[0].errorbar(H2O_expmean(ALV1846), H2O_mean(ALV1846), xerr = H2O_expstd(ALV1846), yerr = H2O_mean(ALV1846) * H2O_rsd(ALV1846), lw = 0.5, c = 'k', zorder = 10)

ax[0].set_xlim([0, 5])
ax[0].set_ylim([0, 5])
ax[0].set_xlabel('$\mathregular{H_2O}$ Expected (wt.%)')
ax[0].set_ylabel('LDEO FTIR $\mathregular{H_2O_t}$ with PyIRoGlass (wt.%)')
l1 = ax[0].legend(loc = 'lower right', labelspacing = 0.2, handletextpad = 0.25, handlelength = 1.00, prop={'size': 13}, frameon=False)
ax[0].tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax[0].tick_params(axis="y", direction='in', length=5, pad = 6.5)

ftir_sym = ax[0].scatter(np.nan, np.nan, s = sz, ec = '#171008', facecolors='white', lw = 0.5, zorder = 20, label = 'FTIR')
sims_sym = ax[0].scatter(np.nan, np.nan, s = 100, marker = 's', ec = '#171008', facecolors='white', lw = 0.5, zorder = 20, label = 'SIMS')
kft_sym = ax[0].scatter(np.nan, np.nan, s = 100, marker = 'D', ec = '#171008', facecolors='white', lw = 0.5, zorder = 20, label = 'KFT')
ea_sym = ax[0].scatter(np.nan, np.nan, s = sz+10, marker = 'p', ec = '#171008', facecolors='white', lw = 0.5, zorder = 20, label = 'KFT')
sat_symb = ax[0].scatter(np.nan, np.nan, s = sz_sm, marker = '>', ec = '#171008', facecolors='white', lw = 0.5, zorder = 20, label = '$\mathregular{H_2O_{t, 3550}}$ Saturated')
ax[0].legend([ftir_sym, sims_sym, kft_sym, ea_sym, sat_symb], ['FTIR', 'SIMS', 'KFT', 'EA', '$\mathregular{H_2O_{t, 3550}}$ Saturated'], loc = (0.0025, 0.50), labelspacing = 0.3, handletextpad = 0.25, handlelength = 1.00, prop={'size': 12.5}, frameon=True)
ax[0].add_artist(l1)
ax[0].annotate("A.", xy=(0.02, 0.95), xycoords="axes fraction", fontsize=20, weight='bold')

h2o_exp = np.array([H2O_expmean(Fiege63), H2O_expmean(Fiege73), H2O_expmean(BF73), H2O_expmean(BF76), H2O_expmean(BF77), H2O_expmean(M35), H2O_expmean(M43), H2O_expmean(NS1), H2O_expmean(ETFSR_Ol8), 
                    H2O_expmean(CD33_12_2_2), H2O_expmean(CD33_22_1_1), H2O_expmean(STD_D1010), H2O_expmean(ALV1833_11), H2O_expmean(WOK5_4), H2O_expmean(ALV1846)]) # 
h2o_py = np.array([H2O_mean(Fiege63), H2O_mean(Fiege73), H2O_mean(BF73), H2O_mean(BF76), H2O_mean(BF77), H2O_mean(M35), H2O_mean(M43), H2O_mean(NS1), H2O_mean(ETFSR_Ol8), 
                    H2O_mean(CD33_12_2_2), H2O_mean(CD33_22_1_1), H2O_mean(STD_D1010), H2O_mean(ALV1833_11), H2O_mean(WOK5_4), H2O_mean(ALV1846)]) 
slope0, intercept0, r_value0, p_value0, std_err0 = scipy.stats.linregress(h2o_exp, h2o_py)
ccc0 = concordance_correlation_coefficient(h2o_exp, h2o_py)
rmse0 = mean_squared_error(h2o_exp, h2o_py, squared=False)

ax[0].annotate("$\mathregular{R^{2}}$="+str(np.round(r_value0**2, 2)), xy=(0.02, 0.8275), xycoords="axes fraction", fontsize=16)
ax[0].annotate("CCC="+str(np.round(ccc0, 2)), xy=(0.02, 0.91), xycoords="axes fraction", fontsize=16)
ax[0].annotate("RMSE="+str(np.round(rmse0, 2)), xy=(0.02, 0.87), xycoords="axes fraction", fontsize=16)
ax[0].annotate("m="+str(np.round(slope0, 2)), xy=(0.02, 0.79), xycoords="axes fraction", fontsize=16)
ax[0].annotate("b="+str(np.round(intercept0, 2)), xy=(0.02, 0.75), xycoords="axes fraction", fontsize=16)



ax[1].plot(co2_line, co2_line, 'k', lw = 0.5, zorder = 0)
ax[1].scatter(CO2_expmean(BF73), CO2_mean(BF73)*347.263295529885/265, s = sz+10, marker = 'p', c = '#fec44f', ec = '#171008', lw = 0.5, zorder = 20, label = 'BF73')
ax[1].errorbar(CO2_expmean(BF73), CO2_mean(BF73)*347.263295529885/265, xerr = CO2_expstd(BF73), yerr = CO2_mean(BF73) * CO2_rsd(BF73) * 2 *347.263295529885/265, lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(BF76), CO2_mean(BF76)*347.263295529885/265, s = sz+10, marker = 'p', c = '#fb9a29', ec = '#171008', lw = 0.5, zorder = 20, label = 'BF76')
ax[1].errorbar(CO2_expmean(BF76), CO2_mean(BF76)*347.263295529885/265, xerr = CO2_expstd(BF76), yerr = CO2_mean(BF76) * CO2_rsd(BF76) * 2 *347.263295529885/265, lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(BF77), CO2_mean(BF77)*347.263295529885/265, s = sz+10, marker = 'p', c = '#ec7014', ec = '#171008', lw = 0.5, zorder = 20, label = 'BF77')
ax[1].errorbar(CO2_expmean(BF77), CO2_mean(BF77)*347.263295529885/265, xerr = CO2_expstd(BF77), yerr = CO2_mean(BF77) * CO2_rsd(BF77) * 2*347.263295529885/265, lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(M35), CO2_mean(M35)*337.751174/317, s = sz, c = '#cc4c02', ec = '#171008', lw = 0.5, zorder = 20, label = 'M35')
ax[1].errorbar(CO2_expmean(M35), CO2_mean(M35)*337.751174/317, xerr = CO2_expstd(M35), yerr = CO2_mean(M35) * CO2_rsd(M35)* 2*337.751174/317, lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(M43), CO2_mean(M43)*344.6140439/317, s = sz, c = '#983404', ec = '#171008', lw = 0.5, zorder = 20, label = 'M43')
ax[1].errorbar(CO2_expmean(M43), CO2_mean(M43)*344.6140439/317, xerr = CO2_expstd(M43), yerr = CO2_mean(M43) * CO2_rsd(M43) * 2*344.6140439/317, lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(NS1), CO2_mean(NS1)*335.2796384/375, s = sz, marker='s', c = '#fb9929', ec = '#171008', lw = 0.5, zorder = 20, label = 'NS-1')
ax[1].errorbar(CO2_expmean(NS1), CO2_mean(NS1)*335.2796384/375, xerr = CO2_expstd(NS1), yerr = CO2_mean(NS1) * CO2_rsd(NS1) * 2/335.2796384*375, lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(CD33_12_2_2), CO2_mean(CD33_12_2_2), s = sz, marker = 's', facecolors='white', ec = '#FEC44F', lw = 2.5, zorder = 20, label = 'CD33-12-2-2')
ax[1].errorbar(CO2_expmean(CD33_12_2_2), CO2_mean(CD33_12_2_2), xerr = CO2_expstd(CD33_12_2_2), yerr = CO2_mean(CD33_12_2_2) * CO2_rsd(CD33_12_2_2) * 2, lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(CD33_22_1_1), CO2_mean(CD33_22_1_1), s = sz, marker = 's', facecolors='white', ec = '#FB9A29', lw = 2.5, zorder = 20, label = 'CD33-22-1-1')
ax[1].errorbar(CO2_expmean(CD33_22_1_1), CO2_mean(CD33_22_1_1), xerr = CO2_expstd(CD33_22_1_1), yerr = CO2_mean(CD33_22_1_1) * CO2_rsd(CD33_22_1_1) * 2, lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(STD_D1010), CO2_mean(STD_D1010)*315.7646212/375, s = sz, facecolors='white', ec = '#EC7014', lw = 2.5, zorder = 20, label = 'D1010')
ax[1].errorbar(CO2_expmean(STD_D1010), CO2_mean(STD_D1010)*315.7646212/375, xerr = CO2_expstd(STD_D1010), yerr = CO2_mean(STD_D1010) * CO2_rsd(STD_D1010) * 2*315.7646212/375, lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(ALV1833_11), CO2_mean(ALV1833_11)*353.8503071/375, s = sz, facecolors='white', ec = '#CC4C02', lw = 2.5, zorder = 20, label = 'ALV1833-11')
ax[1].errorbar(CO2_expmean(ALV1833_11), CO2_mean(ALV1833_11)*353.8503071/375, xerr = CO2_expstd(ALV1833_11), yerr = CO2_mean(ALV1833_11) * CO2_rsd(ALV1833_11) * 2*353.8503071/375, lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(WOK5_4), CO2_mean(WOK5_4)*310.7007261/375, s = sz, facecolors='white', ec = '#993404', lw = 2.5, zorder = 20, label = '23WOK5-4')
ax[1].errorbar(CO2_expmean(WOK5_4), CO2_mean(WOK5_4)*310.7007261/375, xerr = CO2_expstd(WOK5_4), yerr = CO2_mean(WOK5_4) * CO2_rsd(WOK5_4) * 2*310.7007261/375, lw = 0.5, c = 'k', zorder = 10)

ax[1].set_xlim([0, 4000]) # 4250
ax[1].set_ylim([0, 4000])
ax[1].set_xlabel('$\mathregular{CO_2}$ Expected (ppm)')
ax[1].set_ylabel('LDEO FTIR $\mathregular{CO_2}$ with PyIRoGlass (ppm)')
ax[1].tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax[1].tick_params(axis="y", direction='in', length=5, pad = 6.5)
ax[1].legend(loc = 'lower right', labelspacing = 0.2, handletextpad = 0.25, handlelength = 1.00, prop={'size': 13}, frameon=False)
ax[1].annotate("B.", xy=(0.02, 0.95), xycoords="axes fraction", fontsize=20, weight='bold')

co2_exp = np.array([CO2_expmean(BF73), CO2_expmean(BF76), CO2_expmean(BF77), CO2_expmean(M35), CO2_expmean(M43), CO2_expmean(NS1),
                    CO2_expmean(CD33_12_2_2), CO2_expmean(CD33_22_1_1), CO2_expmean(STD_D1010), CO2_expmean(ALV1833_11), CO2_expmean(WOK5_4)])
co2_py = np.array([CO2_mean(BF73)*347.263295529885/265, CO2_mean(BF76)*347.263295529885/265, CO2_mean(BF77)*347.263295529885/265, CO2_mean(M35)*337.751174/317, CO2_mean(M43)*344.6140439/317, CO2_mean(NS1)*335.2796384/375,
                    CO2_mean(CD33_12_2_2), CO2_mean(CD33_22_1_1), CO2_mean(STD_D1010)*315.7646212/375, CO2_mean(ALV1833_11)*353.8503071/375, CO2_mean(WOK5_4)*310.7007261/375])
slope1, intercept1, r_value1, p_value1, std_err1 = scipy.stats.linregress(co2_exp, co2_py)
ccc1 = concordance_correlation_coefficient(co2_exp, co2_py)
rmse1 = mean_squared_error(co2_exp, co2_py, squared=False)

ax[1].annotate("$\mathregular{R^{2}}$="+str(np.round(r_value1**2, 2)), xy=(0.02, 0.8275), xycoords="axes fraction", fontsize=16)
ax[1].annotate("CCC="+str(np.round(ccc1, 2)), xy=(0.02, 0.91), xycoords="axes fraction", fontsize=16)
ax[1].annotate("RMSE="+str(np.round(rmse1, 2)), xy=(0.02, 0.87), xycoords="axes fraction", fontsize=16)
ax[1].annotate("m="+str(np.round(slope1, 2)), xy=(0.02, 0.79), xycoords="axes fraction", fontsize=16)
ax[1].annotate("b="+str(np.round(intercept1, 2)), xy=(0.02, 0.75), xycoords="axes fraction", fontsize=16)

plt.tight_layout()
plt.savefig('FTIRSIMS_Comparison3.pdf', bbox_inches='tight', pad_inches = 0.025)
plt.show()
# %%
# h2o_line = np.array([0, 6])
# co2_line = np.array([0, 6000])
# sz_sm = 80
# sz = 150

# fig, ax = plt.subplots(1, 2, figsize = (14, 7))

# ax = ax.flatten()
# ax[0].plot(h2o_line, h2o_line, 'k', lw = 0.5, zorder = 0)
# ax[0].scatter(H2O_expmean(Fiege63), H2O_mean(Fiege63), s = sz, c = '#B2182B', ec = '#171008', lw = 0.5, zorder = 15, label = 'ABWCl-F0x')
# ax[0].scatter(H2O_expmean(Fiege63)+0.01, H2O_mean(Fiege63), s = sz_sm, marker = '>', c = '#FFFFFF', ec = '#171008', lw = 0.5, zorder = 20)
# ax[0].errorbar(H2O_expmean(Fiege63), H2O_mean(Fiege63), xerr = H2O_expstd(Fiege63), yerr = H2O_mean(Fiege63) * H2O_rsd(Fiege63), lw = 0.5, c = 'k', zorder = 10)

# ax[0].scatter(H2O_expmean(Fiege73), H2O_mean(Fiege73), s = 120, marker = 'D', c = '#D6604D', ec = '#171008', lw = 0.5, zorder = 15, label = 'ABWB-0x')
# ax[0].scatter(H2O_expmean(Fiege73)+0.01, H2O_mean(Fiege73), s = sz_sm, marker = '>', c = '#FFFFFF', ec = '#171008', lw = 0.5, zorder = 20)
# ax[0].errorbar(H2O_expmean(Fiege73), H2O_mean(Fiege73), xerr = H2O_expstd(Fiege73), yerr = H2O_mean(Fiege73) * H2O_rsd(Fiege73), lw = 0.5, c = 'k', zorder = 10)

# ax[0].scatter(H2O_expmean(BF73), H2O_mean(BF73), s = 120, marker = 'D', c = '#F4A582', ec = '#171008', lw = 0.5, zorder = 20, label = 'BF73')
# ax[0].errorbar(H2O_expmean(BF73), H2O_mean(BF73), xerr = H2O_expstd(BF73), yerr = H2O_mean(BF73) * H2O_rsd(BF73), lw = 0.5, c = 'k', zorder = 10)

# ax[0].scatter(H2O_expmean(BF76), H2O_mean(BF76), s = 120, marker = 'D', c = '#FDDBC7', ec = '#171008', lw = 0.5, zorder = 20, label = 'BF76')
# ax[0].errorbar(H2O_expmean(BF76), H2O_mean(BF76), xerr = H2O_expstd(BF76), yerr = H2O_mean(BF76) * H2O_rsd(BF76), lw = 0.5, c = 'k', zorder = 10)

# ax[0].scatter(H2O_expmean(BF77), H2O_mean(BF77), s = 120, marker = 'D', c = '#F7F7F7', ec = '#171008', lw = 0.5, zorder = 20, label = 'BF77')
# ax[0].errorbar(H2O_expmean(BF77), H2O_mean(BF77), xerr = H2O_expstd(BF77), yerr = H2O_mean(BF77) * H2O_rsd(BF77), lw = 0.5, c = 'k', zorder = 10)

# ax[0].scatter(H2O_expmean(M35), H2O_mean(M35), s = 120, marker = 'D', c = '#D1E5F0', ec = '#171008', lw = 0.5, zorder = 20, label = 'M35')
# ax[0].errorbar(H2O_expmean(M35), H2O_mean(M35), xerr = H2O_expstd(M35), yerr = H2O_mean(M35) * H2O_rsd(M35), lw = 0.5, c = 'k', zorder = 10)

# ax[0].scatter(H2O_expmean(M43), H2O_mean(M43), s = 120, marker = 'D', c = '#92C5DE', ec = '#171008', lw = 0.5, zorder = 20, label = 'M43')
# ax[0].errorbar(H2O_expmean(M43), H2O_mean(M43), xerr = H2O_expstd(M43), yerr = H2O_mean(M43) * H2O_rsd(M43), lw = 0.5, c = 'k', zorder = 10)

# ax[0].scatter(H2O_expmean(NS1), H2O_mean(NS1), s = sz, c = '#4393C3', ec = '#171008', lw = 0.5, zorder = 20, label = 'NS-1')
# ax[0].errorbar(H2O_expmean(NS1), H2O_mean(NS1), xerr = H2O_expstd(NS1), yerr = H2O_mean(NS1) * H2O_rsd(NS1), lw = 0.5, c = 'k', zorder = 10)

# ax[0].scatter(H2O_expmean(ETFSR_Ol8), H2O_mean(ETFSR_Ol8), s = sz, marker = 's', c = '#FFFFFF', ec = '#171008', lw = 0.5, zorder = 20, label = 'ETFSR-OL8')
# ax[0].errorbar(H2O_expmean(ETFSR_Ol8), H2O_mean(ETFSR_Ol8), xerr = H2O_expstd(ETFSR_Ol8), yerr = H2O_mean(ETFSR_Ol8) * H2O_rsd(ETFSR_Ol8), lw = 0.5, c = 'k', zorder = 10)

# ax[0].scatter(H2O_expmean(CD33_12_2_2), H2O_mean(CD33_12_2_2), s = sz, c = '#E5E5E5', ec = '#171008', lw = 0.5, zorder = 20, label = 'CD33-12-2-2')
# ax[0].errorbar(H2O_expmean(CD33_12_2_2), H2O_mean(CD33_12_2_2), xerr = H2O_expstd(CD33_12_2_2), yerr = H2O_mean(CD33_12_2_2) * H2O_rsd(CD33_12_2_2), lw = 0.5, c = 'k', zorder = 10)

# ax[0].scatter(H2O_expmean(CD33_22_1_1), H2O_mean(CD33_22_1_1), s = sz, c = '#BEBEBE', ec = '#171008', lw = 0.5, zorder = 20, label = 'CD33-22-1-1')
# ax[0].errorbar(H2O_expmean(CD33_22_1_1), H2O_mean(CD33_22_1_1), xerr = H2O_expstd(CD33_22_1_1), yerr = H2O_mean(CD33_22_1_1) * H2O_rsd(CD33_22_1_1), lw = 0.5, c = 'k', zorder = 10)

# ax[0].scatter(H2O_expmean(STD_D1010), H2O_mean(STD_D1010), s = sz, c = '#9D9D9D', ec = '#171008', lw = 0.5, zorder = 20, label = 'D1010')
# ax[0].errorbar(H2O_expmean(STD_D1010), H2O_mean(STD_D1010), xerr = H2O_expstd(STD_D1010), yerr = H2O_mean(STD_D1010) * H2O_rsd(STD_D1010), lw = 0.5, c = 'k', zorder = 10)

# ax[0].scatter(H2O_expmean(ALV1833_11), H2O_mean(ALV1833_11), s = sz, c = '#7D7D7D', ec = '#171008', lw = 0.5, zorder = 20, label = 'ALV1833-11')
# ax[0].errorbar(H2O_expmean(ALV1833_11), H2O_mean(ALV1833_11), xerr = H2O_expstd(ALV1833_11), yerr = H2O_mean(ALV1833_11) * H2O_rsd(ALV1833_11), lw = 0.5, c = 'k', zorder = 10)

# ax[0].scatter(H2O_expmean(WOK5_4), H2O_mean(WOK5_4), s = sz, c = '#5C5C5C', ec = '#171008', lw = 0.5, zorder = 20, label = '23WOK5-4')
# ax[0].errorbar(H2O_expmean(WOK5_4), H2O_mean(WOK5_4), xerr = H2O_expstd(WOK5_4), yerr = H2O_mean(WOK5_4) * H2O_rsd(WOK5_4), lw = 0.5, c = 'k', zorder = 10)

# ax[0].scatter(H2O_expmean(ALV1846), H2O_mean(ALV1846), s = sz, c = '#000000', ec = '#171008', lw = 0.5, zorder = 20, label = '21ALV1846-9')
# ax[0].errorbar(H2O_expmean(ALV1846), H2O_mean(ALV1846), xerr = H2O_expstd(ALV1846), yerr = H2O_mean(ALV1846) * H2O_rsd(ALV1846), lw = 0.5, c = 'k', zorder = 10)

# ax[0].set_xlim([0, 5])
# ax[0].set_ylim([0, 5])
# ax[0].set_xlabel('$\mathregular{H_2O}$ Expected (wt.%)')
# ax[0].set_ylabel('LDEO FTIR $\mathregular{H_2O_t}$ with PyIRoGlass (wt.%)')
# l1 = ax[0].legend(loc = 'lower right', labelspacing = 0.2, handletextpad = 0.25, handlelength = 1.00, prop={'size': 13}, frameon=False)
# ax[0].tick_params(axis="x", direction='in', length=5, pad = 6.5)
# ax[0].tick_params(axis="y", direction='in', length=5, pad = 6.5)

# ftir_sym = ax[0].scatter(np.nan, np.nan, s = sz, ec = '#171008', facecolors='white', lw = 0.5, zorder = 20, label = 'FTIR')
# sims_sym = ax[0].scatter(np.nan, np.nan, s = 100, marker = 's', ec = '#171008', facecolors='white', lw = 0.5, zorder = 20, label = 'SIMS')
# kft_sym = ax[0].scatter(np.nan, np.nan, s = 100, marker = 'D', ec = '#171008', facecolors='white', lw = 0.5, zorder = 20, label = 'KFT')
# ea_sym = ax[0].scatter(np.nan, np.nan, s = sz+10, marker = 'p', ec = '#171008', facecolors='white', lw = 0.5, zorder = 20, label = 'KFT')
# sat_symb = ax[0].scatter(np.nan, np.nan, s = sz_sm, marker = '>', ec = '#171008', facecolors='white', lw = 0.5, zorder = 20, label = '$\mathregular{H_2O_{t, 3550}}$ Saturated')
# ax[0].legend([ftir_sym, sims_sym, kft_sym, sat_symb], ['FTIR', 'SIMS', 'KFT', '$\mathregular{H_2O_{t, 3550}}$ Saturated'], loc = (0.0025, 0.55), labelspacing = 0.3, handletextpad = 0.25, handlelength = 1.00, prop={'size': 12.5}, frameon=True)
# ax[0].add_artist(l1)
# ax[0].annotate("A.", xy=(0.025, 0.95), xycoords="axes fraction", fontsize=20, weight='bold')

# h2o_exp = np.array([H2O_expmean(Fiege63), H2O_expmean(Fiege73), H2O_expmean(BF73), H2O_expmean(BF76), H2O_expmean(BF77), H2O_expmean(M35), H2O_expmean(M43), H2O_expmean(NS1), H2O_expmean(ETFSR_Ol8), 
#                     H2O_expmean(CD33_12_2_2), H2O_expmean(CD33_22_1_1), H2O_expmean(STD_D1010), H2O_expmean(ALV1833_11), H2O_expmean(WOK5_4), H2O_expmean(ALV1846)]) # 
# h2o_py = np.array([H2O_mean(Fiege63), H2O_mean(Fiege73), H2O_mean(BF73), H2O_mean(BF76), H2O_mean(BF77), H2O_mean(M35), H2O_mean(M43), H2O_mean(NS1), H2O_mean(ETFSR_Ol8), 
#                     H2O_mean(CD33_12_2_2), H2O_mean(CD33_22_1_1), H2O_mean(STD_D1010), H2O_mean(ALV1833_11), H2O_mean(WOK5_4), H2O_mean(ALV1846)]) 
# slope0, intercept0, r_value0, p_value0, std_err0 = scipy.stats.linregress(h2o_exp, h2o_py)
# ccc0 = concordance_correlation_coefficient(h2o_exp, h2o_py)
# rmse0 = mean_squared_error(h2o_exp, h2o_py, squared=False)

# ax[0].annotate("$\mathregular{R^{2}}$="+str(np.round(r_value0**2, 2)), xy=(0.02, 0.8275), xycoords="axes fraction", fontsize=13)
# ax[0].annotate("CCC="+str(np.round(ccc0, 2)), xy=(0.02, 0.91), xycoords="axes fraction", fontsize=13)
# ax[0].annotate("RMSE="+str(np.round(rmse0, 2)), xy=(0.02, 0.87), xycoords="axes fraction", fontsize=13)
# ax[0].annotate("m="+str(np.round(slope0, 2)), xy=(0.02, 0.79), xycoords="axes fraction", fontsize=13)
# ax[0].annotate("b="+str(np.round(intercept0, 2)), xy=(0.02, 0.75), xycoords="axes fraction", fontsize=13)



# ax[1].plot(co2_line, co2_line, 'k', lw = 0.5, zorder = 0)
# ax[1].scatter(CO2_expmean(BF73), CO2_mean(BF73)*338.6880953/265, s = sz+10, marker = 's', c = '#F4A582', ec = '#171008', lw = 0.5, zorder = 20, label = 'BF73')
# ax[1].errorbar(CO2_expmean(BF73), CO2_mean(BF73)*338.6880953/265, xerr = CO2_expstd(BF73), yerr = CO2_mean(BF73) * CO2_rsd(BF73) * 2 *338.6880953/265, lw = 0.5, c = 'k', zorder = 10)

# ax[1].scatter(CO2_expmean(BF76), CO2_mean(BF76)*338.6880953/265, s = sz+10, marker = 's', c = '#FDDBC7', ec = '#171008', lw = 0.5, zorder = 20, label = 'BF76')
# ax[1].errorbar(CO2_expmean(BF76), CO2_mean(BF76)*338.6880953/265, xerr = CO2_expstd(BF76), yerr = CO2_mean(BF76) * CO2_rsd(BF76) * 2 *338.6880953/265, lw = 0.5, c = 'k', zorder = 10)

# ax[1].scatter(CO2_expmean(BF77), CO2_mean(BF77)*338.6880953/265, s = sz+10, marker = 's', c = '#F7F7F7', ec = '#171008', lw = 0.5, zorder = 20, label = 'BF77')
# ax[1].errorbar(CO2_expmean(BF77), CO2_mean(BF77)*338.6880953/265, xerr = CO2_expstd(BF77), yerr = CO2_mean(BF77) * CO2_rsd(BF77) * 2*338.6880953/265, lw = 0.5, c = 'k', zorder = 10)

# ax[1].scatter(CO2_expmean(M35), CO2_mean(M35), s = sz, c = '#D1E5F0', ec = '#171008', lw = 0.5, zorder = 20, label = 'M35')
# ax[1].errorbar(CO2_expmean(M35), CO2_mean(M35), xerr = CO2_expstd(M35), yerr = CO2_mean(M35) * CO2_rsd(M35 )* 2, lw = 0.5, c = 'k', zorder = 10)

# ax[1].scatter(CO2_expmean(M43), CO2_mean(M43), s = sz, c = '#92C5DE', ec = '#171008', lw = 0.5, zorder = 20, label = 'M43')
# ax[1].errorbar(CO2_expmean(M43), CO2_mean(M43), xerr = CO2_expstd(M43), yerr = CO2_mean(M43) * CO2_rsd(M43) * 2, lw = 0.5, c = 'k', zorder = 10)

# ax[1].scatter(CO2_expmean(NS1), CO2_mean(NS1)/315.2724799*375, s = sz, marker='s', c = '#4393C3', ec = '#171008', lw = 0.5, zorder = 20, label = 'NS-1')
# ax[1].errorbar(CO2_expmean(NS1), CO2_mean(NS1)/315.2724799*375, xerr = CO2_expstd(NS1), yerr = CO2_mean(NS1) * CO2_rsd(NS1) * 2/315.2724799*375, lw = 0.5, c = 'k', zorder = 10)

# ax[1].scatter(CO2_expmean(CD33_12_2_2), CO2_mean(CD33_12_2_2), s = sz, marker = 's', c = '#E5E5E5', ec = '#171008', lw = 0.5, zorder = 20, label = 'CD33-12-2-2')
# ax[1].errorbar(CO2_expmean(CD33_12_2_2), CO2_mean(CD33_12_2_2), xerr = CO2_expstd(CD33_12_2_2), yerr = CO2_mean(CD33_12_2_2) * CO2_rsd(CD33_12_2_2) * 2, lw = 0.5, c = 'k', zorder = 10)

# ax[1].scatter(CO2_expmean(CD33_22_1_1), CO2_mean(CD33_22_1_1), s = sz, marker = 's', c = '#BEBEBE', ec = '#171008', lw = 0.5, zorder = 20, label = 'CD33-22-1-1')
# ax[1].errorbar(CO2_expmean(CD33_22_1_1), CO2_mean(CD33_22_1_1), xerr = CO2_expstd(CD33_22_1_1), yerr = CO2_mean(CD33_22_1_1) * CO2_rsd(CD33_22_1_1) * 2, lw = 0.5, c = 'k', zorder = 10)

# ax[1].scatter(CO2_expmean(STD_D1010), CO2_mean(STD_D1010), s = sz, c = '#9D9D9D', ec = '#171008', lw = 0.5, zorder = 20, label = 'D1010')
# ax[1].errorbar(CO2_expmean(STD_D1010), CO2_mean(STD_D1010), xerr = CO2_expstd(STD_D1010), yerr = CO2_mean(STD_D1010) * CO2_rsd(STD_D1010) * 2, lw = 0.5, c = 'k', zorder = 10)

# ax[1].scatter(CO2_expmean(ALV1833_11), CO2_mean(ALV1833_11), s = sz, c = '#7D7D7D', ec = '#171008', lw = 0.5, zorder = 20, label = 'ALV1833-11')
# ax[1].errorbar(CO2_expmean(ALV1833_11), CO2_mean(ALV1833_11), xerr = CO2_expstd(ALV1833_11), yerr = CO2_mean(ALV1833_11) * CO2_rsd(ALV1833_11) * 2, lw = 0.5, c = 'k', zorder = 10)

# ax[1].scatter(CO2_expmean(WOK5_4), CO2_mean(WOK5_4), s = sz, c = '#5C5C5C', ec = '#171008', lw = 0.5, zorder = 20, label = '23WOK5-4')
# ax[1].errorbar(CO2_expmean(WOK5_4), CO2_mean(WOK5_4), xerr = CO2_expstd(WOK5_4), yerr = CO2_mean(WOK5_4) * CO2_rsd(WOK5_4) * 2, lw = 0.5, c = 'k', zorder = 10)

# ax[1].set_xlim([0, 5000]) # 4250
# ax[1].set_ylim([0, 5000])
# ax[1].set_xlabel('$\mathregular{CO_2}$ Expected (ppm)')
# ax[1].set_ylabel('LDEO FTIR $\mathregular{CO_2}$ with PyIRoGlass (ppm)')
# ax[1].tick_params(axis="x", direction='in', length=5, pad = 6.5)
# ax[1].tick_params(axis="y", direction='in', length=5, pad = 6.5)
# ax[1].legend(loc = 'lower right', labelspacing = 0.2, handletextpad = 0.25, handlelength = 1.00, prop={'size': 13}, frameon=False)
# ax[1].annotate("B.", xy=(0.025, 0.95), xycoords="axes fraction", fontsize=20, weight='bold')

# co2_exp = np.array([CO2_expmean(BF73), CO2_expmean(BF76), CO2_expmean(BF77), CO2_expmean(M35), CO2_expmean(M43), CO2_expmean(NS1),
#                     CO2_expmean(CD33_12_2_2), CO2_expmean(CD33_22_1_1), CO2_expmean(STD_D1010), CO2_expmean(ALV1833_11), CO2_expmean(WOK5_4)])
# co2_py = np.array([CO2_mean(BF73), CO2_mean(BF76), CO2_mean(BF77), CO2_mean(M35), CO2_mean(M43), CO2_mean(NS1),
#                     CO2_mean(CD33_12_2_2), CO2_mean(CD33_22_1_1), CO2_mean(STD_D1010), CO2_mean(ALV1833_11), CO2_mean(WOK5_4)])
# slope1, intercept1, r_value1, p_value1, std_err1 = scipy.stats.linregress(co2_exp, co2_py)
# ccc1 = concordance_correlation_coefficient(co2_exp, co2_py)
# rmse1 = mean_squared_error(co2_exp, co2_py, squared=False)

# ax[1].annotate("$\mathregular{R^{2}}$="+str(np.round(r_value1**2, 2)), xy=(0.02, 0.8275), xycoords="axes fraction", fontsize=14)
# ax[1].annotate("CCC="+str(np.round(ccc1, 2)), xy=(0.02, 0.91), xycoords="axes fraction", fontsize=14)
# ax[1].annotate("RMSE="+str(np.round(rmse1, 2)), xy=(0.02, 0.87), xycoords="axes fraction", fontsize=14)
# ax[1].annotate("m="+str(np.round(slope1, 2)), xy=(0.02, 0.79), xycoords="axes fraction", fontsize=14)
# ax[1].annotate("b="+str(np.round(intercept1, 2)), xy=(0.02, 0.75), xycoords="axes fraction", fontsize=14)

# plt.tight_layout()
# # plt.savefig('FTIRSIMS_Comparison1.pdf', bbox_inches='tight', pad_inches = 0.025)
# plt.show()

# %% 

# %% 

CO2_stdexpmean = np.array([CO2_expmean(STD_D1010), CO2_expmean(STD_C1),
    CO2_expmean(STD_CN92C_OL2), CO2_expmean(VF74_127_7), CO2_expmean(VF74_132_2),
    CO2_expmean(Fiege63), CO2_expmean(ETFSR_Ol8), CO2_expmean(Fiege73),
    CO2_expmean(CD33_12_2_2), CO2_expmean(CD33_22_1_1), CO2_expmean(ALV1833_11), 
    CO2_expmean(WOK5_4), CO2_expmean(ALV1846)])

CO2_stdexpstd = np.array([CO2_expstd(STD_D1010), CO2_expstd(STD_C1),
    CO2_expstd(STD_CN92C_OL2), CO2_expstd(VF74_127_7), CO2_expstd(VF74_132_2), 
     CO2_expstd(Fiege63), CO2_expstd(ETFSR_Ol8), CO2_expstd(Fiege73),
    CO2_expstd(CD33_12_2_2), CO2_expstd(CD33_22_1_1), CO2_expstd(ALV1833_11), 
    CO2_expstd(WOK5_4), CO2_expstd(ALV1846)])

H2O_stdexpmean = np.array([H2O_expmean(STD_D1010), H2O_expmean(STD_C1),
    H2O_expmean(STD_CN92C_OL2), H2O_expmean(VF74_127_7), H2O_expmean(VF74_132_2),
    H2O_expmean(Fiege63), H2O_expmean(ETFSR_Ol8), H2O_expmean(Fiege73), 
    H2O_expmean(CD33_12_2_2), H2O_expmean(CD33_22_1_1), H2O_expmean(ALV1833_11), 
    H2O_expmean(WOK5_4), H2O_expmean(ALV1846)])

H2O_stdexpstd = np.array([H2O_expstd(STD_D1010), H2O_expstd(STD_C1),
    H2O_expstd(STD_CN92C_OL2), H2O_expstd(VF74_127_7), H2O_expstd(VF74_132_2),
    H2O_expstd(Fiege63), H2O_expstd(ETFSR_Ol8), H2O_expstd(Fiege73),
    H2O_expstd(CD33_12_2_2), H2O_expstd(CD33_22_1_1), H2O_expstd(ALV1833_11), 
    H2O_expstd(WOK5_4), H2O_expstd(ALV1846)])

CO2_stdmean = np.array([CO2_mean(STD_D1010), CO2_mean(STD_C1),
    CO2_mean(STD_CN92C_OL2), CO2_mean(VF74_127_7), CO2_mean(VF74_132_2),
    CO2_mean(Fiege63), CO2_mean(ETFSR_Ol8), CO2_mean(Fiege73), 
    CO2_mean(CD33_12_2_2), CO2_mean(CD33_22_1_1), CO2_mean(ALV1833_11), 
    CO2_mean(WOK5_4), CO2_mean(ALV1846)])

H2O_stdmean = np.array([H2O_mean(STD_D1010), H2O_mean(STD_C1),
    H2O_mean(STD_CN92C_OL2), H2O_mean(VF74_127_7), H2O_mean(VF74_132_2),
    H2O_mean(Fiege63), H2O_mean(ETFSR_Ol8), H2O_mean(Fiege73), 
    H2O_mean(CD33_12_2_2), H2O_mean(CD33_22_1_1), H2O_mean(ALV1833_11), 
    H2O_mean(WOK5_4), H2O_mean(ALV1846), ])

H2O_stdrsd = np.array([H2O_rsd(STD_D1010), H2O_rsd(STD_C1),
    H2O_rsd(STD_CN92C_OL2), H2O_rsd(VF74_127_7), H2O_rsd(VF74_132_2), 
    H2O_rsd(Fiege63), H2O_rsd(ETFSR_Ol8), H2O_rsd(Fiege73), 
    H2O_rsd(CD33_12_2_2), H2O_rsd(CD33_22_1_1), H2O_rsd(ALV1833_11), 
    H2O_rsd(WOK5_4), H2O_rsd(ALV1846)])

CO2_stdrsd = np.array([CO2_rsd(STD_D1010), CO2_rsd(STD_C1),
    CO2_rsd(STD_CN92C_OL2), CO2_rsd(VF74_127_7), CO2_rsd(VF74_132_2),
    CO2_rsd(Fiege63), CO2_rsd(ETFSR_Ol8), CO2_rsd(Fiege73), 
    CO2_rsd(CD33_12_2_2), CO2_rsd(CD33_22_1_1), CO2_rsd(ALV1833_11), 
    CO2_rsd(WOK5_4), CO2_rsd(ALV1846)])

# %%

h2o_line = np.array([0, 6])
co2_line = np.array([0, 1400])
sz_sm = 80
sz = 150

names = np.array(['D1010', 'C1', 'CN92C_OL2', 'VF74_127_7', 'VF74_132_2',
    'Fiege63', 'ETFSR_Ol8', 'Fiege73', 'CD33_12_2_2', 'CD33_22_1_1', 'ALV1833_11', 'WOK5_4', 'ALV1846'])

h2o_vmin, h2o_vmax = min(H2O_stdexpmean), max(H2O_stdmean)


fig, ax = plt.subplots(1, 2, figsize = (18, 8))
ax = ax.flatten()
sc1 = ax[0].plot(h2o_line, h2o_line, 'k', lw = 0.5, zorder = 0)

for i in range(len(names)): 
    if names[i] in ('C1', 'CN92C_OL2', 'VF74_127_7', 'VF74_132_2', 'ETFSR_Ol8'):
        scatter1 = ax[0].scatter(H2O_stdexpmean[i], H2O_stdmean[i], s = sz, marker = 's', c = H2O_stdmean[i], vmin = 0, vmax = h2o_vmax, cmap = 'Blues', ec = '#171008', lw = 0.5, zorder = 20)
        ax[0].errorbar(H2O_stdexpmean[i], H2O_stdmean[i], marker = 's', xerr = H2O_stdexpstd[i], yerr = H2O_stdmean[i] * H2O_stdrsd[i], lw = 0.5, ls = 'none', c = 'k', zorder = 10)
        ax[1].scatter(CO2_stdexpmean[i], CO2_stdmean[i], s = sz, marker = 's', c = H2O_stdmean[i], vmin = 0, vmax = h2o_vmax, cmap = 'Blues', ec = '#171008', lw = 0.5, zorder = 20)
        ax[1].errorbar(CO2_stdexpmean[i], CO2_stdmean[i], xerr = CO2_stdexpstd[i], yerr = CO2_stdmean[i] * CO2_stdrsd[i], lw = 0.5, ls = 'none', c = 'k', zorder = 10)
    elif names[i] in ('Fiege73'):
        scatter1 = ax[0].scatter(H2O_stdexpmean[i], H2O_stdmean[i], s = sz, marker = 'D', c = H2O_stdmean[i], vmin = 0, vmax = h2o_vmax, cmap = 'Blues', ec = '#171008', lw = 0.5, zorder = 20)
        ax[0].errorbar(H2O_stdexpmean[i], H2O_stdmean[i], marker = 's', xerr = H2O_stdexpstd[i], yerr = H2O_stdmean[i] * H2O_stdrsd[i], lw = 0.5, ls = 'none', c = 'k', zorder = 10)
        ax[1].scatter(CO2_stdexpmean[i], CO2_stdmean[i], s = sz, marker = 's', c = H2O_stdmean[i], vmin = 0, vmax = h2o_vmax, cmap = 'Blues', ec = '#171008', lw = 0.5, zorder = 20)
        ax[1].errorbar(CO2_stdexpmean[i], CO2_stdmean[i], xerr = CO2_stdexpstd[i], yerr = CO2_stdmean[i] * CO2_stdrsd[i], lw = 0.5, ls = 'none', c = 'k', zorder = 10)
    else: 
        ax[0].scatter(H2O_stdexpmean[i], H2O_stdmean[i], s = sz, c = H2O_stdmean[i], vmin = 0, vmax = h2o_vmax, cmap = 'Blues', ec = '#171008', lw = 0.5, zorder = 20)
        ax[0].errorbar(H2O_stdexpmean[i], H2O_stdmean[i], xerr = H2O_stdexpstd[i], yerr = H2O_stdmean[i] * H2O_stdrsd[i], lw = 0.5, ls = 'none', c = 'k', zorder = 10)
        ax[1].scatter(CO2_stdexpmean[i], CO2_stdmean[i], s = sz, c = H2O_stdmean[i], vmin = 0, vmax = h2o_vmax, cmap = 'Blues', ec = '#171008', lw = 0.5, zorder = 20)
        ax[1].errorbar(CO2_stdexpmean[i], CO2_stdmean[i], xerr = CO2_stdexpstd[i], yerr = CO2_stdmean[i] * CO2_stdrsd[i], lw = 0.5, ls = 'none', c = 'k', zorder = 10)
ax[0].scatter(H2O_expmean(Fiege63)+0.01, H2O_mean(Fiege63), s = sz_sm, marker = '>', c = '#FFFFFF', ec = '#171008', lw = 0.5, zorder = 20)
ax[0].scatter(H2O_expmean(Fiege73)+0.01, H2O_mean(Fiege73), s = sz_sm, marker = '>', c = '#FFFFFF', ec = '#171008', lw = 0.5, zorder = 20)

ax[0].set_xlim([0, 6])
ax[0].set_ylim([0, 6])
ax[0].set_xlabel('$\mathregular{H_2O}$ Expected (wt.%)')
ax[0].set_ylabel('$\mathregular{H_2O_t}$ Measured by FTIR (wt.%)')
ax[0].tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax[0].tick_params(axis="y", direction='in', length=5, pad = 6.5)

ax[1].plot(co2_line, co2_line, 'k', lw = 0.5, zorder = 0)
ax[1].set_xlim([0, 1400])
ax[1].set_ylim([0, 1400])
ax[1].set_xlabel('$\mathregular{CO_2}$ Expected (ppm)')
ax[1].set_ylabel('$\mathregular{CO_2}$ Measured by FTIR (ppm)')
ax[1].tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax[1].tick_params(axis="y", direction='in', length=5, pad = 6.5)

cbaxes = inset_axes(ax[1], width="15%", height="5%", loc = 'lower right') 
cbar = fig.colorbar(scatter1, cax=cbaxes, orientation='horizontal')
cbaxes.xaxis.set_ticks_position("top")
cbaxes.tick_params(labelsize=12)

ax[1].text(0.905, 0.13, '$\mathregular{H_2O}$ (wt.%)', fontsize = 12, horizontalalignment='center', verticalalignment='center', transform=ax[1].transAxes)
plt.tight_layout()
# plt.savefig('FTIRSIMS_Comparison_H2O.pdf')
plt.show()

# %%
# %%




h2o_line = np.array([0, 6])
co2_line = np.array([0, 1400])
sz_sm = 80
sz = 150
fig, ax = plt.subplots(2, 2, figsize = (14, 14))
ax = ax.flatten()
ax[0].plot(h2o_line, h2o_line, 'k', lw = 0.5, zorder = 0)

ax[0].scatter(H2O_expmean(STD_D1010), H2O_mean(STD_D1010), s = sz, c = '#0C7BDC', ec = '#171008', lw = 0.5, zorder = 20, label = 'D1010')
ax[0].errorbar(H2O_expmean(STD_D1010), H2O_mean(STD_D1010), xerr = H2O_expstd(STD_D1010), yerr = H2O_mean(STD_D1010) * H2O_rsd(STD_D1010), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(STD_C1), H2O_mean(STD_C1), s = sz, marker = 's', c = '#5DB147', ec = '#171008', lw = 0.5, zorder = 20, label = "CN-C-OL1'")
ax[0].errorbar(H2O_expmean(STD_C1), H2O_mean(STD_C1), xerr = H2O_expstd(STD_C1), yerr = H2O_mean(STD_C1) * H2O_rsd(STD_C1), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(STD_CN92C_OL2), H2O_mean(STD_CN92C_OL2), s = sz, marker = 's', c = '#F9E600', ec = '#171008', lw = 0.5, zorder = 20, label = 'CN92C-OL2')
ax[0].errorbar(H2O_expmean(STD_CN92C_OL2), H2O_mean(STD_CN92C_OL2), xerr = H2O_expstd(STD_CN92C_OL2), yerr = H2O_mean(STD_CN92C_OL2) * H2O_rsd(STD_CN92C_OL2), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(VF74_127_7), H2O_mean(VF74_127_7), s = sz, marker = 's', c = '#E42211', ec = '#171008', lw = 0.5, zorder = 20, label = 'VF74-127-7')
ax[0].errorbar(H2O_expmean(VF74_127_7), H2O_mean(VF74_127_7), xerr = H2O_expstd(VF74_127_7), yerr = H2O_mean(VF74_127_7) * H2O_rsd(VF74_127_7), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(VF74_132_2), H2O_mean(VF74_132_2), s = sz, marker = 's', c = '#FE7D10', ec = '#171008', lw = 0.5, zorder = 20, label = 'VF74-132-2')
ax[0].errorbar(H2O_expmean(VF74_132_2), H2O_mean(VF74_132_2), xerr = H2O_expstd(VF74_132_2), yerr = H2O_mean(VF74_132_2) * H2O_rsd(VF74_132_2), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(ETFSR_Ol8), H2O_mean(ETFSR_Ol8), s = sz, marker = 's', c = '#CCCCCC', ec = '#171008', lw = 0.5, zorder = 20, label = 'ETFSR-OL8')
ax[0].errorbar(H2O_expmean(ETFSR_Ol8), H2O_mean(ETFSR_Ol8), xerr = H2O_expstd(ETFSR_Ol8), yerr = H2O_mean(ETFSR_Ol8) * H2O_rsd(ETFSR_Ol8), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(Fiege63), H2O_mean(Fiege63), s = sz, c = '#8A8A8A', ec = '#171008', lw = 0.5, zorder = 15, label = 'ABWCl-F0x')
ax[0].scatter(H2O_expmean(Fiege63)+0.01, H2O_mean(Fiege63), s = sz_sm, marker = '>', c = '#FFFFFF', ec = '#171008', lw = 0.5, zorder = 20)
ax[0].errorbar(H2O_expmean(Fiege63), H2O_mean(Fiege63), xerr = H2O_expstd(Fiege63), yerr = H2O_mean(Fiege63) * H2O_rsd(Fiege63), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(Fiege73), H2O_mean(Fiege73), s = sz, marker = 'D', c = '#252525', ec = '#171008', lw = 0.5, zorder = 15, label = 'ABWB-0x')
ax[0].scatter(H2O_expmean(Fiege73)+0.01, H2O_mean(Fiege73), s = sz_sm, marker = '>', c = '#FFFFFF', ec = '#171008', lw = 0.5, zorder = 20)
ax[0].errorbar(H2O_expmean(Fiege73), H2O_mean(Fiege73), xerr = H2O_expstd(Fiege73), yerr = H2O_mean(Fiege73) * H2O_rsd(Fiege73), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(CD33_12_2_2), H2O_mean(CD33_12_2_2), s = sz, marker = 's', c = '#F7F7F7', ec = '#171008', lw = 0.5, zorder = 20, label = 'CD33-12-2-2')
ax[0].errorbar(H2O_expmean(CD33_12_2_2), H2O_mean(CD33_12_2_2), xerr = H2O_expstd(CD33_12_2_2), yerr = H2O_mean(CD33_12_2_2) * H2O_rsd(CD33_12_2_2), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(CD33_22_1_1), H2O_mean(CD33_22_1_1), s = sz, marker = 's', c = '#CCCCCC', ec = '#171008', lw = 0.5, zorder = 20, label = 'CD33-22-1-1')
ax[0].errorbar(H2O_expmean(CD33_22_1_1), H2O_mean(CD33_22_1_1), xerr = H2O_expstd(CD33_22_1_1), yerr = H2O_mean(CD33_22_1_1) * H2O_rsd(CD33_22_1_1), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(ALV1833_11), H2O_mean(ALV1833_11), s = sz, c = '#969696', ec = '#171008', lw = 0.5, zorder = 20, label = 'ALV1833-11')
ax[0].errorbar(H2O_expmean(ALV1833_11), H2O_mean(ALV1833_11), xerr = H2O_expstd(ALV1833_11), yerr = H2O_mean(ALV1833_11) * H2O_rsd(ALV1833_11), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(WOK5_4), H2O_mean(WOK5_4), s = sz, c = '#636363', ec = '#171008', lw = 0.5, zorder = 20, label = 'WOK5-4')
ax[0].errorbar(H2O_expmean(WOK5_4), H2O_mean(WOK5_4), xerr = H2O_expstd(WOK5_4), yerr = H2O_mean(WOK5_4) * H2O_rsd(WOK5_4), lw = 0.5, c = 'k', zorder = 10)

ax[0].scatter(H2O_expmean(ALV1846), H2O_mean(ALV1846), s = sz, c = '#252525', ec = '#171008', lw = 0.5, zorder = 20, label = 'ALV1846-9')
ax[0].errorbar(H2O_expmean(ALV1846), H2O_mean(ALV1846), xerr = H2O_expstd(ALV1846), yerr = H2O_mean(ALV1846) * H2O_rsd(ALV1846), lw = 0.5, c = 'k', zorder = 10)
ax[0].set_xlim([0, 6])
ax[0].set_ylim([0, 6])
ax[0].annotate("A.", xy=(0.02, 0.95), xycoords="axes fraction", fontsize=20, weight='bold')
# ax[0].set_xlabel('$\mathregular{H_2O}$ Expected (wt.%)')
ax[0].set_ylabel('$\mathregular{H_2O_t}$ Measured by FTIR (wt.%)')
l1 = ax[0].legend(loc = (0.01, 0.445), labelspacing = 0.2, handletextpad = 0.25, handlelength = 1, prop={'size': 13}, frameon=False)
ax[0].tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax[0].tick_params(axis="y", direction='in', length=5, pad = 6.5)

ftir_sym = ax[0].scatter(np.nan, np.nan, s = sz, ec = '#171008', facecolors='white', lw = 0.5, zorder = 20, label = 'FTIR')
sims_sym = ax[0].scatter(np.nan, np.nan, s = 100, marker = 's', ec = '#171008', facecolors='white', lw = 0.5, zorder = 20, label = 'SIMS')
kft_sym = ax[0].scatter(np.nan, np.nan, s = 100, marker = 'D', ec = '#171008', facecolors='white', lw = 0.5, zorder = 20, label = 'KFT')
sat_symb = ax[0].scatter(np.nan, np.nan, s = sz_sm, marker = '>', ec = '#171008', facecolors='white', lw = 0.5, zorder = 20, label = '$\mathregular{H_2O_{t, 3550}}$ Saturated')
ax[0].legend([ftir_sym, sims_sym, kft_sym, sat_symb], ['FTIR', 'SIMS', 'KFT', '$\mathregular{H_2O_{t, 3550}}$ Saturated'], loc = 'lower right', labelspacing = 0.2, handletextpad = 0.25, handlelength = 1.00, prop={'size': 13}, frameon=False)
ax[0].add_artist(l1)


ax[1].plot(co2_line, co2_line, 'k', lw = 0.5, zorder = 0)

ax[1].scatter(CO2_expmean(STD_D1010), CO2_mean(STD_D1010), s = sz, c = '#0C7BDC', ec = '#171008', lw = 0.5, zorder = 20, label = 'D1010')
ax[1].errorbar(CO2_expmean(STD_D1010), CO2_mean(STD_D1010), xerr = CO2_expstd(STD_D1010), yerr = CO2_mean(STD_D1010) * CO2_rsd(STD_D1010), lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(STD_C1), CO2_mean(STD_C1), s = sz, marker = 's', c = '#5DB147', ec = '#171008', lw = 0.5, zorder = 20, label = "CN-C-OL1'")
ax[1].errorbar(CO2_expmean(STD_C1), CO2_mean(STD_C1), xerr = CO2_expstd(STD_C1), yerr = CO2_mean(STD_C1) * CO2_rsd(STD_C1), lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(STD_CN92C_OL2), CO2_mean(STD_CN92C_OL2), s = sz, marker = 's', c = '#F9E600', ec = '#171008', lw = 0.5, zorder = 20, label = 'CN92C-OL2')
ax[1].errorbar(CO2_expmean(STD_CN92C_OL2), CO2_mean(STD_CN92C_OL2), xerr = CO2_expstd(STD_CN92C_OL2), yerr = CO2_mean(STD_CN92C_OL2) * CO2_rsd(STD_CN92C_OL2), lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(VF74_127_7), CO2_mean(VF74_127_7), s = sz, marker = 's', c = '#E42211', ec = '#171008', lw = 0.5, zorder = 20, label = 'VF74-127-7')
ax[1].errorbar(CO2_expmean(VF74_127_7), CO2_mean(VF74_127_7), xerr = CO2_expstd(VF74_127_7), yerr = CO2_mean(VF74_127_7) * CO2_rsd(VF74_127_7), lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(VF74_132_2), CO2_mean(VF74_132_2), s = sz, marker = 's', c = '#FE7D10', ec = '#171008', lw = 0.5, zorder = 20, label = 'VF74-132-2')
ax[1].errorbar(CO2_expmean(VF74_132_2), CO2_mean(VF74_132_2), xerr = CO2_expstd(VF74_132_2), yerr = CO2_mean(VF74_132_2) * CO2_rsd(VF74_132_2), lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(CD33_12_2_2), CO2_mean(CD33_12_2_2), s = sz, marker = 's', c = '#F7F7F7', ec = '#171008', lw = 0.5, zorder = 20, label = 'CD33-12-2-2')
ax[1].errorbar(CO2_expmean(CD33_12_2_2), CO2_mean(CD33_12_2_2), xerr = CO2_expstd(CD33_12_2_2), yerr = CO2_mean(CD33_12_2_2) * CO2_rsd(CD33_12_2_2), lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(CD33_22_1_1), CO2_mean(CD33_22_1_1), s = sz, marker = 's', c = '#CCCCCC', ec = '#171008', lw = 0.5, zorder = 20, label = 'CD33-22-1-1')
ax[1].errorbar(CO2_expmean(CD33_22_1_1), CO2_mean(CD33_22_1_1), xerr = CO2_expstd(CD33_22_1_1), yerr = CO2_mean(CD33_22_1_1) * CO2_rsd(CD33_22_1_1), lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(ALV1833_11), CO2_mean(ALV1833_11), s = sz, c = '#969696', ec = '#171008', lw = 0.5, zorder = 20, label = 'ALV1833-11')
ax[1].errorbar(CO2_expmean(ALV1833_11), CO2_mean(ALV1833_11), xerr = CO2_expstd(ALV1833_11), yerr = CO2_mean(ALV1833_11) * CO2_rsd(ALV1833_11), lw = 0.5, c = 'k', zorder = 10)

ax[1].scatter(CO2_expmean(WOK5_4), CO2_mean(WOK5_4), s = sz, c = '#636363', ec = '#171008', lw = 0.5, zorder = 20, label = 'WOK5-4')
ax[1].errorbar(CO2_expmean(WOK5_4), CO2_mean(WOK5_4), xerr = CO2_expstd(WOK5_4), yerr = CO2_mean(WOK5_4) * CO2_rsd(WOK5_4), lw = 0.5, c = 'k', zorder = 10)

ax[1].set_xlim([0, 1400])
ax[1].set_ylim([0, 1400])
ax[1].annotate("B.", xy=(0.02, 0.95), xycoords="axes fraction", fontsize=20, weight='bold')

# ax[1].set_title('B.')
# ax[1].set_xlabel('$\mathregular{CO_2}$ Expected (ppm)')
ax[1].set_ylabel('$\mathregular{CO_2}$ Measured by FTIR (ppm)')
ax[1].tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax[1].tick_params(axis="y", direction='in', length=5, pad = 6.5)
ax[1].legend(loc = 'lower right', labelspacing = 0.2, handletextpad = 0.25, handlelength = 1.00, prop={'size': 13}, frameon=False)


sc1 = ax[2].plot(h2o_line, h2o_line, 'k', lw = 0.5, zorder = 0)

for i in range(len(names)): 
    if names[i] in ('CD33_12_2_2', 'CD33_22_1_1', 'C1', 'CN92C_OL2', 'VF74_127_7', 'VF74_132_2', 'ETFSR_Ol8'):
        scatter1 = ax[2].scatter(H2O_stdexpmean[i], H2O_stdmean[i], s = sz, marker = 's', c = H2O_stdmean[i], vmin = 0, vmax = 5.25, cmap = 'Blues', ec = '#171008', lw = 0.5, zorder = 20)
        ax[2].errorbar(H2O_stdexpmean[i], H2O_stdmean[i], marker = 's', xerr = H2O_stdexpstd[i], yerr = H2O_stdmean[i] * H2O_stdrsd[i], lw = 0.5, ls = 'none', c = 'k', zorder = 10)
        ax[3].scatter(CO2_stdexpmean[i], CO2_stdmean[i], s = sz, marker = 's', c = H2O_stdmean[i], vmin = 0, vmax = 5.25, cmap = 'Blues', ec = '#171008', lw = 0.5, zorder = 20)
        ax[3].errorbar(CO2_stdexpmean[i], CO2_stdmean[i], xerr = CO2_stdexpstd[i], yerr = CO2_stdmean[i] * CO2_stdrsd[i], lw = 0.5, ls = 'none', c = 'k', zorder = 10)
    elif names[i] in ('Fiege73'):
        scatter2 = ax[2].scatter(H2O_stdexpmean[i], H2O_stdmean[i], s = sz, marker = 'D', c = H2O_stdmean[i], vmin = 0, vmax = 5.25, cmap = 'Blues', ec = '#171008', lw = 0.5, zorder = 20)
        ax[2].errorbar(H2O_stdexpmean[i], H2O_stdmean[i], marker = 's', xerr = H2O_stdexpstd[i], yerr = H2O_stdmean[i] * H2O_stdrsd[i], lw = 0.5, ls = 'none', c = 'k', zorder = 10)
        ax[3].scatter(CO2_stdexpmean[i], CO2_stdmean[i], s = sz, marker = 's', c = H2O_stdmean[i], vmin = 0, vmax = 5.25, cmap = 'Blues', ec = '#171008', lw = 0.5, zorder = 20)
        ax[3].errorbar(CO2_stdexpmean[i], CO2_stdmean[i], xerr = CO2_stdexpstd[i], yerr = CO2_stdmean[i] * CO2_stdrsd[i], lw = 0.5, ls = 'none', c = 'k', zorder = 10)
    else: 
        ax[2].scatter(H2O_stdexpmean[i], H2O_stdmean[i], s = sz, c = H2O_stdmean[i], vmin = 0, vmax = 5.25, cmap = 'Blues', ec = '#171008', lw = 0.5, zorder = 20)
        ax[2].errorbar(H2O_stdexpmean[i], H2O_stdmean[i], xerr = H2O_stdexpstd[i], yerr = H2O_stdmean[i] * H2O_stdrsd[i], lw = 0.5, ls = 'none', c = 'k', zorder = 10)
        ax[3].scatter(CO2_stdexpmean[i], CO2_stdmean[i], s = sz, c = H2O_stdmean[i], vmin = 0, vmax = 5.25, cmap = 'Blues', ec = '#171008', lw = 0.5, zorder = 20)
        ax[3].errorbar(CO2_stdexpmean[i], CO2_stdmean[i], xerr = CO2_stdexpstd[i], yerr = CO2_stdmean[i] * CO2_stdrsd[i], lw = 0.5, ls = 'none', c = 'k', zorder = 10)
ax[2].scatter(H2O_expmean(Fiege63)+0.01, H2O_mean(Fiege63), s = sz_sm, marker = '>', c = '#FFFFFF', ec = '#171008', lw = 0.5, zorder = 20)
ax[2].scatter(H2O_expmean(Fiege73)+0.01, H2O_mean(Fiege73), s = sz_sm, marker = '>', c = '#FFFFFF', ec = '#171008', lw = 0.5, zorder = 20)

ax[2].set_xlim([0, 6])
ax[2].set_ylim([0, 6])
ax[2].annotate("C.", xy=(0.02, 0.95), xycoords="axes fraction", fontsize=20, weight='bold')
ax[2].set_xlabel('$\mathregular{H_2O}$ Expected (wt.%)')
ax[2].set_ylabel('$\mathregular{H_2O_t}$ Measured by FTIR (wt.%)')
ax[2].tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax[2].tick_params(axis="y", direction='in', length=5, pad = 6.5)

ax[3].plot(co2_line, co2_line, 'k', lw = 0.5, zorder = 0)
ax[3].set_xlim([0, 1400])
ax[3].set_ylim([0, 1400])
ax[3].annotate("D.", xy=(0.02, 0.95), xycoords="axes fraction", fontsize=20, weight='bold')
ax[3].set_xlabel('$\mathregular{CO_2}$ Expected (ppm)')
ax[3].set_ylabel('$\mathregular{CO_2}$ Measured by FTIR (ppm)')
ax[3].tick_params(axis="x", direction='in', length=5, pad = 6.5)
ax[3].tick_params(axis="y", direction='in', length=5, pad = 6.5)

cbaxes = inset_axes(ax[2], width="25%", height="7.5%", loc = 'lower right') 
cbar = fig.colorbar(scatter1, cax=cbaxes, orientation='horizontal')
cbaxes.xaxis.set_ticks_position("top")
cbaxes.tick_params(labelsize=16, pad=-2.5)
cbaxes = inset_axes(ax[3], width="25%", height="7.5%", loc = 'lower right') 
cbar = fig.colorbar(scatter1, cax=cbaxes, orientation='horizontal')
cbaxes.xaxis.set_ticks_position("top")
cbaxes.tick_params(labelsize=16, pad=-2.5)

ax[2].text(0.845, 0.16, '$\mathregular{H_2O}$ (wt.%)', fontsize = 18, horizontalalignment='center', verticalalignment='center', transform=ax[2].transAxes)
ax[3].text(0.845, 0.16, '$\mathregular{H_2O}$ (wt.%)', fontsize = 18, horizontalalignment='center', verticalalignment='center', transform=ax[3].transAxes)
plt.tight_layout()
# plt.savefig('FTIRSIMS_Comparison_combined.pdf', bbox_inches='tight', pad_inches = 0.025)

# %%
# %% 
# %% 
# %% 
# %% 
# %% 

df0 = pd.read_csv(path_parent + '/' + output_dir[-1] + '/' + OUTPUT_PATH[0] + '_DF.csv', index_col = 0)
df1 = pd.read_csv(path_parent + '/' + output_dir[-1] + '/' + OUTPUT_PATH[1] + '_DF.csv', index_col = 0)
df2 = pd.read_csv(path_parent + '/' + output_dir[-1] + '/' + OUTPUT_PATH[2] + '_DF.csv', index_col = 0)
df3 = pd.read_csv(path_parent + '/' + output_dir[-1] + '/' + OUTPUT_PATH[3] + '_DF.csv', index_col = 0)
df4 = pd.read_csv(path_parent + '/' + output_dir[-1] + '/' + OUTPUT_PATH[4] + '_DF.csv', index_col = 0)
df5 = pd.read_csv(path_parent + '/' + output_dir[-1] + '/' + OUTPUT_PATH[5] + '_DF.csv', index_col = 0)

t0 = pd.read_csv(CHEMTHICK_PATH[0], index_col = 0)
t1 = pd.read_csv(CHEMTHICK_PATH[1], index_col = 0)
t2 = pd.read_csv(CHEMTHICK_PATH[2], index_col = 0)
t3 = pd.read_csv(CHEMTHICK_PATH[3], index_col = 0)
t4 = pd.read_csv(CHEMTHICK_PATH[4], index_col = 0)
t5 = pd.read_csv(CHEMTHICK_PATH[5], index_col = 0)


col_lim = ['AVG_BL_BP', 'PCA1_BP', 'PCA2_BP', 'PCA3_BP', 'PCA4_BP', 'm_BP', 'b_BP']
chem_lim = ['SiO2', 'TiO2', 'Al2O3', 'Fe2O3', 'FeO', 'MgO', 'CaO', 'Na2O', 'K2O', 'P2O5']

df = pd.concat([df0, df1, df2]) #, df3, df4, df5]) #, df1])
t = pd.concat([t0, t1, t2]) #, t3, t4, t5]) #, t1], axis=0)

dft = pd.concat([df[col_lim], t[chem_lim]], axis=1)
dft_norm = dft.copy()

dft_norm[col_lim[0]] = dft[col_lim[0]] / t.Thickness.ravel() * 100
dft_norm[col_lim[1]] = dft[col_lim[1]] / t.Thickness.ravel() * 100
dft_norm[col_lim[2]] = dft[col_lim[2]] / t.Thickness.ravel() * 100
dft_norm[col_lim[3]] = dft[col_lim[3]] / t.Thickness.ravel() * 100
dft_norm[col_lim[4]] = dft[col_lim[4]] / t.Thickness.ravel() * 100
dft_norm[col_lim[5]] = dft[col_lim[5]] / t.Thickness.ravel() * 100
dft_norm[col_lim[6]] = dft[col_lim[6]] / t.Thickness.ravel() * 100

dft_norm['Fe2O3T'] = np.nan
dft_norm['FeOT'] = np.nan

def Fe_Conversion(df):

    """
    Handle inconsistent Fe speciation in PetDB datasets by converting all to FeOT. 

    Parameters
    --------------
    df:class:`pandas.DataFrame`
        Array of oxide compositions.

    Returns
    --------
    df:class:`pandas.DataFrame`
        Array of oxide compositions with corrected Fe.
    """

    fe_conv = 1.1113
    conditions = [~np.isnan(df['FeO']) & np.isnan(df['FeOT']) & np.isnan(df['Fe2O3']) & np.isnan([df['Fe2O3T']]),
    ~np.isnan(df['FeOT']) & np.isnan(df['FeO']) & np.isnan(df['Fe2O3']) & np.isnan([df['Fe2O3T']]), 
    ~np.isnan(df['Fe2O3']) & np.isnan(df['Fe2O3T']) & np.isnan(df['FeO']) & np.isnan([df['FeOT']]), # 2
    ~np.isnan(df['Fe2O3T']) & np.isnan(df['Fe2O3']) & np.isnan(df['FeO']) & np.isnan([df['FeOT']]), # 2
    ~np.isnan(df['FeO']) & ~np.isnan(df['Fe2O3']) & np.isnan(df['FeOT']) & np.isnan([df['Fe2O3T']]), # 3
    ~np.isnan(df['FeO']) & ~np.isnan(df['FeOT']) & ~np.isnan(df['Fe2O3']) & np.isnan([df['Fe2O3T']]), # 4
    ~np.isnan(df['FeO']) & ~np.isnan(df['Fe2O3']) & ~np.isnan(df['Fe2O3T']) & np.isnan([df['FeOT']]), # 5
    ~np.isnan(df['FeOT']) & ~np.isnan(df['Fe2O3']) & np.isnan(df['Fe2O3T']) & np.isnan([df['FeO']]), # 6
    ~np.isnan(df['Fe2O3']) & ~np.isnan(df['Fe2O3T']) & np.isnan(df['FeO']) & np.isnan([df['FeOT']]) ] # 7

    choices = [ (df['FeO']), (df['FeOT']),
    (df['Fe2O3']),(df['Fe2O3T']),
    (df['FeO'] + (df['Fe2O3'] / fe_conv)), # 3
    (df['FeOT']), # 4 of interest
    (df['Fe2O3T'] / fe_conv), # 5
    (df['FeOT']), # 6
    (df['Fe2O3T'] / fe_conv) ] # 7

    df.insert(10, 'FeOT_F', np.select(conditions, choices))

    return df 


dft_fe_norm = Fe_Conversion(dft_norm)
dft_fe_norm = dft_fe_norm[['AVG_BL_BP', 'PCA1_BP', 'PCA2_BP', 'PCA3_BP', 'PCA4_BP', 'm_BP', 'b_BP',
       'SiO2', 'TiO2', 'Al2O3', 'FeOT_F', 'MgO', 'CaO', 'Na2O', 'K2O', 'P2O5']]
dft_fe_norm = dft_fe_norm.rename(columns={'FeOT_F': 'FeO'})

dft_mol_norm = dft_fe_norm.copy()
dft_mol_norm['SiO2'] = dft_mol_norm['SiO2'] / 60.08
dft_mol_norm['TiO2'] = dft_mol_norm['TiO2'] / 79.866
dft_mol_norm['Al2O3'] = dft_mol_norm['Al2O3'] / 101.96
dft_mol_norm['FeO'] = dft_mol_norm['FeO'] / 71.844
dft_mol_norm['MgO'] = dft_mol_norm['MgO'] / 40.3044
dft_mol_norm['CaO'] = dft_mol_norm['CaO'] / 56.0774
dft_mol_norm['Na2O'] = dft_mol_norm['Na2O'] / 61.9789
dft_mol_norm['K2O'] = dft_mol_norm['K2O'] / 94.2
dft_mol_norm['P2O5'] = dft_mol_norm['P2O5'] / 141.9445


df_norm_lim = dft_fe_norm.copy()
df_norm_lim = df_norm_lim[df_norm_lim['K2O'] < 3]
df_norm_lim = df_norm_lim[df_norm_lim['TiO2'] < 2]
df_norm_lim = df_norm_lim[df_norm_lim['MgO'] < 10]

# %% 

rc('font',**{'family':'Avenir', 'size': 12})
plt.rcParams["xtick.labelsize"] = 12 # Sets size of numbers on tick marks
plt.rcParams["ytick.labelsize"] = 12 # Sets size of numbers on tick marks
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["axes.labelsize"] = 12 # Axes labels

pd.plotting.scatter_matrix(df_norm_lim, figsize = (15, 15), hist_kwds={'bins':20})
plt.show()

# %% 

dft_mol_norm = dft_mol_norm[dft_mol_norm['AVG_BL_BP'] < 6]
dft_mol_norm = dft_mol_norm[dft_mol_norm['K2O'] < 0.03]

pd.plotting.scatter_matrix(dft_mol_norm, figsize = (15, 15), hist_kwds={'bins':20})
plt.show()


# %% 

df_cat_norm = dft_mol_norm.copy()
