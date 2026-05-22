"""
WWACS Census API Pull
======================
Pulls 2020-2024 ACS 5-year estimates for Wisconsin counties and outputs
CSVs matching the dimension and fact table structure from the WI Women's
Council Power BI model.

Outputs (saved to ./output/):
  - dim_geography.csv
  - dim_metric.csv
  - dim_race.csv
  - dim_race_suffix.csv
  - dim_race_suffix_b20017.csv
  - dim_marital_status.csv
  - dim_occupation.csv
  - dim_occupation_earnings.csv
  - dim_snap_comparison.csv
  - edu_earnings_levels.csv
  - edu_indicator_selector.csv
  - economic_indicator_selector.csv
  - fact_acs_wi_county.csv

SETUP:
  pip install requests pandas
  Set your API key below.
"""

import requests
import pandas as pd
import os

# ── CONFIG ────────────────────────────────────────────────────────────────────
API_KEY   = ""   # <-- paste your Census API key here
YEAR      = 2024
STATE     = "55"                  # Wisconsin FIPS
BASE_URL  = f"https://api.census.gov/data/{YEAR}/acs/acs5"
OUT_DIR   = "./output"
os.makedirs(OUT_DIR, exist_ok=True)

# ── HELPERS ───────────────────────────────────────────────────────────────────
def fetch(get_vars, geo="county:*", state=STATE):
    """Call the Census API and return a DataFrame."""
    vars_str = ",".join(["NAME"] + get_vars)
    url = (
        f"{BASE_URL}?get={vars_str}"
        f"&for={geo}&in=state:{state}"
        f"&key={API_KEY}"
    )
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    df = pd.DataFrame(data[1:], columns=data[0])
    return df

def fetch_variable_labels(table_prefix):
    """
    Pull variable metadata for a given table from the Census variables endpoint.
    Returns a dict: {var_code: label_string}
    """
    url = f"{BASE_URL}/variables.json"
    r = requests.get(url)
    r.raise_for_status()
    variables = r.json()["variables"]
    result = {}
    for k, v in variables.items():
        if k.startswith(table_prefix):
            result[k] = v.get("label", "")
    return result

def save(df, name):
    path = os.path.join(OUT_DIR, f"{name}.csv")
    df.to_csv(path, index=False)
    print(f"  Saved {name}.csv  ({len(df)} rows)")


# ══════════════════════════════════════════════════════════════════════════════
# 1. DIM_GEOGRAPHY
#    Source: ACS NAME field + FIPS codes for all WI counties
# ══════════════════════════════════════════════════════════════════════════════
print("\n[1/13] dim_geography")

geo_df = fetch(["B01001_001E"])   # total pop — just need the geography scaffold
geo_df = geo_df[["NAME", "state", "county"]].copy()
geo_df.rename(columns={"state": "state_fips", "county": "county_fips"}, inplace=True)

# Build geoid = state_fips + county_fips (5-digit FIPS)
geo_df["geoid"]       = geo_df["state_fips"] + geo_df["county_fips"]
geo_df["County Name"] = geo_df["NAME"].str.replace(", Wisconsin", "", regex=False)
geo_df["state_name"]  = "Wisconsin"
geo_df["Location"]    = geo_df["NAME"]   # e.g. "Milwaukee County, Wisconsin"

geo_df = geo_df[["geoid", "county_fips", "state_fips", "County Name", "Location", "state_name"]]
save(geo_df, "dim_geography")


# ══════════════════════════════════════════════════════════════════════════════
# 2. DIM_RACE  (static lookup)
# ══════════════════════════════════════════════════════════════════════════════
print("\n[2/13] dim_race")

race_df = pd.DataFrame({"Race": [
    "White alone",
    "Black or African American alone",
    "American Indian and Alaska Native alone",
    "Asian alone",
    "Native Hawaiian and Other Pacific Islander alone",
    "Some other race alone",
    "Two or more races",
    "Hispanic or Latino",
]})
save(race_df, "dim_race")


