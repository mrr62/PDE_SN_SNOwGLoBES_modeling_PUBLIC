
import numpy as np

# === File paths ===
#ARGON 
events_file = "/YOUR/FILE/PATH/int_flavor_events_per_bin_argon.txt"
timing_file = "pinched_index_full_timing_map_S.txt"
output_file = "/YOUR/FILE/PATH/norm_time_binned_flavor_events_argon.txt"

#WATER
#events_file = "/YOUR/FILE/PATH/int_flavor_events_per_bin_water.txt"
#timing_file = "pinched_index_full_timing_map_S.txt"
#output_file = "/YOUR/FILE/PATH/norm_time_binned_flavor_events_water.txt"

# === Load timing map ===
timing_data = np.loadtxt(timing_file, delimiter="\t", skiprows=1)
# Include bin width in the dict
timing_dict = {int(row[0]): (row[1], row[2], row[3]) for row in timing_data}

# === Load event counts (nue, nuebar, nux) ===
event_data = np.loadtxt(events_file, delimiter=",", skiprows=1)  # skip header
results = []

for row in event_data:
    idx = int(row[0])
    nue = row[1]
    nuebar = row[2]
    nux = row[3]

    if idx in timing_dict:
        start_us, end_us, bin_width_s = timing_dict[idx]
        # 🔑 Multiply each event count by bin width (in seconds)
        nue_scaled = nue * bin_width_s
        nuebar_scaled = nuebar * bin_width_s
        nux_scaled = nux * bin_width_s

        results.append((start_us, end_us, nue_scaled, nuebar_scaled, nux_scaled))
    else:
        print(f"⚠️ Warning: index {idx} not found in timing map")

# === Save output ===
with open(output_file, "w") as f:
    f.write("# start_us, end_us, nue_events, nuebar_events, nux_events\n")
    for start, end, nue, nuebar, nux in results:
        f.write(f"{start:.6f}, {end:.6f}, {nue:.6f}, {nuebar:.6f}, {nux:.6f}\n")

print(f"✅ Done! Output saved to {output_file}")
