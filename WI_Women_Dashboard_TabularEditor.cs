// ============================================================
// Wisconsin Status of Women Dashboard
// Tabular Editor 2 C# Script
// Run via: Tabular Editor 2 → Advanced Scripting → paste & Run
// ============================================================

try
{
    // ----------------------------------------------------------
    // HELPER: create or update a calculated table
    // ----------------------------------------------------------
    Action<string, string> UpsertCalcTable = (tableName, daxExpr) =>
    {
        if (Model.Tables.Any(t => t.Name == tableName))
        {
            var ct = Model.Tables[tableName] as CalculatedTable;
            if (ct != null) ct.Expression = daxExpr;
        }
        else
        {
            Model.AddCalculatedTable(tableName, daxExpr);
        }
    };

    // ----------------------------------------------------------
    // HELPER: create or update a measure
    //   fmt = "" means leave FormatString untouched / auto
    // ----------------------------------------------------------
    Action<string, string, string, string> UpsertMeasure = (tableName, measureName, daxExpr, fmt) =>
    {
        var tbl = Model.Tables[tableName];
        Measure m;
        if (tbl.Measures.Any(x => x.Name == measureName))
        {
            m = tbl.Measures[measureName];
            m.Expression = daxExpr;
        }
        else
        {
            m = tbl.AddMeasure(measureName, daxExpr);
        }
        if (!string.IsNullOrEmpty(fmt))
            m.FormatString = fmt;
    };

    // ==========================================================
    // 1. dim_crime_selector
    //    Controls Victim vs Offender view on Violence page
    // ==========================================================
    UpsertCalcTable("dim_crime_selector", @"DATATABLE(
    ""View Mode"", STRING,
    ""Sort Order"", INTEGER,
    {
        { ""Victim"",   1 },
        { ""Offender"", 2 }
    }
)");

    // ==========================================================
    // 2. dim_crime_demographic
    //    Controls Age vs Race breakdown axis on Violence charts
    // ==========================================================
    UpsertCalcTable("dim_crime_demographic", @"DATATABLE(
    ""Breakdown"", STRING,
    ""Sort Order"", INTEGER,
    {
        { ""Age"",  1 },
        { ""Race"", 2 }
    }
)");

    // ==========================================================
    // 3. dim_geo_cascade
    //    Topic → Indicator → Demographic cascade for Geography page
    //    NOTE: this is NOT dim_metric — do not touch dim_metric
    // ==========================================================
    UpsertCalcTable("dim_geo_cascade", @"DATATABLE(
    ""Topic"",        STRING,
    ""Indicator"",    STRING,
    ""Demographic"",  STRING,
    ""Measure Name"", STRING,
    ""Sort Order"",   INTEGER,
    {
        { ""Demographics"", ""Poverty Rate"",              ""Overall"",            ""Overall Poverty Rate"",                  1  },
        { ""Demographics"", ""Poverty Rate"",              ""Women"",              ""Women Poverty Rate"",                    2  },
        { ""Demographics"", ""Poverty Rate"",              ""Men"",                ""Men Poverty Rate"",                      3  },
        { ""Demographics"", ""Poverty Gap"",               ""Women vs Overall"",   ""Women vs Overall Poverty Gap"",          4  },
        { ""Demographics"", ""Labor Force Participation"", ""Women"",              ""Women Labor Force Participation Rate"",  5  },
        { ""Demographics"", ""Homeownership"",             ""Overall"",            ""Homeownership Rate"",                    6  },
        { ""Demographics"", ""Population Share"",          ""Female"",             ""Female Population Share"",               7  },
        { ""Health"",       ""Total Births"",              ""Overall"",            ""Total Births WI"",                       8  },
        { ""Health"",       ""Teen Births"",               ""Overall"",            ""Teen Birth Count"",                      9  },
        { ""Violence"",     ""Assault"",                   ""Female Victims"",     ""Assault Female Victims"",               10 },
        { ""Violence"",     ""Assault"",                   ""Male Victims"",       ""Assault Male Victims"",                 11 },
        { ""Violence"",     ""Sex Offenses"",              ""Female Victims"",     ""Sex Offense Female Victims"",           12 },
        { ""Violence"",     ""Sex Offenses"",              ""Male Victims"",       ""Sex Offense Male Victims"",             13 },
        { ""Violence"",     ""Homicide"",                  ""Female Victims"",     ""Homicide Female Victims"",              14 },
        { ""Violence"",     ""Homicide"",                  ""Male Victims"",       ""Homicide Male Victims"",                15 },
        { ""Elected"",      ""Officials 2025"",            ""Female"",             ""Female Officials 2025"",                16 },
        { ""Elected"",      ""Officials 2025"",            ""Male"",               ""Male Officials 2025"",                  17 },
        { ""Elected"",      ""Female Share"",              ""Overall"",            ""Female Pct of all Officials"",          18 }
    }
)");

    // ==========================================================
    // 4. Measures on fact_crime_wi_county
    // ==========================================================
    string c = "fact_crime_wi_county";

    // --- Base victim / offender counts ---
    UpsertMeasure(c, "Female Victim Count", @"CALCULATE(
    SUM(fact_crime_wi_county[estimate]),
    fact_crime_wi_county[vic_sex] = ""F""
)", "#,0");

    UpsertMeasure(c, "Male Victim Count", @"CALCULATE(
    SUM(fact_crime_wi_county[estimate]),
    fact_crime_wi_county[vic_sex] = ""M""
)", "#,0");

    UpsertMeasure(c, "Female Offender Count", @"CALCULATE(
    SUM(fact_crime_wi_county[estimate]),
    fact_crime_wi_county[off_sex] = ""F""
)", "#,0");

    UpsertMeasure(c, "Male Offender Count", @"CALCULATE(
    SUM(fact_crime_wi_county[estimate]),
    fact_crime_wi_county[off_sex] = ""M""
)", "#,0");

    // --- Switch measures (respond to dim_crime_selector slicer) ---
    UpsertMeasure(c, "Selected Female Crime Count", @"SWITCH(
    SELECTEDVALUE(dim_crime_selector[View Mode], ""Victim""),
    ""Victim"",   [Female Victim Count],
    ""Offender"", [Female Offender Count]
)", "#,0");

    UpsertMeasure(c, "Selected Male Crime Count", @"SWITCH(
    SELECTEDVALUE(dim_crime_selector[View Mode], ""Victim""),
    ""Victim"",   [Male Victim Count],
    ""Offender"", [Male Offender Count]
)", "#,0");

    // --- Offense-specific victim counts (also routed by Geography SWITCH) ---
    UpsertMeasure(c, "Assault Female Victims", @"CALCULATE(
    SUM(fact_crime_wi_county[estimate]),
    fact_crime_wi_county[offense_category] = ""Assault"",
    fact_crime_wi_county[vic_sex] = ""F""
)", "#,0");

    UpsertMeasure(c, "Assault Male Victims", @"CALCULATE(
    SUM(fact_crime_wi_county[estimate]),
    fact_crime_wi_county[offense_category] = ""Assault"",
    fact_crime_wi_county[vic_sex] = ""M""
)", "#,0");

    UpsertMeasure(c, "Sex Offense Female Victims", @"CALCULATE(
    SUM(fact_crime_wi_county[estimate]),
    fact_crime_wi_county[offense_category] = ""Sex Offenses"",
    fact_crime_wi_county[vic_sex] = ""F""
)", "#,0");

    UpsertMeasure(c, "Sex Offense Male Victims", @"CALCULATE(
    SUM(fact_crime_wi_county[estimate]),
    fact_crime_wi_county[offense_category] = ""Sex Offenses"",
    fact_crime_wi_county[vic_sex] = ""M""
)", "#,0");

    UpsertMeasure(c, "Homicide Female Victims", @"CALCULATE(
    SUM(fact_crime_wi_county[estimate]),
    fact_crime_wi_county[offense_category] = ""Homicide"",
    fact_crime_wi_county[vic_sex] = ""F""
)", "#,0");

    UpsertMeasure(c, "Homicide Male Victims", @"CALCULATE(
    SUM(fact_crime_wi_county[estimate]),
    fact_crime_wi_county[offense_category] = ""Homicide"",
    fact_crime_wi_county[vic_sex] = ""M""
)", "#,0");

    // ==========================================================
    // 5. Measures on fact_acs_wi_county
    // ==========================================================
    string a = "fact_acs_wi_county";

    // Master SWITCH — drives all Geography page visuals
    // FormatString intentionally blank so Power BI inherits from
    // the routed measure at render time
    UpsertMeasure(a, "Selected Geography Measure", @"SWITCH(
    SELECTEDVALUE(dim_geo_cascade[Measure Name]),
    ""Overall Poverty Rate"",                [(IND) Overall Poverty Rate],
    ""Women Poverty Rate"",                  [(IND) Women Poverty Rate],
    ""Men Poverty Rate"",                    [(IND) Men Poverty Rate],
    ""Women vs Overall Poverty Gap"",        [(IND) Women vs Overall Poverty Gap],
    ""Women Labor Force Participation Rate"",[(IND) Women Labor Force Participation Rate],
    ""Homeownership Rate"",                  [Homeownership Rate],
    ""Female Population Share"",             [Female Population Share],
    ""Total Births WI"",                     [Total Births WI],
    ""Teen Birth Count"",                    [Teen Birth Count],
    ""Assault Female Victims"",              [Assault Female Victims],
    ""Assault Male Victims"",                [Assault Male Victims],
    ""Sex Offense Female Victims"",          [Sex Offense Female Victims],
    ""Sex Offense Male Victims"",            [Sex Offense Male Victims],
    ""Homicide Female Victims"",             [Homicide Female Victims],
    ""Homicide Male Victims"",               [Homicide Male Victims],
    ""Female Officials 2025"",               [Female Officials 2025],
    ""Male Officials 2025"",                 [Male Officials 2025],
    ""Female Pct of all Officials"",         [Female Pct of all Officials],
    BLANK()
)", "");

    // KPI card wrappers for Demographics page
    UpsertMeasure(a, "Women Poverty Rate Display", @"CALCULATE(
    [(IND) Women Poverty Rate],
    ALLSELECTED(dim_geography[County Name])
)", "0.00%");

    UpsertMeasure(a, "Men Poverty Rate Display", @"CALCULATE(
    [(IND) Men Poverty Rate],
    ALLSELECTED(dim_geography[County Name])
)", "0.00%");

    UpsertMeasure(a, "Poverty Gap Display", @"CALCULATE(
    [(IND) Women vs Overall Poverty Gap],
    ALLSELECTED(dim_geography[County Name])
)", "0.00%");

    UpsertMeasure(a, "LFP Rate Display", @"CALCULATE(
    [(IND) Women Labor Force Participation Rate],
    ALLSELECTED(dim_geography[County Name])
)", "0.00%");

    // ==========================================================
    // 6. Measures on WISH_counties
    // ==========================================================
    UpsertMeasure("WISH_counties", "Teen Birth Rate", @"DIVIDE(
    [Teen Birth Count],
    [Total Births WI],
    0
)", "0.00%");

    Info("Script complete — all tables and measures created or updated.");
}
catch (Exception ex)
{
    Error("Script failed: " + ex.Message);
}
