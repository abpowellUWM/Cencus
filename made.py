let
    Year = "2022",
    ApiKey = "",
    Url = "https://api.census.gov/data/" & Year & "/acs/acs5?get=NAME,B20017_002E,B20017_003E&for=county:*&in=state:55&key=" & ApiKey,
    Raw = Json.Document(Web.Contents(Url)),
    Headers = Raw{0},
    Rows = List.Skip(Raw, 1),
    ToTable = Table.FromRows(Rows, Headers),
    RenameColumns = Table.RenameColumns(ToTable, {
        {"B20017_002E", "Median_Earnings_Male"},
        {"B20017_003E", "Median_Earnings_Female"}
    }),
    SetTypes = Table.TransformColumnTypes(RenameColumns, {
        {"Median_Earnings_Male", Int64.Type},
        {"Median_Earnings_Female", Int64.Type}
    })
in
    SetTypes
