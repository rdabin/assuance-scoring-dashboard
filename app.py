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

#TODO: spike offline static content (css, js, images)
# app.css.config.serve_locally = True
# app.scripts.config.serve_locally = True
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


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

data_table = html.Div(children=[
    table.generate_table(roc_data)
])


roc_graph = graph.get_graph(roc_data)

slider = html.Div([
    dcc.Slider(
        id='slider',
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.01,
        marks={i/10: '{}'.format(i/10) for i in range(0, 10)}
    )],
    style={'width': '48%', 'display': 'inline-block'}
)


tags = dcc.Dropdown(
    options=[{'label': c, 'value': c} for c in raw_data.columns],
    value=['score', 'class'],
    multi=True
)


app.layout = html.Div([
    html.H4(children='HODAC Threshold Explorer'),
    slider,
    html.Label(children='Threshold:'),
    html.Div(id='threshold'),
    tags,
    roc_graph,
    data_table,
])


@app.callback(
    Output(component_id='threshold', component_property='children'),
    [Input(component_id='slider', component_property='value')]
)
def update_text(input_value):
    return 'Threshold: "{}"'.format(input_value)


if __name__ == '__main__':
    app.run_server()
