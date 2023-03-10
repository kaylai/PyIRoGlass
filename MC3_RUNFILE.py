# %% -*- coding: utf-8 -*-
""" Created on June 12, 2021 // @author: Sarah Shi and Henry Towbin """

# %% Import packages

import os
import glob
import numpy as np
import pandas as pd
import mc3
import MC3_BASELINES as baselines

import matplotlib
from matplotlib import pyplot as plt
from matplotlib import rc, cm

%matplotlib inline
%config InlineBackend.figure_format = 'retina'
# rc('font',**{'size': 12}) # 'family':'Avenir'

# %% 

# Get working paths 
path_parent = os.path.dirname(os.getcwd())
path_beg = os.getcwd() + '/'
path_input = os.getcwd() + '/Inputs/'
output_dir = ["FIGURES", "PLOTFILES", "NPZFILES", "LOGFILES", "FINALDATA"] 

# Create output directories if not in existence 
for ii in range(len(output_dir)):
    if not os.path.exists(path_beg + output_dir[ii]):
       os.makedirs(path_beg + output_dir[ii], exist_ok=True)

# Change paths to direct to folder with SampleSpectra -- last bit should be whatever your folder with spectra is called. 
PATHS = [path_input+'SampleSpectra/Fuego/', path_input+'SampleSpectra/Standards/', path_input+'SampleSpectra/Fuego1974RH/', path_input+'SampleSpectra/SIMS/', path_input+'SampleSpectra/SIMSStd_2/']

# Put ChemThick file in Inputs. Direct to what your ChemThick file is called. 
CHEMTHICK_PATH = [path_input+'FuegoChemThick.csv', path_input+'StandardChemThick.csv', path_input+'DanRHChemThick.csv', path_input+'SIMSChemThick.csv', path_input+'SIMSChemThick_2.csv']

# Change last value in list to be what you want your output directory to be called. 
INPUT_PATHS = [[path_input+'Baseline_AvgPCA.csv', path_input+"Water_Peak_1635_All.csv", path_beg, 'FUEGO_F'],
                [path_input+'Baseline_AvgPCA.csv', path_input+"Water_Peak_1635_All.csv", path_beg, 'STD_F'], 
                [path_input+'Baseline_AvgPCA.csv', path_input+"Water_Peak_1635_All.csv", path_beg, 'FRH_F'],
                [path_input+'Baseline_AvgPCA.csv', path_input+"Water_Peak_1635_All.csv", path_beg, 'SIMS_F'],
                [path_input+'Baseline_AvgPCA.csv', path_input+"Water_Peak_1635_All.csv", path_beg, 'SIMS2_F']]

# Change to be what you want the prefix of your output files to be. 
OUTPUT_PATH = ['F18', 'STD', 'FRH', 'SIMSSTD', 'SIMSSTD2']

# %% 

REF_PATH = path_input + '/ReflectanceSpectra/FuegoOl/'
REF_FILES = glob.glob(REF_PATH + "*")
REF_FILES.sort()

REF_DFS_FILES, REF_DFS_DICT = baselines.Load_SampleCSV(REF_FILES, wn_high = 2800, wn_low = 2000)

# Use DHZ parameterization of olivine reflectance index. 
n_ol = baselines.ReflectanceIndex(0.72)

REF_FUEGO = baselines.ThicknessProcessing(REF_DFS_DICT, n = n_ol, wn_high = 2700, wn_low = 2100, remove_baseline = True, plotting = False, phaseol = True)

# %% 

REF_PATH = path_input + '/ReflectanceSpectra/rf_ND70/'
REF_FILES = glob.glob(REF_PATH + "*")
REF_FILES.sort()

REF_DFS_FILES, REF_DFS_DICT = baselines.Load_SampleCSV(REF_FILES, wn_high = 2850, wn_low = 1700)

# n=1.546 in the range of 2000-2700 cm^-1 following Nichols and Wysoczanski, 2007 for basaltic glass
n_gl = 1.546

REF_FUEGO = baselines.ThicknessProcessing(REF_DFS_DICT, n = n_gl, wn_high = 2850, wn_low = 1700, remove_baseline = True, plotting = False, phaseol = False)

