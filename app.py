# This is a test for git
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from graph import graph
from table import table


app = dash.Dash()


agricultural_data = pd.read_csv('data/usa-agricultural-exports-2011.csv')
table = table.get_table(agricultural_data)


gdp_life_exp_data = pd.read_csv('data/gdp-life-exp-2007.csv')
graph = graph.get_graph(gdp_life_exp_data)

slider = dcc.Slider(value=4, min=-10, max=20, step=0.5,
           marks={-5: '-5 Degrees', 0: '0', 10: '10 Degrees'})


app.layout = html.Div([
    graph,
    table,
    slider
])


if __name__ == '__main__':
    app.run_server()
