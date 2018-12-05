import pandas as pd
from arcgis.geocoding import reverse_geocode
from arcgis import GIS

# this script does the reverse geocoding which gets the address data
# from longitude and latitude data from the ArcGIS server

df = pd.read_csv(
    '../../Car_Crash/Data/raw_crash_data'
    '/Crash_Data__1997_to_Current__Transportation.csv'
    '', skipinitialspace=True)

# replace space in the column names with _
cols = df.columns
cols = cols.map(lambda x: x.replace(' ', '_') if isinstance(x, str) else x)
df.columns = cols

# use data since 2007
df = df[df['Crash_Year'] >= 2007]

# drop rows without location data
df = df.dropna(subset=['Geographic_Location'])
gis = GIS()
df = pd.DataFrame.spatial.from_xy(df, x_column='Longitude_(Decimal)',
                                  y_column='Latitude_(Decimal)')

add_lst = ['Match_addr', 'LongLabel', 'ShortLabel', 'Addr_type', 'Type',
           'PlaceName', 'AddNum', 'Address', 'Block', 'Sector', 'Neighborhood',
           'District', 'City', 'MetroArea', 'Subregion', 'Region', 'Territory',
           'Postal', 'PostalExt', 'CountryCode']

for i, row in df.iterrows():
    try:
        add = reverse_geocode(row['SHAPE'])['address']
        for key in add_lst:
            df.at[i, key] = add[key]
    except:
        pass
df.to_csv('../../Car_Crash/Data/Crash.csv', index=False)
