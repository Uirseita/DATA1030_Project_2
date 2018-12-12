import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go


df = pd.read_csv('../Car_Crash/Data/Crash.csv', skipinitialspace=True)
df = df[~df['Postal'].isnull()]
# convert zip code into strings
df.Postal = df.Postal.astype(int).astype(str)
df.Postal = df.Postal.apply(lambda x: x if len(x) == 5 else '0'+x)

mapbox_access_token = 'pk.eyJ1IjoidWlyc2VpdGEiLCJhIjoiY2pwaGx4eXQ0MDAwdTNxcX' \
                      'dwMGo0cGpxdiJ9.ux2pBATNhOgnghsvMFbQvw'
column_list = ['Crash_Record_Number',
               'County_Name',
               'Crash_Year',
               'Weather',
               'Road_Condition',
               'Collision_Type',
               'Latitude_(Decimal)',
               'Longitude_(Decimal)',
               'Postal']
df1 = df[column_list]
df1['Collision_Type'] = df1['Collision_Type'].astype('category')
df1['Collision_Type_color'] = df1['Collision_Type'].cat.codes
df1['Collision_Type_color'] = df1['Collision_Type_color'] / (
            len(df1['Collision_Type_color'].unique().tolist()) - 1)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

crash_type_list = df1.Collision_Type.unique().tolist()
year_list = df1.Crash_Year.sort_values().unique().tolist()

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='crash_type',
                options=[{'label': i, 'value': i} for i in crash_type_list],
                value=crash_type_list,
                multi=True
            ),
            dcc.Dropdown(
                id='year',
                options=[{'label': i, 'value': i} for i in year_list],
                value=year_list,
                multi=True
            )
        ], style={'width': '20%', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic')
])


@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('crash_type', 'value'),
     dash.dependencies.Input('year', 'value')])
def update_graph(crash_type, year):
    scl = [[0, "rgb(229, 0, 14)"], [1 / 9, "rgb(231, 63, 2)"],
           [2 / 9, "rgb(233, 142, 5)"], [3 / 9, "rgb(235, 220, 8)"],
           [4 / 9, "rgb(177, 237, 11)"], [5 / 9, "rgb(104, 239, 14)"],
           [6 / 9, "rgb(0, 0, 0)"], [7 / 9, "rgb(32, 241, 17)"],
           [8 / 9, "rgb(23, 245, 156)"], [1, "rgb(27, 248, 232)"]]
    plot_df = df1
    plot_df = plot_df[plot_df['Collision_Type'].isin(crash_type)]
    plot_df = plot_df[plot_df['Crash_Year'].isin(year)]

    # the maximum number of points on the mapbox object is 40K
    if plot_df.shape[0] > 40000:
        plot_df = plot_df.sample(n=40000, replace=False, random_state=1)

    data = [
        go.Scattermapbox(
            lon=plot_df['Longitude_(Decimal)'],
            lat=plot_df['Latitude_(Decimal)'],
            text=plot_df['Collision_Type'],
            mode='markers',
            marker=dict(
                size=5,
                opacity=0.7,
                autocolorscale=False,
                colorscale=scl,
                color=plot_df['Collision_Type_color'],
            ),
        )
    ]

    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=41,
                lon=-77
            ),
            pitch=0,
            zoom=6
        ),
    )

    return go.Figure(data=data, layout=layout)


if __name__ == '__main__':
    app.run_server(debug=True)
