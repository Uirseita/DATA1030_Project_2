# this code should be run in Jupyter Notebook
# so that the interactive Mapview object can be viewed in the notebook

import pandas as pd
import matplotlib
from arcgis import GIS
%matplotlib inline

df = pd.read_csv('../../Car_Crash/Data/Crash.csv', skipinitialspace=True)

# replace space in the column names with _
cols = df.columns
cols = cols.map(lambda x: x.replace(' ', '_') if isinstance(x, str) else x)
df.columns = cols

df = df[df['Crash_Year'] >= 2007]
# drop rows without location data
df = df.dropna(subset=['Geographic_Location'])

gis = GIS()

df1 = df[['Crash_Record_Number', 'Collision_Type', 'Longitude_(Decimal)',
          'Latitude_(Decimal)']].sample(frac=0.001, replace=True,
                                        random_state=1)

df1 = pd.DataFrame.spatial.from_xy(df1, x_column='Longitude_(Decimal)',
                                   y_column='Latitude_(Decimal)')

m1 = GIS().map('Pennsylvania')

df1.spatial.plot(map_widget=m1,
                 kind='scatter', renderer_type='u',  # specify the unique
                 # value renderer using its notation 'u'
                 col='Collision_Type',  # column to get unique values from
                 cmap='prism',  # color map to pick colors from for each class
                 alpha=0.7,  # specify opacity
                 outline_style='n',
                 marker_size=5)

m1