# %%

simsno = 3 

PATH = PATHS[simsno]
FILES = glob.glob(PATH + "*")
FILES.sort()

MICOMP, THICKNESS = baselines.Load_ChemistryThickness(CHEMTHICK_PATH[simsno])

DFS_FILES, DFS_DICT = baselines.Load_SampleCSV(FILES, wn_high = 5500, wn_low = 1000)
DF_OUTPUT, FAILURES = baselines.Run_All_Spectra(DFS_DICT, INPUT_PATHS[simsno])


DF_OUTPUT.to_csv(path_beg + output_dir[-1] + '/' + OUTPUT_PATH[simsno] + '_DF.csv')

# DF_OUTPUT = pd.read_csv(path_beg + output_dir[-1] + '/' + OUTPUT_PATH[simsno] + '_DF.csv', index_col = 0)

T_ROOM = 25 # C
P_ROOM = 1 # Bar

N = 500000
DENSITY_EPSILON, MEGA_SPREADSHEET = baselines.Concentration_Output(DF_OUTPUT, N, THICKNESS, MICOMP, T_ROOM, P_ROOM)
MEGA_SPREADSHEET.to_csv(output_dir[-1] + '/' + OUTPUT_PATH[simsno] + '_H2OCO2.csv')
DENSITY_EPSILON.to_csv(output_dir[-1] + '/' + OUTPUT_PATH[simsno] + '_DensityEpsilon.csv')
MEGA_SPREADSHEET

# %%
# %% 

simsno2 = 4

PATH = PATHS[simsno2]
FILES = glob.glob(PATH + "*")
FILES.sort()

MICOMP, THICKNESS = baselines.Load_ChemistryThickness(CHEMTHICK_PATH[simsno2])

DFS_FILES, DFS_DICT = baselines.Load_SampleCSV(FILES, wn_high = 5500, wn_low = 1000)
DF_OUTPUT, FAILURES = baselines.Run_All_Spectra(DFS_DICT, INPUT_PATHS[simsno2])
DF_OUTPUT.to_csv(path_beg + output_dir[-1] + '/' + OUTPUT_PATH[simsno2] + '_DF.csv')

# DF_OUTPUT = pd.read_csv(path_beg + output_dir[-1] + '/' + OUTPUT_PATH[simsno2] + '_DF.csv', index_col = 0)

T_ROOM = 25 # C
P_ROOM = 1 # Bar

N = 500000
DENSITY_EPSILON, MEGA_SPREADSHEET = baselines.Concentration_Output(DF_OUTPUT, N, THICKNESS, MICOMP, T_ROOM, P_ROOM)
MEGA_SPREADSHEET.to_csv(output_dir[-1] + '/' + OUTPUT_PATH[simsno2] + '_H2OCO2.csv')
DENSITY_EPSILON.to_csv(output_dir[-1] + '/' + OUTPUT_PATH[simsno2] + '_DensityEpsilon.csv')
MEGA_SPREADSHEET

# %% 
# %% 

stdno = 1

PATH = PATHS[stdno]
FILES = glob.glob(PATH + "*")
FILES.sort()

MICOMP, THICKNESS = baselines.Load_ChemistryThickness(CHEMTHICK_PATH[stdno])

DFS_FILES, DFS_DICT = baselines.Load_SampleCSV(FILES, wn_high = 5500, wn_low = 1000)
DF_OUTPUT, FAILURES = baselines.Run_All_Spectra(DFS_DICT, INPUT_PATHS[stdno])
DF_OUTPUT.to_csv(path_beg + output_dir[-1] + '/' + OUTPUT_PATH[stdno] + '_DF.csv')

# DF_OUTPUT = pd.read_csv(path_beg + output_dir[-1] + '/' + OUTPUT_PATH[stdno] + '_DF.csv', index_col = 0)

T_ROOM = 25 # C
P_ROOM = 1 # Bar