# ══════════════════════════════════════════════════════════════════════════════
# 3. DIM_RACE_SUFFIX  (table suffix → race label mapping used in most ACS tables)
#    ACS appends A–I suffixes to many table IDs to disaggregate by race
# ══════════════════════════════════════════════════════════════════════════════
print("\n[3/13] dim_race_suffix")

race_suffix_df = pd.DataFrame({
    "TableSuffix": ["A","B","C","D","E","F","G","H","I"],
    "Race": [
        "White alone",
        "Black or African American alone",
        "American Indian and Alaska Native alone",
        "Asian alone",
        "Native Hawaiian and Other Pacific Islander alone",
        "Some other race alone",
        "Two or more races",
        "White alone, not Hispanic or Latino",
        "Hispanic or Latino",
    ]
})
save(race_suffix_df, "dim_race_suffix")


# ══════════════════════════════════════════════════════════════════════════════
# 4. DIM_RACE_SUFFIX_B20017
#    B20017: Median earnings by sex by work experience — race-disaggregated
#    Same A–I suffix scheme but we keep it separate since the fact rows
#    reference it independently
# ══════════════════════════════════════════════════════════════════════════════
print("\n[4/13] dim_race_suffix_b20017")

# B20017 uses the same suffix scheme; keeping as separate table mirrors Sean's model
b20017_suffix_df = race_suffix_df.copy()
save(b20017_suffix_df, "dim_race_suffix_b20017")


# ══════════════════════════════════════════════════════════════════════════════
# 5. DIM_MARITAL_STATUS
#    Source: B12006 — Marital Status by Sex by Labor Force Participation
#    We extract the female rows and their var_base codes
# ══════════════════════════════════════════════════════════════════════════════
print("\n[5/13] dim_marital_status")

# Pull variable labels for B12006
b12006_labels = fetch_variable_labels("B12006_")

# Define the marital status categories and their female var_base pairs
# B12006 structure (female section):
#   Never married:   total=B12006_013E, in LF=B12006_015E
#   Now married:     total=B12006_019E, in LF=B12006_021E
#   Separated:       total=B12006_025E, in LF=B12006_027E
#   Widowed:         total=B12006_031E, in LF=B12006_033E
#   Divorced:        total=B12006_037E, in LF=B12006_039E
marital_df = pd.DataFrame({
    "Marital Status":          ["Never married","Now married","Separated","Widowed","Divorced"],
    "FemaleTotalVarBase":      ["B12006_013E","B12006_019E","B12006_025E","B12006_031E","B12006_037E"],
    "FemaleInLaborForceVarBase":["B12006_015E","B12006_021E","B12006_027E","B12006_033E","B12006_039E"],
})
save(marital_df, "dim_marital_status")


# ══════════════════════════════════════════════════════════════════════════════
# 6. DIM_OCCUPATION
#    Source: C24010 — Sex by Occupation for the Civilian Employed Population
#    We pull variable metadata to get occupation labels and codes
# ══════════════════════════════════════════════════════════════════════════════
print("\n[6/13] dim_occupation")

c24010_labels = fetch_variable_labels("C24010_")

occ_rows = []
for var, label in c24010_labels.items():
    # Label pattern: "Estimate!!Total:!!Male:!!Management, business, and financial occupations:!!..."
    parts = [p.strip() for p in label.replace("Estimate!!", "").split("!!")]
    if len(parts) < 2:
        continue
    sex = None
    if "Male:" in parts:
        sex = "Male"
    elif "Female:" in parts:
        sex = "Female"
    else:
        continue

    occupation = parts[-1].rstrip(":")
    occ_code   = var.replace("E", "").replace("C24010_", "")

    occ_rows.append({
        "var_base":      var,
        "OccupationCode": occ_code,
        "Occupation":    occupation,
        "Sex":           sex,
        "TableType":     "C24010",
        "label":         label,
    })

