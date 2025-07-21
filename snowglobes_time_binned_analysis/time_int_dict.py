import pandas as pd

# === File paths ===
# Update these paths if your files are stored elsewhere
file_time = "/YOUR/FILE/PATH/snowglobes/PDE_pinched_input_TIME_BINS.dat"
file_index = "/YOUR/FILE/PATH/snowglobes/PDE_pinched_input_INTEGER.dat"
output_file = "pinched_index_full_timing_map_S.txt"

# === Load files ===
df_time = pd.read_csv(file_time, delim_whitespace=True, header=None)
df_index = pd.read_csv(file_index, delim_whitespace=True, header=None)

# === Extract start times from TIME_BINS file ===
start_times_ms = df_time.iloc[:, 0].values

# === Build time bin dictionary ===
data = []
for i in range(len(start_times_ms)):
    start_ms = start_times_ms[i]
    if i < len(start_times_ms) - 1:
        end_ms = start_times_ms[i + 1]
    else:
        # Use previous bin width for final bin
        end_ms = start_ms + (start_ms - start_times_ms[i - 1])
    bin_width_s = (end_ms - start_ms) / 1000.0  # Convert ms → s
    data.append([i, start_ms, end_ms, bin_width_s])

# === Save to DataFrame and export ===
df_out = pd.DataFrame(data, columns=["index", "start_time_ms", "end_time_ms", "bin_width_s"])
df_out.to_csv(output_file, sep="\t", index=False)

print(f"✅ Time bin dictionary saved to {output_file}")