N = 500000
DENSITY_EPSILON, MEGA_SPREADSHEET = baselines.Concentration_Output(DF_OUTPUT, N, THICKNESS, MICOMP, T_ROOM, P_ROOM)
MEGA_SPREADSHEET.to_csv(output_dir[-1] + '/' + OUTPUT_PATH[stdno] + '_H2OCO2.csv')
DENSITY_EPSILON.to_csv(output_dir[-1] + '/' + OUTPUT_PATH[stdno] + '_DensityEpsilon.csv')

def STD_DF_MOD(MEGA_SPREADSHEET):
    STD_VAL = pd.DataFrame(index = MEGA_SPREADSHEET.index, columns = ['H2O_EXP', 'H2O_EXP_STD', 'CO2_EXP', 'CO2_EXP_STD'])

    for j in MEGA_SPREADSHEET.index: 
            
        if '21ALV1846' in j: 
            H2O_EXP= 1.89
            H2O_EXP_STD = 0.19
            CO2_EXP = np.nan
            CO2_EXP_STD = np.nan
        elif '23WOK5-4' in j: 
            H2O_EXP = 1.6
            H2O_EXP_STD = 0.16
            CO2_EXP = 64	
            CO2_EXP_STD = 6.4
        elif 'ALV1833-11' in j: 
            H2O_EXP = 1.2
            H2O_EXP_STD = 0.12
            CO2_EXP = 102
            CO2_EXP_STD = 10.2
        elif 'CD33_12-2-2' in j: 
            H2O_EXP = 0.27
            H2O_EXP_STD = 0.03
            CO2_EXP = 170
            CO2_EXP_STD = 17
        elif 'CD33_22-1-1' in j: 
            H2O_EXP = 0.49
            H2O_EXP_STD = 0.05
            CO2_EXP = 109
            CO2_EXP_STD = 10.9
        elif 'ETFSR_Ol8' in j: 
            H2O_EXP = 4.16
            H2O_EXP_STD = 0.42
            CO2_EXP = np.nan
            CO2_EXP_STD = np.nan
        elif 'Fiege63' in j: 
            H2O_EXP = 3.10
            H2O_EXP_STD = 0.31
            CO2_EXP = np.nan
            CO2_EXP_STD = np.nan
        elif 'Fiege73' in j: 
            H2O_EXP = 4.47
            H2O_EXP_STD = 0.45
            CO2_EXP = np.nan
            CO2_EXP_STD = np.nan
        elif 'STD_C1' in j: 
            H2O_EXP = 3.26
            H2O_EXP_STD = 0.33
            CO2_EXP = 169
            CO2_EXP_STD = 16.9
        elif 'STD_CN92C_OL2' in j: 
            H2O_EXP = 4.55
            H2O_EXP_STD = 0.46
            CO2_EXP = 270
            CO2_EXP_STD = 27
        elif 'STD_D1010' in j: 
            H2O_EXP = 1.13
            H2O_EXP_STD = 0.11
            CO2_EXP = 139
            CO2_EXP_STD = 13.9
        elif 'STD_ETFS' in j: 
            H2O_EXP = np.nan
            H2O_EXP_STD = np.nan
            CO2_EXP = np.nan
            CO2_EXP_STD = np.nan
        elif 'VF74_127-7' in j: 
            H2O_EXP = 3.98
            H2O_EXP_STD = 0.39
            CO2_EXP = 439
            CO2_EXP_STD = 43.9
        elif 'VF74_131-1' in j: 
            H2O_EXP = np.nan
            H2O_EXP_STD = np.nan
            CO2_EXP = np.nan
            CO2_EXP_STD = np.nan
        elif 'VF74_131-9' in j: 
            H2O_EXP = np.nan
            H2O_EXP_STD = np.nan
            CO2_EXP = np.nan
            CO2_EXP_STD = np.nan
        elif 'VF74_132-1' in j: 
            H2O_EXP = np.nan
            H2O_EXP_STD = np.nan
            CO2_EXP = np.nan
            CO2_EXP_STD = np.nan
        elif 'VF74_132-2' in j: 
            H2O_EXP = 3.91
            H2O_EXP_STD = 0.39
            CO2_EXP = 198
            CO2_EXP_STD = 19.8
        elif 'VF74_134D-15' in j: 
            H2O_EXP = np.nan
            H2O_EXP_STD = np.nan
            CO2_EXP = np.nan
            CO2_EXP_STD = np.nan
        elif 'VF74_136-3' in j: 
            H2O_EXP = np.nan
            H2O_EXP_STD = np.nan
            CO2_EXP = np.nan
            CO2_EXP_STD = np.nan

        STD_VAL.loc[j] = pd.Series({'H2O_EXP':H2O_EXP,'H2O_EXP_STD':H2O_EXP_STD,'CO2_EXP':CO2_EXP,'CO2_EXP_STD':CO2_EXP_STD})

    MEGA_SPREADSHEET_STD = pd.concat([MEGA_SPREADSHEET, STD_VAL], axis = 1)

    return MEGA_SPREADSHEET_STD

