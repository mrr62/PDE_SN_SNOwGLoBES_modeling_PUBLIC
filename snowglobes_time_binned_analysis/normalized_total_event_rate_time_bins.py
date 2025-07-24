import numpy as np

# === File paths ===
#WATER code
events_file = "/YOUR/FILE/PATH/int_total_water_events_per_bin.txt"
timing_file = "pinched_index_full_timing_map_S.txt"
output_file = "/YOUR/FILE/PATH/norm_time_binned_total_events_water.txt"

#ARGON code
#events_file = "/YOUR/FILE/PATH/int_total_argon_events_per_bin.txt"
#timing_file = "pinched_index_full_timing_map_S.txt"
#output_file = "/YOUR/FILE/PATH/norm_time_binned_total_events_argon.txt"

# === Load timing map ===
timing_data = np.loadtxt(timing_file, delimiter="\t", skiprows=1)
# Now include bin width in the dictionary
timing_dict = {int(row[0]): (row[1], row[2], row[3]) for row in timing_data}

# === Load event counts ===
event_data = np.loadtxt(events_file, delimiter=",")
results = []

for row in event_data:
    idx = int(row[0])
    event_count = row[1]

    if idx in timing_dict:
        start_us, end_us, bin_width_s = timing_dict[idx]
        # Multiply event count by bin width (in seconds)
        normalized_event_count = event_count * bin_width_s
        results.append((start_us, end_us, normalized_event_count))
    else:
        print(f"⚠️ Warning: index {idx} not found in timing map")

# === Save output ===
with open(output_file, "w") as f:
    for start, end, total in results:
        f.write(f"{start:.6f}, {end:.6f}, {total:.6f}\n")

print(f"✅ Done! Output saved to {output_file}")
