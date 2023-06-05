import unittest
import numpy as np
import pandas as pd
import PyIRoGlass as pig


class test_conc_outputs_h2ot(unittest.TestCase):

    def setUp(self): 

        self.molar_mass = 18.01528
        self.absorbance = 1.523342931
        self.sigma_absorbance = 0.003308868
        self.density = 2702.703546
        self.sigma_density = self.density * 0.025
        self.thickness = 39
        self.sigma_thickness = 3
        self.epsilon = 64.46286878
        self.sigma_epsilon = 7.401239521
        self.N = 500000
        self.MI_Composition = {'SiO2': 47.95, 'TiO2': 1.00, 'Al2O3': 18.88, 'Fe2O3': 2.04, 'FeO': 7.45, 'MnO': 0.19,
                               'MgO': 4.34, 'CaO': 9.84, 'Na2O': 3.47, 'K2O': 0.67, 'P2O5': 0.11}
        self.T_room = 25 
        self.P_room = 1 
        self.decimalPlace = 4

    def test_beer_lambert(self):

        result = pig.Beer_Lambert(self.molar_mass, self.absorbance, self.sigma_absorbance, self.density, self.sigma_density, self.thickness, self.sigma_thickness, self.epsilon, self.sigma_epsilon)
        expected = 4.03892743514451
        self.assertAlmostEqual(result, expected, self.decimalPlace, msg="H2Ot test and expected values from the Beer_Lambert function do not agree")

    def test_beer_lambert_error(self):

        result = pig.Beer_Lambert_Error(self.N, self.molar_mass, self.absorbance, self.sigma_absorbance, self.density, self.sigma_density, self.thickness, self.sigma_thickness, self.epsilon, self.sigma_epsilon)
        expected = 0.433803676139589        
        self.assertAlmostEqual(result, expected, self.decimalPlace-3, msg="H2Ot test and expected errors from the Beer_Lambert_Error function do not agree")


class test_conc_outputs_co2(unittest.TestCase):

    def setUp(self): 

        self.molar_mass = 44.01
        self.absorbance = 0.052887397
        self.sigma_absorbance = 0.005128284
        self.density = 2702.703546
        self.sigma_density = self.density * 0.025
        self.thickness = 39
        self.sigma_thickness = 3
        self.epsilon = 302.327096
        self.sigma_epsilon = 18.06823009
        self.N = 500000
        self.MI_Composition = {'SiO2': 47.95, 'TiO2': 1.00, 'Al2O3': 18.88, 'Fe2O3': 2.04, 'FeO': 7.45, 'MnO': 0.19,
                               'MgO': 4.34, 'CaO': 9.84, 'Na2O': 3.47, 'K2O': 0.67, 'P2O5': 0.11}
        self.T_room = 25 
        self.P_room = 1 
        self.decimalPlace = 2

    def test_beer_lambert(self):

        result = pig.Beer_Lambert(self.molar_mass, self.absorbance, self.sigma_absorbance, self.density, self.sigma_density, self.thickness, self.sigma_thickness, self.epsilon, self.sigma_epsilon) * 10000
        expected = 730.4045443
        self.assertAlmostEqual(result, expected, self.decimalPlace, msg="CO2_1515 test and expected values from the Beer_Lambert equation do not agree")

    def test_beer_lambert_error(self):
        
        result = pig.Beer_Lambert_Error(self.N, self.molar_mass, self.absorbance, self.sigma_absorbance, self.density, self.sigma_density, self.thickness, self.sigma_thickness, self.epsilon, self.sigma_epsilon) * 10000
        expected = 97.35842352      
        self.assertAlmostEqual(result, expected, self.decimalPlace-2, msg="CO2_1515 test and expected errors from the Beer_Lambert_Error equation do not agree")


class test_conc_outputss(unittest.TestCase):

    def setUp(self):

        self.MI_Composition = pd.DataFrame({'SiO2': [47.95], 'TiO2': [1.00], 'Al2O3': [18.88], 'Fe2O3': [2.04], 'FeO': [7.45],
                              'MnO': [0.19], 'MgO': [4.34], 'CaO': [9.84], 'Na2O': [3.47], 'K2O': [0.67], 'P2O5': [0.11]},
                              index=['AC4_OL53_101220_256s_30x30_a'])
        self.PH = pd.DataFrame({'PH_3550_M': [1.523342931], 'PH_3550_STD': [0.003308868], 'H2OT_3550_SAT?': ['-'], 'PH_1635_BP': [0.295626169],
                   'PH_1635_STD': [0.003648565], 'PH_1515_BP': [0.050343559], 'PH_1515_STD': [0.005059763],
                   'PH_1430_BP': [0.050484084], 'PH_1430_STD': [0.00609577], 'PH_5200_M': [0.008959072], 'PH_5200_STD': [0.000445132], 
                   'PH_4500_M': [0.012517573], 'PH_4500_STD': [0.000320315], 'S2N_P5200': [6.904155498], 'S2N_P4500': [5.527653038],
                   'ERR_5200': ['-'], 'ERR_4500': ['-']}, index=['AC4_OL53_101220_256s_30x30_a'])
        self.thickness = pd.DataFrame({'Thickness': [39], 'Sigma_Thickness': [3]}, index=['AC4_OL53_101220_256s_30x30_a'])
        self.N = 500000
        self.T_room = 25 
        self.P_room = 1 

        density_epsilon, mega_spreadsheet = pig.Concentration_Output(self.PH, self.N, self.thickness, self.MI_Composition, self.T_room, self.P_room)
        expected_H2O = 4.03892743514451
        expected_CO2 = 730.4045443
        self.assertAlmostEqual(float(mega_spreadsheet['H2OT_MEAN']), expected_H2O, self.decimalPlace-2, msg="H2Ot test values from the Concentration_Output equation do not agree")
        self.assertAlmostEqual(float(mega_spreadsheet['CO2_MEAN']), expected_CO2, self.decimalPlace-2, msg="CO2m test values from the Concentration_Output equation do not agree")


if __name__ == '__main__':
     unittest.main()
