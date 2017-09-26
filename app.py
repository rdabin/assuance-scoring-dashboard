import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import os.path
from src.graph import graph
from src.table import table
from src.metrics_calculator import metric_calculations as mc
from src.data_builder import data_builder
from src.callback_manager import callback_manager


app = dash.Dash()
#TODO: spike offline static content (css, js, images)
# app.css.config.serve_locally = True
# app.scripts.config.serve_locally = True
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


### GET DATA 
# Load data
datafile = 'data/data.csv'
if not os.path.isfile(datafile):
    data_builder.create_sample_datafile(num_records=1000, filename=datafile)
raw_data = pd.read_csv(datafile)

# calculate roc data
roc_data = mc.build_roc_data(raw_data)


### BUILD GRAPHS ETC
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


### SET LAYOUT
app.layout = html.Div([
    html.H4(children='HODAC Threshold Explorer'),
    slider,
    html.Label(children='Threshold:'),
    html.Div(id='threshold'),
    tags,
    roc_graph,
    data_table,
])


### REGISTER CONTROLLER CALLBACKS
callback_manager.register_callbacks(app)

if __name__ == '__main__':
    app.run_server()
