"""Reveal Colombian inflation cycles.

Builds year-over-year (YoY) inflation from the monthly IPC variation, detects the
major cyclical peaks and troughs, shades each peak-to-peak cycle, and marks the
BANREP inflation target band. Saves `fig_inflation_cycles.png`.
"""
import os
os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".mplcache"))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch
from scipy.signal import find_peaks

# ---------------------------------------------------------------- load & prep
df = pd.read_csv("data/datos.csv", sep=";", decimal=",", usecols=[0, 1, 2], skiprows=[1],
                 names=["date", "rate", "infl_mom"], header=0)
df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce")
df = df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
df["infl_mom"] = pd.to_numeric(df["infl_mom"], errors="coerce")
df["rate"] = pd.to_numeric(df["rate"], errors="coerce")

# Year-over-year inflation = compound 12 consecutive monthly changes
df["yoy"] = ((1 + df["infl_mom"] / 100).rolling(12).apply(np.prod, raw=True) - 1) * 100
s = df.dropna(subset=["yoy"]).reset_index(drop=True)
x = s["date"].values
y = s["yoy"].values

# ---------------------------------------------------------------- cycle turning points
# Major peaks and troughs: require a minimum spacing (~2 yrs) and prominence (>=1.5 p.p.)
pk, _ = find_peaks(y,  distance=18, prominence=1.5)
tr, _ = find_peaks(-y, distance=18, prominence=1.5)

# ---------------------------------------------------------------- plot
plt.style.use("seaborn-v0_8-whitegrid") if "seaborn-v0_8-whitegrid" in plt.style.available else None
fig, ax = plt.subplots(figsize=(14, 7))

# BANREP target band 3% +/- 1%
ax.axhspan(2, 4, color="#2ecc71", alpha=0.12, zorder=0)
ax.axhline(3, color="#27ae60", lw=1, ls=":", zorder=1)
ax.text(s["date"].iloc[3], 3.15, "BANREP target 3% (±1% band)", color="#1e8449",
        fontsize=9, fontweight="bold", va="bottom")

# Shade alternating peak-to-peak cycles to make the cyclicality visible
cycle_bounds = list(s["date"].iloc[pk])
for i in range(len(cycle_bounds) - 1):
    if i % 2 == 0:
        ax.axvspan(cycle_bounds[i], cycle_bounds[i + 1], color="#34495e", alpha=0.05, zorder=0)

# Main YoY line
ax.plot(x, y, color="#c0392b", lw=2.1, zorder=3, label="Annual inflation (YoY, %)")

# Peaks & troughs
ax.scatter(s["date"].iloc[pk], y[pk], color="#c0392b", s=55, zorder=5, ec="white", lw=1.2, label="Cycle peak")
ax.scatter(s["date"].iloc[tr], y[tr], color="#2980b9", s=55, zorder=5, ec="white", lw=1.2, label="Cycle trough")

for i in pk:
    ax.annotate(f"{y[i]:.1f}%\n{pd.Timestamp(x[i]):%b-%Y}",
                (x[i], y[i]), textcoords="offset points", xytext=(0, 12),
                ha="center", fontsize=8, color="#c0392b", fontweight="bold")
for i in tr:
    ax.annotate(f"{y[i]:.1f}%\n{pd.Timestamp(x[i]):%b-%Y}",
                (x[i], y[i]), textcoords="offset points", xytext=(0, -22),
                ha="center", fontsize=8, color="#2980b9", fontweight="bold")

ax.set_title("Colombia's inflation cycles, 1999–2026\n"
             "Year-over-year CPI (IPC) inflation with major cyclical peaks and troughs",
             fontsize=14, fontweight="bold")
ax.set_ylabel("Annual inflation — YoY % change of the IPC")
ax.set_xlabel("")
ax.xaxis.set_major_locator(mdates.YearLocator(2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.margins(x=0.01)
ax.set_ylim(bottom=min(-1, y.min() - 1))

handles, labels = ax.get_legend_handles_labels()
handles.append(Patch(facecolor="#2ecc71", alpha=0.2, label="Target band (2–4%)"))
handles.append(Patch(facecolor="#34495e", alpha=0.1, label="Peak-to-peak cycle"))
ax.legend(handles=handles, loc="upper right", fontsize=9, framealpha=0.9)

plt.tight_layout()
plt.savefig("fig_inflation_cycles.png", dpi=130, bbox_inches="tight")
print("Saved fig_inflation_cycles.png")
print(f"\nDetected {len(pk)} major peaks:")
for i in pk:
    print(f"  peak   {pd.Timestamp(x[i]):%Y-%m}  {y[i]:5.2f}%")
print(f"Detected {len(tr)} major troughs:")
for i in tr:
    print(f"  trough {pd.Timestamp(x[i]):%Y-%m}  {y[i]:5.2f}%")
