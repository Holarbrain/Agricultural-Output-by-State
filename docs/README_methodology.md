# Nigeria Agricultural Output Analysis (2014–2024)
### Rice · Cassava · Yam · Maize — State-Level Dataset for Power BI

## 1. Project framing

| | |
|---|---|
| **Business problem** | Government lacks sufficient data to support crop production planning and food security decisions |
| **Analytics goal** | Give planners a state-level, decade-long view of output for 4 priority staples |
| **Target users** | Federal Ministry of Agriculture & Food Security, State Ministries of Agriculture, NBS, donor/NGO food-security teams, ag-investors |
| **Granularity** | State × Crop × Year (2014–2024), 37 states (36 + FCT) × 4 crops × 11 years |
| **Core KPIs** | Production (tonnes), Area harvested (ha), Yield (t/ha), YoY % change, State share of national output, Crop concentration risk by state |
| **Key questions the dataset answers** | Which states drive national output per crop? How is production trending 2014–2024? Which states are most exposed if one crop fails (food-security risk)? Where is yield lagging area growth (productivity gap)? |

## 2. The core data-availability finding

This is worth stating plainly because it **is** the answer to the stated business problem:

**No public source publishes a continuous, official, state-by-state, year-by-year (2014–2024) production series for these four crops in Nigeria.**

- **FAOSTAT** (FAO) publishes Nigeria production annually back to 1961 — but only at the **national** level.
- **World Bank** agriculture indicators for Nigeria are also **national**.
- **NBS/FMAFS (formerly FMARD)** run the Agricultural Performance Survey and, more recently, the **National Agricultural Sample Survey (NASS) 2023** and **National Agricultural Sample Census (NASC) 2022** — these do reach state/LGA resolution, but NASC 2022 is a **single-year snapshot** (the first of its kind in 27 years) and NASS 2023 microdata was only released in October 2025, at farm-household level, not yet packaged as an open annual state-crop time series.
- Community datasets on **Kaggle/Hugging Face** exist but are themselves **synthetic**, not official.

This gap is exactly the evidence base for the dashboard's opening insight slide: *"Nigeria has no open, continuous state-level crop production time series — this is why planning is hampered."*

## 3. How the delivered dataset was built

Because a real state-level series doesn't exist, the dataset was constructed as a **clearly labeled synthetic layer, calibrated to real published national totals**:

1. **National anchors (real):** production totals for 2014, 2019, 2022, 2024 per crop, order-of-magnitude calibrated to FAOSTAT and the FMARD/JICA 2024 agriculture survey (see `Sources` sheet). Intermediate years interpolated; a documented 2022 dip applied nationally, consistent with that year's severe flooding.
2. **State weights (real, directional):** each state's share of national output per crop, derived from documented leading-producer rankings — the FAO/IITA cassava handbook, the FMARD/JICA maize report, FAO/Wikipedia yam and cassava pages, and a 2025 state-agriculture ranking (see `Sources` sheet for each).
3. **Synthetic layer:** state × year production = national total × state weight × small random variation (state-level idiosyncrasy + national-level noise), so the dataset behaves like real reported data rather than a perfectly smooth model. Yield and area are back-calculated from production using realistic crop-specific yield ranges (t/ha).
4. **Validation:** the `National Validation` sheet in the Excel workbook sums the synthetic state data back up and shows it tracks the real national anchor figures within normal variance.

**This is not official data and should not be presented as such.** It is a placeholder analytical layer designed to (a) make the Power BI dashboard fully buildable now, and (b) be swapped for real data — most plausibly the NBS NASS 2023 microdata or the next NASC round — without changing the schema.

## 4. Data quality — Raw vs Clean

The `Raw Data` sheet/CSV intentionally contains realistic issues, fixed in `Clean Data`:

| Issue | Instances | Cleaning method |
|---|---|---|
| Missing `production_tonnes` values | 15 rows | Impute from `area_harvested_ha × yield_t_per_ha` (recompute), or flag and exclude from trend KPIs if both are missing |
| Inconsistent state spelling ("Abuja FCT" vs "FCT Abuja") | ~10 rows | Standardize to a single canonical state list (37 values); use exact-match join against a state lookup table |
| Duplicate row | 1 row | Drop via `state, crop, year` uniqueness check (matches the SQL `UNIQUE` constraint) |
| Outlier (55× production spike, simulated unit-entry error) | 1 row | Flag via z-score/IQR check against that state-crop's own history; cap or correct against the national total constraint |
| Encoding / date issues | None found | N/A — `year` stored as integer, no free-text dates |

## 5. Deliverables in this package

1. `raw_crop_output_nigeria_2014_2024.csv` — raw synthetic dataset with the QA issues above
2. `clean_crop_output_nigeria_2014_2024.csv` — cleaned, analysis-ready
3. `nigeria_crop_production.sql` — normalized schema (`states`, `crops`, `crop_production`) + inserts + 5 example analysis queries
4. `Nigeria_Agricultural_Output_2014_2024.xlsx` — workbook with README, Data Dictionary, Sources, Raw Data, Clean Data, National Validation sheets
5. This methodology note

## 6. Power BI / dashboard recommendations

- **KPI cards:** national production (latest year), YoY % change, average yield, # states above national average yield
- **Map visual:** choropleth of production by state (use Nigeria state shapefile/TopoJSON — not included here), one per crop via slicer
- **Trend line:** national production 2014–2024, small multiples by crop
- **Top-N bar chart:** leading 10 states by cumulative production, per crop
- **Concentration-risk table:** states where one crop is >60% of their 4-crop output (food-security fragility)
- **Yield vs area scatter:** productivity gap — states growing area without growing yield
- **ML/forecast opportunity:** simple trend or ARIMA forecast of 2025–2027 production per crop per state, once real data replaces the synthetic layer
