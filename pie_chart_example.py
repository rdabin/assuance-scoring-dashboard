# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 08:24:39 2017


"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import build_data as bd
import metric_calculations as mc

df = bd.create_sample_df()

app = dash.Dash()

slider = dcc.Slider(id='slider', value=0.5, min=0, max=1, step=0.05,
           marks={0: '0', 0.5: '0.5', 1: '1'})

app.layout = html.Div([dcc.Graph(id='pie_chart'),
                       slider])

# Selectors, main graph -> pie graph
@app.callback(Output('pie_chart', 'figure'),
              [Input('slider', 'value')])
def make_pie_figure(slider):
    
    TP, FP, TN, FN = mc.confusion_matrix(df, slider)
    
    data = [
        dict(
            type='pie',
            ids=['TP', 'FN'],
            labels=['TP', 'FN'],
            values=[TP, FN],
            hoverinfo='label+value',
            name='Recall',
            pull=[0.1, 0],
            sort=False,
            domain={"x": [0, 0.5], 'y':[0.5, 1]},
        ),
        dict(
            type='pie',
            ids=['TP', 'FP'],
            labels=['TP', 'FP'],
            values=[TP, FP],
            hoverinfo='label+value',
            name='Precision',
            pull=[0.1, 0],
            sort=False,
            domain={"x": [0.5, 1], 'y':[0.5, 1]},
        ),
        dict(
            type='pie',
            ids=['TP', 'TN', 'FP', 'FN'],
            labels=['TP', 'TN', 'FP', 'FN'],
            values=[TP, TN, FP, FN],
            hoverinfo='label+value',
            name='Accuracy',
            pull=[0.1, 0.1, 0, 0],
            sort=False,
            domain={"x": [0, 0.5], 'y':[0, 0.5]},
        ),
        dict(
            type='pie',
            ids=['FP', 'TN'],
            labels=['FP', 'TN'],
            values=[FP, TN],
            hoverinfo='label+value',
            name='False positive rate',
            pull=[0.1, 0],
            sort=False,
            domain={"x": [0.5, 1], 'y':[0, 0.5]},
        )
    ]

    figure = dict(data=data)
    return figure

if __name__ == '__main__':
    app.run_server()