occ_df = pd.DataFrame(occ_rows).drop_duplicates(subset=["var_base"])
save(occ_df, "dim_occupation")


# ══════════════════════════════════════════════════════════════════════════════
# 7. DIM_OCCUPATION_EARNINGS
#    Source: B24022 — Sex by Occupation and Median Earnings
#    RowCode = the row number within the table (unique occupation identifier)
# ══════════════════════════════════════════════════════════════════════════════
print("\n[7/13] dim_occupation_earnings")

b24022_labels = fetch_variable_labels("B24022_")

occ_earn_rows = []
seen = set()
for var, label in b24022_labels.items():
    parts = [p.strip() for p in label.replace("Estimate!!", "").split("!!")]
    occupation = parts[-1].rstrip(":")
    row_code   = var.replace("B24022_", "").replace("E", "")
    if occupation not in seen and len(occupation) > 3:
        seen.add(occupation)
        occ_earn_rows.append({
            "Occupation": occupation,
            "RowCode":    row_code,
        })

occ_earn_df = pd.DataFrame(occ_earn_rows)
save(occ_earn_df, "dim_occupation_earnings")


# ══════════════════════════════════════════════════════════════════════════════
# 8. DIM_SNAP_COMPARISON  (static)
# ══════════════════════════════════════════════════════════════════════════════
print("\n[8/13] dim_snap_comparison")

snap_df = pd.DataFrame({"SNAP Comparison": ["Received SNAP", "Did Not Receive SNAP"]})
save(snap_df, "dim_snap_comparison")


# ══════════════════════════════════════════════════════════════════════════════
# 9. EDU_EARNINGS_LEVELS  (static)
# ══════════════════════════════════════════════════════════════════════════════
print("\n[9/13] edu_earnings_levels")

edu_levels_df = pd.DataFrame({"Education Level": [
    "Less than high school graduate",
    "High school graduate (includes equivalency)",
    "Some college or associate's degree",
    "Bachelor's degree",
    "Graduate or professional degree",
]})
save(edu_levels_df, "edu_earnings_levels")


# ══════════════════════════════════════════════════════════════════════════════
# 10. EDU_INDICATOR_SELECTOR  (static)
# ══════════════════════════════════════════════════════════════════════════════
print("\n[10/13] edu_indicator_selector")

edu_sel_df = pd.DataFrame({"Education Indicator": [
    "Educational Attainment",
    "Earnings by Education Level",
    "Employment by Education Level",
]})
save(edu_sel_df, "edu_indicator_selector")


# ══════════════════════════════════════════════════════════════════════════════
# 11. ECONOMIC_INDICATOR_SELECTOR  (static)
# ══════════════════════════════════════════════════════════════════════════════
print("\n[11/13] economic_indicator_selector")

eco_sel_df = pd.DataFrame({"Economic Indicator": [
    "Median Earnings",
    "Earnings Gap",
    "Labor Force Participation Rate",
    "Poverty Rate",
    "SNAP Receipt",
    "Homeownership Rate",
    "Earnings by Occupation",
    "Earnings by Education",
    "Earnings by Marital Status",
    "Earnings by Race",
]})
save(eco_sel_df, "economic_indicator_selector")


# ══════════════════════════════════════════════════════════════════════════════
# 12. FACT_ACS_WI_COUNTY
#     Long/tidy format: one row per county × variable
#     Tables pulled:
#       B19013  — Median household income
#       B17001  — Poverty status by sex
#       B23001  — Sex by age by employment (labor force participation)
#       B20017  — Median earnings by sex by work experience (+ race suffixes A–I)
#       B24022  — Occupation by median earnings by sex
#       C24010  — Sex by occupation (counts)
#       B12006  — Marital status by sex by labor force participation
#       B15002  — Educational attainment by sex
#       B22001  — SNAP receipt
#       B25003  — Tenure (homeownership)
# ══════════════════════════════════════════════════════════════════════════════
print("\n[12/13] fact_acs_wi_county")

