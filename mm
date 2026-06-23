STEP 1 — New Tables
Modeling → New Table → paste each one

Table 1: dim_crime_selector


dim_crime_selector = DATATABLE(
    "View Mode", STRING,
    "Sort Order", INTEGER,
    {
        { "Victim",   1 },
        { "Offender", 2 }
    }
)
Table 2: dim_crime_demographic


dim_crime_demographic = DATATABLE(
    "Breakdown", STRING,
    "Sort Order", INTEGER,
    {
        { "Age",  1 },
        { "Race", 2 }
    }
)
Table 3: dim_geo_cascade


dim_geo_cascade = DATATABLE(
    "Topic",        STRING,
    "Indicator",    STRING,
    "Demographic",  STRING,
    "Measure Name", STRING,
    "Sort Order",   INTEGER,
    {
        { "Demographics", "Poverty Rate",              "Overall",          "Overall Poverty Rate",                  1  },
        { "Demographics", "Poverty Rate",              "Women",            "Women Poverty Rate",                    2  },
        { "Demographics", "Poverty Rate",              "Men",              "Men Poverty Rate",                      3  },
        { "Demographics", "Poverty Gap",               "Women vs Overall", "Women vs Overall Poverty Gap",          4  },
        { "Demographics", "Labor Force Participation", "Women",            "Women Labor Force Participation Rate",  5  },
        { "Demographics", "Homeownership",             "Overall",          "Homeownership Rate",                    6  },
        { "Demographics", "Population Share",          "Female",           "Female Population Share",               7  },
        { "Health",       "Total Births",              "Overall",          "Total Births WI",                       8  },
        { "Health",       "Teen Births",               "Overall",          "Teen Birth Count",                      9  },
        { "Violence",     "Assault",                   "Female Victims",   "Assault Female Victims",               10  },
        { "Violence",     "Assault",                   "Male Victims",     "Assault Male Victims",                 11  },
        { "Violence",     "Sex Offenses",              "Female Victims",   "Sex Offense Female Victims",           12  },
        { "Violence",     "Sex Offenses",              "Male Victims",     "Sex Offense Male Victims",             13  },
        { "Violence",     "Homicide",                  "Female Victims",   "Homicide Female Victims",              14  },
        { "Violence",     "Homicide",                  "Male Victims",     "Homicide Male Victims",                15  },
        { "Elected",      "Officials 2025",            "Female",           "Female Officials 2025",                16  },
        { "Elected",      "Officials 2025",            "Male",             "Male Officials 2025",                  17  },
        { "Elected",      "Female Share",              "Overall",          "Female Pct of all Officials",          18  }
    }
)
STEP 2 — Measures on fact_crime_wi_county
Click fact_crime_wi_county in Fields → Modeling → New Measure

Female Victim Count — format: Whole Number


Female Victim Count =
CALCULATE(
    SUM(fact_crime_wi_county[estimate]),
    fact_crime_wi_county[vic_sex] = "F"
)
Male Victim Count — format: Whole Number


Male Victim Count =
CALCULATE(
    SUM(fact_crime_wi_county[estimate]),
    fact_crime_wi_county[vic_sex] = "M"
)
Female Offender Count — format: Whole Number


Female Offender Count =
CALCULATE(
    SUM(fact_crime_wi_county[estimate]),
    fact_crime_wi_county[off_sex] = "F"
)
Male Offender Count — format: Whole Number


Male Offender Count =
CALCULATE(
    SUM(fact_crime_wi_county[estimate]),
    fact_crime_wi_county[off_sex] = "M"
)
Selected Female Crime Count — format: Whole Number


Selected Female Crime Count =
SWITCH(
    SELECTEDVALUE(dim_crime_selector[View Mode], "Victim"),
    "Victim",   [Female Victim Count],
    "Offender", [Female Offender Count]
)
Selected Male Crime Count — format: Whole Number


Selected Male Crime Count =
SWITCH(
    SELECTEDVALUE(dim_crime_selector[View Mode], "Victim"),
    "Victim",   [Male Victim Count],
    "Offender", [Male Offender Count]
)
Assault Female Victims — format: Whole Number


