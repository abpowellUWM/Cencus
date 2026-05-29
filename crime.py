import pandas as pd

NIBRS = "/Users/adalimepowell/Desktop/WISWOM/WI-2024"

# Step 1 - load tables
victim = pd.read_csv(f"{NIBRS}/NIBRS_VICTIM.csv", usecols=['victim_id', 'incident_id', 'sex_code', 'age_num', 'victim_type_id'])
offense = pd.read_csv(f"{NIBRS}/NIBRS_OFFENSE.csv", usecols=['offense_id', 'incident_id', 'offense_code'])
offense_type = pd.read_csv(f"{NIBRS}/NIBRS_OFFENSE_TYPE.csv", usecols=['offense_code', 'offense_name'])
victim_offense = pd.read_csv(f"{NIBRS}/NIBRS_VICTIM_OFFENSE.csv", usecols=['victim_id', 'offense_id'])
victim_offender = pd.read_csv(f"{NIBRS}/NIBRS_VICTIM_OFFENDER_REL.csv", usecols=['victim_id', 'relationship_id'])
incident = pd.read_csv(f"{NIBRS}/NIBRS_incident.csv", usecols=['incident_id', 'agency_id', 'incident_date'])
agencies = pd.read_csv(f"{NIBRS}/agencies.csv", usecols=['agency_id', 'county_name'])

# Step 2 - join chain
offense_type = offense_type.drop_duplicates('offense_code')
df = victim.merge(incident, on='incident_id')
df = df.merge(agencies, on='agency_id')
df = df.merge(victim_offense, on='victim_id')
df = df.merge(offense, on='offense_id')
df = df.merge(offense_type, on='offense_code')

# Step 3 - filter assault offenses
df = df[df['offense_code'].isin(['13A', '13B', '13C'])]

# Step 4 - filter individual victims (victim_type_id 4 = Individual)
df = df[df['victim_type_id'] == 4]

# Step 5 - aggregate all victims by county and sex
agg = df.groupby(['county_name', 'sex_code']).size().reset_index(name='estimate')
agg['var_base'] = agg['sex_code'].map({'F': 'female_victims', 'M': 'male_victims', 'U': 'unknown_victims'})
agg = agg[['county_name', 'var_base', 'estimate']]

# Step 6 - DV filter and aggregate
# relationship_id integers: SE=21 CS=6 BG=3 XS=26 HR=12 PA=17 SB=19 CH=5 GP=11 GC=10 IL=13 SP=22 SC=20 SS=23 OF=15 CF=4
dv_ids = {3, 4, 5, 6, 10, 11, 12, 13, 15, 17, 19, 20, 21, 22, 23, 26}
df_dv = df.merge(victim_offender, on='victim_id')
df_dv = df_dv[df_dv['relationship_id'].isin(dv_ids)]
df_dv = df_dv[df_dv['sex_code'] == 'F']
dv_agg = df_dv.groupby('county_name').size().reset_index(name='estimate')
dv_agg['var_base'] = 'female_victims_dv'

# Step 7 - combine and format
final = pd.concat([agg, dv_agg]).reset_index(drop=True)
final = final.rename(columns={'county_name': 'county'})
final['geography_level'] = 'county'

final.to_csv(f"{NIBRS}/crime_WI.csv", index=False)
print(final)