# Define the variable groups to pull
# Each entry: (table_id, [list of variable codes])
# We pull _E (estimate) fields only; margins of error excluded for now

TABLES = {
    # Median household income — total, male, female
    "B19013": ["B19013_001E"],

    # Poverty by sex — below poverty female, total female, below poverty male, total male
    "B17001": [
        "B17001_002E","B17001_003E",  # total below poverty, male below poverty
        "B17001_017E",                # female below poverty
        "B17001_001E",                # total
    ],

    # Labor force participation by sex (summary rows)
    "B23001": [
        "B23001_001E",  # total
        "B23001_006E",  # male in labor force
        "B23001_092E",  # female in labor force
    ],

    # Median earnings by sex by work experience
    "B20017": [
        "B20017_001E",  # total median earnings
        "B20017_002E",  # male — worked full time
        "B20017_003E",  # male — other
        "B20017_004E",  # female — worked full time
        "B20017_005E",  # female — other
    ],

    # Educational attainment by sex (key summary rows)
    "B15002": [
        "B15002_001E",  # total
        "B15002_015E",  # male bachelor's
        "B15002_016E",  # male graduate/professional
        "B15002_032E",  # female bachelor's
        "B15002_033E",  # female graduate/professional
    ],

    # SNAP receipt
    "B22001": [
        "B22001_001E",  # total households
        "B22001_002E",  # received SNAP
        "B22001_003E",  # did not receive SNAP
    ],

    # Homeownership (tenure)
    "B25003": [
        "B25003_001E",  # total occupied units
        "B25003_002E",  # owner occupied
        "B25003_003E",  # renter occupied
    ],

    # Marital status labor force (female key rows)
    "B12006": [
        "B12006_013E","B12006_015E",  # never married: total, in LF
        "B12006_019E","B12006_021E",  # now married: total, in LF
        "B12006_025E","B12006_027E",  # separated: total, in LF
        "B12006_031E","B12006_033E",  # widowed: total, in LF
        "B12006_037E","B12006_039E",  # divorced: total, in LF
    ],
}

# Race-disaggregated B20017 (suffixes A–I)
RACE_SUFFIXES = ["A","B","C","D","E","F","G","H","I"]
for suffix in RACE_SUFFIXES:
    table_id = f"B20017{suffix}"
    TABLES[table_id] = [
        f"B20017{suffix}_001E",
        f"B20017{suffix}_002E",
        f"B20017{suffix}_003E",
        f"B20017{suffix}_004E",
        f"B20017{suffix}_005E",
    ]

# Pull each table and stack into long format
all_fact_rows = []

for table_id, var_list in TABLES.items():
    print(f"    Fetching {table_id}...", end=" ")
    try:
        df = fetch(var_list)
        df["geoid"] = df["state"] + df["county"]
        df["geography_level"] = "county"
        df["year"] = YEAR

        # Melt wide → long
        id_cols = ["NAME","state","county","geoid","geography_level","year"]
        val_cols = [c for c in var_list if c in df.columns]
        melted = df.melt(
            id_vars=id_cols,
            value_vars=val_cols,
            var_name="var_base",
            value_name="estimate"
        )
        melted["county"] = melted["NAME"].str.replace(", Wisconsin","",regex=False)
        melted = melted[["geoid","county","geography_level","var_base","estimate","year"]]
        melted["estimate"] = pd.to_numeric(melted["estimate"], errors="coerce")
        all_fact_rows.append(melted)
        print(f"{len(melted)} rows")
    except Exception as e:
        print(f"ERROR — {e}")