MEGA_SPREADSHEET_STD = STD_DF_MOD(MEGA_SPREADSHEET)

MEGA_SPREADSHEET_STD.to_csv(output_dir[-1] + '/' + OUTPUT_PATH[stdno] + '_H2OCO2_FwSTD.csv')

MEGA_SPREADSHEET_STD

# %%

fuegono = 0 

PATH = PATHS[fuegono]
FILES = glob.glob(PATH + "*")
FILES.sort()

MICOMP, THICKNESS = baselines.Load_ChemistryThickness(CHEMTHICK_PATH[fuegono])

DFS_FILES, DFS_DICT = baselines.Load_SampleCSV(FILES, wn_high = 5500, wn_low = 1000)
DF_OUTPUT, FAILURES = baselines.Run_All_Spectra(DFS_DICT, INPUT_PATHS[fuegono])
DF_OUTPUT.to_csv(path_beg + output_dir[-1] + '/' + OUTPUT_PATH[fuegono] + '_DF.csv')

# DF_OUTPUT = pd.read_csv(path_beg + output_dir[-1] + '/' + OUTPUT_PATH[fuegono] + '_DF.csv', index_col = 0)

T_ROOM = 25 # C
P_ROOM = 1 # Bar

N = 500000
DENSITY_EPSILON, MEGA_SPREADSHEET = baselines.Concentration_Output(DF_OUTPUT, N, THICKNESS, MICOMP, T_ROOM, P_ROOM)
MEGA_SPREADSHEET.to_csv(output_dir[-1] + '/' + OUTPUT_PATH[fuegono] + '_H2OCO2.csv')
DENSITY_EPSILON.to_csv(output_dir[-1] + '/' + OUTPUT_PATH[fuegono] + '_DensityEpsilon.csv')
MEGA_SPREADSHEET

# %%

fuegorhno = 2 

PATH = PATHS[fuegorhno]
FILES = glob.glob(PATH + "*")
FILES.sort()

MICOMP, THICKNESS = baselines.Load_ChemistryThickness(CHEMTHICK_PATH[fuegorhno])

DFS_FILES, DFS_DICT = baselines.Load_SampleCSV(FILES, wn_high = 5500, wn_low = 1000)
DF_OUTPUT, FAILURES = baselines.Run_All_Spectra(DFS_DICT, INPUT_PATHS[fuegorhno])
DF_OUTPUT.to_csv(path_beg + output_dir[-1] + '/' + OUTPUT_PATH[fuegorhno] + '_DF.csv')

# DF_OUTPUT = pd.read_csv(path_beg + output_dir[-1] + '/' + OUTPUT_PATH[fuegorhno] + '_DF.csv', index_col = 0)

T_ROOM = 25 # C
P_ROOM = 1 # Bar

N = 500000
DENSITY_EPSILON, MEGA_SPREADSHEET = baselines.Concentration_Output(DF_OUTPUT, N, THICKNESS, MICOMP, T_ROOM, P_ROOM)
MEGA_SPREADSHEET.to_csv(output_dir[-1] + '/' + OUTPUT_PATH[fuegorhno] + '_H2OCO2.csv')
DENSITY_EPSILON.to_csv(output_dir[-1] + '/' + OUTPUT_PATH[fuegorhno] + '_DensityEpsilon.csv')
MEGA_SPREADSHEET

# %%