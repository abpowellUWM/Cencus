let
  Source = fact_crime_wi_county,
  #"Removed columns" = Table.RemoveColumns(Source, {"estimate", "geography_level", "county_name", "NAME"}),
  #"Removed duplicates" = Table.Distinct(#"Removed columns", {"var_base"}),
  #"Renamed columns" = Table.RenameColumns(#"Removed duplicates", {{"var_base", "metric_id"}})
in
  #"Renamed columns"


Metric Label = 
SWITCH(
    dim_metric[metric_id],
    "female_victims",               "Female Victims",
    "male_victims",                 "Male Victims",
    "unknown_victims",              "Unknown Sex Victims",
    "female_victims_age_Under 18",  "Female Victims — Under 18",
    "female_victims_age_18_24",     "Female Victims — 18 to 24",
    "female_victims_age_25_34",     "Female Victims — 25 to 34",
    "female_victims_age_35_44",     "Female Victims — 35 to 44",
    "female_victims_age_45_54",     "Female Victims — 45 to 54",
    "female_victims_age_55_64",     "Female Victims — 55 to 64",
    "female_victims_age_65+",       "Female Victims — 65 and Over",
    "male_victims_age_Under 18",    "Male Victims — Under 18",
    "male_victims_age_18_24",       "Male Victims — 18 to 24",
    "male_victims_age_25_34",       "Male Victims — 25 to 34",
    "male_victims_age_35_44",       "Male Victims — 35 to 44",
    "male_victims_age_45_54",       "Male Victims — 45 to 54",
    "male_victims_age_55_64",       "Male Victims — 55 to 64",
    "male_victims_age_65+",         "Male Victims — 65 and Over",
    "unknown_victims_age_Under 18", "Unknown Sex Victims — Under 18",
    "unknown_victims_age_18_24",    "Unknown Sex Victims — 18 to 24",
    "unknown_victims_age_25_34",    "Unknown Sex Victims — 25 to 34",
    "unknown_victims_age_35_44",    "Unknown Sex Victims — 35 to 44",
    "unknown_victims_age_45_54",    "Unknown Sex Victims — 45 to 54",
    "unknown_victims_age_55_64",    "Unknown Sex Victims — 55 to 64",
    "unknown_victims_age_65+",      "Unknown Sex Victims — 65 and Over",
    dim_metric[metric_id]  -- fallback: returns raw metric_id if no match
)
