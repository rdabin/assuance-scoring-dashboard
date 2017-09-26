import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd


def get_graph(gdp_life_exp_data):

  return dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Scatter(
                    x=gdp_life_exp_data[gdp_life_exp_data['continent'] == i]['gdp per capita'],
                    y=gdp_life_exp_data[gdp_life_exp_data['continent'] == i]['life expectancy'],
                    text=gdp_life_exp_data[gdp_life_exp_data['continent'] == i]['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name = i
                ) for i in gdp_life_exp_data.continent.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
