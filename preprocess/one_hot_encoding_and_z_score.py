import pandas as pd


df = pd.read_csv('../Car_Crash/Data/merged_data.csv', skipinitialspace=True)

# preprocess illumination
df.Illumination = df.Illumination.str.replace('– ', '', regex=False)
df.Illumination = df.Illumination.str.replace('Unknown (expired)', 'Other',
                                              regex=False)
df.Illumination = df.Illumination.fillna('Other')

# preprocess weather
df.Weather = df.Weather.str.replace('Sleet (hail)', 'Sleet(hail)', regex=False)
df.Weather = df.Weather.str.replace('Unknown ', 'Other', regex=False)
df.Weather = df.Weather.fillna('Other')

# preprocess road condition
df.Road_Condition = df.Road_Condition.str.replace('Sand/ mud/ dirt/ oil/ or '
                                                  'gravel',
                                                  'Sand/mud/dirt/oil/or gravel'
                                                  , regex=False)
df.Road_Condition = df.Road_Condition.str.replace('Unknown (expired)',
                                                  'Other', regex=False)
df.Road_Condition = df.Road_Condition.fillna('Other')

# delete the rows with hour of day 99
df = df[~(df['Hour_of_Day'] == 99)]

# convert Yes and No to 1 and 0
df.replace({'Yes': 1, 'No': 0}, inplace=True)

# drop rows with na values
df.dropna(how='any', inplace=True)

df.Collision_Type = df.Collision_Type.astype('category')
df['Collision_Type_num'] = df.Collision_Type.cat.codes

# add a weekend indicator coloum
df['Weekend'] = df['Day_of_Week'].apply(lambda x: 1 if x == 7 or x == 1 else 0)


def z_score(column, df):
    _mean = df[column].mean()
    _std = df[column].std()
    df[f'{column}_zs'] = df[column].apply(lambda x: (x-_mean)/_std)


census_column_list = ['population', 'median_age', 'college',
                      'unemployment_rate', 'household_mean_income']
for column in census_column_list:
    z_score(column, df)

ohe_fields = ['Crash_Month', 'Hour_of_Day', 'Illumination', 'Weather',
              'Road_Condition', 'Urban_/_Rural']

# One-Hot encode a couple of variables
df_ohe = pd.get_dummies(df, columns=ohe_fields)

# Get the one-hot variable names
ohe_feature_names = pd.get_dummies(df[ohe_fields],
                                   columns=ohe_fields).columns.tolist()

df_ohe.Collision_Type = df_ohe.Collision_Type.astype('category')
df_ohe['Collision_Type_num'] = df_ohe.Collision_Type.cat.codes

df_ohe.to_csv('../Car_Crash/Data/data_cleaned.csv', index=False)
