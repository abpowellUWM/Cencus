let
    ApiKey = "",
    Year = "2022",
    Base = "https://api.census.gov/data/" & Year & "/acs/acs5",
    Geo = "&for=county:*&in=state:55&key=" & ApiKey,

    // ── BATCH 1: Population (B01001)
    Batch1Url = Base & "?get=NAME,B01001_001E,B01001_002E,B01001_026E,B01001_027E,B01001_028E,B01001_029E,B01001_030E,B01001_031E,B01001_032E,B01001_033E,B01001_034E,B01001_035E,B01001_036E,B01001_037E,B01001_038E,B01001_039E,B01001_040E,B01001_041E,B01001_042E,B01001_043E,B01001_044E,B01001_045E,B01001_046E,B01001_047E,B01001_048E,B01001_049E" & Geo,
    Raw1 = Json.Document(Web.Contents(Batch1Url)),
    Hdrs1 = Raw1{0}, Rows1 = List.Skip(Raw1,1),
    T1 = Table.FromRows(Rows1, Hdrs1),

    // ── BATCH 2: Marital Status (B12001, B12006)
    Batch2Url = Base & "?get=NAME,B12001_001E,B12001_011E,B12001_012E,B12001_013E,B12001_014E,B12001_015E,B12006_001E,B12006_002E,B12006_003E,B12006_004E,B12006_008E,B12006_009E,B12006_014E,B12006_015E,B12006_019E,B12006_020E,B12006_025E,B12006_026E,B12006_030E,B12006_031E,B12006_036E,B12006_037E" & Geo,
    Raw2 = Json.Document(Web.Contents(Batch2Url)),
    Hdrs2 = Raw2{0}, Rows2 = List.Skip(Raw2,1),
    T2 = Table.FromRows(Rows2, Hdrs2),

    // ── BATCH 3: Fertility & Education (B13002, B15002)
    Batch3Url = Base & "?get=NAME,B13002_001E,B13002_002E,B15002_001E,B15002_002E,B15002_016E,B15002_017E,B15002_018E,B15002_019E,B15002_028E,B15002_031E,B15002_032E,B15002_033E,B15002_034E,B15002_035E" & Geo,
    Raw3 = Json.Document(Web.Contents(Batch3Url)),
    Hdrs3 = Raw3{0}, Rows3 = List.Skip(Raw3,1),
    T3 = Table.FromRows(Rows3, Hdrs3),

    // ── BATCH 4: Poverty (B17001)
    Batch4Url = Base & "?get=NAME,B17001_001E,B17001_002E,B17001_003E,B17001_017E,B17001_032E,B17001_046E" & Geo,
    Raw4 = Json.Document(Web.Contents(Batch4Url)),
    Hdrs4 = Raw4{0}, Rows4 = List.Skip(Raw4,1),
    T4 = Table.FromRows(Rows4, Hdrs4),

    // ── BATCH 5: Earnings by education & sex (B20004, B20017)
    Batch5Url = Base & "?get=NAME,B20004_001E,B20004_002E,B20004_003E,B20004_004E,B20004_005E,B20004_006E,B20004_007E,B20004_013E,B20004_014E,B20004_015E,B20004_016E,B20004_017E,B20017_001E,B20017_002E,B20017_003E,B20017_004E,B20017_005E,B20017_006E" & Geo,
    Raw5 = Json.Document(Web.Contents(Batch5Url)),
    Hdrs5 = Raw5{0}, Rows5 = List.Skip(Raw5,1),
    T5 = Table.FromRows(Rows5, Hdrs5),

    // ── BATCH 6: SNAP & Labor Force (B22002, B22010, B23001)
    Batch6Url = Base & "?get=NAME,B22002_001E,B22002_002E,B22002_006E,B22002_007E,B22002_012E,B22002_013E,B22002_019E,B22002_020E,B22002_025E,B22002_026E,B22010_001E,B22010_002E,B23001_001E,B23001_002E,B23001_088E,B23001_089E,B23001_094E,B23001_101E,B23001_108E,B23001_115E,B23001_122E,B23001_129E,B23001_136E,B23001_141E,B23001_146E,B23001_150E" & Geo,
    Raw6 = Json.Document(Web.Contents(Batch6Url)),
    Hdrs6 = Raw6{0}, Rows6 = List.Skip(Raw6,1),
    T6 = Table.FromRows(Rows6, Hdrs6),

    // ── BATCH 7: Housing & Health Insurance (B25003, B25070, B27001)
    Batch7Url = Base & "?get=NAME,B25003_001E,B25003_002E,B25003_003E,B25070_001E,B25070_002E,B25070_003E,B25070_004E,B25070_005E,B25070_006E,B25070_007E,B25070_008E,B25070_009E,B25070_010E,B27001_001E,B27001_004E" & Geo,
    Raw7 = Json.Document(Web.Contents(Batch7Url)),
    Hdrs7 = Raw7{0}, Rows7 = List.Skip(Raw7,1),
    T7 = Table.FromRows(Rows7, Hdrs7),

    // ── BATCH 8: Occupational earnings — Subject tables (S2411, S2412)
    Batch8Url = "https://api.census.gov/data/" & Year & "/acs/acs5/subject?get=NAME,S2411_C01_001E,S2411_C02_001E,S2411_C03_001E,S2411_C04_001E,S2412_C01_001E,S2412_C02_001E,S2412_C03_001E,S2412_C04_001E" & Geo,
    Raw8 = Json.Document(Web.Contents(Batch8Url)),
    Hdrs8 = Raw8{0}, Rows8 = List.Skip(Raw8,1),
    T8 = Table.FromRows(Rows8, Hdrs8),


    DropCols = {"NAME", "state", "county"},
    T2c = Table.RemoveColumns(T2, DropCols),
    T3c = Table.RemoveColumns(T3, DropCols),
    T4c = Table.RemoveColumns(T4, DropCols),
    T5c = Table.RemoveColumns(T5, DropCols),
    T6c = Table.RemoveColumns(T6, DropCols),
    T7c = Table.RemoveColumns(T7, DropCols),
    T8c = Table.RemoveColumns(T8, DropCols),

    AllCols = List.Combine({
        Table.ColumnNames(T1),
        Table.ColumnNames(T2c),
        Table.ColumnNames(T3c),
        Table.ColumnNames(T4c),
        Table.ColumnNames(T5c),
        Table.ColumnNames(T6c),
        Table.ColumnNames(T7c),
        Table.ColumnNames(T8c)
    }),

    AllVals = List.Combine({
        Table.ToColumns(T1),
        Table.ToColumns(T2c),
        Table.ToColumns(T3c),
        Table.ToColumns(T4c),
        Table.ToColumns(T5c),
        Table.ToColumns(T6c),
        Table.ToColumns(T7c),
        Table.ToColumns(T8c)
    }),

    J7 = Table.FromColumns(AllVals, AllCols),

    // ── Add standard columns
    AddGeoId = Table.AddColumn(DropIdx, "geoid", each "55" & [county]),
    AddGeoLevel = Table.AddColumn(AddGeoId, "geography_level", each "county"),
    AddYear     = Table.AddColumn(AddGeoLevel, "year", each Number.FromText(Year), Int64.Type),
    AddStateFip = Table.AddColumn(AddYear, "state_fips", each "55"),

    // ── Unpivot to long format
    UnpivotCols = Table.UnpivotOtherColumns(
        AddStateFip,
        {"NAME","geoid","geography_level","state_fips","county","year"},
        "var_base",
        "estimate"
    ),

    // ── Label lookup
    AddLabel = Table.AddColumn(UnpivotCols, "label", each
        if [var_base] = "B01001_001E" then "Estimate!!Total!!Total population"
        else if [var_base] = "B01001_002E" then "Estimate!!Total!!Male"
        else if [var_base] = "B01001_026E" then "Estimate!!Total!!Female"
        else if [var_base] = "B01001_027E" then "Estimate!!Total!!Female!!Under 5 years"
        else if [var_base] = "B01001_028E" then "Estimate!!Total!!Female!!5 to 9 years"
        else if [var_base] = "B01001_029E" then "Estimate!!Total!!Female!!10 to 14 years"
        else if [var_base] = "B01001_030E" then "Estimate!!Total!!Female!!15 to 17 years"
        else if [var_base] = "B01001_031E" then "Estimate!!Total!!Female!!18 and 19 years"
        else if [var_base] = "B01001_032E" then "Estimate!!Total!!Female!!20 years"
        else if [var_base] = "B01001_033E" then "Estimate!!Total!!Female!!21 years"
        else if [var_base] = "B01001_034E" then "Estimate!!Total!!Female!!22 to 24 years"
        else if [var_base] = "B01001_035E" then "Estimate!!Total!!Female!!25 to 29 years"
        else if [var_base] = "B01001_036E" then "Estimate!!Total!!Female!!30 to 34 years"
        else if [var_base] = "B01001_037E" then "Estimate!!Total!!Female!!35 to 39 years"
        else if [var_base] = "B01001_038E" then "Estimate!!Total!!Female!!40 to 44 years"
        else if [var_base] = "B01001_039E" then "Estimate!!Total!!Female!!45 to 49 years"
        else if [var_base] = "B01001_040E" then "Estimate!!Total!!Female!!50 to 54 years"
        else if [var_base] = "B01001_041E" then "Estimate!!Total!!Female!!55 to 59 years"
        else if [var_base] = "B01001_042E" then "Estimate!!Total!!Female!!60 and 61 years"
        else if [var_base] = "B01001_043E" then "Estimate!!Total!!Female!!62 to 64 years"
        else if [var_base] = "B01001_044E" then "Estimate!!Total!!Female!!65 and 66 years"
        else if [var_base] = "B01001_045E" then "Estimate!!Total!!Female!!67 to 69 years"
        else if [var_base] = "B01001_046E" then "Estimate!!Total!!Female!!70 to 74 years"
        else if [var_base] = "B01001_047E" then "Estimate!!Total!!Female!!75 to 79 years"
        else if [var_base] = "B01001_048E" then "Estimate!!Total!!Female!!80 to 84 years"
        else if [var_base] = "B01001_049E" then "Estimate!!Total!!Female!!85 years and over"
        else if [var_base] = "B12001_001E" then "Estimate!!Total!!Population 15 years and over"
        else if [var_base] = "B12001_011E" then "Estimate!!Total!!Female!!Never married"
        else if [var_base] = "B12001_012E" then "Estimate!!Total!!Female!!Now married (not separated)"
        else if [var_base] = "B12001_013E" then "Estimate!!Total!!Female!!Separated"
        else if [var_base] = "B12001_014E" then "Estimate!!Total!!Female!!Widowed"
        else if [var_base] = "B12001_015E" then "Estimate!!Total!!Female!!Divorced"
        else if [var_base] = "B15002_001E" then "Estimate!!Total!!Population 25 years and over"
        else if [var_base] = "B15002_016E" then "Estimate!!Total!!Male!!Bachelor's degree"
        else if [var_base] = "B15002_017E" then "Estimate!!Total!!Male!!Master's degree"
        else if [var_base] = "B15002_018E" then "Estimate!!Total!!Male!!Professional school degree"
        else if [var_base] = "B15002_019E" then "Estimate!!Total!!Female!!No schooling completed"
        else if [var_base] = "B15002_028E" then "Estimate!!Total!!Female!!High school graduate"
        else if [var_base] = "B15002_031E" then "Estimate!!Total!!Female!!Some college, no degree"
        else if [var_base] = "B15002_032E" then "Estimate!!Total!!Female!!Associate's degree"
        else if [var_base] = "B15002_033E" then "Estimate!!Total!!Female!!Bachelor's degree"
        else if [var_base] = "B15002_034E" then "Estimate!!Total!!Female!!Master's degree"
        else if [var_base] = "B15002_035E" then "Estimate!!Total!!Female!!Doctorate degree"
        else if [var_base] = "B17001_001E" then "Estimate!!Total!!Population for poverty determination"
        else if [var_base] = "B17001_002E" then "Estimate!!Total!!Below poverty level"
        else if [var_base] = "B17001_003E" then "Estimate!!Total!!Below poverty level!!Male"
        else if [var_base] = "B17001_017E" then "Estimate!!Total!!Below poverty level!!Female"
        else if [var_base] = "B17001_032E" then "Estimate!!Total!!At or above poverty level!!Male"
        else if [var_base] = "B17001_046E" then "Estimate!!Total!!At or above poverty level!!Female"
        else if [var_base] = "B20004_001E" then "Estimate!!Median earnings!!Total"
        else if [var_base] = "B20004_002E" then "Estimate!!Median earnings!!Less than high school"
        else if [var_base] = "B20004_003E" then "Estimate!!Median earnings!!High school graduate"
        else if [var_base] = "B20004_004E" then "Estimate!!Median earnings!!Some college or associate's"
        else if [var_base] = "B20004_005E" then "Estimate!!Median earnings!!Bachelor's degree"
        else if [var_base] = "B20004_006E" then "Estimate!!Median earnings!!Graduate or professional degree"
        else if [var_base] = "B20004_013E" then "Estimate!!Median earnings!!Female!!Less than high school"
        else if [var_base] = "B20004_014E" then "Estimate!!Median earnings!!Female!!High school graduate"
        else if [var_base] = "B20004_015E" then "Estimate!!Median earnings!!Female!!Some college"
        else if [var_base] = "B20004_016E" then "Estimate!!Median earnings!!Female!!Bachelor's degree"
        else if [var_base] = "B20004_017E" then "Estimate!!Median earnings!!Female!!Graduate degree"
        else if [var_base] = "B20017_001E" then "Estimate!!Median earnings!!Total (all workers)"
        else if [var_base] = "B20017_002E" then "Estimate!!Median earnings!!Male"
        else if [var_base] = "B20017_003E" then "Estimate!!Median earnings!!Female"
        else if [var_base] = "B20017_004E" then "Estimate!!Median earnings!!Male!!Full-time year-round"
        else if [var_base] = "B20017_005E" then "Estimate!!Median earnings!!Female!!Full-time year-round"
        else if [var_base] = "B20017_006E" then "Estimate!!Median earnings!!Female!!Other"
        else if [var_base] = "B22002_001E" then "Estimate!!Total!!Households"
        else if [var_base] = "B22002_006E" then "Estimate!!Received SNAP!!Male householder, no spouse"
        else if [var_base] = "B22002_007E" then "Estimate!!Did not receive SNAP!!Male householder, no spouse"
        else if [var_base] = "B22002_012E" then "Estimate!!Received SNAP!!Female householder, no spouse"
        else if [var_base] = "B22002_013E" then "Estimate!!Did not receive SNAP!!Female householder, no spouse"
        else if [var_base] = "B22002_019E" then "Estimate!!Received SNAP!!Nonfamily!!Male householder"
        else if [var_base] = "B22002_025E" then "Estimate!!Received SNAP!!Nonfamily!!Female householder"
        else if [var_base] = "B23001_001E" then "Estimate!!Total!!Civilian noninstitutionalized population 16+"
        else if [var_base] = "B23001_002E" then "Estimate!!Total!!Male 16+"
        else if [var_base] = "B23001_088E" then "Estimate!!Total!!Female 16+"
        else if [var_base] = "B23001_089E" then "Estimate!!Total!!Female!!16 to 19!!In labor force"
        else if [var_base] = "B23001_094E" then "Estimate!!Total!!Female!!20 to 21!!In labor force"
        else if [var_base] = "B23001_101E" then "Estimate!!Total!!Female!!22 to 24!!In labor force"
        else if [var_base] = "B23001_108E" then "Estimate!!Total!!Female!!25 to 29!!In labor force"
        else if [var_base] = "B23001_115E" then "Estimate!!Total!!Female!!30 to 34!!In labor force"
        else if [var_base] = "B23001_122E" then "Estimate!!Total!!Female!!35 to 44!!In labor force"
        else if [var_base] = "B23001_129E" then "Estimate!!Total!!Female!!45 to 54!!In labor force"
        else if [var_base] = "B23001_136E" then "Estimate!!Total!!Female!!55 to 59!!In labor force"
        else if [var_base] = "B23001_141E" then "Estimate!!Total!!Female!!60 to 61!!In labor force"
        else if [var_base] = "B23001_146E" then "Estimate!!Total!!Female!!62 to 64!!In labor force"
        else if [var_base] = "B23001_150E" then "Estimate!!Total!!Female!!65 to 69!!In labor force"
        else if [var_base] = "B25003_001E" then "Estimate!!Total!!Occupied housing units"
        else if [var_base] = "B25003_002E" then "Estimate!!Total!!Owner occupied"
        else if [var_base] = "B25003_003E" then "Estimate!!Total!!Renter occupied"
        else if [var_base] = "B25070_010E" then "Estimate!!Total!!Gross rent 50% or more of income"
        else if [var_base] = "B27001_001E" then "Estimate!!Total!!Civilian noninstitutionalized population"
        else if [var_base] = "B27001_004E" then "Estimate!!Total!!Female!!No health insurance coverage"
        else if [var_base] = "S2411_C01_001E" then "Estimate!!Median earnings!!All workers!!All occupations"
        else if [var_base] = "S2411_C02_001E" then "Estimate!!Median earnings!!Male!!All occupations"
        else if [var_base] = "S2411_C03_001E" then "Estimate!!Median earnings!!Female!!All occupations"
        else if [var_base] = "S2412_C01_001E" then "Estimate!!Median earnings!!All workers!!Management occupations"
        else if [var_base] = "S2412_C02_001E" then "Estimate!!Median earnings!!Male!!Management occupations"
        else if [var_base] = "S2412_C03_001E" then "Estimate!!Median earnings!!Female!!Management occupations"
        else [var_base]
    ),

    // ── Add category
    AddCategory = Table.AddColumn(AddLabel, "category", each
        if Text.Contains([var_base], "_C01_") then "all_workers"
        else if Text.Contains([var_base], "_C02_") then "male"
        else if Text.Contains([var_base], "_C03_") then "female"
        else "estimate"
    ),

    SetTypes = Table.TransformColumnTypes(AddCategory, {
        {"estimate", Int64.Type},
        {"year", Int64.Type}
    })

in
    SetTypes
