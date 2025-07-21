import numpy as np 

#load in file for simulation(s) you want to get total nuetrino count for - must be total event count file in form [start_time_ms, end_time_ms, total_event_count] 
test_file = "FILENAME.txt"

#open file(s) 
nu_count_normalized = np.loadtxt(new_file, delimiter=",")

#separate and sum event count total 
nu_count_norm = 0

for row in nu_count_normalized: 
    nu_count_norm += row[2]
  
#can add as many files as you would like to check, just treat each the same way test_file is loaded and summed over

# Print result
print(f"✅ Normalized neutrino count is {nu_count_norm:.6f}") #can add any additional file totals to be printed here :) 
