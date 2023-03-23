import unittest
import numpy as np
import pandas as pd
import PyIRoGlass as pig
import os
import glob

class test_thickness(unittest.TestCase):
    def setUp(self): 
        self.xfo = 0.72
        self.decimalPlace = 4
        self.wn_high = 2700
        self.wn_low = 2100
        self.wn = [2100.189,2102.118,2104.046,2105.975,2107.903,2109.832,2111.76,2113.689,2115.617,2117.546,2119.475,2121.403,2123.332,2125.26,2127.189,2129.117,2131.046,2132.974,2134.903,2136.832,2138.76,2140.689,2142.617,2144.546,2146.474,2148.403,2150.331,2152.26,2154.188,2156.117,2158.046,2159.974,2161.903,2163.831,2165.76,2167.688,2169.617,2171.545,2173.474,2175.403,2177.331,2179.26,2181.188,2183.117,2185.045,2186.974,2188.902,2190.831,2192.76,2194.688,2196.616,2198.545,2200.474,2202.402,2204.331,2206.259,2208.188,2210.116,2212.045,2213.973,2215.902,2217.831,2219.759,2221.688,2223.616,2225.545,2227.473,2229.402,2231.33,2233.259,2235.188,2237.116,2239.045,2240.973,2242.902,2244.83,2246.759,2248.687,2250.616,2252.544,2254.473,2256.402,2258.33,2260.259,2262.187,2264.116,2266.044,2267.973,2269.901,2271.83,2273.759,2275.687,2277.615,2279.544,2281.473,2283.401,2285.33,2287.258,2289.187,2291.115,2293.044,2294.972,2296.901,2298.83,2300.758,2302.687,2304.615,2306.544,2308.472,2310.401,2312.329,2314.258,2316.187,2318.115,2320.044,2321.972,2323.901,2325.829,2327.758,2329.686,2331.615,2333.543,2335.472,2337.401,2339.329,2341.258,2343.186,2345.115,2347.043,2348.972,2350.9,2352.829,2354.758,2356.686,2358.615,2360.543,2362.472,2364.4,2366.329,2368.257,2370.186,2372.115,2374.043,2375.971,2377.9,2379.829,2381.757,2383.686,2385.614,2387.543,2389.471,2391.4,2393.328,2395.257,2397.186,2399.114,2401.043,2402.971,2404.9,2406.828,2408.757,2410.685,2412.614,2414.542,2416.471,2418.4,2420.328,2422.257,2424.185,2426.114,2428.042,2429.971,2431.899,2433.828,2435.757,2437.685,2439.614,2441.542,2443.471,2445.399,2447.328,2449.256,2451.185,2453.114,2455.042,2456.97,2458.899,2460.828,2462.756,2464.685,2466.613,2468.542,2470.47,2472.399,2474.327,2476.256,2478.185,2480.113,2482.042,2483.97,2485.899,2487.827,2489.756,2491.684,2493.613,2495.542,2497.47,2499.399,2501.327,2503.256,2505.184,2507.113,2509.042,2510.97,2512.898,2514.827,2516.756,2518.684,2520.613,2522.541,2524.47,2526.398,2528.327,2530.255,2532.184,2534.113,2536.041,2537.97,2539.898,2541.827,2543.755,2545.684,2547.612,2549.541,2551.469,2553.398,2555.327,2557.255,2559.184,2561.112,2563.041,2564.969,2566.898,2568.826,2570.755,2572.684,2574.612,2576.541,2578.469,2580.398,2582.326,2584.255,2586.183,2588.112,2590.041,2591.969,2593.897,2595.826,2597.755,2599.683,2601.612,2603.54,2605.469,2607.397,2609.326,2611.254,2613.183,2615.112,2617.04,2618.969,2620.897,2622.826,2624.754,2626.683,2628.611,2630.54,2632.469,2634.397,2636.326,2638.254,2640.183,2642.111,2644.04,2645.968,2647.897,2649.825,2651.754,2653.683,2655.611,2657.54,2659.468,2661.397,2663.325,2665.254,2667.182,2669.111,2671.04,2672.968,2674.896,2676.825,2678.754,2680.682,2682.611,2684.539,2686.468,2688.396,2690.325,2692.253,2694.182,2696.111,2698.039,2699.968]
        self.abs = [0.8771853,0.8784955,0.8778838,0.8758668,0.8732336,0.8701192,0.8663936,0.8623665,0.8588824,0.8566167,0.8554226,0.8553206,0.8561192,0.8576086,0.8597494,0.8626562,0.8655683,0.8679856,0.8701353,0.8715089,0.8719133,0.8713134,0.8699853,0.8681639,0.8652869,0.861811,0.8586689,0.8559095,0.8538229,0.8521714,0.8518564,0.8528331,0.8544457,0.8564513,0.858667,0.8613505,0.8641433,0.8662304,0.867592,0.8678326,0.867177,0.8658627,0.8634521,0.8604652,0.8572671,0.8544174,0.8513765,0.8489732,0.8474135,0.8468698,0.8475645,0.8486117,0.8506775,0.8535439,0.8556452,0.8573649,0.859121,0.8602605,0.8602774,0.8592403,0.8572187,0.8549281,0.8517796,0.8482863,0.8451973,0.8421924,0.8398129,0.8383427,0.8379127,0.8382969,0.8392297,0.8407292,0.8430046,0.8449931,0.8463593,0.8475632,0.8478963,0.8474974,0.8465433,0.8442497,0.8410665,0.8378426,0.834107,0.830825,0.8283697,0.8262495,0.8250093,0.8245685,0.8246834,0.8252645,0.8265327,0.8276843,0.8286586,0.8295341,0.8301092,0.8306162,0.8302415,0.8286915,0.8260401,0.8229305,0.8197907,0.8167899,0.8142602,0.8123196,0.8107562,0.8094115,0.8085777,0.8088179,0.8099348,0.8107235,0.8113704,0.8124402,0.8134915,0.8139005,0.813623,0.8128304,0.8114451,0.809302,0.8072917,0.8055199,0.803097,0.8004071,0.7984169,0.7970756,0.7961122,0.7953587,0.7954882,0.7953625,0.7952263,0.7959703,0.796712,0.7976105,0.79837,0.7986351,0.797862,0.7962294,0.7951571,0.7935983,0.7911855,0.7891254,0.7866024,0.7846335,0.783304,0.78224,0.7814776,0.7812228,0.7812294,0.7810687,0.7814137,0.7821554,0.7823824,0.7820688,0.781585,0.7813405,0.7810469,0.7800974,0.7785708,0.7772884,0.7763857,0.775609,0.7747612,0.7739412,0.7735876,0.7735519,0.7734414,0.7731725,0.7732457,0.7739293,0.7748923,0.7755677,0.775773,0.77577,0.775639,0.7753621,0.7746474,0.7739386,0.7735191,0.7727962,0.771906,0.771325,0.7710848,0.7709936,0.7708869,0.7711281,0.7712479,0.7714913,0.7720421,0.772723,0.7734421,0.7743574,0.7752358,0.7752802,0.7749581,0.7748249,0.7749072,0.7748154,0.7739353,0.7731451,0.7729153,0.7728906,0.7727442,0.7725084,0.7722375,0.7722201,0.7726862,0.7737827,0.7744998,0.7748308,0.7757319,0.7764129,0.776656,0.777181,0.7775484,0.7772357,0.7768981,0.7766709,0.7762403,0.775865,0.7757292,0.775338,0.7748588,0.7748931,0.7750075,0.7749855,0.7749686,0.7756536,0.7767604,0.7771534,0.7775218,0.7784898,0.7785904,0.777928,0.7776617,0.7777568,0.7778146,0.7775217,0.7772473,0.7766877,0.7757088,0.7750791,0.7747837,0.7746765,0.7747367,0.7751387,0.7756333,0.7760683,0.776161,0.7760789,0.7766979,0.7769,0.7763146,0.7760199,0.7760013,0.7754377,0.7750186,0.7745423,0.7734561,0.7723659,0.7718965,0.7714956,0.7708955,0.7704052,0.7699525,0.7697388,0.7698807,0.7700964,0.7704247,0.7704611,0.7703475,0.770279,0.769828,0.7692037,0.7683634,0.7679303,0.7673056,0.7660556,0.7649163,0.7638579,0.762736,0.7616605,0.7611527,0.760515,0.7599469,0.7598943,0.7601219,0.7599848,0.75993,0.7603506,0.7600033,0.7591771,0.7587984,0.758707,0.7584011,0.7573321,0.7557866,0.7542044,0.7527732,0.7516828,0.7508492,0.7500915,0.7496533,0.7492396,0.748831,0.7488262,0.7491466,0.749245,0.7493446,0.7493286,0.7486278,0.7478377,0.7472695,0.7467049]
        self.file = 'AC4_OL27_REF_a'
        self.df = pd.DataFrame({'Wavenumber': wn, 'Absorbance': abs})
        self.df.set_index('Wavenumber', inplace = True)
        self.dfs_dict = {file: df}


    def test_reflectance_index(self):
        result = pig.Reflectance_Index(self.xfo)
        expected = 1.7097733333333334
        self.assertAlmostEqual(result, expected, self.decimalPlace, msg="Reflectance index test and expected values from the Reflectance_Index function do not agree")

    def test_process_thickness(self): 
        result = pig.Reflectance_Index(self.xfo)
        thickness_results = pig.Thickness_Processing(self.dfs_dict, result, self.wn_high, self.wn_low, remove_baseline=False, plotting=False, phaseol=True)
        result = float(thickness_results['Thickness_M'])
        expected = 79.81
        self.assertAlmostEqual(result, expected, self.decimalPlace-2, msg="Thickness test and expected values from the Thickness_Processing function do not agree")

if __name__ == '__main__':
     unittest.main()
