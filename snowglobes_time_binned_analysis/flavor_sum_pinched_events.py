import os
import glob
import numpy as np
from collections import defaultdict

#sums events from supernova.pl output files to get a total event count per flavor per INTEGER and puts them all in one file, formattted like [integer  nue_event_count  nuebar_event_count  nux_event_count] 
#-->sums up event count per integer, so each integer file (i.e. pinched_INT_*.dat is reduced to one number)
#--> uses smeared_unweighted files as input, ignores non-smeared to avoid double counting events

# Path to your event directory
event_dir = "/YOUR/FILE/PATH/globes-3.2.18/snowglobes/out"
os.chdir(event_dir)

# Get all smeared unweighted files : choose between water and argon
#ARGON code: 
files = glob.glob("pinched_*_*_ar40kt_events_smeared_unweighted.dat")
#WATER code: 
#files = glob.glob("pinched_*_*_wc100kt30prct_events_smeared_unweighted.dat")

# Separate event totals by integer index and flavor
event_totals = defaultdict(lambda: {"nue": 0.0, "nuebar": 0.0, "nux": 0.0})

# Function to identify the flavor from filename
def get_flavor(filename):
    if "_nue_" in filename:
        return "nue"
    elif "_nuebar_" in filename:
        return "nuebar"
    elif any(flavor in filename for flavor in ["_numu_", "_numubar_", "_nutau_", "_nutaubar_"]):
        return "nux"
    else:
        return None  # Unknown or doesn't count

for file in files:
    try:
        filename = os.path.basename(file)
        int_index = int(filename.split("_")[1])
        flavor = get_flavor(filename)

        if flavor is None:
            print(f"⚠️ Skipping unknown flavor in: {filename}")
            continue

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
        event_totals[int_index][flavor] += total_events

    except Exception as e:
        print(f"⚠️ Error processing {file}: {e}")

# Sort output and write to file
output_path = "YOUR/FILE/PATH/globes-3.2.18/snowglobes/flavor_events_per_bin_MATERIAL.txt"
with open(output_path, "w") as f:
    f.write("# bin_index, nue_events, nuebar_events, nux_events\n")
    for idx in sorted(event_totals):
        nue = event_totals[idx]["nue"]
        nuebar = event_totals[idx]["nuebar"]
        nux = event_totals[idx]["nux"]
        f.write(f"{idx}, {nue:.6f}, {nuebar:.6f}, {nux:.6f}\n")

print(f"✅ Finished! Results saved to {output_path}")
