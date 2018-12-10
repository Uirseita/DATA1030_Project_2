import pandas as pd
import re

# read data
age_and_sex_df = pd.read_csv('../Car_Crash/Data/Age_and_Sex/ACS_16_5YR_S0101_w'
                             'ith_ann.csv', skipinitialspace=True)
edu_df = pd.read_csv('../Car_Crash/Data/Education/ACS_16_5YR_S1501_with_ann.cs'
                     'v', skipinitialspace=True)
employ_df = pd.read_csv('../Car_Crash/Data/Employment/ACS_16_5YR_S2301_with_an'
                        'n.csv', skipinitialspace=True)
household_income_df = pd.read_csv('../Car_Crash/Data/Income/Household/ACS_16_5'
                                  'YR_S1901_with_ann.csv',
                                  skipinitialspace=True
                                  )
individual_income_df = pd.read_csv('../Car_Crash/Data/Income/Individual/ACS_'
                                   '16_5YR_DP03_with_ann.csv',
                                   skipinitialspace=True)

# age and sex
# extract columns
pattern = r'Id2|(Total; Estimate; (Total population|AGE .+|SUMMARY INDICAT' \
          r'ORS - Median age|SUMMARY INDICATORS - Sex ratio))'
age_and_sex_column_list = age_and_sex_df.iloc[0][age_and_sex_df.iloc[
    0].str.match(pattern)].index.tolist()

# convert first row to column names
age_and_sex = age_and_sex_df[age_and_sex_column_list]
age_and_sex.columns = age_and_sex.iloc[0]
age_and_sex = age_and_sex.reindex(age_and_sex.index.drop(0))

# change column names
age_and_sex_column_names_list = age_and_sex.columns.tolist()
age_and_sex_new_column_names_list = []
for i in age_and_sex_column_names_list:
    if re.match(r'^Id2$', i):
        age_and_sex_new_column_names_list.append('zip_code')
    elif re.search(r'Total population$', i):
        age_and_sex_new_column_names_list.append('population')
    elif re.match(r'Total; Estimate; AGE - Under (\d) years', i):
        match = re.match(r'Total; Estimate; AGE - Under (\d) years', i)
        age_and_sex_new_column_names_list.append('under_' + match.group(1))
    elif re.match(r'Total; Estimate; AGE - (\d+) to (\d+) years', i):
        match = re.match(r'Total; Estimate; AGE - (\d+) to (\d+) years', i)
        age_and_sex_new_column_names_list.append(match.group(1) + '_to_'
                                                 + match.group(2))
    elif re.match(r'Total; Estimate; AGE - (\d+) years and over', i):
        match = re.match(r'Total; Estimate; AGE - (\d+) years and over', i)
        age_and_sex_new_column_names_list.append('over_' + match.group(1))
    elif re.search(r'Median age', i):
        age_and_sex_new_column_names_list.append('median_age')
    elif re.search(r'Sex ratio', i):
        age_and_sex_new_column_names_list.append('sex_ratio')
    else:
        pass
name_dict = dict(zip(age_and_sex_column_names_list,
                     age_and_sex_new_column_names_list))
age_and_sex = age_and_sex.rename(index=str, columns=name_dict)
age_and_sex.zip_code = age_and_sex.zip_code.apply(str)


# education
# extract columns
pattern = r'Id2|(Percent; Estimate; (Percent high school graduate or higher' \
          r'|Percent bachelor\'s degree or higher))'
edu_column_list = edu_df.iloc[0][edu_df.iloc[0].str.match(pattern)]\
    .index.tolist()

# convert first row to column names
edu = edu_df[edu_column_list]
edu.columns = edu.iloc[0]
edu = edu.reindex(edu.index.drop(0))

# change column names
edu_column_names_list = edu.columns.tolist()
edu_new_column_names_list = []
for i in edu_column_names_list:
    if re.match(r'^Id2$',i):
        edu_new_column_names_list.append('zip_code')
    elif re.match(r'Percent; Estimate; Percent high school graduate or '
                  r'higher', i):
        match = re.match(r'Percent; Estimate; Percent high school graduate '
                         r'or higher', i)
        edu_new_column_names_list.append('high_school')
    elif re.match(r'Percent; Estimate; Percent bachelor\'s degree or '
                  r'higher', i):
        match = re.match(r'Percent; Estimate; Percent bachelor\'s degree or '
                         r'higher', i)
        edu_new_column_names_list.append('college')
    else:
        pass
name_dict = dict(zip(edu_column_names_list, edu_new_column_names_list))
edu = edu.rename(index=str, columns=name_dict)
edu.zip_code = edu.zip_code.apply(str)

