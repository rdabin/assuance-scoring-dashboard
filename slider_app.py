import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


import plotly.graph_objs as go
import pandas as pd
import numpy as np

import metric_calculations as mc
import methods as mt
app = dash.Dash()

raw_data = pd.read_csv('data/cover-output-1506343018603.csv')
roc_data = mc.build_roc_data(raw_data)
# define some parameters
resolution = 4 # number of points per 10 - this is not working properly 
bins1 = 40
step = 1/bins1
print(step)
threshold = 0.4
hista, binsa = np.histogram(raw_data['score'], bins = bins1, range = [0,1])




app = dash.Dash()

app.layout = html.Div([
    dcc.Graph(id='hist_with_slider', animate=True),
    dcc.Slider(
        id='th_slider',
        value=0.5,
        min=0.0,
        max=1.0,
        step=step,
        marks={i/10: '{}'.format(i/10) for i in range(0, 10)}),
    html.Div(id='threshold')
    
])

@app.callback(
    dash.dependencies.Output('hist_with_slider', 'figure'),
    [dash.dependencies.Input('th_slider', 'value')])

def update_histogram(threshold):
    hist_exp, bins_exp, colors_exp = mt.histogram_data(raw_data, threshold, resolution, bins1)
    figure={
        'data': [
            go.Scatter(
                x=bins_exp,
                y=hist_exp,
                text='Histogram',
                mode='markers',
                opacity=0.7,
                
                marker={
                    'size': 15,
                    'color' : colors_exp,
                    'line': {'width': 0.5, 'color': 'white'}
                },
            )
        ],
        'layout': go.Layout(
            width = 700,
            height = 400,
            xaxis={'type': 'linear', 'title': 'Threshold'},
            yaxis={'title': 'Counts'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }
    return figure


@app.callback(
    Output(component_id='threshold', component_property='children'),
    [Input(component_id='th_slider', component_property='value')]
)
def update_text(input_value):
    return 'Threshold: "{}"'.format(input_value)


if __name__ == '__main__':
    app.run_server()