import numpy as np 

#allows for a sanity check comparing the total event rate data with the flavor separated event rate data to make sure it matches:) 

#load in file for simulation(s) you want to get total nuetrino count for 
test_file_tot = "/YOUR/FILE/PATH/norm_time_binned_total_events_argon.txt"
test_file_flav = "/YOUR/FILE/PATH/norm_time_binned_flavor_events_argon.txt"

#open file(s) 
nu_count_normalized_tot = np.loadtxt(test_file_tot, delimiter=",")
nu_count_normalized_flav = np.loadtxt(test_file_flav, delimiter=",", skiprows=1)

#separate and sum event count total 
nu_count_norm_tot = 0
nu_count_flav_tot = 0

for row in nu_count_normalized_tot: 
    nu_count_norm_tot += row[2]

# Columns: 0 = start_us, 1 = end_us, 2 = nue, 3 = nuebar, 4 = nux
nue_total = np.sum(nu_count_normalized_flav[:, 2])
nuebar_total = np.sum(nu_count_normalized_flav[:, 3])
nux_total = np.sum(nu_count_normalized_flav[:, 4])
total_all = nue_total + nuebar_total + nux_total

# Print result
print(f"✅ Normalized neutrino count is {nu_count_norm_tot:.6f} for total event file")
print(f"for the flavor separated event file:")
print(f"✅ Total νe events:     {nue_total:.6f}")
print(f"✅ Total ν̄e events:    {nuebar_total:.6f}")
print(f"✅ Total νx events:     {nux_total:.6f}")
print(f"🧾 Total all flavors:   {total_all:.6f}")