# employ
# extract columns
pattern = r'Id2|Unemployment rate; Estimate; Population 16 years and over'
employ_column_list = employ_df.iloc[0][employ_df.iloc[0].str.match(
    pattern)]\
    .index.tolist()

# convert first row to column names
employ = employ_df[employ_column_list]
employ.columns = employ.iloc[0]
employ = employ.reindex(employ.index.drop(0))

# change column names
employ_column_names_list = employ.columns.tolist()
employ_new_column_names_list = []
for i in employ_column_names_list:
    if re.match(r'^Id2$', i):
        employ_new_column_names_list.append('zip_code')
    elif re.search(r'Unemployment rate', i):
        employ_new_column_names_list.append('unemployment_rate')
    else:
        pass
name_dict = dict(zip(employ_column_names_list, employ_new_column_names_list))
employ = employ.rename(index=str, columns=name_dict)
employ.zip_code = employ.zip_code.apply(str)


# household income
# extract columns
pattern = r'Id2|Households; Estimate; Median income \(dollars\)|' \
          r'Households; Estimate; Mean income \(dollars\)'
household_income_column_list = household_income_df.iloc[0][
    household_income_df.iloc[0].str.match(pattern)].index.tolist()

# convert first row to column names
household_income = household_income_df[household_income_column_list]
household_income.columns = household_income.iloc[0]
household_income = household_income.reindex(household_income.index.drop(0))

# change column names
household_income_column_names_list = household_income.columns.tolist()
household_income_new_column_names_list = []
for i in household_income_column_names_list:
    if re.match(r'^Id2$', i):
        household_income_new_column_names_list.append('zip_code')
    elif re.search(r'Median income', i):
        household_income_new_column_names_list.append('household_median_'
                                                      'income')
    elif re.search(r'Mean income', i):
        household_income_new_column_names_list.append('household_mean_income')
    else:
        pass
name_dict = dict(zip(household_income_column_names_list,
                     household_income_new_column_names_list))
household_income = household_income.rename(index=str, columns=name_dict)
household_income.zip_code = household_income.zip_code.apply(str)


# individual income
# extract columns
pattern = r'Id2|Estimate; INCOME AND BENEFITS \(IN 2016 INFLATION-ADJUSTED ' \
          r'DOLLARS\) - Per capita income \(dollars\)'
individual_income_column_list = individual_income_df.iloc[0][
    individual_income_df.iloc[0].str.match(pattern)].index.tolist()

# convert first row to column names
individual_income = individual_income_df[individual_income_column_list]
individual_income.columns = individual_income.iloc[0]
individual_income = individual_income.reindex(individual_income.index.drop(0))

# change column names
individual_income_column_names_list = individual_income.columns.tolist()
individual_income_new_column_names_list = []
for i in individual_income_column_names_list:
    if re.match(r'^Id2$', i):
        individual_income_new_column_names_list.append('zip_code')
    elif re.search(r'Per capita income', i):
        individual_income_new_column_names_list.append('individual_income')
    else:
        pass
name_dict = dict(zip(individual_income_column_names_list,
                     individual_income_new_column_names_list))
individual_income = individual_income.rename(index=str, columns=name_dict)
individual_income.zip_code = individual_income.zip_code.apply(str)

census_df = pd.merge(age_and_sex, edu, on='zip_code')
census_df = pd.merge(census_df, employ, on='zip_code')
census_df = pd.merge(census_df, household_income, on='zip_code')
census_df = pd.merge(census_df, individual_income, on='zip_code')

census_df.zip_code = census_df.zip_code.astype(str).apply(
    lambda x: x if len(x) == 5 else '0'+x)

# fill in empty (- or N) values
census_df['individual_income'] = census_df['individual_income'].str.replace(
    r'N|-', '0', regex=True)
census_df['individual_income'] = census_df['individual_income'].astype('float')
valid_income_df = census_df[census_df['individual_income'] > 0]
individual_mean_income = sum(valid_income_df.population * valid_income_df.
                             individual_income)/sum(valid_income_df.population)

census_df['individual_income'] = census_df['individual_income'].replace(
    0.0, individual_mean_income)

# average number of household members is 2.58
census_df['household_mean_income'] = census_df[['household_mean_income',
                                                'individual_income']].apply(
    lambda x: float(x[0]) if x[0] != '-' and x[0] != 'N' else str(x[1]*2.58),
    axis=1)

census_df.drop(columns='household_median_income', inplace=True)
census_df.replace('-', 0.0, inplace=True)
census_df.household_mean_income = census_df.household_mean_income.astype(float)

census_df.to_csv('../Car_Crash/Data/census_data_cleaned.csv', index=False)




