#code to take various luminosity + energy data and interpolate it to SNOwGLoBES compatible format
"""
Created on 4/11/25

@author: madeleine
"""
#outputs file in [number alpha nue alpha nuebar alpha nux Eavg nue Eavgy nuebar Eavg nux lum nue lum nuebar lum nux] format, where the number is either an integer or bin start time --> the last lines determine this; uncomment code under #INTEGER for integer, and code under #TIME for bin start time
#input is assumed to be in milliseconds, which needs to be accounted for when summing event rates per bin, as SNOwGLoBES assumers an input in seconds 

import pandas as pd
import numpy as np

# Set pinching value
alpha_val = 2.23

# File paths
files = {
    "nue":      "/Users/madeleine/Desktop/HEP Scholberg Research/Animation Data/Final animation CSVs/EN_Animation.csv",
    "nuebar":   "/Users/madeleine/Desktop/HEP Scholberg Research/Animation Data/Final animation CSVs/EA-N_Animation_collab.csv",
    "mu_tau":   "/Users/madeleine/Desktop/HEP Scholberg Research/Animation Data/Final animation CSVs/m_tN_Animation.csv",
}

# Load data
data = {}
for flavor, path in files.items():
    df = pd.read_csv(path, header=None, names=["Em", "Lv", "time"])
    data[flavor] = df

# Use nue times as the reference
common_time = data["nue"]["time"].values

# Interpolate all data to common time
interpolated = {}
for flavor in files:
    Em_interp = np.interp(common_time, data[flavor]["time"], data[flavor]["Em"])
    Lv_interp = np.interp(common_time, data[flavor]["time"], data[flavor]["Lv"])
    interpolated[flavor] = {"Em": Em_interp, "Lv": Lv_interp}

# Lv def
delta_t_s = np.diff(common_time, append=common_time[-1])
for flavor in interpolated:
    interpolated[flavor]["Lv_erg"] = interpolated[flavor]["Lv"] * 1e51

# Write to output file
output_file = "/Users/madeleine/Desktop/HEP Scholberg Research/Fluence Files/PDE_pinched_input.dat"
with open(output_file, "w") as f:
    for i, t in enumerate(common_time):
        Em_nue     = interpolated["nue"]["Em"][i]
        Em_nuebar  = interpolated["nuebar"]["Em"][i]
        Em_nux     = interpolated["mu_tau"]["Em"][i]

        Lv_nue     = interpolated["nue"]["Lv_erg"][i]
        Lv_nuebar  = interpolated["nuebar"]["Lv_erg"][i]
        Lv_nux     = interpolated["mu_tau"]["Lv_erg"][i] / 4.0  # convert total νₓ to per-flavor (numu, numubar, nutau, and nutaubar) 


        #INTEGER - use for input files organized by integer
        #line = f"{i} {alpha_val:.3f} {alpha_val:.3f} {alpha_val:.3f} {Em_nue:.3f} {Em_nuebar:.3f} {Em_nux:.3f} {Lv_nue:.5e} {Lv_nuebar:.5e} {Lv_nux:.5e}\n"
      
        #TIME - use for input files organized by bin start time 
        line = f"{t:.6f} {alpha_val:.3f} {alpha_val:.3f} {alpha_val:.3f} {Em_nue:.3f} {Em_nuebar:.3f} {Em_nux:.3f} {Lv_nue:.5e} {Lv_nuebar:.5e} {Lv_nux:.5e}\n"
      
        f.write(line)
