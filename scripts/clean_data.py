"""
Nigeria Agricultural Output by State (2014-2024)
Step 1: Data Cleaning

Input : data/raw/raw_crop_output_nigeria_2014_2024.csv
Output: data/clean/crop_output_nigeria_2014_2024_clean.csv
        docs/data_quality_log.csv   (record of every row that was changed, and why)

Decisions applied (agreed with project owner):
  1. State naming: 'Abuja FCT' and 'FCT Abuja' both standardized to 'Abuja FCT'
  2. Exact duplicate row removed
  3. Missing production_tonnes (15 rows) recalculated as area_harvested_ha * yield_t_per_ha
  4. Outlier Kwara/Yam/2014 recalculated as area_harvested_ha * yield_t_per_ha
     (original value was ~55x the implied production - data entry error)
"""

import pandas as pd
import numpy as np

RAW_PATH = "data/raw/raw_crop_output_nigeria_2014_2024.csv"
CLEAN_PATH = "data/clean/crop_output_nigeria_2014_2024_clean.csv"
LOG_PATH = "docs/data_quality_log.csv"

df = pd.read_csv(RAW_PATH)
log_rows = []

def log_change(mask, reason, field, old_series=None):
    """Record affected rows into the data quality log."""
    affected = df.loc[mask, ["state", "crop", "year"]].copy()
    affected["field"] = field
    affected["issue"] = reason
    if old_series is not None:
        affected["old_value"] = old_series.loc[mask].values
    log_rows.append(affected)

# ---------------------------------------------------------------
# 1. Standardize state naming: FCT
# ---------------------------------------------------------------
fct_mask = df["state"].isin(["Abuja FCT", "FCT Abuja"])
log_change(fct_mask & (df["state"] == "FCT Abuja"), "Inconsistent state label standardized to 'Abuja FCT'", "state",
            old_series=df["state"])
df["state"] = df["state"].replace({"FCT Abuja": "Abuja FCT"})

# ---------------------------------------------------------------
# 2. Strip whitespace / normalize text fields
# ---------------------------------------------------------------
df["state"] = df["state"].str.strip()
df["crop"] = df["crop"].str.strip()

# ---------------------------------------------------------------
# 3. Remove exact duplicate rows
# ---------------------------------------------------------------
dup_mask = df.duplicated(keep="first")
log_change(dup_mask, "Exact duplicate row removed", "row")
df = df[~dup_mask].reset_index(drop=True)

# ---------------------------------------------------------------
# 4. Recalculate missing production_tonnes as area x yield
# ---------------------------------------------------------------
missing_prod_mask = df["production_tonnes"].isnull()
log_change(missing_prod_mask, "Missing production_tonnes recalculated as area_harvested_ha x yield_t_per_ha",
            "production_tonnes", old_series=df["production_tonnes"])
df.loc[missing_prod_mask, "production_tonnes"] = (
    df.loc[missing_prod_mask, "area_harvested_ha"] * df.loc[missing_prod_mask, "yield_t_per_ha"]
)

# ---------------------------------------------------------------
# 5. Fix outlier(s): production_tonnes deviating >20% from area x yield
# ---------------------------------------------------------------
implied = df["area_harvested_ha"] * df["yield_t_per_ha"]
deviation_pct = (df["production_tonnes"] - implied).abs() / implied * 100
outlier_mask = deviation_pct > 20
log_change(outlier_mask, "production_tonnes deviated >20% from area x yield (data entry error) - recalculated",
            "production_tonnes", old_series=df["production_tonnes"])
df.loc[outlier_mask, "production_tonnes"] = implied.loc[outlier_mask]

# ---------------------------------------------------------------
# 6. Round for consistency
# ---------------------------------------------------------------
df["area_harvested_ha"] = df["area_harvested_ha"].round(1)
df["yield_t_per_ha"] = df["yield_t_per_ha"].round(2)
df["production_tonnes"] = df["production_tonnes"].round(1)

# ---------------------------------------------------------------
# 7. Data types
# ---------------------------------------------------------------
df["year"] = df["year"].astype(int)

# ---------------------------------------------------------------
# 8. Sort for readability
# ---------------------------------------------------------------
df = df.sort_values(["state", "crop", "year"]).reset_index(drop=True)

# ---------------------------------------------------------------
# Save outputs
# ---------------------------------------------------------------
df.to_csv(CLEAN_PATH, index=False)

log_df = pd.concat(log_rows, ignore_index=True) if log_rows else pd.DataFrame()
log_df.to_csv(LOG_PATH, index=False)

print(f"Clean dataset: {df.shape[0]} rows, {df.shape[1]} columns -> {CLEAN_PATH}")
print(f"Data quality log: {log_df.shape[0]} logged changes -> {LOG_PATH}")
print()
print("States after cleaning:", df['state'].nunique())
print("Remaining nulls:\n", df.isnull().sum())
