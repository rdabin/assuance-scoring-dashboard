# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 08:24:39 2017


"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash()

slider = dcc.Slider(id='slider', value=0.5, min=0, max=1, step=0.05,
           marks={0: '0', 0.5: '0.5', 1: '1'})

app.layout = html.Div([dcc.Graph(id='pie_graph'),
                       slider])

# Selectors, main graph -> pie graph
@app.callback(Output('pie_graph', 'figure'),
              [Input('slider', 'value')])
def make_pie_figure(slider):

    data = [
        dict(
            type='pie',
            labels=['This one', 'That one'],
            values=[slider, 1 - slider],
            name='My Pie Chart',
            hole=0.5,
            domain={"x": [0, .45], 'y':[0.2, 0.8]},
        )
    ]

    figure = dict(data=data)
    return figure

if __name__ == '__main__':
    app.run_server()