import os
import glob
import numpy as np
from collections import defaultdict

#sums events from supernova.pl output files to get a total event count per INTEGER and puts them all in one dictionary, formattted like [integer  total_event_count] where total_event_count = nue_count + nuebar_count + nux_count
#-->sums up event count per integer, so each integer file (i.e. pinched_INT_*.dat is reduced to one number)
#--> uses smeared_unweighted files as input, ignores non-smeared to avoid double counting events

# Path to your event directory
event_dir = "/YOUR/FILE/PATH/globes-3.2.18/snowglobes/out"
os.chdir(event_dir)

# Get all smeared unweighted files - choose between water and argon
#WATER code: 
#files = glob.glob("pinched_*_wc100kt30prct_events_smeared_unweighted.dat")
#ARGON code: 
files = glob.glob("pinched_*_ar40kt_events_smeared_unweighted.dat")

# Store event totals for each integer bin
event_totals = defaultdict(float)

for file in files:
    try:
        # Extract the integer index
        filename = os.path.basename(file)
        int_index = int(filename.split("_")[1])

        # Read in only the second column (event rate)
        # Skip lines with formatting issues
        values = []
        with open(file, 'r') as f:
            for line in f:
                if line.strip().startswith("#") or not line.strip():
                    continue
                parts = line.split()
                if len(parts) == 2:
                    try:
                        values.append(float(parts[1]))
                    except ValueError:
                        continue

        total_events = sum(values)
        event_totals[int_index] += total_events

    except Exception as e:
        print(f"⚠️ Error processing {file}: {e}")

# Sort and save to parent directory
output = sorted(event_totals.items())
output_path = "YOUR/FILE/PATH/globes-3.2.18/snowglobes/total_MATERIAL_events_per_bin.txt"
with open(output_path, "w") as f:
    for idx, total in output:
        f.write(f"{idx}, {total:.6f}\n")

print(f"✅ Finished! Results saved to {output_path}")
