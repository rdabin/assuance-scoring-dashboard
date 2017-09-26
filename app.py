# This is a test for git
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
import pandas as pd
import os.path

from graph import graph
from table import table

import metric_calculations as mc
import build_data


app = dash.Dash()

# Load data
datafile = 'data/data.csv'
if not os.path.isfile(datafile):
    build_data.create_sample_datafile(num_records=1000, filename=datafile)
raw_data = pd.read_csv(datafile)

# calculate roc data
roc_data = mc.build_roc_data(raw_data)

#################
# example modules

#app = dash.Dash()

#agricultural_data = pd.read_csv('data/usa-agricultural-exports-2011.csv')
#table = table.get_table(agricultural_data)

#gdp_life_exp_data = pd.read_csv('data/gdp-life-exp-2007.csv')
#graph = graph.get_graph(gdp_life_exp_data)

#app.layout = html.Div([
#    graph,
#    table
#])
################

table = html.Div(children=[
    html.H4(children='Assurance Scoring Threshold Explorer'),
    table.generate_table(roc_data)
])


graph = dcc.Graph(
    id='roc-curve',
    figure={
        'data': [
            go.Scatter(
                x=roc_data['FPR'],
                y=roc_data['TPR'],
                text='hello world',
                mode='lines+markers',
                opacity=0.7,
                marker={
                    'size': 5,
                    'line': {'width': 0.5, 'color': 'white'}
                },
            )
        ],
        'layout': go.Layout(
            xaxis={'type': 'linear', 'title': 'FPR'},
            yaxis={'title': 'TPR'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }
)


slider = dcc.Slider(
    id='slider',
    value=0.5,
    min=0.0,
    max=1.0,
    step=0.01,
    marks={i/10: '{}'.format(i/10) for i in range(0, 10)}
)


tags = dcc.Dropdown(
    options=[{'label': c, 'value': c} for c in raw_data.columns],
    value=['score', 'class'],
    multi=True
)


app.layout = html.Div([
    tags,
    graph,
    table,
    slider,
    html.Div(id='threshold'),
])


@app.callback(
    Output(component_id='threshold', component_property='children'),
    [Input(component_id='slider', component_property='value')]
)
def update_text(input_value):
    return 'Threshold: "{}"'.format(input_value)


if __name__ == '__main__':
    app.run_server()
