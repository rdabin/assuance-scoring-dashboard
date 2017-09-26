# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 08:24:39 2017


"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

app = dash.Dash()

slider = dcc.Slider(id='slider', value=0.5, min=0, max=1, step=0.05,
                    marks={0: '0', 0.5: '0.5', 1: '1'})

app.layout = html.Div([dcc.Graph(id='example_graph'),
                       slider])


# Selectors, main graph -> pie graph
@app.callback(Output('example_graph', 'figure'),
              [Input('slider', 'value')])
def make_pie_figure(slider):
    figure = go.Figure(
        data=[
            go.Bar(
                x=['This one', 'That one'],
                y=[slider, 1 - slider],
                name='My Pie Chart',
            )
        ]
    )

    return figure


if __name__ == '__main__':
    app.run_server()