Assault Female Victims =
CALCULATE(
    SUM(fact_crime_wi_county[estimate]),
    fact_crime_wi_county[offense_category] = "Assault",
    fact_crime_wi_county[vic_sex] = "F"
)
Assault Male Victims — format: Whole Number


Assault Male Victims =
CALCULATE(
    SUM(fact_crime_wi_county[estimate]),
    fact_crime_wi_county[offense_category] = "Assault",
    fact_crime_wi_county[vic_sex] = "M"
)
Sex Offense Female Victims — format: Whole Number


Sex Offense Female Victims =
CALCULATE(
    SUM(fact_crime_wi_county[estimate]),
    fact_crime_wi_county[offense_category] = "Sex Offenses",
    fact_crime_wi_county[vic_sex] = "F"
)
Sex Offense Male Victims — format: Whole Number


Sex Offense Male Victims =
CALCULATE(
    SUM(fact_crime_wi_county[estimate]),
    fact_crime_wi_county[offense_category] = "Sex Offenses",
    fact_crime_wi_county[vic_sex] = "M"
)
Homicide Female Victims — format: Whole Number


Homicide Female Victims =
CALCULATE(
    SUM(fact_crime_wi_county[estimate]),
    fact_crime_wi_county[offense_category] = "Homicide",
    fact_crime_wi_county[vic_sex] = "F"
)
Homicide Male Victims — format: Whole Number


Homicide Male Victims =
CALCULATE(
    SUM(fact_crime_wi_county[estimate]),
    fact_crime_wi_county[offense_category] = "Homicide",
    fact_crime_wi_county[vic_sex] = "M"
)
STEP 3 — Measures on fact_acs_wi_county
Click fact_acs_wi_county in Fields → Modeling → New Measure

Selected Geography Measure — leave format as Auto


Selected Geography Measure =
SWITCH(
    SELECTEDVALUE(dim_geo_cascade[Measure Name]),
    "Overall Poverty Rate",                 [(IND) Overall Poverty Rate],
    "Women Poverty Rate",                   [(IND) Women Poverty Rate],
    "Men Poverty Rate",                     [(IND) Men Poverty Rate],
    "Women vs Overall Poverty Gap",         [(IND) Women vs Overall Poverty Gap],
    "Women Labor Force Participation Rate", [(IND) Women Labor Force Participation Rate],
    "Homeownership Rate",                   [Homeownership Rate],
    "Female Population Share",              [Female Population Share],
    "Total Births WI",                      [Total Births WI],
    "Teen Birth Count",                     [Teen Birth Count],
    "Assault Female Victims",               [Assault Female Victims],
    "Assault Male Victims",                 [Assault Male Victims],
    "Sex Offense Female Victims",           [Sex Offense Female Victims],
    "Sex Offense Male Victims",             [Sex Offense Male Victims],
    "Homicide Female Victims",              [Homicide Female Victims],
    "Homicide Male Victims",                [Homicide Male Victims],
    "Female Officials 2025",                [Female Officials 2025],
    "Male Officials 2025",                  [Male Officials 2025],
    "Female Pct of all Officials",          [Female Pct of all Officials],
    BLANK()
)
Women Poverty Rate Display — format: Percentage (0.00%)


Women Poverty Rate Display =
CALCULATE(
    [(IND) Women Poverty Rate],
    ALLSELECTED(dim_geography[County Name])
)
Men Poverty Rate Display — format: Percentage (0.00%)


Men Poverty Rate Display =
CALCULATE(
    [(IND) Men Poverty Rate],
    ALLSELECTED(dim_geography[County Name])
)
Poverty Gap Display — format: Percentage (0.00%)


Poverty Gap Display =
CALCULATE(
    [(IND) Women vs Overall Poverty Gap],
    ALLSELECTED(dim_geography[County Name])
)
LFP Rate Display — format: Percentage (0.00%)


LFP Rate Display =
CALCULATE(
    [(IND) Women Labor Force Participation Rate],
    ALLSELECTED(dim_geography[County Name])
)
STEP 4 — Measure on WISH_counties
Click WISH_counties in Fields → Modeling → New Measure

Teen Birth Rate — format: Percentage (0.00%)


Teen Birth Rate =
DIVIDE(
    [Teen Birth Count],
    [Total Births WI],
    0
)
