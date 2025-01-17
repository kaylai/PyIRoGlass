import unittest
import numpy as np
import pandas as pd
import PyIRoGlass as pig



class test_density_epsilon_calculation(unittest.TestCase):

    def setUp(self): 

        self.MI_Composition = pd.DataFrame([{'Sample': 'AC4_OL53_101220_256s_30x30_a', 'SiO2': 47.95, 'TiO2': 1.00, 'Al2O3': 18.88, 'Fe2O3': 2.04, 'FeO': 7.45, 'MnO': 0.19, 'MgO': 4.34, 'CaO': 9.84, 'Na2O': 3.47, 'K2O': 0.67, 'P2O5': 0.11, 'H2O': 4.038927}])
        self.MI_Composition.set_index('Sample', inplace = True)
        self.MI_Composition_dry = pd.DataFrame([{'Sample': 'AC4_OL53_101220_256s_30x30_a', 'SiO2': 47.95, 'TiO2': 1.00, 'Al2O3': 18.88, 'Fe2O3': 2.04, 'FeO': 7.45, 'MnO': 0.19, 'MgO': 4.34, 'CaO': 9.84, 'Na2O': 3.47, 'K2O': 0.67, 'P2O5': 0.11, 'H2O': 0}])
        self.MI_Composition_dry.set_index('Sample', inplace = True)
        self.T_room = 25 
        self.P_room = 1 
        self.decimalPlace = 3

    def test_density_calculation(self):

        mol, density = pig.Density_Calculation(self.MI_Composition, self.T_room, self.P_room)
        result = float(density.values)
        expected = 2702.703558
        self.assertAlmostEqual(result, expected, self.decimalPlace, msg="Density test and expected values from the Density_Calculation function do not agree")

    def test_epsilon_calculation(self):
        
        epsilon = pig.Epsilon_Calculation(self.MI_Composition_dry, self.T_room, self.P_room)
        tau = float(epsilon['Tau'].iloc[0])
        expected_tau = 0.682894853
        epsilon_h2ot = float(epsilon['epsilon_H2OT_3550'].iloc[0])
        expected_epsilon_h2ot = 64.4628687805379
        sigma_epsilon_h2ot = float(epsilon['sigma_epsilon_H2OT_3550'].iloc[0])
        expected_sigma_epsilon_h2ot = 7.40123952105104
        self.assertAlmostEqual(tau, expected_tau, self.decimalPlace, msg="Tau test and expected values from the Epsilon_Calc function do not agree")
        self.assertAlmostEqual(epsilon_h2ot, expected_epsilon_h2ot, self.decimalPlace, msg="epsilon_H2Ot test and expected values from the Epsilon_Calc function do not agree")
        self.assertAlmostEqual(sigma_epsilon_h2ot, expected_sigma_epsilon_h2ot, self.decimalPlace, msg="sigma_epsilon_H2Ot test and expected values from the Epsilon_Calc function do not agree")


if __name__ == '__main__':
     unittest.main()