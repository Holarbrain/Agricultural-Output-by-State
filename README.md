# Agricultural Output by State
> A cleaned, modeled, and visualized view of Nigeria's crop production (Rice, Cassava, Yam, Maize) across all 37 states from 2014–2024, built to support data-driven crop planning and food security decisions.

---

## ⚙️ Project Type Flags

- [x] Dashboard / Data Visualization
- [x] Data Cleaning / Wrangling
- [ ] Exploratory Data Analysis (EDA)
- [ ] SQL Analysis / Querying
- [ ] Data Pipeline / ETL
- [ ] Predictive Modelling / Machine Learning
- [ ] End-to-End (multiple of the above)
- [ ] Other: ___________

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Objectives](#2-objectives)
3. [Project Scope & Tools](#3-project-scope--tools)
4. [Repository Structure](#4-repository-structure)
5. [Data Workflow](#5-data-workflow)
6. [Data Model & Schema](#6-data-model--schema)
7. [Analysis & Metrics](#7-analysis--metrics)
8. [Key Insights](#8-key-insights)
9. [Recommendations](#9-recommendations)
10. [Assumptions & Limitations](#10-assumptions--limitations)
11. [Future Enhancements](#11-future-enhancements)
12. [Deliverables](#12-deliverables)
13. [Author](#13-author)

---

## 1. Project Overview

**Context:** Crop production planning in Nigeria requires reliable, state-level output data, but this kind of data is often fragmented, inconsistently labeled, or incomplete when it reaches an analyst. This project works with an 11-year, state-level dataset covering the country's four major staple crops.

**Problem Statement:** Which states and zones are driving national crop production, how has yield efficiency changed over time, and where are the clearest opportunities for planning and investment — land expansion vs. productivity improvement?

**Approach:** The raw dataset was cleaned and validated in Python (standardizing state naming, resolving duplicates, and recalculating missing or erroneous production figures against area × yield), then modeled as a star schema and visualized in Power BI using DAX measures for production, yield, growth, and market share.

**Outcome:** An interactive Power BI dashboard, **"Agricultural Output by State,"** with three report pages — Overview, Trends Over Time, and State Comparison/Planning View — backed by a documented, quality-checked dataset, a data dictionary, and a full data-quality log.

**Dashboard title:** Agricultural Output by State

| Page | Subtitle |
|------|----------|
| Overview | *National Overview: Production, Land Use & Yield Across Nigeria's 37 States (2014–2024)* |
| Trends Over Time | *Production & Yield Trends by Crop, 2014–2024* |
| State Comparison / Planning View | *State & Zone Comparison: Ranking Output and Identifying Land- vs. Yield-Driven Growth* |

---

## 2. Objectives

- **Primary Objective:** Build an interactive Power BI dashboard showing state-level crop production trends across Nigeria from 2014–2024.
- **Secondary Objective 1:** Clean and validate the raw production dataset so every figure in the dashboard is traceable and defensible.
- **Secondary Objective 2:** Quantify which states and geopolitical zones lead national production, and by how much.
- **Secondary Objective 3:** Distinguish states whose output is driven by land area from states driven by yield efficiency, to support differentiated planning decisions.

> 💡 *Every analysis decision in this project traces back to one of these objectives.*

---

## 3. Project Scope & Tools

### Scope

| Dimension | Details |
|-----------|---------|
| **In Scope** | State-level, yearly crop production data for all 37 Nigerian states (36 states + Abuja FCT), covering Rice, Cassava, Yam, and Maize, 2014–2024. |
| **Out of Scope** | LGA-level (sub-state) granularity, crops outside the four staples covered, and non-crop agricultural data (e.g., livestock, fisheries) — none of these were present in the source dataset. |
| **Time Period** | 2014–2024 (11 years) |
| **Granularity** | One row per state × crop × year |

### Tools & Technologies

| Category | Tool(s) Used |
|----------|-------------|
| Data Storage | CSV files |
| Data Processing | Python (pandas) |
| Analysis | pandas, DAX (Power BI measures) |
| Visualization | Power BI (Power Query, DAX, report pages) |
| Documentation | Markdown |

---

## 4. Repository Structure

```
agri-output-project/
│
├── data/
│   ├── raw/                  # Original, unmodified source data - never edited
│   └── clean/                # Cleaned dataset used to build the Power BI model
│
├── scripts/                  # Python cleaning script (01_clean_data.py)
│
├── docs/                     # Data dictionary and data quality log
│
├── visuals/                  # Dashboard page screenshots
│
└── README.md                 # You are here
```

---

## 5. Data Workflow

```
[Raw CSV: crop output by state, 2014-2024]
      ↓
[Ingestion via pandas]
      ↓
[Cleaning & validation in Python]
      ↓
[Modeling & DAX measures in Power BI]
      ↓
[Interactive dashboard: Overview, Trends, State Comparison]
```

1. **Source:** `raw_crop_output_nigeria_2014_2024.csv` — state, crop, year, area harvested (ha), yield (t/ha), and production (tonnes).
2. **Ingestion:** Loaded into Python using pandas (1,145 raw rows).
3. **Cleaning:** Standardized inconsistent state naming (`FCT Abuja` and `Abuja FCT` merged into a single label), removed one exact duplicate row, and recalculated 15 missing and 1 outlier `production_tonnes` value as `area_harvested_ha × yield_t_per_ha`. Every change is logged in `docs/data_quality_log.csv`.
4. **Transformation:** Built two dimension tables in Power Query — `Dim_State` (adds a Zone/geopolitical-region mapping) and `Dim_Year` (2014–2024) — and related them to the fact table in a star schema.
5. **Analysis:** DAX measures for total production, weighted average yield, year-over-year growth, CAGR, and share of national production.
6. **Output:** A three-page interactive Power BI dashboard (National Overview, Trends Over Time, State Comparison/Planning View).

---

## 6. Data Model & Schema

### Table: `Fact_CropOutput`

| Field Name | Data Type | Description | Example Value |
|------------|-----------|-------------|---------------|
| `state` | string | Nigerian state name (37 values incl. Abuja FCT) | "Benue" |
| `crop` | string | Crop type | "Cassava" |
| `year` | string | Reporting year (text, keys to `Dim_Year`) | "2024" |
| `area_harvested_ha` | float | Land area harvested, in hectares | 42,150.0 |
| `yield_t_per_ha` | float | Yield, in tonnes per hectare | 7.3 |
| `production_tonnes` | float | Total production in tonnes | 307,695.0 |

> **Row count:** 1,144 rows
> **Date range:** 2014 – 2024
> **Key relationships:** `Fact_CropOutput.state` → `Dim_State.State` · `Fact_CropOutput.year` → `Dim_Year.YearText`

### Table: `Dim_State`

| Field Name | Data Type | Description | Example Value |
|------------|-----------|-------------|---------------|
| `State` | string | Nigerian state name | "Benue" |
| `Zone` | string | Geopolitical zone | "North Central" |

### Table: `Dim_Year`

| Field Name | Data Type | Description | Example Value |
|------------|-----------|-------------|---------------|
| `Year` | integer | Numeric year, used for CAGR/time logic | 2024 |
| `YearText` | string | Text version of Year, used for the model relationship | "2024" |

*Full field-level documentation, including all DAX measures, is in `docs/data_dictionary.csv`.*

---

## 7. Analysis & Metrics

### Analytical Approach

The dashboard is built around a planning lens: not just "how much was produced," but "is growth coming from more land or better yield, and where is the opportunity to invest?" Measures were designed to support comparison across states, zones, and time rather than a single point-in-time summary.

### Key Metrics Defined

| Metric | Plain-Language Definition | Why It Matters |
|--------|--------------------------|----------------|
| `Total Production` | Sum of production_tonnes across the current filter context | The headline output number for any state/crop/year slice |
| `Avg Yield (t/ha)` | Total Production ÷ Total Area Harvested (weighted, not a simple average) | Shows productivity per hectare without letting small-area states skew the number |
| `YoY Growth %` | Change in Total Production vs. the prior year | Flags volatile or notable years |
| `CAGR 2014–2024` | Compound annual growth rate of production over the full period | Summarizes long-run growth in a single comparable figure |
| `% of National Production` | A state's Total Production ÷ national Total Production | Identifies which states dominate national output |

### Methods Used

- Trend analysis of production and yield across 2014–2024
- State and zone-level ranking/comparison
- Crop-level share-of-total analysis
- Scatter comparison of land area vs. yield to separate land-driven from efficiency-driven output

---

## 8. Key Insights

**Insight 1: Cassava and Yam dominate national output, Rice lags far behind.**
Cassava (≈650M tonnes) and Yam (≈569M tonnes) together account for the large majority of cumulative production across the period, while Rice (≈83M tonnes) is the smallest of the four crops by a wide margin — useful context for any rice self-sufficiency planning conversation.

**Insight 2: Production is geographically concentrated.**
The top 5 producing states (Benue, Kogi, Kaduna, Oyo, Taraba) account for roughly 37% of total national production across all crops and years. Benue alone leads by a wide margin, roughly double the second-place state.

**Insight 3: National output grew, but efficiency was nearly flat.**
National production rose about 32% from 2014 to 2024, but the national weighted average yield barely moved (7.27 → 7.29 t/ha). This suggests the growth was driven primarily by expanding area harvested rather than by improvements in productivity per hectare — a distinction the State Comparison scatter chart is designed to make visible at the state level.

---

## 9. Recommendations

| Priority | Recommendation | Based On | Suggested Owner |
|----------|---------------|----------|-----------------|
| High | Prioritize yield-improvement programs (inputs, extension services, irrigation) over pure land expansion, since national yield has stagnated despite production growth | Insight 3 | Agricultural policy / extension planning bodies |
| Medium | Investigate Rice production specifically — its low volume relative to Cassava/Yam is worth a dedicated deep-dive against national rice demand and import figures | Insight 1 | Crop-specific planning teams |
| Low | Use the State Comparison scatter chart to identify high-area/low-yield states as first candidates for productivity investment | Insight 2, 3 | State-level agricultural planning offices |

---

## 10. Assumptions & Limitations

### Assumptions
- The source dataset's state and crop labels (aside from the FCT naming inconsistency) were treated as accurate and were not independently verified against an external source.
- Where production_tonnes was missing or a clear outlier, it was assumed that `area_harvested_ha × yield_t_per_ha` is the more reliable figure, and the original value was overwritten.

### Limitations
- The dataset covers only 4 crops; conclusions do not extend to other staples (e.g., sorghum, millet, groundnut) that also matter for Nigeria's food security.
- Data is at state-year granularity — no seasonal, LGA-level, or smallholder-vs-commercial breakdown is available, which limits how targeted the recommendations can be.
- 528 state-crop-year combinations present in a full cross-join were absent from the source data (e.g., not every state reports every crop). These were treated as "not grown/not reported" rather than imputed as zero or missing, but this was not independently confirmed against the data source.
- No SQL layer has been built yet for this project; the analysis to date is Python (cleaning) + Power BI/DAX (modeling and visualization) only.

> *The goal here is pre-emptive Q&A. What would a thoughtful skeptic push back on? Document the answer here, before they ask.*

---

## 11. Future Enhancements

- [ ] Add a SQL layer (originally scoped) to answer specific planning questions with queries, e.g., "which states are under-producing relative to available land."
- [ ] Add a `Dim_Crop` table with crop metadata (e.g., staple vs. cash crop) if the analysis expands beyond simple crop-name slicing.
- [ ] Validate the 528 missing state-crop-year combinations against the original data source to confirm they represent true non-cultivation rather than reporting gaps.
- [ ] Extend the dataset to additional staple crops if source data becomes available.

---

## 12. Deliverables

| Deliverable | Description | Location |
|-------------|-------------|----------|
| Cleaned dataset | Validated, standardized crop production data (1,144 rows) | `data/clean/crop_output_nigeria_2014_2024_clean.csv` |
| Cleaning script | Reproducible Python script documenting every cleaning decision | `scripts/01_clean_data.py` |
| Data dictionary | Field-level documentation for all tables and DAX measures | `docs/data_dictionary.csv` |
| Data quality log | Row-level record of every value changed during cleaning, with reasons | `docs/data_quality_log.csv` |
| Power BI dashboard | "Agricultural Output by State" — interactive `.pbix` with Overview, Trends Over Time, and State Comparison/Planning View pages | `[add path once exported]` |

---

## 13. Author

**Ismail Olamide Abdulrazaq**
Data & Analytics Professional — Holarbrain

- 💼 [holarbrain.github.io](https://holarbrain.github.io) · [github.com/holarbrain](https://github.com/holarbrain)
- 📧 ismailabdulrazaq1408@gmail.com

---

*Last updated: August 2026*
