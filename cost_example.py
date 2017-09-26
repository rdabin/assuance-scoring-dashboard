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

slider = dcc.Slider(id='slider', min=0, max=1, step=0.05,
           marks={0: '0', 0.5: '0.5', 1: '1'})

fp_cost = dcc.Input(
        id='fp_cost',
        placeholder='Enter a value...',
        type='number',
        value=1
        )

fn_cost = dcc.Input(
        id='fn_cost',
        placeholder='Enter a value...',
        type='number',
        value=1
        )

goto_cost_minimum = html.Button('Submit', id='goto_cost_minimum')

cost_instructions = html.Div(id='cost_instructions',
             children='Enter a cost for each ' + FP_TEXT + ' and each ' + FN_TEXT
             + ' and press submit')

app.layout = html.Div([fp_cost,
                       fn_cost,
                       goto_cost_minimum,
                       cost_instructions,
                       slider])

@app.callback(Output('slider', 'value'),
              [Input('goto_cost_minimum', 'n_clicks')],
              [State('fp_cost', 'value'),
               State('fn_cost', 'value')]
              )
def find_cost_minimum(n_clicks, fp_cost, fn_cost):
    
    roc_df = mc.build_roc_data(df, fp_cost, fn_cost)
    min_cost = roc_df['cost'].min()
    # If the minimum cost occurs and several different thresholds,
    # we'll take the first one
    min_cost_threshold = roc_df[roc_df['cost']==min_cost]['threshold'].iloc[0]
    
    return min_cost_threshold


if __name__ == '__main__':
    app.run_server()