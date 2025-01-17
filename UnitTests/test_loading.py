import unittest
import os
import glob
import numpy as np
import pandas as pd
import PyIRoGlass as pig



class test_loading_npz(unittest.TestCase):

    def test_load_pc(self):

        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../src/PyIRoGlass/BaselineAvgPC.npz') 
        matrix = pig.Load_PC(file_path)
        
        # Assuming that the PCA matrix should not be empty after reading a valid .npz file
        self.assertIsNotNone(matrix, "Loading the PCA matrix failed.")
        self.assertNotEqual(matrix.size, 0, "PCA matrix is empty.")


    def test_load_wavenumber(self):

        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../src/PyIRoGlass/BaselineAvgPC.npz') 
        wavenumber = pig.Load_Wavenumber(file_path)
        
        # Assuming that the wavenumber array should not be empty after reading a valid .npz file
        self.assertIsNotNone(wavenumber, "Loading the wavenumber array failed.")
        self.assertNotEqual(wavenumber.size, 0, "Wavenumber array is empty.")


class test_loading_csv(unittest.TestCase):

    def test_load_samplecsvs(self):

        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../Inputs/TransmissionSpectra/Fuego/') 
        FILES = sorted(glob.glob(file_path + "*"))

        files, dfs_dict = pig.Load_SampleCSV(FILES, 5500, 1000)
        self.assertEqual(len(files), 97)  # Adjust based on your test data

    def test_load_chemthick(self):

        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../Inputs/ChemThick_Template.csv') 
        Chemistry, Thickness = pig.Load_ChemistryThickness(file_path)
        
        # Assuming that the PCA matrix should not be empty after reading a valid .npz file
        self.assertEqual(Chemistry.shape, (9, 11))  # Adjust based on your test data
        self.assertEqual(Thickness.shape, (9, 2))   # Adjust based on your test data


if __name__ == '__main__':
     unittest.main()
