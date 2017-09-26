import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd


def get_graph(roc_data):

  return html.Div([
         dcc.Graph(
             id='roc-curve',
             figure={
                 'data': [
                     go.Scatter(
                         x=roc_data['FPR'],
                         y=roc_data['TPR'],
                         text='hello world',
                         mode='lines+markers',
                         opacity=0.7,
                         marker={
                             'size': 5,
                             'line': {'width': 0.5, 'color': 'white'}
                         },
                     )
                 ],
                 'layout': go.Layout(
                     xaxis={'type': 'linear', 'title': 'FPR'},
                     yaxis={'title': 'TPR'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                     legend={'x': 0, 'y': 1},
                     hovermode='closest'
                 )
             }
         )
     ],
     style={'width': '48%', 'display': 'inline-block'}
 ) 