# Also pull C24010 and B24022 (large tables — pull all E vars)
for big_table in ["C24010", "B24022"]:
    print(f"    Fetching {big_table} (full table)...", end=" ")
    try:
        labels = fetch_variable_labels(big_table + "_")
        e_vars = [v for v in labels if v.endswith("E")][:50]  # cap at 50 per API call
        df = fetch(e_vars)
        df["geoid"] = df["state"] + df["county"]
        df["geography_level"] = "county"
        df["year"] = YEAR
        id_cols = ["NAME","state","county","geoid","geography_level","year"]
        val_cols = [c for c in e_vars if c in df.columns]
        melted = df.melt(
            id_vars=id_cols,
            value_vars=val_cols,
            var_name="var_base",
            value_name="estimate"
        )
        melted["county"] = melted["NAME"].str.replace(", Wisconsin","",regex=False)
        melted = melted[["geoid","county","geography_level","var_base","estimate","year"]]
        melted["estimate"] = pd.to_numeric(melted["estimate"], errors="coerce")
        all_fact_rows.append(melted)
        print(f"{len(melted)} rows")
    except Exception as e:
        print(f"ERROR — {e}")

fact_df = pd.concat(all_fact_rows, ignore_index=True)
fact_df = fact_df.drop_duplicates(subset=["geoid","var_base"])
save(fact_df, "fact_acs_wi_county")


# ══════════════════════════════════════════════════════════════════════════════
# 13. DIM_METRIC
#     Built from Census variable metadata for every var_base in the fact table
# ══════════════════════════════════════════════════════════════════════════════
print("\n[13/13] dim_metric")

# Pull all variable metadata once
all_vars_url = f"{BASE_URL}/variables.json"
r = requests.get(all_vars_url)
r.raise_for_status()
all_variables = r.json()["variables"]

# Category and format_type inference rules
def infer_category(label):
    label_l = label.lower()
    if any(x in label_l for x in ["earnings","income","wage","salary"]):
        return "Earnings"
    elif any(x in label_l for x in ["poverty","below poverty"]):
        return "Poverty"
    elif any(x in label_l for x in ["labor force","employed","employment","occupation"]):
        return "Employment"
    elif any(x in label_l for x in ["education","school","degree","attainment"]):
        return "Education"
    elif any(x in label_l for x in ["snap","food stamp"]):
        return "Food Assistance"
    elif any(x in label_l for x in ["owner","renter","tenure","homeowner"]):
        return "Housing"
    elif any(x in label_l for x in ["marital","married","widowed","divorced"]):
        return "Marital Status"
    elif any(x in label_l for x in ["race","white","black","asian","hispanic"]):
        return "Race"
    else:
        return "Other"

def infer_format(label, var):
    label_l = label.lower()
    if "median" in label_l or "earnings" in label_l or "income" in label_l:
        return "currency"
    elif "percent" in label_l or "rate" in label_l or "share" in label_l:
        return "percent"
    else:
        return "count"

def infer_unit(format_type):
    return {"currency": "USD", "percent": "%", "count": "persons"}.get(format_type, "")

unique_vars = fact_df["var_base"].unique()
metric_rows = []
for i, var in enumerate(unique_vars):
    meta = all_variables.get(var, {})
    raw_label = meta.get("label", var)
    # Clean label: strip "Estimate!!" prefix and use last meaningful segment
    parts = [p.strip() for p in raw_label.replace("Estimate!!","").split("!!")]
    metric_label = " — ".join(parts) if len(parts) > 1 else parts[0]
    category    = infer_category(raw_label)
    format_type = infer_format(raw_label, var)
    unit        = infer_unit(format_type)
    metric_rows.append({
        "metric_id":    i + 1,
        "var_base":     var,
        "Metric Label": metric_label,
        "category":     category,
        "format_type":  format_type,
        "unit":         unit,
        "notes":        raw_label,  # full raw label as reference
    })

metric_df = pd.DataFrame(metric_rows)
save(metric_df, "dim_metric")

print("\n✅ Done! All files saved to ./output/")
print(f"   fact_acs_wi_county: {len(fact_df):,} rows × {len(fact_df.columns)} columns")
print(f"   dim_metric:         {len(metric_df):,} variables mapped")
