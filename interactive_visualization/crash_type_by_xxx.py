import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go


df = pd.read_csv('../Car_Crash/Data/data_cleaned.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

available_indicators = ['Crash Month', 'Day of Week', 'Hour of Day',
                        'Illumination', 'Weather', 'Road Condition']

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crash_type_by',
                options=[{'label': i, 'value': i} for i in
                         available_indicators],
                value='Crash Month'
            )
        ],
            style={'width': '15%', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic')
])


@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('crash_type_by', 'value')])
def update_graph(x_name_1):
    x_name = '_'.join(x_name_1.split(' '))
    plot_df = df.groupby(
        [x_name, 'Collision_Type']).Crash_Record_Number.count().unstack()
    plot_df['Sum'] = plot_df.sum(axis=1)

    for i in range(len(plot_df.columns.tolist()) - 1):
        plot_df.iloc[:, i] = plot_df.iloc[:, i] / plot_df.Sum * 100
    plot_df = plot_df.iloc[:, :-1]

    index_list = plot_df.index.tolist()

    y_name_list = plot_df.columns.tolist()

    data = []
    for y_name in y_name_list:
        data.append(go.Bar(
            x=index_list,
            y=plot_df[y_name].values.tolist(),
            name=y_name
        ))

    layout = go.Layout(
        barmode='stack',
        title=f'Crash Type Percentage by {x_name_1}'
    )

    return {
        'data': data,
        'layout': layout
    }


if __name__ == '__main__':
    app.run_server(debug=True)
