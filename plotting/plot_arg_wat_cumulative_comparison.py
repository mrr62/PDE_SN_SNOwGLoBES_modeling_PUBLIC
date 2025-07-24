import pandas as pd
import matplotlib.pyplot as plt
import os

#plots the total event count over time for argon and water detectors on the same set of axis to better compare the detector output event count. For detectors with different masses,(40 kton argon vs. 100kton water), there is an  optional section to scale water down to 40ktons if a direct comparison is desired  

# File paths
water_file = "/YOUR/FILE/PATH/norm_time_binned_total_events_water.txt"
argon_file = "/YOUR/FILE/PATH/norm_time_binned_total_events_argon.txt"
save_dir = "/YOUR/FILE/PATH/PDE_figures"

# Load both files (assuming format: start, end, event_rate)
col_names = ["start", "end", "event_rate"]
df_water = pd.read_csv(water_file, names=col_names, comment="#")
df_argon = pd.read_csv(argon_file, names=col_names, comment="#")

# Add time centers + cumulative sum
df_water["time_center"] = (df_water["start"] + df_water["end"]) / 2
df_argon["time_center"] = (df_argon["start"] + df_argon["end"]) / 2
df_water["cumulative_events"] = df_water["event_rate"].cumsum()
df_argon["cumulative_events"] = df_argon["event_rate"].cumsum()

# Optionally scale water to 40 kton (if comparing on equal mass basis)
df_water_scaled = df_water.copy()
df_water_scaled["cumulative_events"] *= 0.4

# ===== Plot Overlay =====
plt.figure(figsize=(10, 6))
plt.plot(df_water_scaled["time_center"], df_water_scaled["cumulative_events"],
         color="#DA70D6", label="Water (scaled to 40 kton)", linewidth=2.0)
plt.plot(df_argon["time_center"], df_argon["cumulative_events"],
         color="#5C7FA3", label="Argon (40 kton)", linewidth=2.0)
plt.xlabel("Time [μs]")
plt.ylabel("Cumulative Event Count")
plt.title("Cumulative PDE Events: Water vs Argon Detectors (40 kton)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()

save_path = os.path.join(save_dir, "cumulative_counts_water_vs_argon_40kton_comparsion.png")
plt.savefig(save_path, dpi=300)
print(f"✅ Plot saved to {save_path}")
plt.show()
