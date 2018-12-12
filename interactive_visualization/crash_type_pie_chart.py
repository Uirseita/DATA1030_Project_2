import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('../Car_Crash/Data/Crash.csv', skipinitialspace=True)

crash_type_df = df.groupby('Collision_Type').Crash_Record_Number.count()\
    .reset_index()
crash_type_df.Crash_Record_Number = crash_type_df.Crash_Record_Number / \
                                    crash_type_df.Crash_Record_Number.sum()\
                                    * 100
crash_type_df.rename(columns={'Crash_Record_Number': 'Percentage'},
                     inplace=True)

labels = crash_type_df.Collision_Type.values.tolist()
values = crash_type_df.Percentage.values.tolist()

trace = go.Pie(labels=labels, values=values,
               hoverinfo='label+percent',
               textfont=dict(size=20),
               marker=dict(line=dict(color='#000000', width=2)))

py.iplot([trace], filename='styled_pie_chart')
