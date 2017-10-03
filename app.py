import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import os.path
from src.graph import graph
from src.table import table
import metric_calculations as mc
from src.data_builder import data_builder
from src.callback_manager import callback_manager

from dash.dependencies import Input, Output


TP_COLOUR = '#e03344'
FP_COLOUR = '#ef7b28'
TN_COLOUR = '#09ef33'
FN_COLOUR = '#aabf22'

TP_TEXT = 'hit'
FP_TEXT = 'false alarm'
TN_TEXT = 'meh'
FN_TEXT = 'miss'


########### Load data
# datafile = 'data/data.csv'
# if not os.path.isfile(datafile):
#     raw_data = build_data.create_sample_datafile(num_records=1000, datafile)
# else:
#     raw_data = pd.read_csv(datafile)
raw_data = data_builder.create_sample_df()

# calculate roc data
roc_data = mc.build_roc_data(raw_data)
###########



########### create graph divs
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

roc_graph = graph.get_graph(roc_data)

def generate_bar_of_dots(c1=100, c2=16, width=15):
    return pd.DataFrame([
        {
            'type': 0 if i < c1 else 1,
            'x': i % width,
            'y': i // width,
        } for i in range(0, c1 + c2 - 1)
    ])
dots = generate_bar_of_dots()

volume = html.Div([
    dcc.Graph(
        id='volume1',
        config={
        'displayModeBar': False
        },
        figure={
            'data': [
                go.Scatter(
                    x=dots[dots['type'] == i]['x'],
                    y=dots[dots['type'] == i]['y'],
                    text='foo',
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 10,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in dots['type'].unique()
            ],
            'layout': go.Layout(
                width=315,
                height=300,
                showlegend=False,
                xaxis=dict(
                    autorange=True,
                    showgrid=False,
                    zeroline=False,
                    showline=False,
                    autotick=True,
                    ticks='',
                    showticklabels=False
                ),
                yaxis=dict(
                    autorange='reversed',
                    showgrid=False,
                    zeroline=False,
                    showline=False,
                    autotick=True,
                    ticks='',
                    showticklabels=False
                )
            )
        }
    )],
    style={'width': '20%', 'display': 'inline-block'})

pie_chart = dcc.Graph(id='pie_chart')

histogram = dcc.Graph(id='histogram')

cost_graph = graph.get_cost_graph(roc_data)
###############



######## initialise app
app = dash.Dash()

#TODO: spike offline static content (css, js, images)
# app.css.config.serve_locally = True
# app.scripts.config.serve_locally = True
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

### SET LAYOUT
app.layout = html.Div([
    html.H4(children='HODAC Threshold Explorer'),
    slider,
    roc_graph,
    volume,
    pie_chart,
    histogram,
    cost_graph
])
#########



######## callbacks
@app.callback(Output('pie_chart', 'figure'),
              [Input('slider', 'value')])
def make_pie_figure(slider):
    
    tp, fp, tn, fn = mc.confusion_matrix(raw_data, slider)
    
    data = [
        dict(
            type='pie',
            ids=['TP', 'FN'],
            labels=['True positive', 'False negative'],
            values=[tp, fn],
            text=[TP_TEXT, FN_TEXT],
            hoverinfo='value',
            name='Recall',
            pull=[0.1, 0],
            hole=0.5,
            sort=False,
            domain={"x": [0, 0.4], 'y':[0.6, 1]},
            marker=dict(colors=[TP_COLOUR, FN_COLOUR]),
            # Haven't been able to get this annotation to work yet
            # annotations=[dict(text='Recall', x=0.2, y=0.9, xref='paper', yref='paper')]
        ),
        dict(
            type='pie',
            ids=['TP', 'FP'],
            labels=['True positive', 'False positive'],
            values=[tp, fp],
            hoverinfo='value',
            text=[TP_TEXT, FP_TEXT],            
            name='Precision',
            pull=[0.1, 0],
            hole=0.5,
            sort=False,
            domain={"x": [0.6, 1], 'y':[0.6, 1]},
            marker=dict(colors=[TP_COLOUR, FP_COLOUR])                        
        ),
        dict(
            type='pie',
            ids=['TP', 'TN', 'FP', 'FN'],
            labels=['True positive', 'True negative', 'False positive', 'False negative'],
            values=[tp, tn, fp, fn],
            text=[TP_TEXT, TN_TEXT, FP_TEXT, FN_TEXT],                        
            hoverinfo='value',
            name='Accuracy',
            pull=[0, 0, 0.1, 0.1],
            hole=0.5,
            sort=False,
            domain={"x": [0, 0.4], 'y':[0, 0.4]},
            marker=dict(colors=[TP_COLOUR, TN_COLOUR, FP_COLOUR, FN_COLOUR])                                    
        ),
        dict(
            type='pie',
            ids=['FP', 'TN'],
            labels=['False positive', 'True negative'],
            values=[fp, tn],
            text=[FP_TEXT, TN_TEXT],                        
            hoverinfo='value',
            name='False positive rate',
            pull=[0.1, 0],
            hole=0.5,
            sort=False,
            domain={"x": [0.6, 1], 'y':[0, 0.4]},
            marker=dict(colors=[FP_COLOUR, TN_COLOUR])                        
        )
    ]

    figure = dict(data=data, layout=dict(autosize=True, title='Confusion Matrix Explanation'))
    
    return figure


@app.callback(Output('histogram', 'figure'),
              [Input('slider', 'value')])
def make_histogram_figure(slider):

    TP, FP, TN, FN = mc.confusion_matrix(df, slider)

    figure = go.Figure(
        data=[
            go.Bar(
                x=['TP', 'FP', 'TN', 'FN'],
                y=[TP, FP, TN, FN],
                name='My Bar Chart'
            )
        ]
    )

    return figure



### REGISTER CONTROLLER CALLBACKS
#callback_manager.register_callbacks(app)


if __name__ == '__main__':
    app.run_server()
