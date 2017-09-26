# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 14:57:22 2017
Handle different costs for false positives and false negatives
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import build_data as bd
import metric_calculations as mc

TP_COLOUR = '#e03344'
FP_COLOUR = '#ef7b28'
TN_COLOUR = '#09ef33'
FN_COLOUR = '#aabf22'

TP_TEXT = 'hit'
FP_TEXT = 'false alarm'
TN_TEXT = 'meh'
FN_TEXT = 'miss'

df = bd.create_sample_df()

app = dash.Dash()

slider = dcc.Slider(id='slider', value=0.5, min=0, max=1, step=0.05,
           marks={0: '0', 0.5: '0.5', 1: '1'})

input_cost_ratio = dcc.Input(
        id='input_cost_ratio',
        placeholder='Enter a value...',
        type='number',
        value=1
        )

goto_cost_minimum = html.Button('Submit', id='goto_cost_minimum')

cost_instructions = html.Div(id='cost_instructions',
             children='Enter a cost ratio (' + FP_TEXT + ' cost/' + FN_TEXT
             + ' cost) and press submit')

app.layout = html.Div([input_cost_ratio,
                       goto_cost_minimum,
                       cost_instructions,
                       slider])

@app.callback(Output('slider', 'value'),
              [Input('goto_cost_minimum', 'n_clicks')],
              [State('input_cost_ratio', 'value')]
              )
def make_pie_figure(n_clicks, cost_ratio):
    return cost_ratio


if __name__ == '__main__':
    app.run_server()